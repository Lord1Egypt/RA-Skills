# Docker Socket Proxy

OpenClaw skill for managing Docker containers via a [Tecnativa docker-socket-proxy](https://github.com/Tecnativa/docker-socket-proxy) instance.

## Why docker-socket-proxy

Exposing the raw Docker socket to an agent is equivalent to giving it root access to the host — it can mount any path, run privileged containers, or do anything the Docker daemon allows.

docker-socket-proxy sits in front of the socket and acts as a firewall. Each API section (containers, images, networks, volumes, Swarm, etc.) is individually toggled on or off via env vars. The agent can only do what you explicitly enable. If you only turn on `CONTAINERS=1` and `ALLOW_RESTARTS=1`, it can restart containers and nothing else.

Use this skill when you want an agent that can manage Docker without handing it the keys to the host.

## Requirements

- [`tecnativa/docker-socket-proxy`](https://github.com/Tecnativa/docker-socket-proxy) running and exposed over TCP
- `$DOCKER_HOST` set to the proxy address (e.g. `tcp://docker-host:2375`), or `$DOCKER_PROXY_URL` set to the HTTP equivalent
- `curl` and `jq` on PATH

## Features

Covers the full Docker REST API surface exposed by docker-socket-proxy:

| Category | Operations |
|----------|-----------|
| System | ping, version, info, events, disk usage |
| Containers | list, inspect, top, logs, stats, filesystem changes, start, stop, restart, kill, pause, unpause, rename, exec, prune |
| Images | list, inspect, history, prune |
| Networks | list, inspect, prune |
| Volumes | list, inspect, prune |
| Swarm | info, nodes, services, tasks, configs, secrets |
| Plugins | list |

Available modes depend on which API sections are enabled on your proxy instance. Disabled sections return HTTP 403.

## Installation

```bash
clawhub install docker-socket-proxy
```

Or copy the skill directory into your OpenClaw workspace:

```
~/.openclaw/workspace/skills/docker-socket-proxy/
```

## Usage

```bash
bash {baseDir}/scripts/run-docker.sh <mode> [args...]
```

Run with no arguments for the full mode reference.

### Examples

```bash
# List running containers
bash scripts/run-docker.sh list

# Show logs (last 50 lines)
bash scripts/run-docker.sh logs myapp 50

# Restart a container by partial name
bash scripts/run-docker.sh restart myapp

# Container resource usage
bash scripts/run-docker.sh stats myapp

# Stream recent events
bash scripts/run-docker.sh events

# List all images
bash scripts/run-docker.sh images
```

### Name matching

Container names support partial matching: `myapp` matches `project-myapp-1`. Exact match is tried first, then substring. Errors clearly if 0 or 2+ containers match.

## Configuration

| Variable | Description |
|----------|-------------|
| `DOCKER_PROXY_URL` | HTTP URL of the proxy (e.g. `http://docker-host:2375`) |
| `DOCKER_HOST` | Standard Docker host in `tcp://host:port` format, auto-converted to HTTP |

If neither is set, defaults to `http://localhost:2375`.

## License

MIT-0 (as required by ClawhHub)
