#!/bin/bash
# Fun-ASR-Nano-2512 虚拟环境激活脚本

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$SKILL_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ 虚拟环境不存在: $VENV_DIR"
    echo "请运行: bash scripts/setup_venv.sh"
    return 1
fi

echo "🐍 激活 Python 3.12 虚拟环境..."
source "$VENV_DIR/bin/activate"

echo "✅ 虚拟环境已激活"
echo "   Python: $(python --version)"
echo "   路径: $VENV_DIR"
echo ""
echo "可用命令:"
echo "  python scripts/transcribe.py audio.wav"
echo "  python scripts/batch_transcribe.py ./audio/"
echo ""
