#!/bin/bash
# 获取文档信息
# 用法：doc-info.sh <file_path>

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
if [ -d "$SKILL_DIR/.venv" ]; then
    source "$SKILL_DIR/.venv/bin/activate"
fi

python3 "$SKILL_DIR/doc_processor.py" \
    --action info \
    --input "$1" \
    --format json
