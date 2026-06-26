#!/usr/bin/env bash
# add_worker.sh —— 调用 Python 版添加员工脚本
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/add_worker.py" "$@"
