#!/bin/bash
# 快速报表生成脚本 - shell 包装

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

python3 "$PROJECT_ROOT/scripts/generator.py" "$@"
