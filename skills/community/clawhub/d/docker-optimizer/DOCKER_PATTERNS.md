# Docker Optimization Patterns Reference

A comprehensive guide to Docker optimization patterns, anti-patterns, and best practices.

## Multi-Stage Build Patterns

### Pattern: Build and Runtime Separation

**Purpose**: Separate build-time dependencies from runtime dependencies

❌ **Single Stage (Bloated)**:
```dockerfile
FROM node:20
WORKDIR /app
COPY . .
RUN npm install  # Installs ALL dependencies
RUN npm run build
CMD ["node", "dist/server.js"]
# Result: 1.2GB image with dev dependencies
```

✅ **Multi-Stage (Optimized)**:
```dockerfile
# Build stage
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
# Result: 180MB image, production dependencies only
```

---

### Pattern: Minimal Final Stage

**Purpose**: Use the smallest possible base for final image

✅ **Go - Scratch Base**:
```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o app

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /app/app /app
ENTRYPOINT ["/app"]
# Result: 8MB image
```

✅ **Node.js - Distroless**:
```dockerfile
FROM node:20 AS builder
# ... build steps ...

FROM gcr.io/distroless/nodejs20-debian11
COPY --from=builder /app /app
CMD ["server.js"]
# Result: 120MB, no shell/package manager
```

---

### Pattern: Dependency Extraction

**Purpose**: Separate dependencies from application code for better caching

✅ **Python with Requirements**:
```dockerfile
# Dependency stage
FROM python:3.11-slim AS deps
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
COPY --from=deps /root/.local /root/.local
COPY . /app
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "app.py"]
```

---

## Layer Caching Patterns

### Pattern: Dependency-First Copying

**Purpose**: Cache dependency installation when source code changes

❌ **Poor Caching**:
```dockerfile
COPY . .
RUN npm install  # Re-runs on any file change
```

✅ **Optimized Caching**:
```dockerfile
# Copy only dependency files
COPY package.json package-lock.json ./
RUN npm ci  # Cached unless package files change

# Then copy source code
COPY . .  # Source changes don't invalidate npm install
```

---

### Pattern: Cache Mounts (BuildKit)

**Purpose**: Persist package manager caches across builds

✅ **Node.js Cache Mount**:
```dockerfile
RUN --mount=type=cache,target=/root/.npm \
    npm ci
```

✅ **Go Module Cache**:
```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download
```

✅ **Python Pip Cache**:
```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

---

### Pattern: Combine Commands

**Purpose**: Reduce layers and enable cleanup in same layer

❌ **Multiple Layers**:
```dockerfile
RUN apt-get update
RUN apt-get install -y git curl
RUN apt-get clean
# Each RUN creates a layer, cleanup doesn't reduce size
```

✅ **Single Layer**:
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      git \
      curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Everything in one layer, cleanup works
```

---

## Base Image Patterns

### Pattern: Choosing the Right Base

**Size vs. Compatibility Trade-offs:**

**Full Base Images** (Ubuntu/Debian):
```dockerfile
FROM ubuntu:22.04  # ~80MB base
# Use when: Need full GNU userland, complex dependencies
# Avoid when: Size matters, security critical
```

**Slim Variants**:
```dockerfile
FROM python:3.11-slim  # ~180MB vs 900MB full
# Use when: Need some system tools, complex C extensions
# Best for: Python, Node.js production
```

**Alpine Linux**:
```dockerfile
FROM node:20-alpine  # ~120MB vs 900MB full
# Use when: Size critical, simple dependencies
# Watch out: musl libc compatibility issues
```

**Distroless**:
```dockerfile
FROM gcr.io/distroless/python3-debian11  # ~50MB
# Use when: Maximum security, no debugging needed
# Trade-off: No shell, harder to debug
```

**Scratch**:
```dockerfile
FROM scratch  # 0MB base
# Use when: Static binaries (Go, Rust)
# Requires: Self-contained binary
```

---

### Pattern: Language-Specific Base Selection

**Node.js:**
```dockerfile
# Development
FROM node:20  # 900MB, full tools

# Production
FROM node:20-alpine  # 120MB, minimal

# Maximum security
FROM gcr.io/distroless/nodejs20-debian11  # 120MB, no shell
```

**Python:**
```dockerfile
# ML/Data Science (need compilation)
FROM python:3.11  # 900MB, full build tools

# Web apps (some C extensions)
FROM python:3.11-slim  # 180MB, basic tools

# Minimal (pure Python only)
FROM python:3.11-alpine  # 50MB, musl issues possible
```

**Java:**
```dockerfile
# With JDK (for building)
FROM eclipse-temurin:17  # 450MB

# JRE only (production)
FROM eclipse-temurin:17-jre  # 270MB

# Minimal JRE (Alpine)
FROM eclipse-temurin:17-jre-alpine  # 170MB
```

