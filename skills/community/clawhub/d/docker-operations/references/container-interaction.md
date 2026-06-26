# Container Interaction Commands

Commands for interacting with running containers - executing commands, viewing logs, copying files, and monitoring.

## docker exec

Execute a command in a running container.

```bash
docker exec [OPTIONS] CONTAINER COMMAND [ARG...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-d, --detach` | Detached mode: run command in the background |
| `--detach-keys string` | Override the key sequence for detaching a container |
| `-e, --env list` | Set environment variables |
| `--env-file list` | Read in a file of environment variables |
| `-i, --interactive` | Keep STDIN open even if not attached |
| `--privileged` | Give extended privileges to the command |
| `-t, --tty` | Allocate a pseudo-TTY |
| `-u, --user string` | Username or UID (format: "<name|uid>[:<group|gid>]") |
| `-w, --workdir string` | Working directory inside the container |

**Examples:**
```bash
docker exec -it my_container bash
docker exec my_container ls -la
docker exec -u www-data my_container whoami
docker exec -d my_container sleep 100
docker exec -w /app my_container node index.js
```

## docker attach

Attach local standard input, output, and error streams to a running container.

```bash
docker attach [OPTIONS] CONTAINER
```

**Options:**
| Option | Description |
|--------|-------------|
| `--detach-keys string` | Override the key sequence for detaching a container |
| `--no-stdin` | Do not attach STDIN |
| `--sig-proxy` | Proxy all received signals to the process (default true) |

**Examples:**
```bash
docker attach my_container
docker attach --sig-proxy=false my_container
```

> Use `--detach-keys` to customize the key sequence for detaching.

## docker logs

Fetch the logs of a container.

```bash
docker logs [OPTIONS] CONTAINER
```

**Options:**
| Option | Description |
|--------|-------------|
| `--details` | Show extra details provided to logs |
| `-f, --follow` | Follow log output (like tail -f) |
| `--since string` | Show logs since timestamp (e.g. "2013-01-02T13:23:37Z") or relative (e.g. "42m") |
| `-n, --tail string` | Number of lines to show from the end of the logs (default "all") |
| `-t, --timestamps` | Show timestamps |
| `--until string` | Show logs before a timestamp or relative (e.g. "42m") |

**Examples:**
```bash
docker logs my_container
docker logs -f my_container
docker logs --tail 100 my_container
docker logs --since 2h my_container
docker logs --since 2024-01-01 my_container
docker logs --timestamps my_container
```

## docker top

Display the running processes of a container.

```bash
docker top CONTAINER [ps OPTIONS]
```

**Examples:**
```bash
docker top my_container
docker top my_container aux
```

## docker stats

Display a live stream of container(s) resource usage statistics.

```bash
docker stats [OPTIONS] [CONTAINER...]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Show all containers (default shows just running) |
| `--format string` | Format output using a custom template |
| `--no-stream` | Disable streaming stats and only pull the first result |
| `--no-trunc` | Do not truncate output |

**Format templates:**
- `table`: Print output in table format with column headers (default)
- `json`: Print in JSON format
- Custom: `{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}`

**Examples:**
```bash
docker stats my_container
docker stats --no-stream my_container
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
docker stats --all
```

## docker cp

Copy files/folders between a container and the local filesystem.

```bash
docker cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-
docker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --archive` | Archive mode (copy all uid/gid information) |
| `-L, --follow-link` | Always follow symbol link in SRC_PATH |
| `-q, --quiet` | Suppress progress output during copy |

**Examples:**
```bash
docker cp my_container:/app/config.json ./config.json
docker cp ./upload.txt my_container:/var/www/uploads/
docker cp my_container:/var/logs/. - | tar xf -
docker cp -a my_container:/data ./data
```

## docker diff

Inspect changes to files or directories on a container's filesystem.

```bash
docker diff CONTAINER
```

**Output indicators:**
- `A` - Added
- `D` - Deleted
- `C` - Changed

**Examples:**
```bash
docker diff my_container
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Execute command | `docker exec -it <id> bash` |
| Execute detached | `docker exec -d <id> <command>` |
| Attach to container | `docker attach <id>` |
| View logs | `docker logs -f <id>` |
| View last 100 lines | `docker logs --tail 100 <id>` |
| View since time | `docker logs --since 2h <id>` |
| Show timestamps | `docker logs -t <id>` |
| Show processes | `docker top <id>` |
| Show resource usage | `docker stats <id>` |
| Stream stats | `docker stats <id>` |
| Non-streaming stats | `docker stats --no-stream <id>` |
| Copy from container | `docker cp <id>:/path dest` |
| Copy to container | `docker cp src <id>:/path` |
| Show filesystem changes | `docker diff <id>` |
