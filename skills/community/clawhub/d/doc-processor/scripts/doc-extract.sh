#!/bin/bash
# 提取文档数据
# 用法：doc-extract.sh <file_path> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
if [ -d "$SKILL_DIR/.venv" ]; then
    source "$SKILL_DIR/.venv/bin/activate"
fi

python3 "$SKILL_DIR/doc_processor.py" \
    --action extract \
    --input "$1" \
    --options "${2:-{}}" \
    --format json
