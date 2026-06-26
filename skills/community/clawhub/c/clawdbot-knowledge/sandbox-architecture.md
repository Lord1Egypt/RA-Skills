# Sandbox Architecture

OpenClaw uses Docker containers to provide isolated execution environments for agents. This document explains the architecture, container types, and lifecycle.

## Overview

OpenClaw sandbox architecture provides:
- **Isolation** - Each agent/session runs in its own container
- **Security** - Restricted tool access and permissions per policy
- **Consistency** - Reproducible execution environments
- **Scalability** - Multiple agents can run in parallel

## Container Types

### Agent Containers

**Purpose:** Isolated execution environments for specific AI agents.

**Naming:** `openclaw-agent-<agent-name>`

**Characteristics:**
- Dedicated workspace directory
- Agent-specific tool permissions
- Isolated from other agents
- Persistent across agent turns

**Use cases:**
- Autonomous coding agents (Codex, Claude Code)
- Task-specific agents (testing, deployment)
- Long-running background processes

### Browser Containers

**Purpose:** Dedicated Chrome/Chromium instances for web automation.

**Naming:** `openclaw-browser-<session-name>`

**Characteristics:**
- Full browser environment
- Access to web APIs
- Isolated cookies and sessions
- Can be controlled via automation

**Use cases:**
- Web scraping
- Browser testing
- Form filling
- Screenshot generation

### Session Containers

**Purpose:** Workspace-isolated environments for conversation sessions.

**Naming:** `openclaw-session-<session-key>`

**Characteristics:**
- Session-specific workspace
- Inherits default tool policy
- Temporary (lifespan tied to session)
- Clean state per session

**Use cases:**
- Single conversation interactions
- Short-term tasks
- Testing/experimentation
- Multi-user environments

## Container Lifecycle

### Creation

Containers are created when:

1. **Agent starts** - First turn of an autonomous agent
2. **Session begins** - New conversation session
3. **Browser requested** - First web automation task

```bash
# Automatic creation
openclaw agent --to +15555550123 --message "Run analysis"
# Creates: openclaw-session-main
```

### Running

Containers run continuously until:

- **Agent shutdown** - Autonomous agent stopped
- **Session ends** - Conversation closed
- **Manual recreation** - Explicit `recreate` command

```bash
# Check running containers
openclaw sandbox list
docker ps | grep openclaw
```

### Recreation

Containers are recreated when:

- **Config changes** - OpenClaw config updated
- **Docker updates** - Base image changed
- **Manual command** - `recreate` command run
- **Corruption detected** - Container damaged

```bash
# Force recreation
openclaw sandbox recreate --all
openclaw sandbox recreate --session main
openclaw sandbox recreate --agent mybot
```

### Removal

Containers are removed during recreation or when:

- **Session expires** - Inactive for extended period
- **Agent deleted** - Agent configuration removed
- **Manual cleanup** - `docker rm` command

```bash
# Manual cleanup
docker ps -a | grep openclaw | awk '{print $1}' | xargs docker rm -f
```

## Docker Images

OpenClaw uses pre-built Docker images for containers:

| Container Type | Base Image | Size |
|----------------|------------|------|
| Agent | `openclaw/agent:latest` | ~500MB |
| Browser | `openclaw/browser:latest` | ~1.2GB |
| Session | `openclaw/session:latest` | ~400MB |

**Image updates:**
- Pulled automatically on first run
- Updated via `openclaw update`
- Can be updated manually with `docker pull`

## Networking

Containers use Docker bridge networking:

- **Bridge network:** Default for all containers
- **Port mapping:** Browser containers expose specific ports
- **DNS resolution:** Containers can resolve each other by name

**Network isolation:**
- No internet access by default (unless configured)
- Inter-container communication allowed
- Host access restricted by policy

## Storage

### Workspace Volumes

Each container mounts a workspace directory:

