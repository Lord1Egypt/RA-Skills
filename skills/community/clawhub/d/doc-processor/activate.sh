#!/bin/bash
# 激活文档处理 Skill 的虚拟环境
# 虚拟环境统一存放在：~/.openclaw/workspace/.venvs/

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="$(basename "$SCRIPT_DIR")"
VENV_DIR="$HOME/.openclaw/workspace/.venvs/$SKILL_NAME"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ 虚拟环境不存在"
    echo "   路径：$VENV_DIR"
    echo ""
    echo "请先运行安装脚本:"
    echo "   cd $SCRIPT_DIR && ./setup.sh"
    return 1 2>/dev/null || exit 1
fi

source "$VENV_DIR/bin/activate"
echo "✅ 已激活 $SKILL_NAME 虚拟环境"
echo "   路径：$VENV_DIR"
echo "   Python: $(which python3)"
echo "   退出：deactivate"