---

## Security Patterns

### Pattern: Non-Root User

**Purpose**: Minimize damage from container compromise

❌ **Running as Root**:
```dockerfile
FROM node:20-alpine
COPY . /app
CMD ["node", "server.js"]
# Runs as root (uid 0)
```

✅ **Non-Root User**:
```dockerfile
FROM node:20-alpine

# Create user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

WORKDIR /app

# Copy with correct ownership
COPY --chown=nodejs:nodejs . .

# Switch to non-root
USER nodejs

CMD ["node", "server.js"]
```

---

### Pattern: Read-Only Root Filesystem

**Purpose**: Prevent malicious file modifications

✅ **Read-Only FS**:
```dockerfile
FROM node:20-alpine
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs

WORKDIR /app
COPY --chown=nodejs:nodejs . .

# Create writable temp directory
RUN mkdir -p /tmp/app && chown nodejs:nodejs /tmp/app

USER nodejs

# Run with read-only root
# (Set at runtime: docker run --read-only --tmpfs /tmp ...)
CMD ["node", "server.js"]
```

---

### Pattern: No Secrets in Layers

**Purpose**: Prevent secret exposure in image layers

❌ **Secret in Layer**:
```dockerfile
COPY .env /app/.env  # Secret persists in layer
RUN npm run build
RUN rm .env  # Too late, still in previous layer
```

✅ **Build-Time Secrets (BuildKit)**:
```dockerfile
RUN --mount=type=secret,id=env,target=/app/.env \
    npm run build
# Secret mounted temporarily, not in layers

# Build with:
# docker build --secret id=env,src=.env .
```

✅ **Runtime Secrets**:
```dockerfile
# Don't copy secrets, pass at runtime
CMD ["node", "server.js"]

# Run with:
# docker run -e DATABASE_URL="..." app
```

---

### Pattern: Security Scanning

**Purpose**: Detect vulnerabilities before deployment

```dockerfile
# Use specific versions for reproducibility
FROM node:20.11.0-alpine3.19

# Scan during CI/CD
# docker scan image:tag
# trivy image image:tag
```

---

## Size Optimization Patterns

### Pattern: Package Manager Cleanup

**Purpose**: Remove package manager caches and temporary files

❌ **Leaves Garbage**:
```dockerfile
RUN apt-get update && apt-get install -y git
# Leaves /var/lib/apt/lists/* (~100MB)
```

✅ **Cleans Up**:
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**All Package Managers:**

```dockerfile
# Debian/Ubuntu
RUN apt-get update && \
    apt-get install -y --no-install-recommends <packages> && \
    rm -rf /var/lib/apt/lists/*

# Alpine
RUN apk add --no-cache <packages>

# Python pip
RUN pip install --no-cache-dir -r requirements.txt

# Node.js npm
RUN npm ci --only=production && \
    npm cache clean --force

# Go modules
RUN go mod download && \
    go clean -modcache  # If not using cache mount
```

---

### Pattern: Multi-Stage Dependency Pruning

**Purpose**: Include only production dependencies

✅ **Node.js Production Dependencies**:
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci  # Install ALL dependencies
COPY . .
RUN npm run build

# Separate stage for prod deps
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Final stage
FROM node:20-alpine
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/server.js"]
```

---

### Pattern: Slim Dependencies

**Purpose**: Install only required dependencies, no recommendations

❌ **Installs Recommendations**:
```dockerfile
RUN apt-get install git
# Installs git + 50+ recommended packages
```

✅ **Minimal Install**:
```dockerfile
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*
# Installs only git and required dependencies
```

---

## Build Performance Patterns

### Pattern: Parallel Builds

**Purpose**: Build independent stages in parallel

✅ **BuildKit Parallel**:
```dockerfile
FROM node:20-alpine AS deps
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS tester
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm test

# Both builder and tester can run in parallel
```

---

### Pattern: External Dependency Caching

**Purpose**: Pre-build dependency layers

✅ **Separate Dependency Image**:
```dockerfile
# Dockerfile.deps
FROM node:20-alpine
COPY package*.json ./
RUN npm ci
# Build and tag: docker build -f Dockerfile.deps -t myapp:deps .

# Dockerfile (main)
FROM myapp:deps AS deps
FROM node:20-alpine
COPY --from=deps /node_modules ./node_modules
COPY . .
# Much faster when dependencies don't change
```

---

## Health Check Patterns

### Pattern: Application Health Checks

**Purpose**: Enable container orchestration to detect unhealthy containers

✅ **Node.js HTTP Health Check**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"
```

✅ **Python Flask Health Check**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"
```

✅ **Using curl (if available)**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8080/health || exit 1
```

