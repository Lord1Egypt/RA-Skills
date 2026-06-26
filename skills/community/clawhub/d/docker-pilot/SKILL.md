---
name: docker-pilot
version: 1.0.0
description: "Safe, intelligent Docker container management — fleet status, lifecycle operations, cleanup, compose stacks, troubleshooting, and security hardening. Classifies every command by risk level (READ / RISKY / DESTRUCTIVE) with mandatory confirmation gates. Use when managing Docker containers, images, volumes, networks, compose stacks, or debugging container issues."
changelog: Initial release — fleet view, safety classification, cleanup playbook, compose setup, troubleshooting runbooks, Telegram formatting
metadata: {"clawdbot":{"emoji":"🚢","requires":{"bins":["docker"]},"os":["linux","darwin","win32"]}}
---

# Docker Pilot 🚢

Safe, intelligent Docker management. Not just a command reference — an operational guide that classifies risk, protects critical services, and formats output for chat.

## When to Use

Use when the task involves Docker, Dockerfiles, containers, images, Compose, volumes, networking, debugging, or any container lifecycle operation. This is the **default Docker skill** — apply it whenever Docker work appears.

## Companion Skills

This skill **extends** the existing ClawHub `docker` skill (v1.0.4 by ivangdavila). Install both for full coverage:
- `clawhub install docker` — Dockerfile patterns, image building, security hardening reference
- `clawhub install docker-pilot` — Operational management, safety rails, fleet view, troubleshooting

---

## Safety Architecture ⚠️

Every Docker command is classified by risk level. **Follow these rules without exception.**

### 🟢 READ (Safe — Can Always Run)

No side effects. Use freely.

```bash
docker ps                                          # Running containers
docker ps -a                                       # All containers (including stopped)
docker ps --format '{{json .}}'                    # JSON output (parseable)
docker images                                       # All images
docker images --filter "dangling=true"             # Dangling images only
docker system df                                   # Disk usage overview
docker system df -v                                # Detailed disk usage
docker logs --tail 50 CONTAINER                     # Recent logs
docker logs --since 1h CONTAINER                    # Last hour of logs
docker inspect CONTAINER                            # Full container config (JSON)
docker stats --no-stream                            # Resource snapshot (not streaming)
docker network ls                                   # List networks
docker network inspect NETWORK                      # Network details
docker volume ls                                    # List volumes
docker volume inspect VOLUME                        # Volume details
docker history IMAGE                                # Image layer history
docker diff CONTAINER                               # Filesystem changes in container
docker port CONTAINER                               # Port mappings
docker top CONTAINER                                # Processes in container
docker events --since 1h                            # Recent daemon events
```

**Parsing tip:** Always use `--format '{{json .}}'` with `python3 -m json.tool` for structured data. `docker inspect` returns an array — always index `[0]`.

### 🟡 RISKY (Modifies State — Show Impact First)

Requires showing the user what will change before executing.

```bash
docker stop CONTAINER           # Cuts service — show uptime first
docker start CONTAINER          # Starts stopped container
docker restart CONTAINER        # Brief outage — confirm first
docker pull IMAGE               # Network + disk usage — check free space
docker tag SOURCE TARGET        # Namespace change — confirm intended tag
docker network create/connect   # Topology change — check port conflicts
docker volume create             # Low risk but irreversible mount
docker update --restart=always  # Changes restart behavior — good practice
docker container rename         # May break scripts — check dependencies
docker compose up -d            # Starts/modifies stack — show diff first
docker compose stop             # Stops stack — show what's running
docker compose restart          # Restarts stack — brief outage
```

