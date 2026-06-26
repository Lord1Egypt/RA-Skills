#!/usr/bin/env bash
# apply_preset.sh —— 调用 Python 版团队预设脚本
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/apply_preset.py" "$@"
