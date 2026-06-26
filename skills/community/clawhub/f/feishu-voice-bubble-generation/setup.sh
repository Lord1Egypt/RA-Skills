#!/bin/bash
# setup.sh - 安装 feishu-voice-bubble 技能所需的依赖
# OpenClaw 在安装此技能时会自动执行此脚本

set -e

echo "=== feishu-voice-bubble 依赖安装 ==="

# 安装 edge-tts
echo "[1/2] 安装 edge-tts..."
if command -v pip3 &>/dev/null; then
    pip3 install --quiet edge-tts
elif command -v pip &>/dev/null; then
    pip install --quiet edge-tts
else
    echo "错误：未找到 pip，请手动安装 Python 和 pip 后重试。"
    exit 1
fi
echo "✓ edge-tts 安装完成"

# 安装 ffmpeg
echo "[2/2] 安装 ffmpeg..."
if command -v ffmpeg &>/dev/null; then
    echo "✓ ffmpeg 已安装，跳过"
else
    if command -v apt-get &>/dev/null; then
        apt-get install -y -q ffmpeg
    elif command -v brew &>/dev/null; then
        brew install ffmpeg
    elif command -v yum &>/dev/null; then
        yum install -y ffmpeg
    else
        echo "错误：无法自动安装 ffmpeg，请手动安装（版本 4.4.2+）。"
        exit 1
    fi
    echo "✓ ffmpeg 安装完成"
fi

echo ""
echo "=== 所有依赖安装完成，feishu-voice-bubble 技能已就绪 ==="