**Rule:** Before any 🟡 command, show:
1. Current state (what's running, what will be affected)
2. Expected impact (downtime, resource usage)
3. Ask for confirmation

### 🔴 DESTRUCTIVE (Irreversible — Mandatory Confirmation)

**NEVER run without:**
1. Showing exactly what will be destroyed
2. Getting explicit verbal confirmation from the user
3. No chained destructive commands (`docker rm $(docker ps -aq)` is FORBIDDEN)

```bash
docker rm CONTAINER              # Deletes container — check volumes, networks first
docker rmi IMAGE                 # Deletes image — check dependent containers
docker volume rm VOLUME          # DATA LOSS — show contents, confirm twice
docker system prune              # Removes stopped containers + dangling images
docker system prune -a           # Removes ALL unused images — full audit required
docker system prune --volumes    # Removes unused volumes — DATA LOSS
docker compose down -v           # Destroys volumes — triple confirm
docker network rm NETWORK        # Breaks attached containers — show list
docker rm -f CONTAINER           # Force-remove running container — dangerous
docker exec CONTAINER rm -rf /   # Destructive inside container — catch pattern
docker swarm leave --force       # Dissolves swarm — catastrophic
```

**Confirmation pattern:**
```
⚠️ DESTRUCTIVE OPERATION
Will remove: [list items]
Impact: [data loss / service disruption / etc.]
Type "confirm" to proceed:
```

### 🛡️ Protected Services

Some services are critical infrastructure. **Never stop, restart, or remove these without explicit override:**

```yaml
# Default protected services (customize per deployment)
protected_services:
  - adguardhome      # DNS for entire network — stopping breaks internet
  - unbound          # DNS resolver
  - nginx            # Reverse proxy — stopping breaks all web services
  - traefik          # Reverse proxy
  - pihole           # DNS/ad-blocking
```

**Rule:** Before stopping a protected service, check DNS fallback:
```bash
# Verify host has alternative DNS
cat /etc/resolv.conf | grep -v adguard | grep nameserver
# If no fallback — WARN USER: "Stopping this will break DNS resolution"
```

---

## Fleet Status 📊

The primary interface for understanding what's running. Use this format for all status reports in chat:

### Fleet Overview (Telegram-Formatted)

```
🐳 Docker Fleet — 5 containers

🟢 adguardhome     Up 4 days    43MB   DNS/ad-blocking  [PROTECTED]
🟢 buck-dashboard  Up 8 days    120MB  System dashboard
🟢 verdaccio       Up 21 days   58MB   NPM registry
🟢 mockserver      Up 21 days   42MB   API mocking
🟢 gitbox          Up 21 days   35MB   Git server

📦 Images: 45 total (37 dangling, ~3GB reclaimable)
💾 Disk: 68GB/233GB used (31%)
🔧 Compose: NOT INSTALLED
```

### Commands to Generate Fleet View

```bash
# Container status with resource usage
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Image}}'

# Resource usage snapshot
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}'

# Image count and dangling
docker images | wc -l
docker images --filter "dangling=true" -q | wc -l

# Disk usage
docker system df

# Check if compose is installed
docker compose version 2>/dev/null || docker-compose version 2>/dev/null || echo "NOT INSTALLED"
```

### Service Map

Map container names to functional roles. Maintain this in a local config:

```yaml
# ~/.openclaw/workspace/docker-pilot/services.yaml (create if needed)
services:
  adguardhome:
    role: "DNS/ad-blocking"
    critical: true
    protected: true
    port: 53
    network: host
  buck-dashboard:
    role: "System dashboard"
    critical: false
    port: 8080
    network: bridge
  verdaccio:
    role: "NPM registry"
    critical: false
    port: 4873
    network: bridge
  mockserver:
    role: "API mocking"
    critical: false
    port: 1080
    network: bridge
  gitbox:
    role: "Git server"
    critical: false
    port: 8081
    network: bridge
```

---

## Compose Setup 🔧

If `docker compose` is not installed, install it first:

```bash
# Check current status
docker compose version 2>/dev/null || echo "NOT INSTALLED"

# Install compose plugin (no daemon restart needed)
sudo apt install docker-compose-v2

# Verify
docker compose version
```

**Why compose matters:** Without compose, every container is a `docker run` command with 10+ flags that must be memorized or scripted. Compose gives you declarative, version-controlled, reproducible deployments.

---

## Cleanup Playbook 🧹

Run this when disk usage is high or when `docker system df` shows bloat.

### Step 1: Audit (Always READ first)

```bash
# Show what's reclaimable
docker system df

# Dangling images (tagged <none>)
docker images --filter "dangling=true"

# Stopped containers
docker ps --filter "status=exited" --filter "status=created"

# Unused networks
docker network ls --filter "type=custom"

# Unused volumes
docker volume ls --filter "dangling=true"

# Build cache size
docker system df -v | grep "Build Cache"
```

### Step 2: Safe Cleanup (No data loss)

```bash
# Remove dangling images (no running container uses them)
docker image prune

# Remove stopped containers
docker container prune

# Remove unused networks
docker network prune

# Remove build cache
docker builder prune
```

### Step 3: Aggressive Cleanup (⚠️ Confirm first)

```bash
# Remove ALL unused images (not just dangling)
docker image prune -a
# ⚠️ CONFIRM: "This removes images not used by any running container. Next pull will re-download."

# Remove unused volumes (DATA LOSS RISK)
docker volume prune
# ⚠️ CONFIRM: "This deletes volume data. Show volume contents first."
# Before: docker volume inspect VOLUME_NAME
# Show contents: docker run --rm -v VOLUME_NAME:/mnt alpine ls -la /mnt

# Nuclear option
docker system prune -a --volumes
# ⚠️ DOUBLE CONFIRM: "This removes everything not used by a running container including volumes."
```

### Step 4: Verify

```bash
docker system df
docker ps
docker images
```

---

## Health Checks 🩺

### Add Health Checks to Running Containers

```bash
# Check if container has a health check
docker inspect --format='{{.Config.Health}}' CONTAINER

# Add health check to existing container (requires recreate)
docker update --health-cmd="curl -f http://localhost:8080/ || exit 1" \
  --health-interval=30s \
  --health-timeout=5s \
  --health-retries=3 \
  CONTAINER
```

### Common Health Check Commands

```bash
# HTTP endpoint
curl -f http://localhost:PORT/ || exit 1

# TCP port
nc -z localhost PORT || exit 1

# DNS (for AdGuard)
dig +short google.com @localhost || exit 1

# Process check
pgrep -x PROCESS_NAME || exit 1
```

### Restart Policies

```bash
# Set restart policy (prevents manual restart after reboot)
docker update --restart=always CONTAINER

# Check current policy
docker inspect --format='{{.HostConfig.RestartPolicy.Name}}' CONTAINER

# Policies:
#   no          — Never restart (default)
#   on-failure  — Restart only on non-zero exit
#   always      — Always restart, including on daemon start
#   unless-stopped — Always restart except when manually stopped
```

---

## Log Management 📋

### Configure Log Rotation (Prevents Disk Fill)

```bash
# Add log limits to existing container (requires recreate)
docker run --log-opt max-size=10m --log-opt max-file=3 ...

# Global daemon config: /etc/docker/daemon.json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

### Smart Log Reading

```bash
# Last 50 lines
docker logs --tail 50 CONTAINER

# Last hour
docker logs --since 1h CONTAINER

# Follow with timeout (don't leave streaming)
docker logs -f --since 5m CONTAINER &  PID=$! ; sleep 30 ; kill $PID

# Search for errors
docker logs CONTAINER 2>&1 | grep -i "error\|exception\|fail\|fatal" | tail -20

# JSON log format (if container outputs JSON)
docker logs CONTAINER --since 1h | python3 -m json.tool | grep "error"
```

---

## Troubleshooting Runbooks 🔍

### Container Won't Start

```bash
# 1. Check exit code
docker inspect --format='{{.State.ExitCode}}' CONTAINER
# Common codes: 0=graceful, 1=app error, 137=OOM killed, 139=segfault, 125=docker error

# 2. Check logs
docker logs --tail 50 CONTAINER

# 3. Check if OOM killed
docker inspect --format='{{.State.OOMKilled}}' CONTAINER

# 4. Check resource limits
docker inspect --format='{{.HostConfig.Memory}}' CONTAINER

# 5. Try interactive debug
docker run --rm -it --entrypoint /bin/sh IMAGE
```

### Port Conflict

```bash
# Find what's using a port
ss -tlnp | grep :PORT
# or
lsof -i :PORT

# Check if it's a Docker container
docker ps --filter "publish=PORT"

# Fix: change host port mapping or stop conflicting service
```

### Disk Full

```bash
# 1. Check Docker disk usage
docker system df -v

# 2. Check host disk
df -h /var/lib/docker

# 3. Quick reclaim (safe)
docker image prune
docker container prune
docker builder prune

# 4. If still full (confirm first!)
docker image prune -a  # Remove ALL unused images
```

### Image Pull Failure

```bash
# 1. Check network
curl -I https://registry-1.docker.io/v2/

# 2. Check auth
docker login

# 3. Check rate limits (Docker Hub)
# Anonymous: 100 pulls/6hr, Authenticated: 200 pulls/6hr

# 4. Try specific digest instead of tag
docker pull image@sha256:DIGEST
```

### Crash Loop

```bash
# 1. See restart count
docker inspect --format='{{.RestartCount}}' CONTAINER

# 2. Read crash logs
docker logs --tail 100 CONTAINER

# 3. Common causes:
#    - Missing env vars: look for "required" or "must set" in logs
#    - File permissions: look for "permission denied"
#    - Port conflict: look for "address already in use"
#    - OOM: check docker inspect State.OOMKilled
```

### Network Issues

```bash
# Containers can't reach each other
# Default bridge has NO DNS — use custom network
docker network create mynet
docker network connect mynet CONTAINER

# Container can't reach host
# Use host.docker.internal (Docker Desktop) or host IP
# On Linux: add to /etc/docker/daemon.json:
#   {"hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]}

# DNS not resolving in container
docker exec CONTAINER cat /etc/resolv.conf
docker exec CONTAINER nslookup google.com
```

---

## Compose Stacks 📦

### Creating a Compose File

```yaml
# docker-compose.yml — declarative, version-controlled, reproducible
version: "3.8"

services:
  app:
    image: myapp:1.0
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
    volumes:
      - app-data:/data
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: "0.5"
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"

volumes:
  app-data:
```

### Compose Lifecycle

```bash
# Start stack
docker compose up -d

# View stack status
docker compose ps

# View logs
docker compose logs -f --tail 50

# Restart single service
docker compose restart app

# Pull and recreate (update)
docker compose pull && docker compose up -d

# Stop (keep data)
docker compose down

# Stop AND remove volumes (⚠️ DATA LOSS)
docker compose down -v
```

### Compose Traps

- `depends_on` waits for container start, NOT service ready — use `condition: service_healthy`
- `.env` file must be next to docker-compose.yml — wrong directory = silently ignored
- Volume mounts overwrite container files — empty host dir = empty container dir
- `docker compose run` does NOT start dependencies
- YAML anchors don't work across files — use multiple compose files instead

---

## Security Hardening 🔒

### Container Security

```bash
# Run as non-root (always prefer this)
docker run --user 1000:1000 ...

# Drop all capabilities, add only what's needed
docker run --cap-drop ALL --cap-add NET_BIND_SERVICE ...

# Read-only root filesystem
docker run --read-only --tmpfs /tmp ...

# Resource limits (always set these)
docker run -m 512m --cpus=0.5 ...

# No new privileges
docker run --security-opt=no-new-privileges ...
```

### Image Security

```bash
# Pin versions (never use :latest in production)
docker pull nginx:1.25.3-alpine

# Scan for vulnerabilities
docker scout cves IMAGE

# Verify image integrity
docker pull image@sha256:DIGEST
```

### NEVER Do These

- ❌ `docker run --privileged` — disables ALL security
- ❌ `-v /:/host` — mounts entire host filesystem
- ❌ `--pid=host` — can see/kill host processes
- ❌ `--network=host` on non-DNS containers — unnecessary exposure
- ❌ Secrets in ENV or ARG — visible in `docker inspect` and `docker history`
- ❌ `docker rm $(docker ps -aq)` — chained destructive command
- ❌ `docker system prune -a` without audit first

---

## Resource Monitoring 📈

### Quick Health Check

```bash
# One-liner fleet health
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

# Resource usage
docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}'

