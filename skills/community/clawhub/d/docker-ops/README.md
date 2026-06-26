# docker-ops

An OpenClaw agent skill for managing Docker containers via docker-socket-proxy.

## Overview

This skill provides safe, whitelist-controlled Docker container management:
- **Status reports** — container health, resource usage, uptime
- **Log analysis** — error/warning counts, filtered log output
- **Restarts** — controlled restarts with post-restart verification

All operations go through a docker-socket-proxy (read-only socket access + limited write for restarts).

## Prerequisites

- `docker` CLI available in PATH
- `jq` available in PATH
- `DOCKER_HOST` environment variable pointing to the docker-socket-proxy (e.g. `tcp://docker-socket-proxy:2375`)
- A whitelist YAML file defining allowed containers

## Whitelist

The skill reads a YAML whitelist to determine which containers it can operate on:

```yaml
containers:
  - name: my_container
    description: "Service description"
    can_restart: true
```

**Path resolution:**
- `SYSCTL_WHITELIST_PATH` environment variable (required). There is no fallback — if the variable is not set, no Docker commands will be executed.

## Security Model

### Allowed commands
- `docker ps` — list containers
- `docker inspect` — container details
- `docker stats --no-stream` — resource usage (one-shot)
- `docker logs --since --tail` — log analysis
- `docker restart` — restart (explicit user request only)

### Forbidden commands
Everything else: `rm`, `stop`, `kill`, `exec`, `run`, `pull`, `build`, `push`, `network`, `volume`, `image`, `system`, `compose`.

### Safety rules
- Container names are validated against the whitelist before any command
- User input is never passed directly into shell commands
- Restarts require explicit user request and `can_restart: true` in the whitelist
- Log output is capped at 500 lines per query

## Directory Structure

```
docker-ops/
├── SKILL.md                         # Main skill instructions
├── README.md                        # This file
├── LICENSE                          # MIT License
├── CHANGELOG.md                     # Version history
├── references/
│   └── docker-commands.md           # Docker CLI quick reference
└── scripts/
    └── container-report.sh          # Automated report script
```

## Usage

This skill is used by the SysCtl agent automatically. When a user asks for container status, logs, or a restart, the agent follows the procedures defined in `SKILL.md`.

### Example requests
- "Status report for uuidgen"
- "Show errors in the last 2 hours"
- "Restart the uuidgen container"

## License

MIT — see [LICENSE](LICENSE).
