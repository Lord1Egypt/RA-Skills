#!/usr/bin/env bash
set -euo pipefail

# 用法：
#   ./scripts/run-playwright-auto.sh [grep过滤词]
# 示例：
#   ./scripts/run-playwright-auto.sh "@smoke"

FILTER="${1:-}"
BASE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

LOCAL_RUN="$BASE_DIR/scripts/run-playwright.sh"
DOCKER_RUN="$BASE_DIR/scripts/run-playwright-docker.sh"

cd "$BASE_DIR"

echo "[auto] 尝试本地模式（local）..."
if "$LOCAL_RUN" "$FILTER"; then
  echo "[auto] 本地模式执行成功。"
  exit 0
fi

echo "[auto] 本地模式失败，切换 Docker 模式..."
if command -v docker >/dev/null 2>&1; then
  "$DOCKER_RUN" "$FILTER"
  echo "[auto] Docker 模式执行完成。"
  exit 0
fi

echo "[error] 本地模式失败，且未检测到 docker 命令。"
echo "[hint] 请先安装 Docker，或修复本地 Playwright 依赖后重试。"
exit 1
