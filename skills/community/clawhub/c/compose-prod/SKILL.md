---
name: compose-prod
description: "Generate production-grade docker-compose.yml for any project. Includes health checks for every service, network segmentation (frontend/backend/db), resource limits, log rotation, restart policies, secrets management, and backup volumes. Stack-agnostic — works with Node.js, Python, Go, Java, Ruby, PHP, or any Dockerized app. Use when the user says 'docker compose', 'production compose', 'dockerize', 'containerize', or needs a production-ready Compose file."
---

# Production Docker Compose Generator

Generate a production-grade `docker-compose.yml` from any project, with health checks, network segmentation, resource limits, logging, secrets, and backup volumes.

## When to Use

- User says "docker compose", "production compose", "dockerize", "containerize"
- User has an app and needs a production-ready Compose file
- User wants to add health checks, resource limits, or networking to an existing Compose file
- User is preparing an app for deployment with Docker

## When NOT to Use

- Kubernetes manifests (use a k8s skill)
- Cloud-managed container services (ECS, Cloud Run) with their own config formats
- Development-only Compose files where none of this matters

## Prerequisites

- A project directory with application code
- A `Dockerfile` in the project (or enough context to generate one)
- Docker and Docker Compose installed on the target machine

## Execution Flow

### Phase 1: Detect the Stack

Scan the project directory to determine:

1. **Application type** — detect from files present:
   - `package.json` -> Node.js / Next.js / Remix / etc.
   - `requirements.txt` / `pyproject.toml` / `Pipfile` -> Python
   - `go.mod` -> Go
   - `pom.xml` / `build.gradle` -> Java
   - `Gemfile` -> Ruby
   - `composer.json` -> PHP
   - `Cargo.toml` -> Rust
2. **Application port** — detect from `Dockerfile` EXPOSE, framework defaults, or ask
3. **Database dependencies** — detect from dependency files:
   - `pg`, `prisma`, `psycopg`, `sqlalchemy+postgresql` -> PostgreSQL
   - `redis`, `ioredis`, `bull`, `celery[redis]` -> Redis
   - `mongoose`, `mongodb`, `pymongo`, `motor` -> MongoDB
   - `mysql2`, `mysqlclient`, `pymysql` -> MySQL
4. **Existing Dockerfile** — check if one exists. If not, offer to generate one.
5. **Existing docker-compose.yml** — check if one exists. If upgrading, read it first.
6. **Environment variables** — scan `.env`, `.env.local`, `.env.example` for required vars

### Phase 2: Generate docker-compose.yml

Generate the full Compose file following EVERY rule below. Do NOT skip any section.

#### 2a. File Header

```yaml
# Production Docker Compose
# Generated for: <project-name>
# Stack: <detected-stack>
# Run: docker compose up -d
# Validate: docker compose config

services:
```

#### 2b. Application Service

```yaml
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: <project-name>-app
    restart: unless-stopped
    ports:
      - "127.0.0.1:${APP_PORT:-3000}:${APP_PORT:-3000}"
    env_file:
      - .env
    networks:
      - frontend
      - backend
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:${APP_PORT:-3000}/health || curl -f http://localhost:${APP_PORT:-3000}/ || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.25'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    depends_on:
      # Add database services here with condition: service_healthy
```

Key rules for the app service:
- **ALWAYS** bind to `127.0.0.1` — never expose directly to `0.0.0.0`. Use a reverse proxy (Nginx/Traefik/Caddy) for external traffic.
- **ALWAYS** use `env_file` instead of inline `environment` with secrets.
- **ALWAYS** include `restart: unless-stopped`.
- Adjust port, memory, and CPU based on the detected stack and expected load.
- For Next.js standalone output, set memory limit to at least 512M.
- For Python ML/AI apps, set memory limit to at least 1G.

#### 2c. Database Services

Include ONLY the databases detected in Phase 1. Every database MUST have: health check, volume, resource limits, logging, restart policy, and be on the `database` network only.

