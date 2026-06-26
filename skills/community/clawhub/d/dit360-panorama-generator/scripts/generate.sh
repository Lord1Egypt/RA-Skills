#!/bin/bash
# generate.sh - DiT360 全景图生成器入口脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPT="${1:-sunset over ocean beach}"
SEED="${2:-42}"
STEPS="${3:-50}"

echo "🎨 DiT360 全景图生成器"
echo "======================"
echo ""

# 检查 uv
if ! command -v uv &> /dev/null; then
    echo "❌ 请先安装 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# 安装依赖
echo "📦 检查依赖..."
uv pip install gradio_client --quiet 2>/dev/null || pip3 install gradio_client --quiet 2>/dev/null

echo ""
echo "🚀 开始生成..."
echo ""

# 运行生成器
uv run --with gradio_client python3 "$SCRIPT_DIR/generator.py" "$PROMPT" "$SEED" "$STEPS"

echo ""
echo "✅ 完成! 浏览器应该已经自动打开。"
echo "   如果没有，请手动访问: http://localhost:8899/viewer.html"
