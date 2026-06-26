#!/bin/bash
# devbox — 为任意项目创建 Docker 开发环境
# Usage: devbox <project-path> [port] [options]
#
# Options:
#   --framework <type>    强制指定框架（覆盖自动检测）
#   --with <services>     附加服务（逗号分隔：postgres,mysql,redis,mongo,minio）
#   --env-file <path>     指定环境变量文件
#   --use-dockerfile      使用项目自带的 Dockerfile
#
# Supported: Node.js, Python, Go, Rust, Java, Ruby, PHP, C#/.NET, Kotlin, Swift, Hugo, static
#
# Volume 隔离策略：
#   源码通过 bind mount 挂载，所有生成文件（依赖、缓存、构建产物）使用命名卷隔离。
#   这样做的好处：
#   1. 宿主机和容器的缓存完全隔离，避免 Mac/Linux 路径/权限踩踏
#   2. macOS 上 bind mount 构建目录极慢，命名卷在 Linux VM 内原生读写
#   3. 重建容器不丢缓存，重启即恢复

set -e

# ── 参数解析 ──────────────────────────────────────────────────
PROJECT_PATH=""
PORT=""
FRAMEWORK=""
WITH_SERVICES=""
ENV_FILE=""
USE_DOCKERFILE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --framework) FRAMEWORK="$2"; shift 2 ;;
    --with) WITH_SERVICES="$2"; shift 2 ;;
    --env-file) ENV_FILE="$2"; shift 2 ;;
    --use-dockerfile) USE_DOCKERFILE=true; shift ;;
    -h|--help)
      echo "Usage: devbox <project-path> [port] [options]"
      echo ""
      echo "Options:"
      echo "  --framework <type>    Force framework detection"
      echo "  --with <services>     Add services: postgres,mysql,redis,mongo,minio"
      echo "  --env-file <path>     Environment variable file"
      echo "  --use-dockerfile      Use existing Dockerfile"
      echo ""
      echo "Frameworks:"
      echo "  Frontend:  nuxt, next, vue, react, vitepress, svelte"
      echo "  Backend:   node, python-fastapi, python-django, python-flask,"
      echo "             go, rust, java-spring, java-gradle, kotlin, ruby-rails,"
      echo "             php-laravel, dotnet, swift"
      echo "  Static:    hugo, static"
      echo ""
      echo "Services: postgres, mysql, redis, mongo, minio"
      exit 0
      ;;
    *)
      if [ -z "$PROJECT_PATH" ]; then
        PROJECT_PATH="$1"
      elif [ -z "$PORT" ]; then
        PORT="$1"
      fi
      shift
      ;;
  esac
done

if [ -z "$PROJECT_PATH" ]; then
  echo "❌ Usage: devbox <project-path> [port] [options]"
  echo "   Run 'devbox --help' for full usage"
  exit 1
fi

if [ ! -d "$PROJECT_PATH" ]; then
  echo "❌ 目录不存在: $PROJECT_PATH"
  exit 1
fi

PROJECT_NAME=$(basename "$PROJECT_PATH")
COMPOSE_FILE="$PROJECT_PATH/docker-compose.dev.yml"

# ── 端口冲突检测与自动分配 ──────────────────────────────────────
is_port_in_use() {
  lsof -i ":$1" -sTCP:LISTEN -t >/dev/null 2>&1 || \
  docker ps --format '{{.Ports}}' 2>/dev/null | grep -q ":${1}->" 2>/dev/null
}

find_free_port() {
  local start=$1
  local port=$start
  while is_port_in_use "$port"; do
    port=$((port + 1))
    if [ $port -gt $((start + 50)) ]; then
      echo ""
      return 1
    fi
  done
  echo "$port"
}

