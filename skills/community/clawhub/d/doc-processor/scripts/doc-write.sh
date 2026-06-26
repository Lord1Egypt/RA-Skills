#!/bin/bash
# 写入文档
# 用法：echo '{"title": "标题", "paragraphs": ["内容"]}' | doc-write.sh -o output.docx

OUTPUT_PATH=""
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -o|--output) OUTPUT_PATH="$2"; shift ;;
        *) echo "未知参数：$1"; exit 1 ;;
    esac
    shift
done

if [ -z "$OUTPUT_PATH" ]; then
    echo "❌ 需要指定输出文件：-o <file>"
    exit 1
fi

CONTENT="$(cat)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
if [ -d "$SKILL_DIR/.venv" ]; then
    source "$SKILL_DIR/.venv/bin/activate"
fi

python3 "$SKILL_DIR/doc_processor.py" \
    --action write \
    --output "$OUTPUT_PATH" \
    --content "$CONTENT" \
    --format json
