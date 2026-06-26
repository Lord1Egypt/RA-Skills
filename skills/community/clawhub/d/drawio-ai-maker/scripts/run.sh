#!/bin/bash
# drawio-generator 标准执行脚本
# 用法: ./run.sh "图表标题" '{"title":"...","nodes":[...],"edges":[...]}' [flowchart|sequence|...]
#
# 输出到: /Users/owen/Desktop/drawio-generator/

TITLE="${1:-未命名图表}"
JSON="${2:-}"
TYPE="${3:-flowchart}"
OUTPUT_DIR="/Users/owen/Desktop/drawio-generator"

if [ -z "$JSON" ]; then
    echo "用法: $0 \"图表标题\" '{\"title\":\"...\",\"nodes\":[...]}' [类型]"
    exit 1
fi

cd "$(dirname "$0")"
python3 __main__.py \
    --title "$TITLE" \
    --type "$TYPE" \
    --from-llm "$JSON" \
    --output-dir "$OUTPUT_DIR"