# ── 项目类型自动检测 ──────────────────────────────────────────
detect_framework() {
  local dir="$1"

  if [ -n "$FRAMEWORK" ]; then echo "$FRAMEWORK"; return; fi

  # Dockerfile 优先
  if [ "$USE_DOCKERFILE" = true ] && [ -f "$dir/Dockerfile" ]; then
    echo "dockerfile"; return
  fi

  # ── Frontend ──
  if ls "$dir"/nuxt.config.* 1>/dev/null 2>&1; then echo "nuxt"; return; fi
  if ls "$dir"/next.config.* 1>/dev/null 2>&1; then echo "next"; return; fi
  if [ -d "$dir/docs/.vitepress" ]; then echo "vitepress"; return; fi
  if ls "$dir"/svelte.config.* 1>/dev/null 2>&1; then echo "svelte"; return; fi

  # Vite 项目
  if ls "$dir"/vite.config.* 1>/dev/null 2>&1; then
    if grep -ql "vue" "$dir"/package.json 2>/dev/null; then echo "vue"; return; fi
    if grep -ql "react" "$dir"/package.json 2>/dev/null; then echo "react"; return; fi
    echo "vue"; return
  fi

  # ── Hugo ──
  if [ -f "$dir/hugo.toml" ] || ([ -f "$dir/config.toml" ] && [ -d "$dir/content" ]); then
    echo "hugo"; return
  fi

  # ── Java (Maven / Gradle) ──
  if [ -f "$dir/pom.xml" ]; then
    if grep -ql "spring-boot" "$dir"/pom.xml 2>/dev/null; then
      echo "java-spring"; return
    fi
    echo "java-maven"; return
  fi
  if [ -f "$dir/build.gradle" ] || [ -f "$dir/build.gradle.kts" ]; then
    echo "java-gradle"; return
  fi

  # ── Kotlin (无 Java 标志时) ──
  if ls "$dir"/*.kt 1>/dev/null 2>&1 && [ ! -f "$dir/pom.xml" ] && [ ! -f "$dir/build.gradle" ]; then
    echo "kotlin"; return
  fi

  # ── Python ──
  if [ -f "$dir/manage.py" ]; then echo "python-django"; return; fi
  if [ -f "$dir/requirements.txt" ] || [ -f "$dir/pyproject.toml" ] || [ -f "$dir/Pipfile" ]; then
    if grep -ql "fastapi" "$dir"/requirements.txt "$dir"/pyproject.toml 2>/dev/null; then
      echo "python-fastapi"; return
    fi
    if grep -ql "flask" "$dir"/requirements.txt "$dir"/pyproject.toml 2>/dev/null; then
      echo "python-flask"; return
    fi
    echo "python-fastapi"; return
  fi
  if ls "$dir"/*.py 1>/dev/null 2>&1; then echo "python-fastapi"; return; fi

  # ── Ruby ──
  if [ -f "$dir/Gemfile" ]; then
    if grep -ql "rails" "$dir"/Gemfile 2>/dev/null; then echo "ruby-rails"; return; fi
    echo "ruby-sinatra"; return
  fi

  # ── PHP ──
  if [ -f "$dir/composer.json" ]; then
    if grep -ql "laravel" "$dir"/composer.json 2>/dev/null; then echo "php-laravel"; return; fi
    echo "php"; return
  fi

  # ── C# / .NET ──
  if ls "$dir"/*.csproj 1>/dev/null 2>&1; then echo "dotnet"; return; fi
  if ls "$dir"/*.sln 1>/dev/null 2>&1; then echo "dotnet"; return; fi
  if [ -f "$dir/Program.cs" ] || [ -f "$dir/Startup.cs" ]; then echo "dotnet"; return; fi

  # ── Swift ──
  if [ -f "$dir/Package.swift" ]; then echo "swift"; return; fi

  # ── Go ──
  if [ -f "$dir/go.mod" ]; then echo "go"; return; fi

  # ── Rust ──
  if [ -f "$dir/Cargo.toml" ]; then echo "rust"; return; fi

  # ── Node.js ──
  if [ -f "$dir/package.json" ]; then echo "node"; return; fi

  # ── 静态文件 ──
  if ls "$dir"/*.html 1>/dev/null 2>&1; then echo "static"; return; fi

  echo "unknown"
}

# ══════════════════════════════════════════════════════════════
# 语言版本检测（全部带 fallback）
# ══════════════════════════════════════════════════════════════

detect_node_version() {
  if [ -n "$NVM_DIR" ] && [ -s "$NVM_DIR/nvm.sh" ]; then
    . "$NVM_DIR/nvm.sh" 2>/dev/null
  fi
  local ver
  ver=$(node --version 2>/dev/null | sed 's/^v//' | cut -d. -f1)
  echo "${ver:-22}"
}

detect_python_version() {
  local ver
  ver=$(python3 --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
  echo "${ver:-3.12}"
}

detect_go_version() {
  local ver
  ver=$(go version 2>/dev/null | awk '{print $3}' | sed 's/go//')
  echo "${ver:-1.22}"
}

detect_rust_version() {
  local ver
  ver=$(rustc --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
  echo "${ver:-1.77}"
}

detect_java_version() {
  local ver
  ver=$(java -version 2>&1 | head -1 | awk -F '"' '{print $2}' | cut -d. -f1)
  echo "${ver:-21}"
}

detect_ruby_version() {
  local ver
  ver=$(ruby --version 2>/dev/null | awk '{print $2}' | cut -d. -f1,2)
  echo "${ver:-3.3}"
}

detect_php_version() {
  local ver
  ver=$(php --version 2>/dev/null | head -1 | awk '{print $2}' | cut -d. -f1,2)
  echo "${ver:-8.3}"
}

detect_dotnet_version() {
  local ver
  ver=$(dotnet --version 2>/dev/null | cut -d. -f1,2)
  echo "${ver:-8.0}"
}

detect_kotlin_version() {
  local ver
  ver=$(kotlin -version 2>/dev/null | awk '{print $3}' | cut -d. -f1,2)
  echo "${ver:-2.0}"
}

detect_swift_version() {
  local ver
  ver=$(swift --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+' | head -1)
  echo "${ver:-5.10}"
}

# ── 包管理器检测 ──────────────────────────────────────────────
detect_pkg_manager() {
  local dir="$1"
  if [ -f "$dir/pnpm-lock.yaml" ]; then echo "pnpm"
  elif [ -f "$dir/yarn.lock" ]; then echo "yarn"
  elif [ -f "$dir/package-lock.json" ]; then echo "npm"
  elif [ -f "$dir/bun.lockb" ]; then echo "bun"
  else echo "npm"
  fi
}

get_pnpm_store() {
  pnpm store path 2>/dev/null || echo "$HOME/.local/share/pnpm/store/v3"
}

# ── .gitignore 管理 ──────────────────────────────────────────
ensure_gitignore() {
  local dir="$1"
  shift
  local entries=("$@")
  local gitignore="$dir/.gitignore"

  for entry in "${entries[@]}"; do
    if [ -f "$gitignore" ]; then
      if ! grep -qF "$entry" "$gitignore" 2>/dev/null; then
        echo "$entry" >> "$gitignore"
        echo "📝 .gitignore +: $entry"
      fi
    else
      echo "$entry" >> "$gitignore"
      echo "📝 .gitignore 创建: $entry"
    fi
  done
}

# ══════════════════════════════════════════════════════════════
# Docker Compose 生成
# ══════════════════════════════════════════════════════════════
generate_compose() {
  local fw="$1" port="$2" proj_path="$3" proj_name="$4" pkg_mgr="$5" pnpm_store="$6" env_file="$7"

  cat > "$COMPOSE_FILE" << 'HEADER'
# Auto-generated by devbox (https://github.com/Nciae-Zyh/devbox)
# Usage: docker compose -f docker-compose.dev.yml up -d
#
# Volume 隔离策略：
#   源码通过 bind mount 挂载，所有生成文件（依赖、缓存、构建产物）使用命名卷。
#   好处：宿主机/容器完全隔离，macOS 原生速度，重建不丢缓存。
services:
HEADER

  echo "  ${proj_name}:" >> "$COMPOSE_FILE"

  case "$fw" in

    # ════════════════════════════════════════════════
    # Node.js 前端
    # ════════════════════════════════════════════════
    nuxt|next|vue|react|vitepress|svelte)
      local nv; nv=$(detect_node_version)
      echo "    image: node:${nv}-bookworm" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app:delegated" >> "$COMPOSE_FILE"
      echo "      # node_modules 隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-nm:/app/node_modules" >> "$COMPOSE_FILE"
      [ "$pkg_mgr" = "pnpm" ] && {
        echo "      # pnpm store 隔离" >> "$COMPOSE_FILE"
        echo "      - ${proj_name}-pnpm-store:/root/.local/share/pnpm/store/v3" >> "$COMPOSE_FILE"
      }
      [ "$fw" = "nuxt" ] && {
        echo "      # Nuxt 缓存隔离（.nuxt + .output）" >> "$COMPOSE_FILE"
        echo "      - ${proj_name}-nuxt:/app/.nuxt" >> "$COMPOSE_FILE"
        echo "      - ${proj_name}-nuxt-output:/app/.output" >> "$COMPOSE_FILE"
      }
      [ "$fw" = "next" ] && {
        echo "      # Next.js 缓存隔离（.next）" >> "$COMPOSE_FILE"
        echo "      - ${proj_name}-next:/app/.next" >> "$COMPOSE_FILE"
      }
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:${port}\"" >> "$COMPOSE_FILE"
      echo "    environment:" >> "$COMPOSE_FILE"
      echo "      - NODE_ENV=development" >> "$COMPOSE_FILE"

      # Nuxt 专用环境变量
      if [ "$fw" = "nuxt" ]; then
        echo "      # Nuxt 端口与 Host 绑定" >> "$COMPOSE_FILE"
        echo "      - NITRO_PORT=${port}" >> "$COMPOSE_FILE"
        echo "      - NITRO_HOST=0.0.0.0" >> "$COMPOSE_FILE"
      fi

      echo "      # Vite HMR 文件监听优化" >> "$COMPOSE_FILE"
      echo "      - CHOKIDAR_USEPOLLING=true" >> "$COMPOSE_FILE"
      echo "      - CHOKIDAR_INTERVAL=300" >> "$COMPOSE_FILE"
      echo "      - VITE_DEV_SERVER_HOST=0.0.0.0" >> "$COMPOSE_FILE"

      local install_cmd dev_cmd
      case "$pkg_mgr" in
        pnpm) install_cmd="npm install -g pnpm && pnpm install --no-frozen-lockfile" ;;
        yarn) install_cmd="npm install -g yarn && yarn install" ;;
        bun)  install_cmd="curl -fsSL https://bun.sh/install | bash && export BUN_INSTALL=/root/.bun && export PATH=\$BUN_INSTALL/bin:\$PATH && bun install" ;;
        *)    install_cmd="npm install" ;;
      esac

      case "$fw" in
        nuxt)
          case "$pkg_mgr" in
            pnpm) dev_cmd="PORT=${port} pnpm dev --host 0.0.0.0 --port ${port}" ;;
            yarn) dev_cmd="PORT=${port} yarn dev --host 0.0.0.0 --port ${port}" ;;
            bun)  dev_cmd="PORT=${port} bun run dev --host 0.0.0.0 --port ${port}" ;;
            *)    dev_cmd="PORT=${port} npm run dev -- --host 0.0.0.0 --port ${port}" ;;
          esac ;;
        next)
          case "$pkg_mgr" in
            pnpm) dev_cmd="PORT=${port} pnpm dev -H 0.0.0.0 -p ${port}" ;;
            yarn) dev_cmd="PORT=${port} yarn dev -H 0.0.0.0 -p ${port}" ;;
            bun)  dev_cmd="PORT=${port} bun run dev -H 0.0.0.0 -p ${port}" ;;
            *)    dev_cmd="PORT=${port} npm run dev -- -H 0.0.0.0 -p ${port}" ;;
          esac ;;
        vue|react|vitepress|svelte)
          case "$pkg_mgr" in
            pnpm) dev_cmd="pnpm dev --host 0.0.0.0 --port ${port}" ;;
            yarn) dev_cmd="yarn dev --host 0.0.0.0 --port ${port}" ;;
            bun)  dev_cmd="bun run dev --host 0.0.0.0 --port ${port}" ;;
            *)    dev_cmd="npm run dev -- --host 0.0.0.0 --port ${port}" ;;
          esac ;;
      esac

      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"${install_cmd} && ${dev_cmd}\"" >> "$COMPOSE_FILE"

      # 健康检查
      echo "    healthcheck:" >> "$COMPOSE_FILE"
      echo "      test: [\"CMD\", \"curl\", \"-f\", \"http://localhost:${port}/\"]" >> "$COMPOSE_FILE"
      echo "      interval: 30s" >> "$COMPOSE_FILE"
      echo "      timeout: 10s" >> "$COMPOSE_FILE"
      echo "      retries: 3" >> "$COMPOSE_FILE"
      echo "      start_period: 60s" >> "$COMPOSE_FILE"

      # 资源限制
      echo "    deploy:" >> "$COMPOSE_FILE"
      echo "      resources:" >> "$COMPOSE_FILE"
      echo "        limits:" >> "$COMPOSE_FILE"
      echo "          memory: 4G" >> "$COMPOSE_FILE"
      echo "          cpus: \"2\"" >> "$COMPOSE_FILE"

      echo "    tty: true" >> "$COMPOSE_FILE"
      echo "    stdin_open: true" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Hugo
    # ════════════════════════════════════════════════
    hugo)
      echo "    image: klakegg/hugo:ext-alpine" >> "$COMPOSE_FILE"
      echo "    working_dir: /src" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/src" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:1313\"" >> "$COMPOSE_FILE"
      echo "    command: server --bind 0.0.0.0 --port 1313" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Python
    # ════════════════════════════════════════════════
    python-fastapi|python-django|python-flask)
      local pv; pv=$(detect_python_version)
      echo "    image: python:${pv}-slim" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # pip 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-pip:/root/.cache/pip" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"

      case "$fw" in
        python-fastapi)
          echo "      - \"${port}:8000\"" >> "$COMPOSE_FILE"
          echo "    command: >" >> "$COMPOSE_FILE"
          echo "      sh -c \"pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000 --reload\"" >> "$COMPOSE_FILE"
          ;;
        python-django)
          echo "      - \"${port}:8000\"" >> "$COMPOSE_FILE"
          echo "    command: >" >> "$COMPOSE_FILE"
          echo "      sh -c \"pip install -r requirements.txt && python manage.py runserver 0.0.0.0:8000\"" >> "$COMPOSE_FILE"
          ;;
        python-flask)
          echo "      - \"${port}:5000\"" >> "$COMPOSE_FILE"
          echo "    environment:" >> "$COMPOSE_FILE"
          echo "      - FLASK_APP=app.py" >> "$COMPOSE_FILE"
          echo "      - FLASK_ENV=development" >> "$COMPOSE_FILE"
          echo "    command: >" >> "$COMPOSE_FILE"
          echo "      sh -c \"pip install -r requirements.txt && flask run --host 0.0.0.0 --port 5000 --reload\"" >> "$COMPOSE_FILE"
          ;;
      esac
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Go
    # ════════════════════════════════════════════════
    go)
      local gv; gv=$(detect_go_version)
      echo "    image: golang:${gv}" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Go module 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-go-mod:/go/pkg/mod" >> "$COMPOSE_FILE"
      echo "      # Go build 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-go-cache:/root/.cache/go-build" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8080\"" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"go mod download && go run .\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Rust
    # ════════════════════════════════════════════════
    rust)
      local rv; rv=$(detect_rust_version)
      echo "    image: rust:${rv}" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Cargo registry 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-cargo-registry:/usr/local/cargo/registry" >> "$COMPOSE_FILE"
      echo "      # Cargo git 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-cargo-git:/usr/local/cargo/git" >> "$COMPOSE_FILE"
      echo "      # Cargo build 产物隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-cargo-target:/app/target" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8080\"" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"cargo install cargo-watch 2>/dev/null; cargo watch -x run\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Java (Maven)
    # ════════════════════════════════════════════════
    java-spring|java-maven)
      local jv; jv=$(detect_java_version)
      echo "    image: eclipse-temurin:${jv}-jdk-jammy" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Maven 本地仓库隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-m2:/root/.m2" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8080\"" >> "$COMPOSE_FILE"
      if [ "$fw" = "java-spring" ]; then
        echo "    command: >" >> "$COMPOSE_FILE"
        echo "      sh -c \"./mvnw spring-boot:run -Dspring-boot.run.arguments='--server.port=8080'\"" >> "$COMPOSE_FILE"
      else
        echo "    command: >" >> "$COMPOSE_FILE"
        echo "      sh -c \"mvn compile exec:java -Dexec.mainClass=Main -Dexec.port=${port}\"" >> "$COMPOSE_FILE"
      fi
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Java (Gradle)
    # ════════════════════════════════════════════════
    java-gradle)
      local jv; jv=$(detect_java_version)
      echo "    image: eclipse-temurin:${jv}-jdk-jammy" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Gradle 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-gradle:/root/.gradle" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8080\"" >> "$COMPOSE_FILE"
      if [ -f "$PROJECT_PATH/gradlew" ]; then
        echo "    command: >" >> "$COMPOSE_FILE"
        echo "      sh -c \"chmod +x ./gradlew && ./gradlew bootRun\"" >> "$COMPOSE_FILE"
      else
        echo "    command: >" >> "$COMPOSE_FILE"
        echo "      sh -c \"gradle bootRun\"" >> "$COMPOSE_FILE"
      fi
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Kotlin
    # ════════════════════════════════════════════════
    kotlin)
      echo "    image: eclipse-temurin:21-jdk-jammy" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Kotlin 构建缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-kotlin-cache:/root/.cache" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8080\"" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"kotlinc *.kt -include-runtime -d app.jar && java -jar app.jar\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Ruby
    # ════════════════════════════════════════════════
    ruby-rails)
      local rv; rv=$(detect_ruby_version)
      echo "    image: ruby:${rv}-slim" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Bundler gems 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-gems:/usr/local/bundle" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:3000\"" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"bundle install && bin/rails server -b 0.0.0.0 -p 3000\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    ruby-sinatra)
      local rv; rv=$(detect_ruby_version)
      echo "    image: ruby:${rv}-slim" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Bundler gems 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-gems:/usr/local/bundle" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:4567\"" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"bundle install && ruby app.rb\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # PHP
    # ════════════════════════════════════════════════
    php-laravel|php)
      local phpv; phpv=$(detect_php_version)
      echo "    image: php:${phpv}-cli" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Composer 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-composer:/root/.composer" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8000\"" >> "$COMPOSE_FILE"
      if [ "$fw" = "php-laravel" ]; then
        echo "    command: >" >> "$COMPOSE_FILE"
        echo "      sh -c \"composer install && php artisan serve --host=0.0.0.0 --port=8000\"" >> "$COMPOSE_FILE"
      else
        echo "    command: >" >> "$COMPOSE_FILE"
        echo "      sh -c \"composer install && php -S 0.0.0.0:8000\"" >> "$COMPOSE_FILE"
      fi
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # C# / .NET
    # ════════════════════════════════════════════════
    dotnet)
      local dv; dv=$(detect_dotnet_version)
      echo "    image: mcr.microsoft.com/dotnet/sdk:${dv}" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # NuGet 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-nuget:/root/.nuget" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:5000\"" >> "$COMPOSE_FILE"
      echo "    environment:" >> "$COMPOSE_FILE"
      echo "      - ASPNETCORE_URLS=http://0.0.0.0:5000" >> "$COMPOSE_FILE"
      echo "      - DOTNET_ENVIRONMENT=Development" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"dotnet restore && dotnet watch run\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Swift
    # ════════════════════════════════════════════════
    swift)
      local swv; swv=$(detect_swift_version)
      echo "    image: swift:${swv}" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # Swift build 缓存隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-swift:/app/.build" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:8080\"" >> "$COMPOSE_FILE"
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"swift package resolve && swift run\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # Node.js 后端
    # ════════════════════════════════════════════════
    node)
      local nv; nv=$(detect_node_version)
      echo "    image: node:${nv}-bookworm" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      # 源码挂载" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "      # node_modules 隔离" >> "$COMPOSE_FILE"
      echo "      - ${proj_name}-nm:/app/node_modules" >> "$COMPOSE_FILE"
      [ "$pkg_mgr" = "pnpm" ] && {
        echo "      # pnpm store 隔离" >> "$COMPOSE_FILE"
        echo "      - ${proj_name}-pnpm-store:/root/.local/share/pnpm/store/v3" >> "$COMPOSE_FILE"
      }
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:3000\"" >> "$COMPOSE_FILE"
      echo "    environment:" >> "$COMPOSE_FILE"
      echo "      - NODE_ENV=development" >> "$COMPOSE_FILE"

      local install_cmd
      case "$pkg_mgr" in
        pnpm) install_cmd="npm install -g pnpm && pnpm install --no-frozen-lockfile" ;;
        yarn) install_cmd="npm install -g yarn && yarn install" ;;
        bun)  install_cmd="curl -fsSL https://bun.sh/install | bash && export BUN_INSTALL=/root/.bun && export PATH=\$BUN_INSTALL/bin:\$PATH && bun install" ;;
        *)    install_cmd="npm install" ;;
      esac
      echo "    command: >" >> "$COMPOSE_FILE"
      echo "      sh -c \"${install_cmd} && node server.js\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # 静态文件
    # ════════════════════════════════════════════════
    static)
      echo "    image: nginx:alpine" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/usr/share/nginx/html:ro" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:80\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # 自定义 Dockerfile
    # ════════════════════════════════════════════════
    dockerfile)
      echo "    build: ." >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:${port}\"" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      ;;

    # ════════════════════════════════════════════════
    # 未知类型
    # ════════════════════════════════════════════════
    *)
      echo "    image: ubuntu:22.04" >> "$COMPOSE_FILE"
      echo "    working_dir: /app" >> "$COMPOSE_FILE"
      echo "    volumes:" >> "$COMPOSE_FILE"
      echo "      - ${proj_path}:/app" >> "$COMPOSE_FILE"
      echo "    ports:" >> "$COMPOSE_FILE"
      echo "      - \"${port}:${port}\"" >> "$COMPOSE_FILE"
      echo "    stdin_open: true" >> "$COMPOSE_FILE"
      echo "    tty: true" >> "$COMPOSE_FILE"
      echo "    restart: unless-stopped" >> "$COMPOSE_FILE"
      echo "    # ⚠️ 未识别项目类型，请手动配置 command" >> "$COMPOSE_FILE"
      ;;
  esac

  # ── 环境变量文件 ──
  if [ -n "$env_file" ] && [ -f "$proj_path/$env_file" ]; then
    echo "    env_file:" >> "$COMPOSE_FILE"
    echo "      - ${env_file}" >> "$COMPOSE_FILE"
  fi

  # ── 附加服务 ──
  if [ -n "$WITH_SERVICES" ]; then
    IFS=',' read -ra SVCS <<< "$WITH_SERVICES"
    for svc in "${SVCS[@]}"; do
      svc=$(echo "$svc" | tr -d ' ')
      case "$svc" in
        postgres|pg)
          cat >> "$COMPOSE_FILE" << 'EOF'

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
EOF
          ;;
        mysql)
          cat >> "$COMPOSE_FILE" << 'EOF'

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
EOF
          ;;
        redis)
          cat >> "$COMPOSE_FILE" << 'EOF'

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
EOF
          ;;
        mongo|mongodb)
          cat >> "$COMPOSE_FILE" << 'EOF'

  mongo:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo-data:/data/db
    restart: unless-stopped
EOF
          ;;
        minio)
          cat >> "$COMPOSE_FILE" << 'EOF'

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
EOF
          ;;
        *) echo "⚠️ 未知服务: $svc (跳过)" ;;
      esac
    done
  fi

  # ── volumes 声明 ──
  echo "" >> "$COMPOSE_FILE"
  echo "volumes:" >> "$COMPOSE_FILE"

  case "$fw" in
    nuxt|next|vue|react|vitepress|svelte|node)
      echo "  ${proj_name}-nm:" >> "$COMPOSE_FILE"
      [ "$pkg_mgr" = "pnpm" ] && echo "  ${proj_name}-pnpm-store:" >> "$COMPOSE_FILE"
      [ "$fw" = "nuxt" ] && {
        echo "  ${proj_name}-nuxt:" >> "$COMPOSE_FILE"
        echo "  ${proj_name}-nuxt-output:" >> "$COMPOSE_FILE"
      }
      [ "$fw" = "next" ] && echo "  ${proj_name}-next:" >> "$COMPOSE_FILE"
      ;;
    python-fastapi|python-django|python-flask)
      echo "  ${proj_name}-pip:" >> "$COMPOSE_FILE"
      ;;
    go)
      echo "  ${proj_name}-go-mod:" >> "$COMPOSE_FILE"
      echo "  ${proj_name}-go-cache:" >> "$COMPOSE_FILE"
      ;;
    rust)
      echo "  ${proj_name}-cargo-registry:" >> "$COMPOSE_FILE"
      echo "  ${proj_name}-cargo-git:" >> "$COMPOSE_FILE"
      echo "  ${proj_name}-cargo-target:" >> "$COMPOSE_FILE"
      ;;
    java-spring|java-maven)
      echo "  ${proj_name}-m2:" >> "$COMPOSE_FILE"
      ;;
    java-gradle)
      echo "  ${proj_name}-gradle:" >> "$COMPOSE_FILE"
      ;;
    kotlin)
      echo "  ${proj_name}-kotlin-cache:" >> "$COMPOSE_FILE"
      ;;
    ruby-rails|ruby-sinatra)
      echo "  ${proj_name}-gems:" >> "$COMPOSE_FILE"
      ;;
    php-laravel|php)
      echo "  ${proj_name}-composer:" >> "$COMPOSE_FILE"
      ;;
    dotnet)
      echo "  ${proj_name}-nuget:" >> "$COMPOSE_FILE"
      ;;
    swift)
      echo "  ${proj_name}-swift:" >> "$COMPOSE_FILE"
      ;;
  esac

  # 附加服务 volumes
  if [ -n "$WITH_SERVICES" ]; then
    IFS=',' read -ra SVCS <<< "$WITH_SERVICES"
    for svc in "${SVCS[@]}"; do
      svc=$(echo "$svc" | tr -d ' ')
      case "$svc" in
        postgres|pg) echo "  pg-data:" >> "$COMPOSE_FILE" ;;
        mysql)        echo "  mysql-data:" >> "$COMPOSE_FILE" ;;
        mongo|mongodb) echo "  mongo-data:" >> "$COMPOSE_FILE" ;;
        minio)        echo "  minio-data:" >> "$COMPOSE_FILE" ;;
      esac
    done
  fi
}

# ══════════════════════════════════════════════════════════════
# 主流程
# ══════════════════════════════════════════════════════════════

DETECTED_FW=$(detect_framework "$PROJECT_PATH")
echo "🔍 项目类型: $DETECTED_FW"

# 自动分配端口
if [ -z "$PORT" ]; then
  case "$DETECTED_FW" in
    nuxt|next|node) PORT=3000 ;;
    vue|react|vitepress|svelte) PORT=5173 ;;
    hugo) PORT=1313 ;;
    python-fastapi|python-django|java-spring|java-maven|java-gradle) PORT=8000 ;;
    python-flask|ruby-rails) PORT=5000 ;;
    php-laravel|php|dotnet) PORT=5000 ;;
    ruby-sinatra) PORT=4567 ;;
    go|rust|kotlin|swift|static|dockerfile) PORT=8080 ;;
    *) PORT=3000 ;;
  esac
fi

if is_port_in_use "$PORT"; then
  echo "⚠️  端口 $PORT 已被占用"
  AUTO_PORT=$(find_free_port "$PORT")
  if [ -n "$AUTO_PORT" ]; then
    echo "🔄 自动分配端口: $AUTO_PORT"
    PORT=$AUTO_PORT
  else
    echo "❌ 无法找到空闲端口（$PORT ~ $((PORT + 50)) 都被占用）"
    exit 1
  fi
fi

# 检测包管理器
PKG_MANAGER="npm"
PNPM_STORE=""
if [[ "$DETECTED_FW" =~ ^(nuxt|next|vue|react|vitepress|svelte|node)$ ]]; then
  PKG_MANAGER=$(detect_pkg_manager "$PROJECT_PATH")
  echo "📦 包管理器: $PKG_MANAGER"
  if [ "$PKG_MANAGER" = "pnpm" ]; then
    PNPM_STORE=$(get_pnpm_store)
    echo "📂 pnpm store: $PNPM_STORE"
  fi
fi

echo "🚀 创建开发环境: $PROJECT_NAME (port: $PORT, type: $DETECTED_FW)"

generate_compose "$DETECTED_FW" "$PORT" "$PROJECT_PATH" "$PROJECT_NAME" "$PKG_MANAGER" "$PNPM_STORE" "$ENV_FILE"

# 更新 .gitignore
IGNORE_ENTRIES=("docker-compose.dev.yml" ".env.local" ".env.development" ".env")
case "$DETECTED_FW" in
  nuxt|next|vue|react|vitepress|svelte|node)
    IGNORE_ENTRIES+=("node_modules/" ".pnpm-store/")
    [ "$DETECTED_FW" = "next" ] && IGNORE_ENTRIES+=(".next/")
    [ "$DETECTED_FW" = "nuxt" ] && IGNORE_ENTRIES+=(".nuxt/" ".output/")
    ;;
  go) IGNORE_ENTRIES+=("vendor/") ;;
  rust) IGNORE_ENTRIES+=("target/") ;;
  java-spring|java-maven|java-gradle) IGNORE_ENTRIES+=("target/" "build/" ".gradle/") ;;
  ruby-rails|ruby-sinatra) IGNORE_ENTRIES+=("vendor/bundle/") ;;
  php-laravel|php) IGNORE_ENTRIES+=("vendor/") ;;
  dotnet) IGNORE_ENTRIES+=("bin/" "obj/") ;;
esac
ensure_gitignore "$PROJECT_PATH" "${IGNORE_ENTRIES[@]}"

# 输出摘要
echo ""
echo "✅ 已创建: $COMPOSE_FILE"
echo ""
echo "📋 配置摘要:"
echo "   项目类型: $DETECTED_FW"
echo "   端口:     $PORT"

case "$DETECTED_FW" in
  nuxt|next|vue|react|vitepress|svelte|node)
    local nv; nv=$(detect_node_version)
    echo "   镜像:     node:${nv}-bookworm"
    echo "   包管理器: $PKG_MANAGER"
    [ "$PKG_MANAGER" = "pnpm" ] && echo "   pnpm store: 已挂载"
    ;;
  python-fastapi|python-django|python-flask)
    local pv; pv=$(detect_python_version)
    echo "   镜像:     python:${pv}-slim"
    ;;
  go)
    local gv; gv=$(detect_go_version)
    echo "   镜像:     golang:${gv}"
    ;;
  rust)
    local rv; rv=$(detect_rust_version)
    echo "   镜像:     rust:${rv}"
    ;;
  java-spring|java-maven|java-gradle)
    local jv; jv=$(detect_java_version)
    echo "   镜像:     eclipse-temurin:${jv}-jdk-jammy"
    ;;
  ruby-rails|ruby-sinatra)
    local rv; rv=$(detect_ruby_version)
    echo "   镜像:     ruby:${rv}-slim"
    ;;
  php-laravel|php)
    local phpv; phpv=$(detect_php_version)
    echo "   镜像:     php:${phpv}-cli"
    ;;
  dotnet)
    local dv; dv=$(detect_dotnet_version)
    echo "   镜像:     dotnet/sdk:${dv}"
    ;;
  swift)
    local swv; swv=$(detect_swift_version)
    echo "   镜像:     swift:${swv}"
    ;;
esac

[ -n "$WITH_SERVICES" ] && echo "   附加服务: $WITH_SERVICES"

echo ""
echo "📋 下一步:"
echo "   1. cd $PROJECT_PATH"
echo "   2. docker compose -f docker-compose.dev.yml up -d"
echo "   3. 访问 http://localhost:$PORT"
echo ""
echo "💡 Volume 隔离提示:"
echo "   所有生成文件（依赖/缓存/构建产物）在命名卷中，宿主机不可见。"
echo "   重建容器不丢缓存。清理: docker volume rm <volume-name>"
echo ""
