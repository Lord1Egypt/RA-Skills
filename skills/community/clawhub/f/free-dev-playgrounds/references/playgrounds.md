# LabEx Free Dev Playgrounds

Use this catalog to map user requests for temporary sandboxes, disposable environments, or browser-based runtimes to the closest public LabEx playground URL.

## Generic

- General catalog
  URL: https://labex.io/playgrounds
  Use for broad requests such as "show me the playgrounds" or when no exact match exists.

## Operating Systems

- Ubuntu Linux
  URL: https://labex.io/playgrounds/ubuntu-linux
  Aliases: ubuntu, linux shell, terminal, bash on ubuntu, generic linux

- Ubuntu Desktop
  URL: https://labex.io/playgrounds/ubuntu-desktop
  Aliases: gui linux, desktop linux, browser desktop, ubuntu gui

- Debian
  URL: https://labex.io/playgrounds/debian
  Aliases: debian linux

- Kali Linux
  URL: https://labex.io/playgrounds/kali-linux
  Aliases: kali, pentest linux, security distro

- RHEL
  URL: https://labex.io/playgrounds/rhel
  Aliases: red hat enterprise linux, redhat

- CentOS
  URL: https://labex.io/playgrounds/centos
  Aliases: centos linux

- Alpine
  URL: https://labex.io/playgrounds/alpine
  Aliases: alpine linux, minimal linux

- Fedora
  URL: https://labex.io/playgrounds/fedora
  Aliases: fedora linux

- openSUSE
  URL: https://labex.io/playgrounds/opensuse
  Aliases: suse, opensuse linux

- Arch Linux
  URL: https://labex.io/playgrounds/archlinux
  Aliases: arch, arch linux

## Containers And Infrastructure

- Docker
  URL: https://labex.io/playgrounds/docker
  Aliases: containers, docker engine, container sandbox

- Kubernetes
  URL: https://labex.io/playgrounds/kubernetes
  Aliases: k8s, kubectl, kubernetes basics, cluster management

- Kubernetes Cluster
  URL: https://labex.io/playgrounds/kubernetes-cluster
  Aliases: multi-node kubernetes, clustered k8s, full cluster

- Ansible
  URL: https://labex.io/playgrounds/ansible
  Aliases: automation, ansible playbooks

- Jenkins
  URL: https://labex.io/playgrounds/jenkins
  Aliases: ci cd, continuous integration, jenkins pipeline

- Git
  URL: https://labex.io/playgrounds/git
  Aliases: git sandbox, version control practice

## Programming Languages And Shell

- Python
  URL: https://labex.io/playgrounds/python
  Aliases: python runtime, python sandbox

- JavaScript
  URL: https://labex.io/playgrounds/javascript
  Aliases: js, javascript runtime

- Node.js
  URL: https://labex.io/playgrounds/node
  Aliases: node, nodejs, npm runtime, server-side javascript

- Golang
  URL: https://labex.io/playgrounds/golang
  Aliases: go, golang runtime

- C++
  URL: https://labex.io/playgrounds/cpp
  Aliases: cpp, c plus plus

- Java
  URL: https://labex.io/playgrounds/java
  Aliases: jdk, java runtime

- Rust
  URL: https://labex.io/playgrounds/rust
  Aliases: rustlang, cargo

- PHP
  URL: https://labex.io/playgrounds/php
  Aliases: php runtime

- Ruby
  URL: https://labex.io/playgrounds/ruby
  Aliases: ruby runtime

- Lua
  URL: https://labex.io/playgrounds/lua
  Aliases: lua runtime

- R
  URL: https://labex.io/playgrounds/r
  Aliases: r language, statistical computing

- TypeScript
  URL: https://labex.io/playgrounds/typescript
  Aliases: ts, typescript runtime

- Bash
  URL: https://labex.io/playgrounds/bash
  Aliases: shell, bash shell, command line practice

- Perl
  URL: https://labex.io/playgrounds/perl
  Aliases: perl runtime

- C
  URL: https://labex.io/playgrounds/c
  Aliases: c language, gcc

## Data Science

- scikit-learn
  URL: https://labex.io/playgrounds/scikit-learn
  Aliases: sklearn, machine learning python

- Matplotlib
  URL: https://labex.io/playgrounds/matplotlib
  Aliases: plotting, charts in python

- Pandas
  URL: https://labex.io/playgrounds/pandas
  Aliases: dataframe, data analysis python

- NumPy
  URL: https://labex.io/playgrounds/numpy
  Aliases: arrays, numerical python

## Security Tools

- Nmap
  URL: https://labex.io/playgrounds/nmap
  Aliases: port scan, network scanner

- Wireshark
  URL: https://labex.io/playgrounds/wireshark
  Aliases: packet capture, packet analysis, pcap

- Hydra
  URL: https://labex.io/playgrounds/hydra
  Aliases: password auditing, login brute force tool

## Databases

- MySQL
  URL: https://labex.io/playgrounds/mysql
  Aliases: mysql database

- PostgreSQL
  URL: https://labex.io/playgrounds/postgresql
  Aliases: postgres, postgresql database

- SQLite
  URL: https://labex.io/playgrounds/sqlite
  Aliases: sqlite database, embedded sql

- MongoDB
  URL: https://labex.io/playgrounds/mongodb
  Aliases: mongo, nosql document database

- Redis
  URL: https://labex.io/playgrounds/redis
  Aliases: key value store, redis cache

## Frontend And Web

- React
  URL: https://labex.io/playgrounds/react
  Aliases: react.js, react frontend

- HTML
  URL: https://labex.io/playgrounds/html
  Aliases: static web page, html sandbox

- CSS
  URL: https://labex.io/playgrounds/css
  Aliases: styling, css sandbox

- Vue
  URL: https://labex.io/playgrounds/vue
  Aliases: vue.js, vue frontend

- Svelte
  URL: https://labex.io/playgrounds/svelte
  Aliases: svelte frontend

## Recommendation Heuristics

- Prefer `ubuntu-linux` for general Linux terminal requests.
- Prefer `ubuntu-desktop` when the user explicitly needs a desktop GUI.
- Prefer `node` over `javascript` when the user mentions npm, packages, backend JavaScript, or server runtime.
- Prefer `javascript` for quick language-only JavaScript experiments.
- Prefer `kubernetes-cluster` over `kubernetes` when the user explicitly needs a cluster or multi-node behavior.
- Prefer the exact named playground whenever the user names a supported stack directly.
