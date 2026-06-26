#!/bin/bash
# 测试脚本：验证 Flomo 转换功能

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
EXAMPLE_HTML="$PROJECT_DIR/examples/sample-flomo-export.html"
OUTPUT_DIR="$PROJECT_DIR/test-output"

echo "🧪 开始测试 Flomo to Obsidian 转换..."
echo ""

# 清理旧的测试输出
if [ -d "$OUTPUT_DIR" ]; then
    echo "清理旧的测试输出..."
    rm -rf "$OUTPUT_DIR"
fi

# 检查依赖
echo "检查 Python 依赖..."
python3 -c "import bs4, markdownify" 2>/dev/null || {
    echo "❌ 缺少依赖库，正在安装..."
    pip3 install -q beautifulsoup4 markdownify
}

echo "✅ 依赖检查完成"
echo ""

# 测试 1: By-Date 模式
echo "测试 1: By-Date 模式"
python3 "$SCRIPT_DIR/convert.py" \
    --input "$EXAMPLE_HTML" \
    --output "$OUTPUT_DIR/by-date" \
    --mode by-date \
    --verbose

echo ""
echo "输出文件："
ls -lh "$OUTPUT_DIR/by-date"
echo ""

# 测试 2: Individual 模式
echo "测试 2: Individual 模式"
python3 "$SCRIPT_DIR/convert.py" \
    --input "$EXAMPLE_HTML" \
    --output "$OUTPUT_DIR/individual" \
    --mode individual \
    --preserve-time

echo ""
echo "输出文件："
ls -lh "$OUTPUT_DIR/individual"
echo ""

# 测试 3: Single 模式
echo "测试 3: Single 模式"
python3 "$SCRIPT_DIR/convert.py" \
    --input "$EXAMPLE_HTML" \
    --output "$OUTPUT_DIR/single" \
    --mode single

echo ""
echo "输出文件："
ls -lh "$OUTPUT_DIR/single"
echo ""

# 测试 4: 带标签前缀
echo "测试 4: 带标签前缀"
python3 "$SCRIPT_DIR/convert.py" \
    --input "$EXAMPLE_HTML" \
    --output "$OUTPUT_DIR/with-prefix" \
    --mode by-date \
    --tag-prefix "imported/flomo/"

echo ""

# 显示示例文件内容
echo "========================================="
echo "示例输出 (By-Date 模式):"
echo "========================================="
head -n 30 "$OUTPUT_DIR/by-date/2024-03-15.md"
echo ""
echo "... (更多内容请查看文件)"
echo ""

echo "✅ 所有测试完成！"
echo ""
echo "测试输出目录: $OUTPUT_DIR"
echo "你可以将这些文件复制到 Obsidian vault 中查看效果。"
