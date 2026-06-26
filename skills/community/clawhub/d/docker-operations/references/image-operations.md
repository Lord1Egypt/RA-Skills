# Image Operations Commands

Commands for managing Docker images - pulling, pushing, building, tagging, saving, loading, and removing.

## docker images

List images.

```bash
docker images [OPTIONS] [REPOSITORY[:TAG]]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Show all images (default hides intermediate images) |
| `--digests` | Show digests |
| `-f, --filter filter` | Filter output based on conditions provided |
| `--format string` | Format output using a custom template |
| `--no-trunc` | Don't truncate output |
| `-q, --quiet` | Only show image IDs |
| `--tree` | List multi-platform images as a tree (EXPERIMENTAL) |

**Format templates:**
- `table`: Print output in table format with column headers (default)
- `json`: Print in JSON format

**Examples:**
```bash
docker images
docker images nginx
docker images -q
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## docker pull

Download an image from a registry.

```bash
docker pull [OPTIONS] NAME[:TAG|@DIGEST]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all-tags` | Download all tagged images in the repository |
| `--disable-content-trust` | Skip image verification (default true) |
| `--platform string` | Set platform if server is multi-platform capable |
| `-q, --quiet` | Suppress verbose output |

**Examples:**
```bash
docker pull nginx:latest
docker pull ubuntu:22.04
docker pull myregistry.com/myimage:tag
docker pull --all-tags nginx
docker pull --quiet nginx
```

## docker push

Upload an image to a registry.

```bash
docker push [OPTIONS] NAME[:TAG]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all-tags` | Push all tags of an image to the repository |
| `--disable-content-trust` | Skip image signing (default true) |
| `--platform string` | Push a platform-specific manifest as a single-platform image |
| `-q, --quiet` | Suppress verbose output |

**Examples:**
```bash
docker push myregistry.com/myimage:tag
docker push myimage:latest
docker push --all-tags myimage
```

## docker build

Build an image from a Dockerfile.

```bash
docker build [OPTIONS] PATH | URL | -
```

**Options:**
| Option | Description |
|--------|-------------|
| `--add-host list` | Add a custom host-to-IP mapping ("host:ip") |
| `--build-arg list` | Set build-time variables |
| `--cache-from strings` | Images to consider as cache sources |
| `--cgroup-parent string` | Set the parent cgroup for the "RUN" instructions during build |
| `--compress` | Compress the build context using gzip |
| `--cpu-period int` | Limit the CPU CFS period |
| `--cpu-quota int` | Limit the CPU CFS quota |
| `-c, --cpu-shares int` | CPU shares (relative weight) |
| `--cpuset-cpus string` | CPUs in which to allow execution (0-3, 0,1) |
| `--cpuset-mems string` | MEMs in which to allow execution (0-3, 0,1) |
| `--disable-content-trust` | Skip image verification (default true) |
| `-f, --file string` | Name of the Dockerfile (Default is "PATH/Dockerfile") |
| `--force-rm` | Always remove intermediate containers |
| `--iidfile string` | Write the image ID to the file |
| `--isolation string` | Container isolation technology |
| `--label list` | Set metadata for an image |
| `-m, --memory bytes` | Memory limit |
| `--memory-swap bytes` | Swap limit equal to memory plus swap |
| `--network string` | Set the networking mode for the RUN instructions during build |
| `--no-cache` | Do not use cache when building the image |
| `--platform string` | Set platform if server is multi-platform capable |
| `--pull` | Always attempt to pull a newer version of the image |
| `-q, --quiet` | Suppress the build output and print image ID on success |
| `--rm` | Remove intermediate containers after a successful build (default true) |
| `--security-opt strings` | Security options |
| `--shm-size bytes` | Size of "/dev/shm" |
| `-t, --tag list` | Name and optionally a tag in the "name:tag" format |
| `--target string` | Set the target build stage to build |
| `--ulimit ulimit` | Ulimit options |

**Examples:**
```bash
docker build -t myapp:latest .
docker build -t myapp:1.0 -f Dockerfile.prod .
docker build --build-arg VERSION=1.0 -t myapp:latest .
docker build --no-cache -t myapp:latest .
docker build --pull -t myapp:latest .
docker build -t myapp:latest -m 512m .
```

## docker tag

Create a tag TARGET_IMAGE that refers to SOURCE_IMAGE.

```bash
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```

**Examples:**
```bash
docker tag nginx:latest myregistry.com/nginx:latest
docker tag myapp:latest myapp:v1.0.0
```

## docker save

Save one or more images to a tar archive (streamed to STDOUT by default).

```bash
docker save [OPTIONS] IMAGE [IMAGE...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-o, --output string` | Write to a file, instead of STDOUT |

**Examples:**
```bash
docker save -o nginx.tar nginx:latest
docker save -o images.tar image1:latest image2:latest
docker save nginx:latest > nginx.tar
```

## docker load

Load an image from a tar archive or STDIN.

```bash
docker load [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-i, --input string` | Read from tar archive file, instead of STDIN |
| `-q, --quiet` | Suppress the load output |

**Examples:**
```bash
docker load -i nginx.tar
docker load < nginx.tar
docker load --quiet -i nginx.tar
```

## docker export

Export a container's filesystem as a tar archive.

```bash
docker export [OPTIONS] CONTAINER
```

**Options:**
| Option | Description |
|--------|-------------|
| `-o, --output string` | Write to a file, instead of STDOUT |

**Examples:**
```bash
docker export my_container -o my_container.tar
docker export my_container > my_container.tar
```

## docker import

Import the contents from a tarball to create a filesystem image.

```bash
docker import [OPTIONS] file|URL|- [REPOSITORY[:TAG]]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-c, --change list` | Apply Dockerfile instruction to the created image |
| `-m, --message string` | Set commit message for imported image |
| `--platform string` | Set platform if server is multi-platform capable |

**Examples:**
```bash
docker import my_container.tar
docker import my_container.tar myimage:1.0
docker import -c "ENV VAR=value" my_container.tar
```

## docker history

Show the history of an image.

```bash
docker history [OPTIONS] IMAGE
```

**Options:**
| Option | Description |
|--------|-------------|
| `--format string` | Format output using a custom template |
| `-H, --human` | Print sizes and dates in human readable format (default true) |
| `--no-trunc` | Don't truncate output |
| `-q, --quiet` | Only show image IDs |

**Examples:**
```bash
docker history nginx
docker history --no-trunc nginx
docker history -q nginx
docker history --format "{{.ID}}: {{.CreatedBy}}" nginx
```

## docker rmi

Remove one or more images.

```bash
docker rmi [OPTIONS] IMAGE [IMAGE...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --force` | Force removal of the image |
| `--no-prune` | Do not delete untagged parent images |

**Examples:**
```bash
docker rmi nginx:latest
docker rmi myapp:1.0 myapp:2.0
docker rmi -f myapp:latest
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| List images | `docker images` |
| List image IDs | `docker images -q` |
| Pull image | `docker pull <image>:<tag>` |
| Push image | `docker push <image>:<tag>` |
| Build image | `docker build -t <name>:<tag> <path>` |
| Tag image | `docker tag <source> <target>` |
| Save image | `docker save -o <file> <image>` |
| Load image | `docker load -i <file>` |
| Export container | `docker export -o <file> <container>` |
| Import tarball | `docker import <file> <image>:<tag>` |
| Show history | `docker history <image>` |
| Remove image | `docker rmi <image>` |
| Force remove | `docker rmi -f <image>` |
