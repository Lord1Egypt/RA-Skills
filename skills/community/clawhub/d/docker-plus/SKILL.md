---
name: docker-plus
description: "Enhanced Docker with Dockerfile templates, multi-stage builds, security hardening, production best practices, Docker Compose patterns, and troubleshooting guides."
metadata:
  author: opencode
  version: 2.0
  tags: docker, containers, dockerfile, compose, production
  compatibility: opencode
  license: MIT
---

# Docker Plus

Enhanced Docker with templates, security hardening, and production best practices.

## Features

- **Dockerfile Templates**: Ready-to-use templates for common languages
- **Multi-stage Builds**: Optimize image size
- **Security Hardening**: CIS benchmarks, best practices
- **Production Best Practices**: Health checks, logging, monitoring
- **Troubleshooting**: Common issues and solutions

## Quick Reference

| Task | Command |
|------|---------|
| Build | `docker build -t app:latest .` |
| Run | `docker run -d -p 8080:80 app:latest` |
| Logs | `docker logs -f container_name` |
| Exec | `docker exec -it container_name sh` |
| Clean | `docker system prune -af` |

## Dockerfile Templates

### Node.js

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
RUN addgroup -g 1001 -S nodejs && adduser -S nextjs -u 1001
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
USER nextjs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Python

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim
WORKDIR /app
RUN groupadd -r appuser && useradd -r -g appuser appuser
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
USER appuser
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Production stage
FROM alpine:3.18
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
CMD ["./main"]
```

### Rust

```dockerfile
# Build stage
FROM rust:1.72 AS builder
WORKDIR /app
COPY . .
RUN cargo build --release

# Production stage
FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends ca-certificates && rm -rf /var/lib/apt/lists/*
COPY --from=builder /app/target/release/myapp /usr/local/bin/
CMD ["myapp"]
```

## Multi-Stage Builds

### Optimization Pattern

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Stage 3: Production
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

## Security Hardening

### CIS Benchmark Compliance

```dockerfile
# Run as non-root
RUN addgroup -g 1001 -S appgroup && adduser -u 1001 -S appuser -G appgroup
USER appuser

# Read-only filesystem
RUN chmod -R 555 /app

# Remove unnecessary packages
RUN apt-get purge -y --auto-remove curl wget

# Set proper permissions
RUN chown -R appuser:appgroup /app
```

### Security Best Practices

```dockerfile
# Don't store secrets in image
ARG DB_PASSWORD
ENV DB_PASSWORD=$DB_PASSWORD

# Use specific versions
FROM node:20.10.0-alpine3.18

# Scan for vulnerabilities
RUN apk add --no-cache trivy

# Enable security scanning
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

## Docker Compose Patterns

### Production Stack

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://user:pass@db:5432/app
    depends_on:
      db:
        condition: service_healthy
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

## Production Best Practices

### Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8080/health || exit 1
```

### Logging

```dockerfile
# Use JSON logging
RUN npm install winston

# Log to stdout/stderr
CMD ["node", "dist/index.js"]
```

### Resource Limits

```bash
# Run with resource limits
docker run -d \
  --name app \
  --memory="512m" \
  --cpus="0.5" \
  --pids-limit=100 \
  -p 8080:8080 \
  app:latest
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Container exits immediately | Check logs: `docker logs container_name` |
| Port already in use | Stop existing container or change port |
| OOM killed | Increase memory limit |
| Permission denied | Check file ownership and USER directive |
| DNS resolution fails | Use custom network, not default bridge |

### Debug Commands

```bash
# Check container logs
docker logs -f --tail 100 container_name

# Inspect container
docker inspect container_name

# Execute into container
docker exec -it container_name sh

# Check resource usage
docker stats container_name

# View container processes
docker top container_name
```

## Best Practices

1. **Use multi-stage builds** - Separate build and runtime
2. **Run as non-root** - Security requirement
3. **Set resource limits** - Prevent OOM kills
4. **Health checks** - Monitor container health
5. **Pin versions** - Reproducible builds
6. **Minimize layers** - Combine RUN commands
7. **Use .dockerignore** - Exclude unnecessary files
8. **Log to stdout/stderr** - Container logging best practice