**PostgreSQL:**
```yaml
  postgres:
    image: postgres:17-alpine
    container_name: <project-name>-postgres
    restart: unless-stopped
    volumes:
      - pgdata:/var/lib/postgresql/data
      - pgbackup:/backups
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-app}
      POSTGRES_USER: ${POSTGRES_USER:-app}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}
    networks:
      - database
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-app} -d ${POSTGRES_DB:-app}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.25'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

**Redis:**
```yaml
  redis:
    image: redis:7-alpine
    container_name: <project-name>-redis
    restart: unless-stopped
    command: redis-server --requirepass ${REDIS_PASSWORD:-changeme} --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redisdata:/data
    networks:
      - database
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD:-changeme}", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
      start_period: 10s
    deploy:
      resources:
        limits:
          memory: 256M
          cpus: '0.5'
        reservations:
          memory: 64M
          cpus: '0.1'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

**MongoDB:**
```yaml
  mongo:
    image: mongo:8
    container_name: <project-name>-mongo
    restart: unless-stopped
    volumes:
      - mongodata:/data/db
      - mongobackup:/backups
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USER:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:?MONGO_PASSWORD is required}
      MONGO_INITDB_DATABASE: ${MONGO_DB:-app}
    networks:
      - database
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')", "-u", "${MONGO_USER:-admin}", "-p", "${MONGO_PASSWORD}", "--authenticationDatabase", "admin", "--quiet"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.25'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

**MySQL:**
```yaml
  mysql:
    image: mysql:9
    container_name: <project-name>-mysql
    restart: unless-stopped
    volumes:
      - mysqldata:/var/lib/mysql
      - mysqlbackup:/backups
    environment:
      MYSQL_DATABASE: ${MYSQL_DB:-app}
      MYSQL_USER: ${MYSQL_USER:-app}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:?MYSQL_PASSWORD is required}
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD:?MYSQL_ROOT_PASSWORD is required}
    networks:
      - database
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost", "-u", "root", "-p${MYSQL_ROOT_PASSWORD}"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.25'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
```

#### 2d. Network Segmentation

ALWAYS define three isolated networks. Services connect ONLY to the networks they need:

```yaml
networks:
  frontend:
    driver: bridge
    name: <project-name>-frontend
  backend:
    driver: bridge
    name: <project-name>-backend
  database:
    driver: bridge
    name: <project-name>-database
    internal: true  # No external connectivity for the database network
```

Network assignment rules:
- **frontend**: Reverse proxy (Nginx/Traefik/Caddy) and the app service
- **backend**: App service and any worker/queue services
- **database**: App service and database services ONLY
- The app service joins `frontend`, `backend`, AND `database` (it bridges all three)
- Database services join `database` ONLY — never `frontend`
- Worker services join `backend` and `database` — never `frontend`
- The `database` network MUST be `internal: true` to block external access

#### 2e. Volumes

Define named volumes for ALL persistent data. Include backup volumes for databases:

```yaml
volumes:
  pgdata:
    driver: local
    name: <project-name>-pgdata
  pgbackup:
    driver: local
    name: <project-name>-pgbackup
  redisdata:
    driver: local
    name: <project-name>-redisdata
  mongodata:
    driver: local
    name: <project-name>-mongodata
  mongobackup:
    driver: local
    name: <project-name>-mongobackup
  mysqldata:
    driver: local
    name: <project-name>-mysqldata
  mysqlbackup:
    driver: local
    name: <project-name>-mysqlbackup
```

Only include volumes for services that are actually in the Compose file.

#### 2f. Secrets (When Applicable)

For higher security, use Docker Compose file-based secrets instead of env_file for sensitive values:

```yaml
secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

Then reference in services:

```yaml
services:
  app:
    secrets:
      - db_password
      - api_key
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
```

Secret rules:
- Default to `env_file` approach — it works everywhere and most teams know it.
- Offer the `secrets:` approach when the user asks for tighter security.
- If using secrets, create a `secrets/` directory with `.gitignore` to exclude it.
- NEVER put secrets inline in the Compose file.
- NEVER commit secret files to version control.

### Phase 3: Generate .env.example

Create a `.env.example` file listing ALL environment variables used in the Compose file with safe placeholder values:

