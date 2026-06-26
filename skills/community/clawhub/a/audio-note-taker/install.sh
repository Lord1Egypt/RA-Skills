#!/bin/bash
# audio-note-taker 安装脚本

set -e

echo "🎙️ 正在安装 audio-note-taker..."

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要 Python 3.7+"
    exit 1
fi

# 安装 Python 依赖
echo "📦 安装 Python 依赖..."
pip3 install --user openai>=1.0.0

# 检查 ffmpeg（可选，用于音频格式转换）
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  建议安装 ffmpeg 以支持更多音频格式转换"
    echo "   运行: apt install -y ffmpeg"
fi

# 检查 OPENAI_API_KEY
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  未设置 OPENAI_API_KEY 环境变量"
    echo "   请设置: export OPENAI_API_KEY='your-key'"
    echo "   或配置: ~/.openclaw/openclaw.json"
fi

echo "✅ audio-note-taker 安装完成！"
echo ""
echo "快速开始："
echo "  audio-note-taker /path/to/audio.mp3 --language zh"
echo ""
echo "查看文档："
echo "  cat SKILL.md"
