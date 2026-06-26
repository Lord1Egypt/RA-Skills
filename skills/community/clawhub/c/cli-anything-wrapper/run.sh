#!/bin/bash
# CLI-Anything Wrapper 快捷入口
# 用法: ./run.sh [参数]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/scripts/run.py" "$@"
