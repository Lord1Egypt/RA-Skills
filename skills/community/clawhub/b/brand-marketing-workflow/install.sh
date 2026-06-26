#!/usr/bin/env bash
# install.sh — Brand Marketing Workflow 云端执行入口
# ClawDex 通过 oc_execute_skill 解密后执行此脚本
# Python 模块位于 lib/ 目录下
set -euo pipefail
for cmd in python3; do
  command -v "$cmd" >/dev/null 2>&1 || {
    printf '{"success":false,"error":"missing: %s"}\n' "$cmd"; exit 0
  }
done
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/lib/run.py" "$@"
