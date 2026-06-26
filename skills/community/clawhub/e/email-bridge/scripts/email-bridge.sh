#!/bin/bash
# Email Bridge CLI wrapper
# This script ensures email-bridge is installed and forwards commands

set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VENV_DIR="$SKILL_DIR/.venv"

# Check if installed
if [ ! -d "$VENV_DIR" ]; then
    echo "📧 Email Bridge 未安装，正在安装..."
    cd "$SKILL_DIR"
    
    if command -v uv &> /dev/null; then
        uv sync
    else
        python3 -m venv .venv
        source .venv/bin/activate
        pip install -e .
    fi
    
    echo "✅ 安装完成"
fi

# Activate venv and run command
source "$VENV_DIR/bin/activate"
email-bridge "$@"