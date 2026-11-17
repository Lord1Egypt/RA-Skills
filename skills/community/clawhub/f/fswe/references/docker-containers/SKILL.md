# Docker & Containers

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| language | string | en | en, id |
| depth | string | standard | quick, standard, deep |

## Checklist

### Dockerfile Best Practices
- [ ] Use multi-stage builds (builder → runtime)
- [ ] Pin base image versions (`node:20-alpine`, not `latest`)
- [ ] Use `.dockerignore` (node_modules, .git, .env)
- [ ] Run as non-root user (`USER node`)
- [ ] Minimize layers — combine `RUN` commands
- [ ] Use `COPY --chown` instead of separate `chown` layer
- [ ] Place frequently changing layers last (deps before source)

### Docker Compose
- [ ] Use `depends_on` with `condition: service_healthy`
- [ ] Define healthchecks for all services
- [ ] Use volumes for development, named volumes for persistence
- [ ] Pin image versions in compose
- [ ] Use `.env` files for secrets (never commit)
- [ ] Define networks for service isolation

### Health Checks
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### Multi-Stage Build Template
```dockerfile
# Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Runtime
FROM node:20-alpine AS runtime
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
USER node
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Security
- [ ] Scan images: `docker scout cves <image>`
- [ ] Never store secrets in ENV (use Docker secrets or vault)
- [ ] Use read-only filesystem where possible
- [ ] Limit resources: `--memory`, `--cpus`
- [ ] Use specific tags, not `latest`

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `FROM node:latest` | `FROM node:20-alpine` |
| Running as root | Add `USER node` |
| No `.dockerignore` | Create one, exclude node_modules, .git |
| Copy all then npm install | Copy package*.json first, then install, then copy source |
| No healthcheck | Add HEALTHCHECK instruction |
