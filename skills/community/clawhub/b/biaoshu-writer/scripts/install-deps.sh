#!/bin/bash
# biaoshu-writer 依赖安装脚本
# 运行方式: bash install-deps.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "📦 开始安装 biaoshu-writer 依赖..."

# 1. 创建虚拟环境（隔离系统Python）
echo "🐍 创建虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "✅ 虚拟环境已存在，跳过创建"
else
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境创建成功"
fi

# 激活虚拟环境
source "$VENV_DIR/bin/activate"

# 2. 安装Python依赖
echo "📚 安装Python依赖..."
pip install --upgrade pip -q
pip install python-docx pdfplumber openpyxl PyPDF2 -q

# 3. 检查 SimSun 字体
FONT_PATH="$HOME/Library/Fonts/SimSun.ttf"
if [ -f "$FONT_PATH" ]; then
    echo "✅ SimSun 字体已安装"
else
    echo "⚠️ SimSun 字体未安装"
    echo ""
    echo "   请手动安装:"
    echo "   1. 从 Windows 系统复制 SimSun.ttf 到 ~/Library/Fonts/"
    echo "   2. 或从网上下载 SimSun.ttf"
    echo "   3. 验证: ls -lh ~/Library/Fonts/SimSun.ttf"
fi

echo ""
echo "✅ 依赖安装完成！"
echo ""
echo "激活虚拟环境命令:"
echo "  source $VENV_DIR/bin/activate"
echo ""
echo "使用脚本时加虚拟环境前缀:"
echo "  source $VENV_DIR/bin/activate"
echo "  python3 scripts/parse_bid_files.py <文件>"
echo "  python3 scripts/convert_to_word.py <输入.md> <输出.docx>"
echo ""
echo "后续步骤:"
echo "1. 将 biaoshu-writer 技能安装到 OpenClaw:"
echo "   openclaw skills install <skill路径>"
