#!/bin/bash
# create-dev-env.sh — 兼容旧版调用，转发到 devbox
# Usage: create-dev-env.sh <project-path> <port> [framework]
# 建议直接使用 devbox 命令

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 转换旧参数格式
PROJECT_PATH="$1"
PORT="$2"
FRAMEWORK="${3:-}"

if [ -z "$PROJECT_PATH" ]; then
  echo "⚠️  此脚本已弃用，请使用 devbox 命令"
  echo "   用法: devbox <project-path> [port] [options]"
  exit 1
fi

ARGS=("$PROJECT_PATH")
[ -n "$PORT" ] && ARGS+=("$PORT")
[ -n "$FRAMEWORK" ] && ARGS+=("--framework" "$FRAMEWORK")

exec "$SCRIPT_DIR/devbox.sh" "${ARGS[@]}"
