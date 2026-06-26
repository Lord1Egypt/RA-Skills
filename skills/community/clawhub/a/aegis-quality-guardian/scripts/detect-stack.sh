#!/usr/bin/env bash
# aegis/scripts/detect-stack.sh — Detect project language/framework stack
# Usage: bash detect-stack.sh /path/to/project
# Output: JSON with detected languages, frameworks, and recommended tools
#
# Used by init-project.sh and setup-guardrails.sh to auto-configure checks

set -euo pipefail

PROJECT_PATH="${1:?Usage: detect-stack.sh <project-path>}"

detect() {
  local langs=()
  local frameworks=()
  local pkg_managers=()

  # --- TypeScript / JavaScript ---
  if [ -f "$PROJECT_PATH/tsconfig.json" ]; then
    langs+=("typescript")
  fi
  if [ -f "$PROJECT_PATH/package.json" ]; then
    langs+=("javascript")
    # Detect package manager
    if [ -f "$PROJECT_PATH/pnpm-lock.yaml" ]; then
      pkg_managers+=("pnpm")
    elif [ -f "$PROJECT_PATH/yarn.lock" ]; then
      pkg_managers+=("yarn")
    elif [ -f "$PROJECT_PATH/bun.lockb" ]; then
      pkg_managers+=("bun")
    else
      pkg_managers+=("npm")
    fi
    # Detect frameworks
    if grep -q '"next"' "$PROJECT_PATH/package.json" 2>/dev/null; then
      frameworks+=("nextjs")
    fi
    if grep -q '"react"' "$PROJECT_PATH/package.json" 2>/dev/null; then
      frameworks+=("react")
    fi
    if grep -q '"vue"' "$PROJECT_PATH/package.json" 2>/dev/null; then
      frameworks+=("vue")
    fi
    if grep -q '"fastify"' "$PROJECT_PATH/package.json" 2>/dev/null; then
      frameworks+=("fastify")
    fi
    if grep -q '"express"' "$PROJECT_PATH/package.json" 2>/dev/null; then
      frameworks+=("express")
    fi
    if grep -q '"@nestjs/core"' "$PROJECT_PATH/package.json" 2>/dev/null; then
      frameworks+=("nestjs")
    fi
  fi

  # --- Go ---
  if [ -f "$PROJECT_PATH/go.mod" ]; then
    langs+=("go")
    if grep -q "github.com/gin-gonic/gin" "$PROJECT_PATH/go.mod" 2>/dev/null; then
      frameworks+=("gin")
    fi
    if grep -q "github.com/gofiber/fiber" "$PROJECT_PATH/go.mod" 2>/dev/null; then
      frameworks+=("fiber")
    fi
    if grep -q "github.com/aws/aws-lambda-go" "$PROJECT_PATH/go.mod" 2>/dev/null; then
      frameworks+=("aws-lambda")
    fi
    if grep -q "github.com/aws/aws-cdk-go" "$PROJECT_PATH/go.mod" 2>/dev/null; then
      frameworks+=("aws-cdk")
    fi
  fi

  # --- Python ---
  if [ -f "$PROJECT_PATH/pyproject.toml" ] || [ -f "$PROJECT_PATH/setup.py" ] || [ -f "$PROJECT_PATH/requirements.txt" ]; then
    langs+=("python")
    if [ -f "$PROJECT_PATH/pyproject.toml" ]; then
      if grep -q "fastapi" "$PROJECT_PATH/pyproject.toml" 2>/dev/null; then
        frameworks+=("fastapi")
      fi
      if grep -q "django" "$PROJECT_PATH/pyproject.toml" 2>/dev/null; then
        frameworks+=("django")
      fi
      if grep -q "flask" "$PROJECT_PATH/pyproject.toml" 2>/dev/null; then
        frameworks+=("flask")
      fi
      # Package manager
      if grep -q "poetry" "$PROJECT_PATH/pyproject.toml" 2>/dev/null; then
        pkg_managers+=("poetry")
      elif [ -f "$PROJECT_PATH/uv.lock" ]; then
        pkg_managers+=("uv")
      else
        pkg_managers+=("pip")
      fi
    fi
  fi

  # --- Rust ---
  if [ -f "$PROJECT_PATH/Cargo.toml" ]; then
    langs+=("rust")
    pkg_managers+=("cargo")
    if grep -q "actix-web" "$PROJECT_PATH/Cargo.toml" 2>/dev/null; then
      frameworks+=("actix")
    fi
    if grep -q "axum" "$PROJECT_PATH/Cargo.toml" 2>/dev/null; then
      frameworks+=("axum")
    fi
  fi

  # --- Java / Kotlin ---
  if [ -f "$PROJECT_PATH/pom.xml" ]; then
    langs+=("java")
    pkg_managers+=("maven")
  fi
  if [ -f "$PROJECT_PATH/build.gradle" ] || [ -f "$PROJECT_PATH/build.gradle.kts" ]; then
    langs+=("java")
    pkg_managers+=("gradle")
    if [ -f "$PROJECT_PATH/build.gradle.kts" ]; then
      langs+=("kotlin")
    fi
  fi

  # --- Monorepo detection ---
  local is_monorepo="false"
  if [ -f "$PROJECT_PATH/pnpm-workspace.yaml" ] || [ -f "$PROJECT_PATH/lerna.json" ] || [ -d "$PROJECT_PATH/packages" ]; then
    is_monorepo="true"
  fi

  # --- Docker ---
  local has_docker="false"
  if [ -f "$PROJECT_PATH/Dockerfile" ] || [ -f "$PROJECT_PATH/docker-compose.yml" ] || [ -f "$PROJECT_PATH/docker-compose.yaml" ]; then
    has_docker="true"
  fi

  # --- Database detection ---
  local databases=()
  # Check common dependency files for database drivers
  local dep_files=("$PROJECT_PATH/package.json" "$PROJECT_PATH/pyproject.toml" "$PROJECT_PATH/requirements.txt" "$PROJECT_PATH/go.mod" "$PROJECT_PATH/Cargo.toml" "$PROJECT_PATH/Gemfile")
  local all_deps=""
  for df in "${dep_files[@]}"; do
    [ -f "$df" ] && all_deps+=" $(cat "$df")"
  done
  # Also check docker-compose for existing DB services
  for dc in "$PROJECT_PATH/docker-compose.yml" "$PROJECT_PATH/docker-compose.yaml"; do
    [ -f "$dc" ] && all_deps+=" $(cat "$dc")"
  done

  if echo "$all_deps" | grep -qi "mongo\|pymongo\|mongoose\|mongodb"; then databases+=("mongodb"); fi
  if echo "$all_deps" | grep -qi "redis\|ioredis\|aioredis\|redis-py"; then databases+=("redis"); fi
  if echo "$all_deps" | grep -qi "mysql\|mysqlclient\|mysql2\|mariadb"; then databases+=("mysql"); fi
  if echo "$all_deps" | grep -qi "postgres\|psycopg\|pg \|sequelize.*postgres\|prisma.*postgres\|asyncpg\|sqlx.*postgres"; then databases+=("postgresql"); fi
  if echo "$all_deps" | grep -qi "sqlite\|better-sqlite\|rusqlite"; then databases+=("sqlite"); fi

  # --- IaC ---
  local iac=()
  if [ -f "$PROJECT_PATH/cdk.json" ]; then
    iac+=("cdk")
  fi
  if [ -f "$PROJECT_PATH/template.yaml" ] || [ -f "$PROJECT_PATH/template.yml" ]; then
    iac+=("sam")
  fi
  if ls "$PROJECT_PATH"/*.tf 2>/dev/null | head -1 >/dev/null 2>&1; then
    iac+=("terraform")
  fi

  # Output JSON
  echo "{"
  echo "  \"languages\": [$(printf '"%s",' "${langs[@]}" | sed 's/,$//')],"
  echo "  \"frameworks\": [$(printf '"%s",' "${frameworks[@]}" 2>/dev/null | sed 's/,$//')],"
  echo "  \"packageManagers\": [$(printf '"%s",' "${pkg_managers[@]}" 2>/dev/null | sed 's/,$//')],"
  echo "  \"databases\": [$(printf '"%s",' "${databases[@]}" 2>/dev/null | sed 's/,$//')],"
  echo "  \"monorepo\": $is_monorepo,"
  echo "  \"docker\": $has_docker,"
  echo "  \"iac\": [$(printf '"%s",' "${iac[@]}" 2>/dev/null | sed 's/,$//')]"
  echo "}"
}

detect
