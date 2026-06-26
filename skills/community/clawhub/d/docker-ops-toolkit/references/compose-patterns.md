# Docker Compose Patterns

## Common Service Patterns

### Web App + Database
```yaml
services:
  web:
    build: .
    ports: ["${PORT:-3000}:3000"]
    environment:
      - DB_HOST=db
      - DB_USER=${DB_USER:-app}
      - DB_PASSWORD=${DB_PASSWORD:-secret}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
      - /app/node_modules    # anonymous volume to not override

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: appdb
      POSTGRES_USER: ${DB_USER:-app}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-secret}
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U app"]
      interval: 5s
      timeout: 3s
      retries: 5
    ports: ["${DB_PORT:-5432}:5432"]

volumes:
  pgdata:
```

### Multi-stage build (example Dockerfile)
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json .
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

## Health Check Patterns

```yaml
services:
  app:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## .env File Template
```
# .env — automatically loaded by docker compose
PORT=3000
DB_PORT=5432
DB_USER=app
DB_PASSWORD=change_me_in_prod
NODE_ENV=development
```

## Useful Compose Commands

| Command | Purpose |
|---------|---------|
| `docker compose config` | Validate and view resolved config |
| `docker compose top` | List running processes per service |
| `docker compose events` | Stream container events |
| `docker compose images` | List images used by services |
| `docker compose pause/resume` | Pause/resume service containers |

## Tips

- Use `${VAR:-default}` for env vars with defaults — keeps compose.yml portable
- Always pin image tags in production (e.g. `postgres:16-alpine`, not `postgres:latest`)
- Use `platform: linux/amd64` if running on ARM and images don't support multi-arch
- Never mount `.env` as a bind mount — it's auto-loaded
