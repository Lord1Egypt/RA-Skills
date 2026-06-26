#!/bin/bash
# 安装 audio-translator 所需依赖 (安全版本)
# 不再使用 curl | bash

set -e

echo "========== 安装 audio-translator 依赖 =========="

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "检测到 macOS"
    
    # 检查并安装 Homebrew（安全方式）
    if ! command -v brew &> /dev/null; then
        echo "Homebrew 未安装，请手动安装："
        echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        echo ""
        echo "或者访问: https://brew.sh"
        exit 1
    fi
    
    # 检查并安装 FFmpeg
    if ! command -v ffmpeg &> /dev/null; then
        echo "安装 FFmpeg..."
        brew install ffmpeg
    else
        echo "FFmpeg 已安装"
    fi

elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "检测到 Linux"
    
    if ! command -v ffmpeg &> /dev/null; then
        echo "安装 FFmpeg..."
        sudo apt update
        sudo apt install -y ffmpeg
    else
        echo "FFmpeg 已安装"
    fi
else
    echo "不支持的操作系统: $OSTYPE"
    exit 1
fi

# 检查并安装 Python 3.11
PYTHON_BIN=""
for py in /usr/local/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/bin/python3.11 python3.11; do
    if command -v $py &> /dev/null; then
        PYTHON_BIN=$py
        break
    fi
done

if [[ -z "$PYTHON_BIN" ]]; then
    echo "Python 3.11 未安装"
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "运行: brew install python@3.11"
    fi
    exit 1
fi

# 安装 Python 依赖
echo ""
echo "安装 Python 依赖..."
cd "$(dirname "$0")"
$PYTHON_BIN -m pip install --user -r requirements.txt 2>/dev/null || \
$PYTHON_BIN -m pip install -r requirements.txt

echo ""
echo "========== 依赖安装完成！=========="
echo ""
echo "后续使用："
echo "  ./translate.sh <输入音频> <目标语言> [输出路径]"
echo ""
echo "示例："
echo "  ./translate.sh /Users/winer/录音.mp3 en"
echo "  ./translate.sh https://example.com/audio.m4a zh"
