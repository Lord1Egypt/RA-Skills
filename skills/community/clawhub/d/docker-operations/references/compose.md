# Docker Compose Commands

Comprehensive reference for Docker Compose v2 commands. Docker Compose is a tool for defining and running multi-container Docker applications using YAML files.

## docker compose up

Start services defined in the compose file.

```bash
docker compose up [options]
```

**Common Options:**
- `-d` - Detached mode (run containers in background)
- `--build` - Build images before starting containers
- `--no-build` - Don't build images, even if missing
- `-f <file>` - Specify compose file (default: docker-compose.yml)
- `--scale <service=n>` - Scale service to n instances
- `--abort-on-container-exit` - Stop all containers if any container stops
- `--attach-dependencies` - Attach to dependent services
- `--no-attach <services>` - Don't attach to specific services
- `-t, --timeout <seconds>` - Timeout for shutdown (default: 10)
- `--renew-anon-volumes` - Recreate anonymous volumes instead of retrieving data

**Examples:**
```bash
# Start all services in foreground
docker compose up

# Start in detached mode
docker compose up -d

# Build and start
docker compose up --build

# Start specific services
docker compose up web db

# Start with scaling
docker compose up -d --scale web=3
```

---

## docker compose down

Stop and remove containers, networks, and optionally volumes.

```bash
docker compose down [options]
```

**Common Options:**
- `-v, --volumes` - Remove named volumes declared in the volumes section
- `--remove-orphans` - Remove containers for services not defined in compose file
- `-t, --timeout <seconds>` - Timeout for shutdown (default: 10)
- `--rmi <type>` - Remove images (types: local, all)

**Examples:**
```bash
# Stop and remove containers/networks
docker compose down

# Also remove volumes
docker compose down -v

# Remove images
