# Container Lifecycle Commands

Commands for creating, starting, stopping, pausing, and managing container lifecycle.

## docker create

Create a container without starting it.

```bash
docker create [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--add-host list` | Add a custom host-to-IP mapping (host:ip) |
| `--annotation map` | Add an annotation to the container |
| `-a, --attach list` | Attach to STDIN, STDOUT or STDERR |
| `--blkio-weight uint16` | Block IO (relative weight), between 10 and 1000 |
| `--cap-add list` | Add Linux capabilities |
| `--cap-drop list` | Drop Linux capabilities |
| `--cgroup-parent string` | Optional parent cgroup for the container |
| `--cidfile string` | Write the container ID to the file |
| `--cpu-period int` | Limit CPU CFS period |
| `--cpu-quota int` | Limit CPU CFS quota |
| `-c, --cpu-shares int` | CPU shares (relative weight) |
| `--cpus decimal` | Number of CPUs |
| `--cpuset-cpus string` | CPUs in which to allow execution (0-3, 0,1) |
| `--cpuset-mems string` | MEMs in which to allow execution (0-3, 0,1) |
| `-d, --detach` | Run container in background |
| `--detach-keys string` | Override the key sequence for detaching |
| `--device list` | Add a host device to the container |
| `--device-read-bps list` | Limit read rate (bytes per second) from a device |
| `--device-read-iops list` | Limit read rate (IO per second) from a device |
| `--device-write-bps list` | Limit write rate (bytes per second) to a device |
| `--device-write-iops list` | Limit write rate (IO per second) to a device |
| `--disable-content-trust` | Skip image verification (default true) |
| `--dns list` | Set custom DNS servers |
| `--dns-option list` | Set DNS options |
| `--dns-search list` | Set custom DNS search domains |
| `-e, --env list` | Set environment variables |
| `--env-file list` | Read in a file of environment variables |
| `--expose list` | Expose a port or a range of ports |
| `--gpus gpu-request` | GPU devices to add to the container |
| `--group-add list` | Add additional groups to join |
| `--health-cmd string` | Command to run to check health |
| `--health-interval duration` | Time between running the check |
| `--health-retries int` | Consecutive failures needed to report unhealthy |
| `--health-timeout duration` | Maximum time to allow one check to run |
| `-h, --hostname string` | Container host name |
| `--init` | Run an init inside the container |
| `-i, --interactive` | Keep STDIN open even if not attached |
| `--ip string` | IPv4 address |
| `--ip6 string` | IPv6 address |
| `--isolation string` | Container isolation technology |
| `-l, --label list` | Set meta data on a container |
| `--link list` | Add link to another container |
| `--log-driver string` | Logging driver for the container |
| `--log-opt list` | Log driver options |
| `--mac-address string` | Container MAC address |
| `-m, --memory bytes` | Memory limit |
| `--memory-reservation bytes` | Memory soft limit |
| `--memory-swap bytes` | Swap limit equal to memory plus swap |
| `--mount mount` | Attach a filesystem mount to the container |
| `--name string` | Assign a name to the container |
| `--network network` | Connect a container to a network |
| `--network-alias list` | Add network-scoped alias for the container |
| `--no-healthcheck` | Disable any container-specified HEALTHCHECK |
| `--oom-kill-disable` | Disable OOM Killer |
| `-p, --publish list` | Publish a container's port(s) to the host |
| `-P, --publish-all` | Publish all exposed ports to random ports |
| `--pull string` | Pull image before creating ("always", "missing", "never") |
| `-q, --quiet` | Suppress the pull output |
| `--read-only` | Mount the container's root filesystem as read only |
| `--restart string` | Restart policy to apply when a container exits |
| `--rm` | Automatically remove the container when it exits |
| `--runtime string` | Runtime to use for this container |
| `--security-opt list` | Security Options |
| `--shm-size bytes` | Size of /dev/shm |
| `--stop-signal string` | Signal to stop the container |
| `--stop-timeout int` | Timeout (in seconds) to stop a container |
| `-t, --tty` | Allocate a pseudo-TTY |
| `-u, --user string` | Username or UID |
| `-v, --volume list` | Bind mount a volume |
| `--volumes-from list` | Mount volumes from the specified container(s) |
| `-w, --workdir string` | Working directory inside the container |

**Examples:**
```bash
docker create nginx
docker create --name my_container -p 8080:80 -e ENV=prod nginx
docker create --memory 512m --cpus 0.5 nginx
```

## docker start

Start one or more stopped containers.

```bash
docker start [OPTIONS] CONTAINER [CONTAINER...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --attach` | Attach STDOUT/STDERR and forward signals |
| `--detach-keys string` | Override the key sequence for detaching a container |
| `-i, --interactive` | Attach container's STDIN |

**Examples:**
```bash
docker start my_container
docker start -a my_container
docker start -i my_container
```

## docker run

