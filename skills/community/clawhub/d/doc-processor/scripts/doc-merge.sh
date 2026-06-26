#!/bin/bash
# 合并多个文档
# 用法：doc-merge.sh file1.docx file2.docx -o merged.docx

OUTPUT=""
INPUTS=()

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -o|--output) OUTPUT="$2"; shift ;;
        *) INPUTS+=("$1") ;;
    esac
    shift
done

if [ ${#INPUTS[@]} -lt 2 ]; then
    echo "❌ 需要至少 2 个输入文件"
    echo "   用法：doc-merge.sh file1.docx file2.docx -o merged.docx"
    exit 1
fi

if [ -z "$OUTPUT" ]; then
    echo "❌ 需要指定输出文件：-o <file>"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# 激活虚拟环境
if [ -d "$SKILL_DIR/.venv" ]; then
    source "$SKILL_DIR/.venv/bin/activate"
fi

python3 "$SKILL_DIR/doc_processor.py" \
    --action merge \
    --input "${INPUTS[@]}" \
    --output "$OUTPUT" \
    --format json