```env
# Application
APP_PORT=3000
NODE_ENV=production

# PostgreSQL
POSTGRES_DB=app
POSTGRES_USER=app
POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD

# Redis
REDIS_PASSWORD=CHANGE_ME_STRONG_PASSWORD

# MongoDB
MONGO_DB=app
MONGO_USER=admin
MONGO_PASSWORD=CHANGE_ME_STRONG_PASSWORD
```

### Phase 4: Optional Services

Offer to add these based on the project's needs. Ask the user before including:

**Nginx reverse proxy (if no external proxy exists):**
```yaml
  nginx:
    image: nginx:alpine
    container_name: <project-name>-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    networks:
      - frontend
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      resources:
        limits:
          memory: 128M
          cpus: '0.5'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    depends_on:
      app:
        condition: service_healthy
```

**Worker / queue processor:**
```yaml
  worker:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: <project-name>-worker
    restart: unless-stopped
    command: <worker-command>  # e.g., "npm run worker", "celery -A app worker"
    env_file:
      - .env
    networks:
      - backend
      - database
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
    logging:
      driver: json-file
      options:
        max-size: "10m"
        max-file: "3"
    depends_on:
      app:
        condition: service_healthy
```

### Phase 5: Validate

After generating, run validation:

```bash
docker compose config
```

This checks:
- YAML syntax is valid
- All referenced env vars have defaults or are present
- Volume and network references are consistent
- No unknown keys

If validation fails, fix the issue and re-validate. Do NOT deliver an invalid Compose file.

### Phase 6: Deliver and Explain

Tell the user:

1. What services were included and why
2. Network topology — which services can talk to which
3. How to start: `docker compose up -d`
4. How to view logs: `docker compose logs -f`
5. How to check health: `docker compose ps` (shows health status)
6. How to stop: `docker compose down`
7. How to stop and delete data: `docker compose down -v` (warn: destroys volumes)
8. Remind them to copy `.env.example` to `.env` and fill in real values

## Mandatory Rules (NEVER Skip These)

1. **Health check on EVERY service** — no exceptions. If a service has no obvious health check, use `test: ["CMD-SHELL", "exit 0"]` as a placeholder and comment that the user should replace it.
2. **Resource limits on EVERY service** — memory and CPU limits prevent runaway containers.
3. **Logging with rotation on EVERY service** — `json-file` driver with `max-size: 10m` and `max-file: 3`.
4. **Restart policy on EVERY service** — `unless-stopped` for all production services.
5. **Network segmentation** — three networks minimum (frontend, backend, database). Database network MUST be `internal: true`.
6. **Named volumes** — never use bind mounts for database data in production.
7. **No exposed database ports** — databases are NEVER published to the host in the default config.
8. **env_file over inline environment** for secrets — never hardcode credentials.
9. **Backup volumes** for every database — a dedicated volume mounted at `/backups` for dump scripts.
10. **Container naming** — use `container_name: <project>-<service>` for easy identification.
11. **Port binding to 127.0.0.1** — app services bind to localhost only, not 0.0.0.0.
12. **depends_on with condition: service_healthy** — services wait for their dependencies to be healthy.
13. **Validate with `docker compose config`** before delivering.

## Adapting to Multi-Service Architectures

For microservice projects with multiple apps:

- Each service gets its own build context or image
- Shared databases are in the `database` network
- Inter-service communication happens on the `backend` network
- Only the API gateway / reverse proxy touches `frontend`
- Use `depends_on` to express the dependency graph
- Each service gets independent resource limits tuned to its role:
  - API services: 512M-1G memory
  - Workers: 256M-1G memory depending on task
  - Proxies: 128M memory
  - Databases: 512M-2G memory depending on dataset size
  - Caches (Redis): 256M memory

## Troubleshooting

- **Health check failing**: Check that the health check command is available in the container image (e.g., `curl` may not be in slim images — use `wget` or a custom binary)
- **Container OOM killed**: Increase memory limit or investigate the memory leak
- **Network connectivity issues**: Verify services are on the correct networks with `docker network inspect`
- **Secrets not readable**: Check file permissions on secret files (should be 600)
- **Compose config invalid**: Run `docker compose config` to see the expanded and validated config
