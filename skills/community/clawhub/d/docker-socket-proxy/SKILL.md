---
name: docker-socket-proxy
description: Manage a remote Docker host via a Tecnativa docker-socket-proxy instance. Unlike raw Docker socket access (which is root-equivalent), docker-socket-proxy acts as a firewall: each API section is individually enabled or disabled via env vars, so the agent only gets access to what you explicitly allow. Requires docker-socket-proxy exposed over TCP. Covers the full Docker REST API surface: container lifecycle (list, start, stop, restart, kill, pause, unpause, rename, exec), inspection (logs, stats, top, changes), images, networks, volumes, Swarm, plugins, system info, and event streaming.
homepage: https://github.com/BP602/docker-socket-proxy
metadata: {"openclaw":{"requires":{"bins":["curl","jq"]}}}
---

# Docker Socket Proxy

Manages Docker containers via the `tecnativa/docker-socket-proxy` REST API using `curl` and `jq`. Which modes are available depends on which API sections the proxy instance has enabled.

## Trigger conditions

- User asks to list, start, stop, restart, kill, pause, or unpause a container or service
- User wants container logs, stats, top processes, or filesystem changes
- User asks about Docker images, networks, volumes, swarm services, or tasks
- A service needs to be restarted after a config change

## Usage

```
bash {baseDir}/scripts/run-docker.sh <mode> [args...]
```

Run with no arguments for full usage. Proxy URL is resolved from `$DOCKER_PROXY_URL` → `$DOCKER_HOST` (tcp→http) → `http://localhost:2375`.

## Modes

### System
| Mode | Description |
|------|-------------|
| `ping` | Health check |
| `version` | Docker version |
| `info` | Host summary (containers, memory, etc.) |
| `events [--since T] [--until T] [--filters k=v]` | Recent events (1s window) |
| `system-df` | Disk usage by images/containers/volumes |

### Containers
| Mode | Description |
|------|-------------|
| `list` | Running containers |
| `list-all` | All containers including stopped |
| `inspect <name>` | Full container details |
| `top <name> [ps-args]` | Running processes inside container |
| `logs <name> [tail]` | Container logs (default tail=100) |
| `stats <name>` | CPU, memory, network, block I/O |
| `changes <name>` | Filesystem changes since start |
| `start <name>` | Start container |
| `stop <name> [timeout]` | Stop container |
| `restart <name> [timeout]` | Restart container |
| `kill <name> [signal]` | Kill container (default SIGKILL) |
| `pause <name>` | Pause container |
| `unpause <name>` | Unpause container |
| `rename <name> <new-name>` | Rename container |
| `exec <name> <cmd> [args...]` | Run command in container |
| `prune-containers` | Remove stopped containers |

### Images
| Mode | Description |
|------|-------------|
| `images` | List images |
| `image-inspect <name>` | Image details |
| `image-history <name>` | Layer history |
| `prune-images` | Remove unused images |

### Networks
| Mode | Description |
|------|-------------|
| `networks` | List networks |
| `network-inspect <name>` | Network details and connected containers |
| `prune-networks` | Remove unused networks |

### Volumes
| Mode | Description |
|------|-------------|
| `volumes` | List volumes |
| `volume-inspect <name>` | Volume details |
| `prune-volumes` | Remove unused volumes |

### Swarm
| Mode | Description |
|------|-------------|
| `swarm` | Swarm info |
| `nodes` | List nodes |
| `node-inspect <name>` | Node details |
| `services` | List services |
| `service-inspect <name>` | Service details |
| `service-logs <name> [tail]` | Service logs |
| `tasks` | List tasks |
| `configs` | List configs |
| `secrets` | List secrets |

### Plugins
| Mode | Description |
|------|-------------|
| `plugins` | List plugins |

## Name matching

Container names can be partial — `myapp` matches `project-myapp-1`. Exact match is tried first, then substring. Errors clearly if 0 or 2+ containers match.

## Notes

- Modes that require disabled proxy sections (e.g. `IMAGES`, `NETWORKS`, `VOLUMES`, `SYSTEM`) will return HTTP 403. This is expected — enable the relevant env var on the proxy to unlock them.
- `exec` is two-step (create + start) and streams multiplexed output.
- `events` uses a 1-second window by default; use `--since` / `--until` to adjust.
