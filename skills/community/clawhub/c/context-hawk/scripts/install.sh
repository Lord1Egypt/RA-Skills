#!/bin/bash
# context-hawk 一键安装脚本
set -e

echo "Installing context-hawk..."

# 1. 检测 Python 版本
PYTHON=$(command -v python3.12 || command -v python3 || command -v python)
echo "Using Python: $PYTHON"

# 2. 安装核心依赖
$PYTHON -m pip install lancedb openai -q

# 3. 验证安装
$PYTHON -c "from hawk.memory import MemoryManager; print('hawk installed OK')"

# 4. 自动导入已有记忆（如有）
if [ -d "$HOME/.openclaw/memory" ]; then
    echo "发现记忆文件，自动导入..."
    $PYTHON -m hawk.markdown_importer --memory-dir "$HOME/.openclaw/memory" 2>/dev/null || true
fi

echo "context-hawk 安装完成！"
echo ""
echo "使用方式："
echo "  python3.12 -c \"from hawk.memory import MemoryManager; print('OK')\""
