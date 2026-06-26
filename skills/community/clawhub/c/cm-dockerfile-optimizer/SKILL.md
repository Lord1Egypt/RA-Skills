---
name: dockerfile-optimizer
description: Optimize Dockerfiles for smaller images, faster builds, better security, and production readiness — multi-stage builds, layer caching, vulnerability reduction.
metadata:
  tags: ["docker", "optimization", "security", "containers", "devops"]
---

# Dockerfile Optimizer

Analyze and optimize Dockerfiles for smaller image sizes, faster builds, better layer caching, and production security. Reviews build stages, base images, layer ordering, secrets handling, and runtime configuration. Use when Docker images are too large, builds are slow, or preparing containers for production.

## Usage

```
"Optimize this Dockerfile"
"Reduce my Docker image size"
"Check my Dockerfile for security issues"
"Speed up my Docker builds"
"Make this Dockerfile production-ready"
```

## How It Works

### 1. Dockerfile Analysis

Parse the Dockerfile and analyze:

```bash
# Find all Dockerfiles
find . -name "Dockerfile*" -not -path "*/node_modules/*"
# Check current image sizes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | head -20
# Analyze layers
docker history <image> --no-trunc --format "{{.Size}}\t{{.CreatedBy}}" 2>/dev/null
```

### 2. Image Size Reduction

**Base image optimization:**
- `node:18` (900MB) → `node:18-slim` (200MB) → `node:18-alpine` (120MB)
- `python:3.12` (1GB) → `python:3.12-slim` (140MB) → `python:3.12-alpine` (50MB)
- `ubuntu:22.04` (77MB) → `debian:bookworm-slim` (74MB) → `alpine:3.19` (7MB)
- Consider distroless images for production: `gcr.io/distroless/nodejs20` (130MB)
- Check if base image tag is pinned (`:latest` is unpredictable)

**Layer optimization:**
- Combine RUN statements to reduce layers
- Remove package manager caches in the same layer: `apt-get clean && rm -rf /var/lib/apt/lists/*`
- Remove build dependencies after compilation
- Use `.dockerignore` to exclude `node_modules`, `.git`, tests, docs

**Multi-stage builds:**
- Separate build stage from runtime stage
- Copy only built artifacts to final stage
- Use builder pattern for compiled languages (Go, Rust, C++)
- Cache mount for package managers: `--mount=type=cache,target=/root/.npm`

**Content analysis:**
- Large files that shouldn't be in the image
- Development dependencies in production images
- Unnecessary system packages
- Debug tools left in production images

### 3. Build Speed

**Layer caching:**
- Order layers from least to most frequently changing
- Copy dependency manifests before source code
- Use `COPY package.json package-lock.json ./` before `COPY . .`
- BuildKit cache mounts for package managers

**BuildKit features:**
- `--mount=type=cache` for persistent package caches
- `--mount=type=secret` for build-time secrets
- `--mount=type=ssh` for private repo access
- Parallel multi-stage builds

**CI integration:**
- Registry-backed cache: `--cache-from` / `--cache-to`
- GitHub Actions cache integration
- Layer-aware cache invalidation

### 4. Security Hardening

- Run as non-root user (`USER 1001`)
- Use `COPY --chown` instead of `RUN chown`
- No secrets in build args or environment variables
- Healthcheck configured
- Read-only root filesystem where possible
- Minimal attack surface (no shells, no package managers in production)
- Pin package versions for reproducibility
- Scan base image for CVEs

### 5. Production Readiness

- `HEALTHCHECK` instruction present
- `EXPOSE` documents the correct ports
- `ENTRYPOINT` vs `CMD` used correctly
- Signal handling (PID 1 problem, `tini` or `--init`)
- Graceful shutdown support
- Logging to stdout/stderr (not files)
- Environment variable configuration with sensible defaults

## Output

```
## Dockerfile Optimization Report

**Current image:** myapp:latest (847MB, 23 layers)
**Optimized estimate:** ~95MB (8 layers)

### 🔴 Critical Issues (3)
1. **Running as root** — no USER instruction
   → Add: `RUN addgroup -g 1001 app && adduser -u 1001 -G app -D app`
   → Add: `USER app` before ENTRYPOINT

2. **Secret in build arg** — `ARG DB_PASSWORD`
   → Use `--mount=type=secret` or runtime env var

3. **No .dockerignore** — sending 2.1GB build context
   → Create .dockerignore: node_modules, .git, *.md, tests/

### ⚡ Size Reduction
| Change | Size Impact |
|--------|------------|
| node:18 → node:18-alpine | -780MB |
| Multi-stage build | -340MB (dev deps) |
| .dockerignore | -2.1GB context |
| Combined RUN layers | -45MB (cache) |
| **Total** | **847MB → ~95MB (-89%)** |

### 🏗️ Optimized Dockerfile
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
RUN addgroup -g 1001 app && adduser -u 1001 -G app -D app
WORKDIR /app
COPY --from=builder --chown=app:app /app/dist ./dist
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/package.json ./
USER app
EXPOSE 3000
HEALTHCHECK --interval=30s CMD wget -qO- http://localhost:3000/health
ENTRYPOINT ["node", "dist/index.js"]
```

### Build Speed
- Added layer caching: dependency install cached separately
- BuildKit cache mount: npm cache persists across builds
- Estimated build time: 45s → 12s (warm cache)
```