# Per-container disk usage
docker system df -v

# Host resources
df -h /var/lib/docker
free -h
```

### Alert Thresholds

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Disk usage | >80% | >90% | Run cleanup playbook |
| Memory | >80% | >95% | Add limits or restart heavy containers |
| Container restarts | >3/hour | >10/hour | Check logs, likely crash loop |
| Dangling images | >10 | >30 | Run image prune |
| Log file size | >100MB | >1GB | Add log rotation |

---

## Dockerfile Patterns 📝

### Layer Cache Optimization

```dockerfile
# ✅ GOOD — requirements rarely change, code changes often
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ❌ BAD — invalidates cache on every code change
COPY . .
RUN pip install -r requirements.txt
```

### Multi-Stage Build

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/server.js"]
```

### Image Size Traps

- Multi-stage: forgotten `--from=builder` copies from wrong stage silently
- `COPY . .` before `RUN npm install` = cache invalidated on every code change
- `ADD` extracts archives automatically — use `COPY` unless you need extraction
- `rm -rf /var/lib/apt/lists` in separate RUN = space not reclaimed (layers)
- `.git` copied = megabytes of bloat — use `.dockerignore`

### ARG vs ENV

- `ARG` only available during build, visible in `docker history` — NEVER for secrets
- `ENV` persists at runtime — use for configuration
- `ARG` with empty override uses default, not empty string
- `ARG` must be re-declared after each `FROM` in multi-stage

