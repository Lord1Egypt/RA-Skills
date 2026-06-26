# Cleanup Commands

Commands for cleaning up unused Docker resources - containers, images, volumes, and networks.

## docker container prune

Remove all stopped containers.

```bash
docker container prune [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--filter filter` | Provide filter values (e.g. "until=<timestamp>") |
| `-f, --force` | Do not prompt for confirmation |

**Examples:**
```bash
docker container prune
docker container prune -f
docker container prune --filter "until=24h"
docker container prune --filter "until=2024-01-01"
```

## docker image prune

Remove unused images.

```bash
docker image prune [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Remove all unused images, not just dangling ones |
| `--filter filter` | Provide filter values (e.g. "until=<timestamp>") |
| `-f, --force` | Do not prompt for confirmation |

**Examples:**
```bash
# Remove dangling images (untagged)
docker image prune

# Remove all unused images
docker image prune -a

# Remove images older than 24h
docker image prune -a --filter "until=24h"

# Force prune without confirmation
docker image prune -f
```

## docker volume prune

Remove unused local volumes.

```bash
docker volume prune [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Remove all unused volumes, not just anonymous ones |
| `--filter filter` | Provide filter values (e.g. "label=<label>") |
| `-f, --force` | Do not prompt for confirmation |

> ⚠️ Warning: This will delete all volumes not used by at least one container.

**Examples:**
```bash
docker volume prune
docker volume prune -f
docker volume prune --filter "label=env=dev"
```

## docker network prune

Remove all unused networks.

```bash
docker network prune [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `--filter filter` | Provide filter values (e.g. "until=<timestamp>") |
| `-f, --force` | Do not prompt for confirmation |

**Examples:**
```bash
docker network prune
docker network prune -f
docker network prune --filter "until=24h"
```

## docker system prune

Remove unused data (stopped containers, unused networks, dangling images).

```bash
docker system prune [OPTIONS]
```

**Options:**
| Option | Description |
|--------|-------------|
| `-a, --all` | Remove all unused images not just dangling ones |
| `--filter filter` | Provide filter values (e.g. "label=<key>=<value>") |
| `-f, --force` | Do not prompt for confirmation |
| `--volumes` | Prune anonymous volumes |

**Examples:**
```bash
# Basic prune (dangling images, stopped containers, unused networks)
docker system prune

# Prune with force (no confirmation)
docker system prune -f

# Prune all unused images
docker system prune -a

# Prune including volumes
docker system prune --volumes

# Prune with time filter
docker system prune -a --filter "until=24h"

# Prune everything with volumes
docker system prune -a --volumes -f
```

## Quick Reference

| Operation | Command |
|-----------|---------|
| Prune stopped containers | `docker container prune` |
| Prune dangling images | `docker image prune` |
| Prune all unused images | `docker image prune -a` |
| Prune unused volumes | `docker volume prune` |
| Prune unused networks | `docker network prune` |
| Full system prune | `docker system prune` |
| Full prune with volumes | `docker system prune --volumes` |
| Force prune (no confirm) | `docker container prune -f` |
| Prune with filter | `docker system prune -a --filter "until=24h"` |
