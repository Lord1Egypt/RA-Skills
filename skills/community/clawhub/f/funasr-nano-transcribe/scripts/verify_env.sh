#!/bin/bash
# Fun-ASR-Nano-2512 环境验证脚本

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "========================================"
echo "Fun-ASR-Nano-2512 环境验证"
echo "========================================"
echo ""

# 检查虚拟环境
echo "📁 检查虚拟环境..."
if [ -d "$SKILL_DIR/.venv" ]; then
    echo "✅ 虚拟环境存在"
    source "$SKILL_DIR/.venv/bin/activate"
    echo "✅ Python 版本: $(python --version)"
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi

echo ""
echo "📦 检查依赖..."

# 检查关键包
PACKAGES=("torch" "torchaudio" "funasr" "modelscope" "numpy" "loguru")
for pkg in "${PACKAGES[@]}"; do
    if pip show "$pkg" > /dev/null 2>&1; then
        version=$(pip show "$pkg" | grep Version | awk '{print $2}')
        echo "✅ $pkg: $version"
    else
        echo "❌ $pkg: 未安装"
    fi
done

echo ""
echo "🔍 检查模型文件..."
MODEL_DIR="$SKILL_DIR/models/Fun-ASR-Nano-2512"
if [ -d "$MODEL_DIR" ]; then
    echo "✅ 模型目录存在: $MODEL_DIR"
    file_count=$(find "$MODEL_DIR" -type f | wc -l)
    echo "   文件数量: $file_count"
else
    echo "❌ 模型目录不存在: $MODEL_DIR"
fi

echo ""
echo "========================================"
echo "✅ 环境验证完成"
echo "========================================"
