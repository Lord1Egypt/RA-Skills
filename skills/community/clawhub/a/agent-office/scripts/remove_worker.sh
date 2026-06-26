#!/usr/bin/env bash
# remove_worker.sh —— 调用 Python 版移除员工脚本
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/remove_worker.py" "$@"
