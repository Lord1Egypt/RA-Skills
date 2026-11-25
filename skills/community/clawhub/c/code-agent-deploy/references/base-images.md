# Base images and downloading dependencies

## Where the build happens

The image is built on the deployment platform. The developer's computer does not need Docker installed or running.

## Choosing a base image

A Dockerfile's `FROM` can use:

1. **A base image the platform provides**: write the name alone, with no registry address, tag or digest. At build time the platform puts the image it maintains in its place. These are kept on the build server ahead of time, so the build neither waits for a download nor fails when the outside registry cannot be reached. Prefer them when the version fits.

   | Name | Contents |
   |---|---|
   | `node-base` | Node.js 24.22.1, npm 11.19.1, Debian 12 slim; no build tools, no curl / wget |
   | `python-3.12` | Python 3.12, Debian 12 slim |
   | `go-1.24` | Go 1.24, Debian 12 (build stage: compile the binary here) |
   | `debian-12` | Debian 12 slim (runtime stage for a compiled binary, e.g. one built with `go-1.24`) |
   | `java-21-jdk` | Eclipse Temurin JDK 21 (build stage) |
   | `java-21-jre` | Eclipse Temurin JRE 21 (runtime stage) |
   | `maven-3.9-java-21` | Maven 3.9 + JDK 21 (build stage) |
   | `gradle-8-java-21` | Gradle 8 + JDK 21 (build stage) |
   | `tomcat-10.1-java-21` | Tomcat 10.1 + JDK 21 (WAR deployments, see stack conventions) |

   There is one stable version of each stack. A project developed against an older one (Node.js 20 or 22, Python 3.11, Java 17) usually builds and runs on it unchanged: use it rather than another public image. All are linux/amd64. MySQL and PostgreSQL are not used as base images; see the database service in [stack conventions](stacks.md).

2. **Another public image**: for example `nginx:1.27-alpine`, `golang:1.25-bookworm`. Images on Docker Hub are written the usual way (the platform pulls them through a mirror at build time; it is not kept ahead, so the first build waits for the download and can fail when the mirror is unreachable). Give an explicit version tag rather than `latest`. Other registries (ghcr.io, quay.io and so on) are not guaranteed to be reachable; when a pull fails, report it to the user.

The project's own Node / Python version constraint comes first: do not upgrade or downgrade it to suit the platform.

## Installing, upgrading and overriding on top of a base image

On any base image you may install system packages, upgrade the runtime or its tools, and overwrite files in the image. For example, the build tools a native module needs:

~~~dockerfile
FROM node-base AS build
RUN sed -i 's#deb.debian.org#mirrors.aliyun.com#g' /etc/apt/sources.list.d/debian.sources \
 && apt-get update \
 && apt-get install -y --no-install-recommends python3 make g++ \
 && rm -rf /var/lib/apt/lists/*
~~~

- On Debian / Ubuntu images, switch the package source to `mirrors.aliyun.com` before using apt (the official source downloads very slowly from the platform and drags the build into its time limit). On Alpine use `sed -i 's#dl-cdn.alpinelinux.org#mirrors.aliyun.com#g' /etc/apk/repositories`.
- Build tools belong in the build stage only; the runtime stage stays small (multi-stage build, copy only the output).
- Tools can be upgraded with `npm install -g npm@<version>` and the like; mind the lock file's compatibility.

## What the runtime stage must satisfy (whatever the image)

The server runs containers one fixed way, so the image has to:

- Run as user 10001:10001 (the Dockerfile's runtime stage has `USER 10001`). The application must not depend on root. Files it has to read inside the image are readable by that user.
- Live with a read-only root filesystem: at run time it can write only to the storage declared in the manifest (persistent or ephemeral). Cache directories (such as `/app/.next/cache`) are declared ephemeral.
- Need no Linux capabilities at all, and not bind a port below 1024 (containerPort is 1024–65535).
- Be linux/amd64.

The health check is made by the platform from outside the container, so the image needs no curl or wget for it.

## npm registry

npm dependencies use npmmirror (`https://registry.npmmirror.com`) by default, which is the fastest; the complete setup is in the [example project](example-nextjs-sqlite/) (`.npmrc`, `Dockerfile`).

- Add an `.npmrc` in the project's root (no credentials in it): `registry=https://registry.npmmirror.com`, plus the binary-mirror lines the actual dependencies need (such as `better_sqlite3_binary_host=https://registry.npmmirror.com/-/binary/better-sqlite3`). The Dockerfile's build stage copies `.npmrc` before `npm ci`.
- With Prisma, set `ENV PRISMA_ENGINES_MIRROR=https://registry.npmmirror.com/-/binary/prisma` in the build stage. When no browser is needed, set `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1`.
- The package-lock.json of npm 7+ needs no change. For yarn 1.x, replace `registry.yarnpkg.com` with `registry.npmmirror.com` in yarn.lock.
- Local `npm run dev` is not affected: `.npmrc` only changes where downloads come from.
- Native modules (such as better-sqlite3): prefer a version that has prebuilt binaries (better-sqlite3 12.11.1 is verified to have one for Node 24). When there is none, install the build tools in the build stage (see the section above) and compile from source.

## What the build can download

The build environment can reach the official npm registry, npmmirror, GitHub and Alibaba Cloud's system package mirrors, but some addresses abroad are slow. Check the resolved URLs in the lock file, binaries downloaded by install scripts, fonts, and external APIs called during the build; when a download is slow or times out, move it to a mirror in mainland China first.

## When to stop, and what to report

When pulling an image or downloading a dependency fails or times out, report the exact error and what is missing; do not retry without end. When handing over, say which base image each build stage uses.
