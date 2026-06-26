#!/bin/bash
# DolphinDB 环境检查统一入口
# 所有子技能都可以通过此脚本检查和加载环境

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行环境检测
echo "🔍 检查 DolphinDB Python 环境..."
"$SCRIPT_DIR/init_dolphindb_env.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 环境检查通过"
    echo ""
    echo "📌 使用方法:"
    echo "  source $SCRIPT_DIR/dolphin_wrapper.sh"
    echo "  或"
    echo "  source $SCRIPT_DIR/dolphin_global.sh  # 可在任何位置调用"
    exit 0
else
    echo ""
    echo "❌ 环境检查失败"
    echo ""
    echo "💡 请运行以下命令安装:"
    echo "  $SCRIPT_DIR/init_dolphindb_env.py"
    exit 1
fi