Create and run a new container from an image.

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--add-host list` | Add a custom host-to-IP mapping (host:ip) |
| `--annotation map` | Add an annotation to the container |
| `-a, --attach list` | Attach to STDIN, STDOUT or STDERR |
| `--blkio-weight uint16` | Block IO (relative weight), between 10 and 1000 |
| `--cap-add list` | Add Linux capabilities |
| `--cap-drop list` | Drop Linux capabilities |
| `--cgroup-parent string` | Optional parent cgroup for the container |
| `--cidfile string` | Write the container ID to the file |
| `--cpu-period int` | Limit CPU CFS period |
| `--cpu-quota int` | Limit CPU CFS quota |
| `-c, --cpu-shares int` | CPU shares (relative weight) |
| `--cpus decimal` | Number of CPUs |
| `--cpuset-cpus string` | CPUs in which to allow execution (0-3, 0,1) |
| `--cpuset-mems string` | MEMs in which to allow execution (0-3, 0,1) |
| `-d, --detach` | Run container in background and print container ID |
| `--detach-keys string` | Override the key sequence for detaching a container |
| `--device list` | Add a host device to the container |
| `--device-read-bps list` | Limit read rate (bytes per second) from a device |
| `--device-read-iops list` | Limit read rate (IO per second) from a device |
| `--device-write-bps list` | Limit write rate (bytes per second) to a device |
| `--device-write-iops list` | Limit write rate (IO per second) to a device |
| `--disable-content-trust` | Skip image verification (default true) |
| `--dns list` | Set custom DNS servers |
| `--dns-option list` | Set DNS options |
| `--dns-search list` | Set custom DNS search domains |
| `-e, --env list` | Set environment variables |
| `--env-file list` | Read in a file of environment variables |
| `--expose list` | Expose a port or a range of ports |
| `--gpus gpu-request` | GPU devices to add to the container |
| `--group-add list` | Add additional groups to join |
| `--health-cmd string` | Command to run to check health |
| `--health-interval duration` | Time between running the check |
| `--health-retries int` | Consecutive failures needed to report unhealthy |
| `--health-timeout duration` | Maximum time to allow one check to run |
| `-h, --hostname string` | Container host name |
| `--init` | Run an init inside the container |
| `-i, --interactive` | Keep STDIN open even if not attached |
| `--ip string` | IPv4 address |
| `--ip6 string` | IPv6 address |
| `--isolation string` | Container isolation technology |
| `-l, --label list` | Set meta data on a container |
| `--link list` | Add link to another container |
| `--log-driver string` | Logging driver for the container |
| `--log-opt list` | Log driver options |
| `--mac-address string` | Container MAC address |
| `-m, --memory bytes` | Memory limit |
| `--memory-reservation bytes` | Memory soft limit |
| `--memory-swap bytes` | Swap limit equal to memory plus swap |
| `--mount mount` | Attach a filesystem mount to the container |
| `--name string` | Assign a name to the container |
| `--network network` | Connect a container to a network |
| `--network-alias list` | Add network-scoped alias for the container |
| `--no-healthcheck` | Disable any container-specified HEALTHCHECK |
| `--oom-kill-disable` | Disable OOM Killer |
| `-p, --publish list` | Publish a container's port(s) to the host |
| `-P, --publish-all` | Publish all exposed ports to random ports |
| `--pull string` | Pull image before running ("always", "missing", "never") |
| `-q, --quiet` | Suppress the pull output |
| `--read-only` | Mount the container's root filesystem as read only |
| `--restart string` | Restart policy to apply when a container exits |
| `--rm` | Automatically remove the container when it exits |
| `--runtime string` | Runtime to use for this container |
| `--security-opt list` | Security Options |
| `--shm-size bytes` | Size of /dev/shm |
| `--sig-proxy` | Proxy received signals to the process (default true) |
| `--stop-signal string` | Signal to stop the container |
| `--stop-timeout int` | Timeout (in seconds) to stop a container |
| `-t, --tty` | Allocate a pseudo-TTY |
| `-u, --user string` | Username or UID |
| `-v, --volume list` | Bind mount a volume |
| `--volumes-from list` | Mount volumes from the specified container(s) |
| `-w, --workdir string` | Working directory inside the container |

**Examples:**
```bash
docker run nginx
docker run -d --name web -p 8080:80 nginx
docker run -it ubuntu bash
docker run --rm -v $(pwd):/app nginx
docker run --memory 512m --cpus 0.5 nginx
```

## docker stop

Stop one or more running containers.

```bash
docker stop [OPTIONS] CONTAINER [CONTAINER...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-s, --signal string` | Signal to send to the container |
| `-t, --timeout int` | Seconds to wait before killing the container (default: 10) |

**Examples:**
```bash
docker stop my_container
docker stop -t 30 my_container
docker stop $(docker ps -q)
```

## docker restart

Restart one or more containers.

```bash
docker restart [OPTIONS] CONTAINER [CONTAINER...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-s, --signal string` | Signal to send to the container |
| `-t, --timeout int` | Seconds to wait before killing the container (default: 10) |

**Examples:**
```bash
docker restart my_container
docker restart -t 30 my_container
docker restart $(docker ps -q)
```

> ⚠️ Confirm with user before stopping/restarting production containers.

## docker pause

Pause all processes within one or more containers.

```bash
docker pause CONTAINER [CONTAINER...]
```

**Examples:**
```bash
docker pause my_container
docker pause container1 container2
```

## docker unpause

Unpause all processes within one or more containers.

```bash
docker unpause CONTAINER [CONTAINER...]
```

**Examples:**
```bash
docker unpause my_container
```

## docker rm

Remove one or more containers.

```bash
docker rm [OPTIONS] CONTAINER [CONTAINER...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-f, --force` | Force the removal of a running container (uses SIGKILL) |
| `-l, --link` | Remove the specified link |
| `-v, --volumes` | Remove anonymous volumes associated with the container |

**Examples:**
```bash
docker rm my_container
docker rm -f my_container
docker rm -v my_container
docker rm $(docker ps -aq)
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Create container | `docker create <image>` |
| Start container | `docker start <id>` |
| Run container | `docker run <image>` |
| Stop container | `docker stop <id>` |
| Restart container | `docker restart <id>` |
| Pause container | `docker pause <id>` |
| Unpause container | `docker unpause <id>` |
| Remove container | `docker rm <id>` |
| Run interactively | `docker run -it <image> bash` |
| Run detached | `docker run -d <image>` |
| Remove after exit | `docker run --rm <image>` |
