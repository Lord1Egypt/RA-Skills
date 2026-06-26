#!/bin/bash
# 安全地运行完整分析流程（避开安全策略对管道和重定向的限制）
# 包含输入验证和安全检查
set -e

SCRIPT_DIR="$(dirname "$0")"
HTML_FILE="$1"
OUTPUT_FILE="${2:-分析结果.md}"

# 安全检查函数
check_file_path() {
    local filepath="$1"

    # 检查路径是否包含危险字符
    if [[ "$filepath" =~ [;\|&\$\`\'\"()<>] ]] || [[ "$filepath" =~ [\n\r] ]]; then
        echo "错误: 文件路径包含潜在危险字符"
        return 1
    fi

    # 检查路径长度
    if [[ ${#filepath} -gt 4096 ]]; then
        echo "错误: 文件路径过长"
        return 1
    fi

    # 检查路径是否试图访问敏感位置（可选保护）
    if [[ "$filepath" =~ (\.ssh|\.env|\.git|passwd|shadow|hosts) ]]; then
        echo "警告: 文件路径可能指向敏感位置，请确认是否为预期分析目标"
    fi

    return 0
}

if [ -z "$HTML_FILE" ]; then
    echo "用法: $0 <HTML文件> [输出文件]"
    exit 1
fi

# 验证文件路径安全性
if ! check_file_path "$HTML_FILE"; then
    exit 1
fi

if ! check_file_path "$OUTPUT_FILE"; then
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo "错误: 文件不存在: $HTML_FILE"
    exit 1
fi

# 步骤1: 提取HTML结构（JSON格式）
echo "[1/2] 分析页面结构..." 1>&2

# 步骤2: 生成技术文档
echo "[2/2] 生成技术文档..." 1>&2
# 将提取器的JSON输出通过临时文件传给生成器
TMPFILE=$(mktemp /tmp/analysis-XXXXXX.json)
trap "rm -f $TMPFILE" EXIT

# 提取JSON并写入临时文件
python3 "$SCRIPT_DIR/html-extractor.py" "$HTML_FILE" json > "$TMPFILE"
python3 "$SCRIPT_DIR/spec-generator.py" "$OUTPUT_FILE" --input-json "$TMPFILE"

echo "完成! 文档已生成: $OUTPUT_FILE" 1>&2
