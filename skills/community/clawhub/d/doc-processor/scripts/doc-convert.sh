#!/bin/bash
# 转换文档格式
# 用法：doc-convert.sh <input> <output>

INPUT="$1"
OUTPUT="$2"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "❌ 需要指定输入和输出文件"
    echo "   用法：doc-convert.sh <input> <output>"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
if [ -d "$SKILL_DIR/.venv" ]; then
    source "$SKILL_DIR/.venv/bin/activate"
fi

python3 "$SKILL_DIR/doc_processor.py" \
    --action convert \
    --input "$INPUT" \
    --output "$OUTPUT" \
    --format json