```bash
# Agent container
~/.openclaw/workspaces/agents/<agent-name>:/workspace

# Session container
~/.openclaw/workspaces/sessions/<session-key>:/workspace

# Browser container (temporary)
/tmp/openclaw-browser-<session>:/workspace
```

### Persistence

- **Agent containers:** Persistent workspace (survives recreation)
- **Session containers:** Temporary workspace (cleared on recreation)
- **Browser containers:** No persistence (state lost on exit)

## Resource Limits

Default resource limits per container:

| Resource | Limit | Description |
|----------|-------|-------------|
| CPU | 2 cores | Maximum CPU usage |
| Memory | 2GB | Maximum RAM usage |
| Disk | 10GB | Workspace storage limit |
| Network | Restricted | Tool-dependent access |

**Customization:** Limits can be adjusted in `~/.openclaw/openclaw.json`.

## Security Model

### Isolation Levels

| Level | Isolation | Use Case |
|-------|-----------|----------|
| **Full** | Complete isolation | Production, sensitive data |
| **Standard** | Normal sandbox | Development, testing |
| **Permissive** | Relaxed restrictions | Trusted environments |

### Tool Access

Tool access is controlled by policy:

```bash
# Check policy
openclaw sandbox explain

# Example output
Allowed tools:
  - exec (bash, python, node)
  - filesystem (read, write)
  - network (http, https)

Denied tools:
  - docker
  - system (reboot, shutdown)
```

## Monitoring

### Container Health

Check container health:

```bash
# OpenClaw CLI
openclaw sandbox list

# Docker commands
docker ps --filter "name=openclaw" --format "table {{.Names}}\t{{.Status}}"
docker stats --no-stream --filter "name=openclaw"
```

### Logs

View container logs:

```bash
# Docker logs
docker logs openclaw-agent-mybot
docker logs -f openclaw-session-main  # Follow logs

# OpenClaw logs
openclaw logs --session main
```

### Resource Usage

Monitor resource consumption:

```bash
# Docker stats
docker stats --filter "name=openclaw"

# System resources
docker exec openclaw-agent-mybot top
docker exec openclaw-session-main df -h
```

## Troubleshooting

### Container Won't Start

```bash
# Check Docker daemon
docker info

# Check image
docker images | grep openclaw

# Check logs
docker logs <container-name>

# Force recreation
openclaw sandbox recreate --all
```

### Permission Errors

```bash
# Check policy
openclaw sandbox explain

# Verify Docker permissions
groups | grep docker

# Restart Docker
sudo systemctl restart docker
```

### Disk Space Issues

```bash
# Check disk usage
docker system df

# Clean up
docker system prune -a

# Check workspace size
du -sh ~/.openclaw/workspaces/
```

## Best Practices

1. **Recreate selectively** - Use `--session` or `--agent` instead of `--all`
2. **Monitor resources** - Keep an eye on CPU, memory, and disk usage
3. **Backup workspaces** - Save important data before recreation
4. **Check policies** - Always review `explain` output before troubleshooting
5. **Clean up regularly** - Remove unused containers and images

## Advanced Topics

### Custom Container Images

Create custom agent images:

```dockerfile
FROM openclaw/agent:latest

# Install additional tools
RUN apt-get update && apt-get install -y git-lfs

# Set environment
ENV CUSTOM_TOOL_PATH=/usr/local/bin/custom-tool

COPY custom-tool /usr/local/bin/
```

### Multi-Architecture Support

OpenClaw supports multiple architectures:

- **x86_64** - Standard Linux systems
- **arm64** - Apple Silicon, ARM servers
- **arm/v7** - Raspberry Pi

### Container Orchestration

For production deployments, use orchestration tools:

- **Docker Compose** - Local development
- **Kubernetes** - Cloud deployments
- **Docker Swarm** - Cluster management

---

**For troubleshooting specific issues, see [troubleshooting.md](./troubleshooting.md).**  
**For policy details, see [policies.md](./policies.md).**
