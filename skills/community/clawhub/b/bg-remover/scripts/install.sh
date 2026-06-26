#!/bin/bash
# 安装 bg-remover 依赖
set -e

echo "🔧 安装 bg-remover 依赖..."

# 检查 pip/pip3
if command -v pip3 &>/dev/null; then
    PIP=pip3
elif command -v pip &>/dev/null; then
    PIP=pip
else
    echo "❌ 未找到 pip，请先安装 Python3"
    exit 1
fi

$PIP install rembg Pillow numpy onnxruntime --quiet
echo "✅ 依赖安装完成"
