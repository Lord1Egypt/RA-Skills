---
name: docker-helper
description: "Manage Docker containers, images, volumes, networks, and Docker Compose projects. Use when the user wants to: (1) List/start/stop/restart Docker containers, (2) View container logs and stats, (3) Build and manage Docker images, (4) Create and manage docker-compose.yml files, (5) Clean up unused Docker resources, (6) Debug container issues. Best for developers, DevOps engineers, and anyone running Docker on their server."
version: 1.0.0
homepage: https://clawhub.ai
metadata:
  openclaw:
    emoji: "🐳"
    requires:
      bins:
        - docker
        - docker-compose
---

# Docker Helper

Simplify Docker container management, compose setup, and debugging through natural language commands.

## When to Use

✅ **USE this skill when:**

- "Show me all running containers"
- "Start/stop/restart container [name]"
- "Show logs for [container]"
- "Check disk usage of Docker"
- "Prune unused containers/images"
- "Create a docker-compose.yml for [service]"
- "What's running on port 8080?"
- "Container [name] won't start, debug it"

❌ **DON'T use this skill when:**

- Need Kubernetes management → use a K8s skill
- Building complex multi-service orchestrations → consider Docker Swarm/K8s skills
- Production deployment with zero-downtime → use deployment-specific skills

## Workflow

### 1. Container Management

When the user asks about containers, the agent runs:

```
# List all
docker ps -a
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Inspect specific
docker inspect [container] | jq '.[0].NetworkSettings.Ports'
docker stats [container] --no-stream

# Control
docker start/stop/restart [container]
docker rm -f [container]    (only with user confirmation)
```

### 2. Logs & Debugging

For debugging container issues:

```
# Standard logs
docker logs [container] --tail 50
docker logs [container] --tail 200 | grep -i error

# Resource issues
docker stats --no-stream

# Check why container exited
docker inspect [container] | jq '.[0].State'
docker logs [container] --tail 20 --timestamps
```

### 3. Image Management

```
# List images
docker images

# Build
docker build -t [name]:[tag] .

# Cleanup (with confirmation)
docker image prune -a -f
```

### 4. Docker Compose

When the user needs a compose file:

1. Ask what services they need (e.g., "nginx + postgres + redis")
2. Generate a `docker-compose.yml` with:
   - Appropriate image tags (avoid `latest` in production)
   - Volume mounts for persistence
   - Network configuration
   - Health checks where applicable
   - Environment variable stubs (`.env` file)
3. Show the user the generated file, offer to adjust

### 5. Resource Cleanup (WITH CONFIRMATION)

Always ask for confirmation before:

- `docker system prune -a -f` (removes ALL unused resources)
- `docker volume prune -f` (removes orphaned volumes with data)
- `docker image rm` without the `-f` flag first

### Common Templates

**Web App (Node/Python + Postgres):**
```yaml
services:
  app:
    build: .
    ports: ["${PORT}:${PORT}"]
    env_file: .env
    depends_on: [db]
  db:
    image: postgres:16-alpine
    volumes: ["pgdata:/var/lib/postgresql/data"]
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_PASSWORD: ${DB_PASS}
volumes: {pgdata:}
```

**Nginx Reverse Proxy:**
```yaml
services:
  nginx:
    image: nginx:alpine
    ports: ["80:80", "443:443"]
    volumes: ["./nginx.conf:/etc/nginx/nginx.conf:ro", "./html:/usr/share/nginx/html:ro"]
```

## Examples

> **User**: "What containers are running?"
> **Agent**: Runs `docker ps --format "table..."` and shows a clean table
>
> **User**: "My nginx container won't start"
> **Agent**: Checks logs + inspect, identifies the port conflict or config error
>
> **User**: "Clean up Docker, it's using too much space"
> **Agent**: Runs `docker system df`, shows usage, asks what to prune
>
> **User**: "Create a compose file for a Python app with Redis"
> **Agent**: Generates docker-compose.yml + .env.example, explains each part

## Notes

- Always prefix destructive commands with confirmation
- Use `docker compose` (v2) over `docker-compose` (v1) when available
- Prefer alpine-based images for smaller footprint
- For security: never expose Docker socket without TLS
