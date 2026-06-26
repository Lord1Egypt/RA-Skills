---
name: docker-cleanup
description: "Docker resource cleanup, pruning, and disk usage analysis toolkit. Inspect containers, images, volumes, networks, and build cache usage. Prune stopped containers, dangling images, unused volumes, and orphaned networks. Generate HTML cleanup reports. Use when Codex needs to: (1) Free up Docker disk space, (2) Analyze Docker resource usage, (3) Prune stopped containers and dangling images, (4) Remove unused volumes and networks, (5) Generate Docker cleanup reports, (6) Audit Docker environment health."
---

# Docker Cleanup Toolkit (docker-cleanup)

Analyze, prune, and reclaim disk space from Docker resources with a single command.

## Quick start

```bash
python3 skills/docker-cleanup/scripts/docker_cleanup.py
```

Output:
```
🐳 Docker Engine v26.1.3

Type             Count      Size            Reclaimable    
---------------------------------------------------------------
images           12         2.4GB           856MB          
containers       8          1.1GB           0B             
volumes          4          520MB           320MB          
build cache      15         1.8GB           1.5GB          

CONTAINER ID    NAME                    IMAGE                    STATUS               CREATED     
---------------------------------------------------------------------------------------------------
abc123...       my-app                  node:20                  Up 3 days            2d ago      
def456...       old-db                  postgres:15              Exited (0) 5 days    1w ago      

⚠ Dangling images: 3
  sha256:x1y2 → 450MB
  sha256:p3q4 → 120MB
```

## Commands

| Command | Description |
|---------|-------------|
| `python3 docker_cleanup.py` | Default: analyze only (dry-run, no changes) |
| `python3 docker_cleanup.py --containers` | Prune stopped containers |
| `python3 docker_cleanup.py --images` | Prune dangling images |
| `python3 docker_cleanup.py --volumes` | Prune unused volumes |
| `python3 docker_cleanup.py --networks` | Prune unused networks |
| `python3 docker_cleanup.py --all` | Full system prune (all of the above) |
| `python3 docker_cleanup.py --all --force` | Auto-confirm all pruning |
| `python3 docker_cleanup.py --json` | JSON output for programmatic use |
| `python3 docker_cleanup.py --report` | Generate HTML report |
| `python3 docker_cleanup.py --analyze` | Explicit analysis mode |

## Typical workflows

### 1. Quick check (no changes made)

```bash
python3 skills/docker-cleanup/scripts/docker_cleanup.py
```

### 2. Dangling images cleanup

```bash
python3 skills/docker-cleanup/scripts/docker_cleanup.py --images --force
```

### 3. Full spring cleaning

```bash
python3 skills/docker-cleanup/scripts/docker_cleanup.py --all --force
```

### 4. Audit + report

```bash
python3 skills/docker-cleanup/scripts/docker_cleanup.py --report
# Creates: docker-cleanup-report-20260515-090500.html
```

### 5. Monitor with JSON

```bash
python3 skills/docker-cleanup/scripts/docker_cleanup.py --json
```

## Exit codes

- **0**: Success (or no issues found)
- **1**: Docker not running or errors occurred

## Requirements

- Docker Engine (any recent version)
- Python 3.6+ (stdlib only)
- Linux / macOS / Windows (WSL)
