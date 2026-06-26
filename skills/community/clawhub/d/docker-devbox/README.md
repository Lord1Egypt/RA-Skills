# 🧊 Devbox

**One-command Docker dev environment for any project.** Auto-detects project type, language version, and package manager. Generates `docker-compose.dev.yml` with database service support.

## Features

- 🔍 **Smart Detection** — Recognizes 20+ project types
- 📦 **Version Matching** — Reads local runtime versions, matches Docker images
- 🔗 **pnpm Hard-Links** — Mounts host pnpm store for instant installs
- 🚀 **Port Management** — Auto-detects conflicts and assigns free ports
- 🗄️ **Database Support** — Attach PostgreSQL / MySQL / Redis / MongoDB / MinIO

## Quick Start

```bash
# Install
cp scripts/devbox.sh /usr/local/bin/devbox
chmod +x /usr/local/bin/devbox

# Auto-detect and run
devbox /path/to/your/project

# With databases
devbox /path/to/your/project 8000 --with postgres,redis
```

Then:
```bash
cd /path/to/your/project
docker compose -f docker-compose.dev.yml up -d
```

## Supported Project Types

| Type | Detection | Default Port | Docker Image |
|------|-----------|-------------|--------------|
| Nuxt 3/4 | `nuxt.config.*` | 3000 | `node:{ver}-bookworm` |
| Next.js | `next.config.*` | 3000 | `node:{ver}-bookworm` |
| Vue + Vite | `vite.config.*` + vue | 5173 | `node:{ver}-bookworm` |
| React + Vite | `vite.config.*` + react | 5173 | `node:{ver}-bookworm` |
| Svelte | `svelte.config.*` | 5173 | `node:{ver}-bookworm` |
| VitePress | `docs/.vitepress/` | 5173 | `node:{ver}-bookworm` |
| Node.js backend | `package.json` | 3000 | `node:{ver}-bookworm` |
| Python FastAPI | `requirements.txt` + fastapi | 8000 | `python:{ver}-slim` |
| Python Django | `manage.py` | 8000 | `python:{ver}-slim` |
| Python Flask | `requirements.txt` + flask | 5000 | `python:{ver}-slim` |
| Go | `go.mod` | 8080 | `golang:{ver}` |
| Rust | `Cargo.toml` | 8080 | `rust:{ver}` |
| Java (Spring Boot) | `pom.xml` + spring-boot | 8080 | `eclipse-temurin:{ver}-jdk` |
| Java (Maven) | `pom.xml` | 8080 | `eclipse-temurin:{ver}-jdk` |
| Java (Gradle) | `build.gradle` / `.kts` | 8080 | `eclipse-temurin:{ver}-jdk` |
| Kotlin | `*.kt` | 8080 | `eclipse-temurin:21-jdk` |
| Ruby on Rails | `Gemfile` + rails | 3000 | `ruby:{ver}-slim` |
| Ruby Sinatra | `Gemfile` | 4567 | `ruby:{ver}-slim` |
| PHP Laravel | `composer.json` + laravel | 5000 | `php:{ver}-cli` |
| PHP | `composer.json` | 8000 | `php:{ver}-cli` |
| C# / .NET | `*.csproj` / `*.sln` | 5000 | `dotnet/sdk:{ver}` |
| Swift | `Package.swift` | 8080 | `swift:{ver}` |
| Hugo | `hugo.toml` | 1313 | `klakegg/hugo:ext-alpine` |
| Static HTML | `*.html` | 80 | `nginx:alpine` |

## Dependencies

**Required:** `docker` + `docker compose`

**Optional** (for version detection): `node`, `python3`, `go`, `rustc`, `java`, `ruby`, `php`, `dotnet`, `swift`, `pnpm`/`yarn`/`bun`

**Optional** (for port conflict detection): `lsof`

## Attach Services

```bash
devbox ./my-app --with postgres,redis,mongo
```

| Service | Image | Port |
|---------|-------|------|
| `postgres` / `pg` | `postgres:16-alpine` | 5432 |
| `mysql` | `mysql:8-alpine` | 3306 |
| `redis` | `redis:7-alpine` | 6379 |
| `mongo` | `mongo:7` | 27017 |
| `minio` | `minio/minio` | 9000/9001 |

## CLI Reference

```
devbox <project-path> [port] [options]

Options:
  --framework <type>    Override auto-detection
  --with <services>     Comma-separated services to attach
  --env-file <path>     Environment variable file
  --use-dockerfile      Use project's existing Dockerfile
  -h, --help            Show help
```

## As an OpenClaw Skill

```bash
clawhub install docker-devbox
```

## License

MIT