✅ **Using wget (Alpine)**:
```dockerfile
RUN apk add --no-cache wget
HEALTHCHECK CMD wget --quiet --tries=1 --spider http://localhost:8080/health || exit 1
```

---

## Signal Handling Patterns

### Pattern: Proper Signal Forwarding

**Purpose**: Enable graceful shutdown

❌ **Shell Form (Wrong)**:
```dockerfile
CMD npm start
# Runs as /bin/sh -c "npm start"
# Signals go to shell, not app
```

✅ **Exec Form**:
```dockerfile
CMD ["node", "server.js"]
# Runs directly as PID 1, receives signals
```

✅ **Using Tini/Dumb-Init**:
```dockerfile
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
# Tini handles signals properly
```

---

## Metadata Patterns

### Pattern: Image Labels

**Purpose**: Document image metadata

✅ **Comprehensive Labels**:
```dockerfile
LABEL org.opencontainers.image.title="My App" \
      org.opencontainers.image.description="Application description" \
      org.opencontainers.image.version="1.2.3" \
      org.opencontainers.image.authors="team@example.com" \
      org.opencontainers.image.source="https://github.com/org/repo" \
      org.opencontainers.image.licenses="MIT"
```

---

## Development vs Production Patterns

### Pattern: Multi-Target Builds

**Purpose**: Single Dockerfile for dev and prod

✅ **Conditional Stages**:
```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

# Development stage
FROM base AS development
RUN npm install  # All dependencies including dev
COPY . .
CMD ["npm", "run", "dev"]

# Build stage
FROM base AS builder
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001 -G nodejs
COPY --from=builder --chown=nodejs:nodejs /app/dist ./dist
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
USER nodejs
CMD ["node", "dist/server.js"]

# Build dev: docker build --target development -t app:dev .
# Build prod: docker build --target production -t app:prod .
```

---

## .dockerignore Patterns

### Pattern: Comprehensive Exclusions

**Purpose**: Reduce build context size and avoid copying unnecessary files

✅ **Complete .dockerignore**:
```
# Dependencies
node_modules
bower_components
vendor

# Build outputs
dist
build
*.out
*.exe

# Logs
*.log
logs
npm-debug.log*

# Test files
coverage
.nyc_output
**/*.test.js
**/*.spec.js
__tests__

# Development files
.git
.gitignore
.env
.env.local
.env.*.local
*.md
README.md
.editorconfig

# IDE files
.vscode
.idea
*.swp
*.swo
.DS_Store

# CI/CD
.github
.gitlab-ci.yml
.travis.yml

# Docker files
Dockerfile
docker-compose.yml
.dockerignore
```

---

## Common Anti-Patterns to Avoid

### Anti-Pattern: Using :latest Tag

❌ **Unpredictable**:
```dockerfile
FROM node:latest
# Breaks when new version released
```

✅ **Specific Version**:
```dockerfile
FROM node:20.11.0-alpine3.19
# Reproducible builds
```

---

### Anti-Pattern: Copying Unnecessary Files

❌ **Copies Everything**:
```dockerfile
COPY . .
# Copies node_modules, .git, build artifacts
```

✅ **Selective Copying**:
```dockerfile
COPY package*.json ./
COPY src ./src
COPY public ./public
# Or use .dockerignore
```

---

### Anti-Pattern: Running apt-get update in Separate Layer

❌ **Cache Issues**:
```dockerfile
RUN apt-get update
RUN apt-get install -y git
# Stale package lists if cached
```

✅ **Combined**:
```dockerfile
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*
```

---

### Anti-Pattern: Installing Build Dependencies in Final Image

❌ **Bloated**:
```dockerfile
FROM python:3.11-slim
RUN apt-get update && apt-get install -y gcc python3-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
# gcc and python3-dev still in image
```

✅ **Multi-Stage**:
```dockerfile
FROM python:3.11-slim AS builder
RUN apt-get update && apt-get install -y gcc python3-dev
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
# Build deps not in final image
```

---

## Summary

**Key Patterns for Optimization:**
- ✅ Multi-stage builds (separate build/runtime)
- ✅ Minimal base images (Alpine/Distroless/Scratch)
- ✅ Layer caching (copy dependencies first)
- ✅ Non-root users (security)
- ✅ Cache mounts (BuildKit)
- ✅ Package cleanup (same layer)
- ✅ Production dependencies only
- ✅ Health checks
- ✅ Proper signal handling
- ✅ Comprehensive .dockerignore

**Impact Hierarchy (Biggest Wins First):**
1. Multi-stage builds (60-90% size reduction)
2. Alpine/Slim base images (50-80% size reduction)
3. Layer caching optimization (5-20× build speed)
4. Security hardening (non-root, minimal surface)
5. BuildKit features (cache mounts, secrets)

Apply these patterns systematically for production-ready, secure, and efficient Docker images!
