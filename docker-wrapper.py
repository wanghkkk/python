#!/usr/bin/python
# coding=utf8

import os
import sys

# azure mirrors for gcr.io,k8s.gcr.io,quay.io in china
gcr_mirror = "gcr.azk8s.cn"
docker_mirror = "dockerhub.azk8s.cn"
quay_mirror = "quay.azk8s.cn"

k8s_namespace = "google_containers"

gcr_prefix = "gcr.io"
special_gcr_prefix = "k8s.gcr.io"
quay_prefix = "quay.io"


def execute_sys_cmd(cmd):
    result = os.system(cmd)
    if result != 0:
        print(cmd + " failed.")
        sys.exit(-1)


def usage():
    print("Usage: " + sys.argv[0] + " pull ")
    print("Examples:")
    print(sys.argv[0] + " pull k8s.gcr.io/kube-apiserver:v1.14.1")
    print(sys.argv[0] + " pull gcr.io/google_containers/kube-apiserver:v1.14.1")
    print(sys.argv[0] + " pull quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.26.1")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        usage()
        sys.exit(-1)
    elif sys.argv[1] != 'pull':
        usage()
        sys.exit(-1)

    # image name like k8s.gcr.io/kube-apiserver:v1.14.1 or gcr.io/google_containers/kube-apiserver:v1.14.1
    image = sys.argv[2]
    imageArray = image.split("/")

    if imageArray[0] == gcr_prefix:
        imageArray[0] = gcr_mirror
    elif imageArray[0] == special_gcr_prefix:
        imageArray[0] = gcr_mirror
        imageArray.insert(1, k8s_namespace)
    elif imageArray[0] == quay_prefix:
        imageArray[0] = quay_mirror

    temp_image = "/".join(imageArray)

    if image == temp_image:
        cmd = "docker pull {image}".format(image=image)
        print("------Execute_cmd: %s" % cmd)
        execute_sys_cmd(cmd)
        sys.exit(0)
    else:
        cmd = "docker pull {image}".format(image=temp_image)
        print("------Execute_cmd: %s" % cmd)
        execute_sys_cmd(cmd)

        cmd = "docker tag {newImage} {image}".format(newImage=temp_image, image=image)
        print("------Execute_cmd: %s" % cmd)
        execute_sys_cmd(cmd)

        cmd = "docker rmi {newImage}".format(newImage=temp_image)
        print("------Execute_cmd: %s" % cmd)
        execute_sys_cmd(cmd)

        print("------Pull %s done" % image)
        sys.exit(0)
