# Docker Compose Templates

## Volume 隔离策略

所有模板遵循统一的隔离原则：
- **源码**：通过 bind mount 挂载
- **生成文件**：依赖、缓存、构建产物全部使用命名卷隔离
- **好处**：宿主机/容器完全隔离，macOS 上避免 bind mount 构建目录的性能问题，重建容器不丢缓存

## Frontend Templates

### Nuxt 3/4

```yaml
services:
  my-nuxt:
    image: node:24-bookworm
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app:delegated
      # node_modules 隔离
      - my-nuxt-nm:/app/node_modules
      # pnpm store 隔离
      - my-nuxt-pnpm-store:/root/.local/share/pnpm/store/v3
      # Nuxt 缓存隔离（.nuxt + .output）
      - my-nuxt-nuxt:/app/.nuxt
      - my-nuxt-nuxt-output:/app/.output
    ports:
      - "3000:3000"
    command: >
      sh -c "npm install -g pnpm &&
             pnpm install --no-frozen-lockfile &&
             PORT=3000 pnpm dev --host 0.0.0.0 --port 3000"
    environment:
      - NODE_ENV=development
      - NITRO_PORT=3000
      - NITRO_HOST=0.0.0.0
      - CHOKIDAR_USEPOLLING=true
      - CHOKIDAR_INTERVAL=300
      - VITE_DEV_SERVER_HOST=0.0.0.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2"
    tty: true
    stdin_open: true
    restart: unless-stopped

volumes:
  my-nuxt-nm:
  my-nuxt-pnpm-store:
  my-nuxt-nuxt:
  my-nuxt-nuxt-output:
```

### Next.js

```yaml
services:
  my-next:
    image: node:24-bookworm
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app:delegated
      # node_modules 隔离
      - my-next-nm:/app/node_modules
      # Next.js 缓存隔离（.next）
      - my-next-next:/app/.next
    ports:
      - "3000:3000"
    command: >
      sh -c "npm install -g pnpm &&
             pnpm install --no-frozen-lockfile &&
             PORT=3000 pnpm dev -H 0.0.0.0 -p 3000"
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
      - CHOKIDAR_INTERVAL=300
      - VITE_DEV_SERVER_HOST=0.0.0.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2"
    tty: true
    stdin_open: true
    restart: unless-stopped

volumes:
  my-next-nm:
  my-next-next:
```

### Vue + Vite / React + Vite

```yaml
services:
  my-app:
    image: node:24-bookworm
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app:delegated
      # node_modules 隔离
      - my-app-nm:/app/node_modules
      # pnpm store 隔离
      - my-app-pnpm-store:/root/.local/share/pnpm/store/v3
    ports:
      - "5173:5173"
    command: >
      sh -c "npm install -g pnpm &&
             pnpm install --no-frozen-lockfile &&
             pnpm dev --host 0.0.0.0 --port 5173"
    environment:
      - NODE_ENV=development
      - CHOKIDAR_USEPOLLING=true
      - CHOKIDAR_INTERVAL=300
      - VITE_DEV_SERVER_HOST=0.0.0.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5173/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: "2"
    tty: true
    stdin_open: true
    restart: unless-stopped

volumes:
  my-app-nm:
  my-app-pnpm-store:
```

## Backend Templates

### Python FastAPI

```yaml
services:
  my-api:
    image: python:3.12-slim
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # pip 缓存隔离
      - my-api-pip:/root/.cache/pip
    ports:
      - "8000:8000"
    command: >
      sh -c "pip install -r requirements.txt &&
             uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    restart: unless-stopped

volumes:
  my-api-pip:
```

### Python Django

```yaml
services:
  my-django:
    image: python:3.12-slim
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # pip 缓存隔离
      - my-django-pip:/root/.cache/pip
    ports:
      - "8000:8000"
    command: >
      sh -c "pip install -r requirements.txt &&
             python manage.py runserver 0.0.0.0:8000"
    restart: unless-stopped

volumes:
  my-django-pip:
```

### Go

```yaml
services:
  my-go:
    image: golang:1.22
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # Go module 缓存隔离
      - my-go-go-mod:/go/pkg/mod
      # Go build 缓存隔离
      - my-go-go-cache:/root/.cache/go-build
    ports:
      - "8080:8080"
    command: >
      sh -c "go mod download && go run ."
    restart: unless-stopped

volumes:
  my-go-go-mod:
  my-go-go-cache:
```

### Rust

```yaml
services:
  my-rust:
    image: rust:1.77
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # Cargo registry 缓存隔离
      - my-rust-cargo-registry:/usr/local/cargo/registry
      # Cargo git 缓存隔离
      - my-rust-cargo-git:/usr/local/cargo/git
      # Cargo build 产物隔离
      - my-rust-cargo-target:/app/target
    ports:
      - "8080:8080"
    command: >
      sh -c "cargo install cargo-watch && cargo watch -x run"
    restart: unless-stopped

volumes:
  my-rust-cargo-registry:
  my-rust-cargo-git:
  my-rust-cargo-target:
```

### Java (Spring Boot / Maven)

```yaml
services:
  my-java:
    image: eclipse-temurin:21-jdk-jammy
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # Maven 本地仓库隔离
      - my-java-m2:/root/.m2
    ports:
      - "8080:8080"
    command: >
      sh -c "./mvnw spring-boot:run -Dspring-boot.run.arguments='--server.port=8080'"
    restart: unless-stopped

volumes:
  my-java-m2:
```