---

## Telegram Formatting Guide 📱

When reporting Docker status in Telegram, use this format:

### Fleet Status
```
🐳 **Docker Fleet** — 5 running

🟢 **adguardhome** — DNS/ad-blocking [PROTECTED]
   Up 4 days · 43MB RAM · :53

🟢 **buck-dashboard** — Dashboard
   Up 8 days · 120MB RAM · :8080

🟢 **verdaccio** — NPM registry
   Up 21 days · 58MB RAM · :4873

🟡 **mockserver** — API mocking
   Up 21 days · 42MB RAM · :1080

🟢 **gitbox** — Git server
   Up 21 days · 35MB RAM · :8081

📦 37 dangling images (3GB reclaimable)
💾 68GB/233GB disk (31%)
```

### Alert Format
```
⚠️ **Container Alert**

🔴 **mockserver** — Exited (1) 2min ago
Last log: `Connection refused on port 1080`

Restart? (3 restarts in last hour)
```

### Cleanup Report
```
🧹 **Docker Cleanup**

Removed:
- 12 dangling images (450MB)
- 3 stopped containers
- 1 unused network

Reclaimed: **1.2GB**
Current disk: 62GB/233GB (27%)
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Fleet status | `docker ps --format 'table {{.Names}}\t{{.Status}}'` |
| Resource usage | `docker stats --no-stream` |
| Disk usage | `docker system df` |
| Container logs | `docker logs --tail 50 CONTAINER` |
| Inspect JSON | `docker inspect CONTAINER \| python3 -m json.tool` |
| Find dangling | `docker images --filter "dangling=true" -q \| wc -l` |
| Safe cleanup | `docker image prune && docker container prune && docker builder prune` |
| Health check | `docker inspect --format='{{.State.Health.Status}}' CONTAINER` |
| Restart policy | `docker update --restart=always CONTAINER` |
| Compose up | `docker compose up -d` |
| Compose logs | `docker compose logs -f --tail 50` |

---

## First-Run Setup

When this skill is activated for the first time on a new machine:

1. **Check compose:** `docker compose version` — if missing, install it
2. **Scan fleet:** `docker ps -a` + `docker system df` — understand current state
3. **Set restart policies:** `docker update --restart=unless-stopped` for all running containers
4. **Configure log rotation:** Add max-size/max-file to daemon.json or per-container
5. **Clean up:** Run safe cleanup (image prune, container prune, builder prune)
6. **Build service map:** Document what each container does
7. **Set up monitoring:** Consider a cron to check fleet health periodically

---

## Credits

Built on top of the `docker` skill by ivangdavila (v1.0.4). This skill adds:
- 🛡️ Safety architecture (READ/RISKY/DESTRUCTIVE classification with confirmation gates)
- 📊 Fleet status view with Telegram formatting
- 🔍 Troubleshooting runbooks (crash loops, disk full, port conflicts, DNS)
- 🧹 Step-by-step cleanup playbook
- 🩺 Health check and restart policy configuration
- 📋 Log management and rotation
- 🛡️ Protected services list (never stop AdGuard without DNS fallback)
- 📦 Compose setup guide and lifecycle management
- 🔒 Security hardening checklist
- 🚀 First-run setup guide