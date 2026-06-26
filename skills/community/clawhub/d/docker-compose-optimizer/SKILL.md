---
name: docker-compose-optimizer
description: Optimize Docker Compose configurations for development and production — audit services, networking, volumes, health checks, and resource management.
metadata:
  tags: ["docker-compose", "containers", "devops", "optimization", "development"]
---

# Docker Compose Optimizer

Analyze Docker Compose files for best practices, security, performance, and production readiness. Audit service configurations, networking, volume mounts, health checks, dependency management, and resource constraints.

## Usage

```
"Optimize my docker-compose.yml"
"Check Docker Compose for security issues"
"Review my multi-service setup"
"Make my Compose config production-ready"
```

## How It Works

### 1. Configuration Analysis

```bash
cat docker-compose.yml 2>/dev/null || cat docker-compose.yaml 2>/dev/null || cat compose.yml 2>/dev/null
ls docker-compose*.yml 2>/dev/null
```

### 2. Service Audit

- Image pinning: using tagged versions (not `latest`)
- Health checks defined for each service
- Restart policies appropriate (`unless-stopped` for production)
- Environment variables: secrets in `.env` file, not inline
- Build context: `.dockerignore` configured?
- Port mapping: unnecessary host port exposure

### 3. Networking

- Custom network vs default bridge
- Service discovery via DNS names
- Unnecessary port exposure to host
- Network isolation between service groups
- External network connections

### 4. Volumes & Storage

- Named volumes vs bind mounts (named for data persistence)
- Bind mounts for development (hot reload)
- Volume drivers for production (backup, replication)
- Tmpfs for temporary/sensitive data
- Proper volume cleanup strategy

### 5. Dependencies & Ordering

- `depends_on` with health check conditions
- Startup ordering for database → app → worker
- Graceful shutdown (stop_grace_period)
- Init containers pattern (using `profiles`)

### 6. Resource Management

- Memory limits (`mem_limit`, `memswap_limit`)
- CPU limits (`cpus`, `cpu_shares`)
- Logging configuration (driver, max-size, max-file)
- Ulimits for production services

### 7. Dev vs Production

- Override files (`docker-compose.override.yml` for dev)
- Profile-based service selection
- Dev-only services (mailhog, adminer, pgadmin)
- Production-only services (monitoring, logging)

## Output

```
## Docker Compose Analysis

**Services:** 6 | **Networks:** 1 (default) | **Volumes:** 3

### 🔴 Issues (2)
1. **No health checks** — 4/6 services missing health checks
   `depends_on` without `condition: service_healthy` is unreliable
   → Add healthcheck to db, redis, api, worker

2. **Secrets in compose file** — DB password inline
   `POSTGRES_PASSWORD: mypassword123`
   → Move to .env file or Docker secrets

### 🟡 Improvements (4)
3. No memory limits on any service — risk of one service OOM-killing others
4. Using `latest` tag on redis and postgres images
5. Default bridge network — create custom network for service isolation
6. No logging limits — logs will grow unbounded

### ✅ Good Practices
- Named volumes for database persistence
- Restart policy set to `unless-stopped`
- Build context uses multi-stage Dockerfile
- Override file separates dev config
```
