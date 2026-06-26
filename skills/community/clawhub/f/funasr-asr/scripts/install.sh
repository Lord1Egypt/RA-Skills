#!/bin/bash
# FunASR ASR 安装脚本

set -e

echo "========================================"
echo "🎙️ FunASR 本地语音识别安装"
echo "========================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python 版本: $PYTHON_VERSION"

# 检查 pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip3，请先安装"
    exit 1
fi

echo ""
echo "正在安装 FunASR..."

# 安装 FunASR
pip3 install -U funasr onnxruntime

# 检查安装
if python3 -c "import funasr" 2>/dev/null; then
    echo ""
    echo "✅ FunASR 安装成功！"
    echo ""
    echo "📋 安装信息："
    python3 -c "import funasr; print(f'FunASR 版本: {funasr.__version__}')"
    echo ""
    echo "📝 使用方法："
    echo "  1. 发送语音消息到 OpenClaw"
    echo "  2. 系统会自动使用 FunASR 进行转录"
    echo "  3. 转录结果会自动转换为文字"
    echo ""
    echo "💡 首次使用时会自动下载模型文件（约 2GB）"
else
    echo "❌ FunASR 安装失败"
    exit 1
fi

echo ""
echo "========================================"
echo "安装完成"
echo "========================================"
