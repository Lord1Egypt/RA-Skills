#!/bin/bash
# auto-subtitle 安装脚本

set -e

echo "🎬 正在安装 auto-subtitle..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 python3，请先安装 Python 3.7+"
    exit 1
fi

echo "✅ Python 检查通过"

# 检查 ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  警告：未找到 ffmpeg"
    echo "   Ubuntu/Debian: sudo apt install ffmpeg"
    echo "   macOS: brew install ffmpeg"
fi

# 安装依赖
echo "📦 正在安装 openai 和 pydub..."
pip install openai pydub

echo ""
echo "🎉 auto-subtitle 安装完成！"
echo ""
echo "使用前请设置环境变量："
echo "  export OPENAI_API_KEY='your-api-key-here'"
echo ""
echo "使用方法："
echo "  python source/auto_subtitle.py --help"
echo ""
echo "快速开始："
echo "  # 为视频生成中文字幕"
echo "  python source/auto_subtitle.py --language zh"
echo ""
echo "  # 翻译为英文"
echo "  python source/auto_subtitle.py --task translate --language en"
echo ""
