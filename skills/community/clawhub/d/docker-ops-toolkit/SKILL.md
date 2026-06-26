---
name: docker-ops
description: Docker container lifecycle management, health checks, log analysis, cleanup, compose orchestration, and troubleshooting. Use when Codex needs to manage Docker containers, debug running services, inspect logs, clean up resources, or orchestrate multi-service setups with Docker Compose.
---

# Docker Ops

## Overview

Docker container lifecycle management, health checks, log analysis, cleanup, compose orchestration, and troubleshooting. Use when Codex needs to manage Docker containers, debug running services, or clean up Docker resources.

## Quick Start

### Prerequisites
- Docker Engine (docker CLI)
- `docker compose` plugin (for compose)

### Check what's running
```bash
docker ps -a --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}'
docker stats --no-stream                   # live resource usage
```

### Inspect a container
```bash
docker inspect <container> | jq '.[0].State'   # status, exit code, health
docker inspect <container> --format '{{json .Mounts}}' | jq .
```

### Logs analysis
```bash
docker logs <container> --tail 100 --since 5m
# Use docker-log-inspector.py for filtering:
python3 scripts/docker-log-inspector.py <container> --since 30m --filter ERROR --summary
```

### Clean up unused resources
```bash
# Standard cleanup
bash scripts/docker-cleanup.sh
# Aggressive cleanup (removes volumes + build cache)
bash scripts/docker-cleanup.sh --aggressive
# Preview only
bash scripts/docker-cleanup.sh --dry-run
```

### Health check
```bash
bash scripts/docker-health.sh                     # all containers
bash scripts/docker-health.sh <container-name>    # single container
```

## Common Tasks

### Docker Compose workflows
```bash
docker compose up -d                      # start services
docker compose down -v                    # stop + remove volumes
docker compose logs -f --tail 50          # follow logs
docker compose ps                         # status
docker compose exec <service> sh          # shell into a service
docker compose build --no-cache <svc>     # rebuild without cache
docker compose restart <service>          # restart one service
```

### Port conflicts
```bash
# Find what's using a port
sudo lsof -i :<port>
docker ps --format '{{.Names}} {{.Ports}}' | grep <port>
# Fix: change port mapping in docker-compose.yml or stop conflicting container
```

### Resource limits and OOM
```bash
docker inspect <container> --format '{{json .HostConfig.Memory}}'
docker stats <container> --no-stream
# Fix: add to docker-compose.yml
#   deploy:
#     resources:
#       limits:
#         memory: 512M
#         cpus: '0.5'
```

### Image management
```bash
docker images --format 'table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedSince}}'
docker image prune -a                    # remove all unused images
docker rmi <image-id>                    # remove specific image
docker pull <image>:<tag>                # update image
docker build -t <name>:<tag> .           # build
docker build --no-cache -t <name> .      # force rebuild
```

### Network troubleshooting
```bash
docker network ls
docker network inspect <network>
# Test connectivity from a container:
docker exec <container> ping <other-container>
docker exec <container> curl -v http://service:port
```

### Data volumes
```bash
docker volume ls
docker volume inspect <volume>
docker run --rm -v <volume>:/data alpine ls -la /data   # inspect volume contents
```

## Troubleshooting

### Container exits immediately
```bash
docker logs <container>                   # check exit reason
docker inspect <container> --format '{{.State.ExitCode}}'
# Common causes:
#   0  → clean exit (expected?)
#   1  → application error (check logs)
#   137 → SIGKILL (OOM kill)
#   139 → segfault
```

### Disk space issues
```bash
docker system df                          # disk overview
du -sh /var/lib/docker/containers/        # container overlay sizes
bash scripts/docker-cleanup.sh --aggressive
```

### Container can't resolve DNS
```bash
docker exec <container> cat /etc/resolv.conf
# Fix: add to docker-compose.yml
#   dns:
#     - 8.8.8.8
#     - 1.1.1.1
```

### Permission errors
```bash
# Add user to docker group
sudo usermod -aG docker $USER && newgrp docker
```

## Resources

- **`scripts/docker-cleanup.sh`** — Interactive cleanup with dry-run mode
- **`scripts/docker-health.sh`** — Multi-container health overview
- **`scripts/docker-log-inspector.py`** — Regex filtering + severity summary for logs
- **`references/compose-patterns.md`** — Docker Compose patterns and recipes
