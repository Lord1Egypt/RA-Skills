#!/usr/bin/env bash
# cron-edit-safe CLI 入口
# 用法：cron-edit-safe <cron-id> [options]
# 特点：自动管理 jq 依赖（首次运行检测）+ 凭证透传 + 软链解析

set -euo pipefail

# 解析软链到真实路径（支持 ~/.local/bin/cron-edit-safe 软链调用）
# 用 python os.path.realpath 替代 readlink -f（readlink -f 在某些环境解析错）
SCRIPT_PATH="$(python3 -c "import os, sys; print(os.path.realpath(sys.argv[1]))" "${BASH_SOURCE[0]}")"
SKILL_DIR="$(dirname "$(dirname "$SCRIPT_PATH")")"
SCRIPT="${SKILL_DIR}/scripts/cron-edit-safe.sh"

# 前置检查：jq 必须存在
if ! command -v jq >/dev/null 2>&1; then
  echo "❌ jq 未安装" >&2
  echo "   安装方法：" >&2
  echo "   - Debian/Ubuntu: sudo apt install jq" >&2
  echo "   - macOS: brew install jq" >&2
  echo "   - CentOS/RHEL: sudo yum install jq" >&2
  exit 1
fi

# 前置检查：openclaw 必须存在
if ! command -v openclaw >/dev/null 2>&1; then
  echo "❌ openclaw CLI 未安装" >&2
  echo "   安装方法: https://docs.openclaw.ai" >&2
  exit 1
fi

# 前置检查：核心脚本必须存在
if [[ ! -f "$SCRIPT" ]]; then
  echo "❌ 核心脚本不存在: $SCRIPT" >&2
  exit 1
fi

# 凭证透传（未来扩展用）
if [[ -n "${EM_API_KEY:-}" ]]; then
  export EM_API_KEY
fi
if [[ -n "${MINIMAX_API_KEY:-}" ]]; then
  export MINIMAX_API_KEY
fi

# 转发所有参数给核心脚本
exec bash "$SCRIPT" "$@"