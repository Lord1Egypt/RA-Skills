#!/bin/bash
# Fun-ASR-Nano-2512 虚拟环境安装脚本

set -e

echo "========================================"
echo "Fun-ASR-Nano-2512 环境配置脚本"
echo "========================================"

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SKILL_DIR/.venv"

echo ""
echo "📁 技能目录: $SKILL_DIR"
echo "🐍 虚拟环境: $VENV_DIR"

# 检查 Python 版本
echo ""
echo "🔍 检查 Python 版本..."
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python 版本过低: $PYTHON_VERSION"
    echo "   需要 Python >= 3.8"
    exit 1
fi

echo "✅ Python 版本: $PYTHON_VERSION"

# 创建虚拟环境
echo ""
echo "📦 创建虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  虚拟环境已存在，是否重建? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm -rf "$VENV_DIR"
        python3 -m venv "$VENV_DIR"
        echo "✅ 虚拟环境已重建"
    else
        echo "⏭️  跳过创建，使用现有环境"
    fi
else
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境已创建"
fi

# 激活虚拟环境
echo ""
echo "🔌 激活虚拟环境..."
source "$VENV_DIR/bin/activate"

# 升级 pip
echo ""
echo "⬆️  升级 pip..."
pip install --upgrade pip

# 安装 PyTorch (CPU 版本，如需 GPU 请手动修改)
echo ""
echo "🔥 安装 PyTorch..."
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# 安装 FunASR 和 ModelScope
echo ""
echo "🎤 安装 FunASR 和 ModelScope..."
pip install funasr modelscope

# 安装其他依赖
echo ""
echo "📚 安装其他依赖..."
pip install numpy loguru

echo ""
echo "========================================"
echo "✅ 安装完成!"
echo "========================================"
echo ""
echo "使用方法:"
echo "  1. 激活虚拟环境:"
echo "     source $VENV_DIR/bin/activate"
echo ""
echo "  2. 运行转写:"
echo "     python3 scripts/transcribe.py audio.wav"
echo ""
echo "  3. 退出虚拟环境:"
echo "     deactivate"
echo ""