### Java (Gradle)

```yaml
services:
  my-gradle:
    image: eclipse-temurin:21-jdk-jammy
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # Gradle 缓存隔离
      - my-gradle-gradle:/root/.gradle
    ports:
      - "8080:8080"
    command: >
      sh -c "chmod +x ./gradlew && ./gradlew bootRun"
    restart: unless-stopped

volumes:
  my-gradle-gradle:
```

### Ruby on Rails

```yaml
services:
  my-rails:
    image: ruby:3.3-slim
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # Bundler gems 缓存隔离
      - my-rails-gems:/usr/local/bundle
    ports:
      - "3000:3000"
    command: >
      sh -c "bundle install && bin/rails server -b 0.0.0.0 -p 3000"
    restart: unless-stopped

volumes:
  my-rails-gems:
```

### PHP Laravel

```yaml
services:
  my-laravel:
    image: php:8.3-cli
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # Composer 缓存隔离
      - my-laravel-composer:/root/.composer
    ports:
      - "8000:8000"
    command: >
      sh -c "composer install && php artisan serve --host=0.0.0.0 --port=8000"
    restart: unless-stopped

volumes:
  my-laravel-composer:
```

### C# / .NET

```yaml
services:
  my-dotnet:
    image: mcr.microsoft.com/dotnet/sdk:8.0
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app
      # NuGet 缓存隔离
      - my-dotnet-nuget:/root/.nuget
    ports:
      - "5000:5000"
    environment:
      - ASPNETCORE_URLS=http://0.0.0.0:5000
      - DOTNET_ENVIRONMENT=Development
    command: >
      sh -c "dotnet restore && dotnet watch run"
    restart: unless-stopped

volumes:
  my-dotnet-nuget:
```

## Static & Docs Templates

### Hugo

```yaml
services:
  my-hugo:
    image: klakegg/hugo:ext-alpine
    working_dir: /src
    volumes:
      - /path/to/your/project:/src
    ports:
      - "1313:1313"
    command: server --bind 0.0.0.0 --port 1313
    restart: unless-stopped
```

### VitePress

```yaml
services:
  my-docs:
    image: node:24-bookworm
    working_dir: /app
    volumes:
      # 源码挂载
      - /path/to/your/project:/app:delegated
      # node_modules 隔离
      - my-docs-nm:/app/node_modules
    ports:
      - "5173:5173"
    command: >
      sh -c "npm install -g pnpm &&
             pnpm install --no-frozen-lockfile &&
             pnpm docs:dev --host 0.0.0.0 --port 5173"
    restart: unless-stopped

volumes:
  my-docs-nm:
```

### Static HTML (nginx)

```yaml
services:
  my-static:
    image: nginx:alpine
    volumes:
      - /path/to/your/project:/usr/share/nginx/html:ro
    ports:
      - "8080:80"
    restart: unless-stopped
```

## Database Services

### PostgreSQL + Redis (与应用组合)

```yaml
services:
  my-app:
    image: node:24-bookworm
    working_dir: /app
    volumes:
      - /path/to/your/project:/app:delegated
      - my-app-nm:/app/node_modules
      - my-app-pnpm-store:/root/.local/share/pnpm/store/v3
    ports:
      - "3000:3000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    environment:
      - DATABASE_URL=postgresql://devbox:devbox@postgres:5432/devbox
      - REDIS_URL=redis://redis:6379
    restart: unless-stopped

  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=devbox
      - POSTGRES_PASSWORD=devbox
      - POSTGRES_DB=devbox
    ports:
      - "5432:5432"
    volumes:
      - pg-data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U devbox"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  my-app-nm:
  my-app-pnpm-store:
  pg-data:
```

### MySQL + MinIO (与应用组合)

```yaml
services:
  my-app:
    image: python:3.12-slim
    working_dir: /app
    volumes:
      - /path/to/your/project:/app
      - my-app-pip:/root/.cache/pip
    ports:
      - "8000:8000"
    depends_on:
      mysql:
        condition: service_healthy
    environment:
      - DATABASE_URL=mysql://devbox:devbox@mysql:3306/devbox
      - MINIO_ENDPOINT=http://minio:9000
    restart: unless-stopped

  mysql:
    image: mysql:8-alpine
    environment:
      - MYSQL_ROOT_PASSWORD=devbox
      - MYSQL_DATABASE=devbox
      - MYSQL_USER=devbox
      - MYSQL_PASSWORD=devbox
    ports:
      - "3306:3306"
    volumes:
      - mysql-data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      - MINIO_ROOT_USER=devbox
      - MINIO_ROOT_PASSWORD=devbox123
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio-data:/data
    restart: unless-stopped

volumes:
  my-app-pip:
  mysql-data:
  minio-data:
```

## Volume 隔离策略速查表

| 项目类型 | 命名卷 |
|---------|--------|
| Nuxt | `nm`, `pnpm-store`, `nuxt`, `nuxt-output` |
| Next.js | `nm`, `next` |
| Vue/React/Vite/Svelte | `nm`, `pnpm-store` |
| Python | `pip` |
| Go | `go-mod`, `go-cache` |
| Rust | `cargo-registry`, `cargo-git`, `cargo-target` |
| Java Maven | `m2` |
| Java Gradle | `gradle` |
| Ruby | `gems` |
| PHP | `composer` |
| .NET | `nuget` |
| Swift | `swift` |
