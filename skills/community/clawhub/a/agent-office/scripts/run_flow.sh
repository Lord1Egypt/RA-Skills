#!/usr/bin/env bash
# run_flow.sh —— 调用 Python 版流转脚本
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/run_flow.py" "$@"
