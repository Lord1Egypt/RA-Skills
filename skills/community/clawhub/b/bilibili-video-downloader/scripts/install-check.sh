#!/bin/bash
# install-check.sh - 检查依赖是否安装

set -e

echo "🔍 检查 Bilibili Video Downloader 依赖..."
echo ""

# 检查 Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python: $PYTHON_VERSION"
else
    echo "❌ Python3 未安装"
    echo "   请访问 https://www.python.org/downloads/ 安装"
    exit 1
fi

# 检查 yt-dlp
if command -v yt-dlp &> /dev/null; then
    YTDLP_VERSION=$(yt-dlp --version)
    echo "✅ yt-dlp: $YTDLP_VERSION"
else
    echo "⚠️  yt-dlp 未安装"
    echo "   正在安装..."
    pip3 install yt-dlp
    echo "✅ yt-dlp 安装完成"
fi

# 检查 ffmpeg
if command -v ffmpeg &> /dev/null; then
    FFMPEG_VERSION=$(ffmpeg -version | head -n1)
    echo "✅ ffmpeg: $FFMPEG_VERSION"
else
    echo "⚠️  ffmpeg 未安装"
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu: sudo apt install ffmpeg"
    echo "   Windows: 下载 https://ffmpeg.org/download.html"
fi

# 检查 BBDown (可选)
if command -v BBDown &> /dev/null; then
    BBDOWN_VERSION=$(BBDown --version 2>/dev/null || echo "installed")
    echo "✅ BBDown: $BBDOWN_VERSION (可选，已安装)"
else
    echo "ℹ️  BBDown 未安装 (可选)"
    echo "   如需高级功能，请从 https://github.com/nilaoda/BBDown/releases 下载"
fi

echo ""
echo "🎉 依赖检查完成！"
