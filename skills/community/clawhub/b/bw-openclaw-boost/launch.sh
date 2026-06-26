#!/bin/bash
# bw-openclaw-boost 统一启动器
# 用法: ./launch.sh <command>

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS_DIR="$SCRIPT_DIR/tools"
PYTHON="${PYTHON:-python3}"

show_help() {
    echo "📦 bw-openclaw-boost 工具集"
    echo ""
    echo "用法: ./launch.sh <command>"
    echo ""
    echo "可用命令:"
    echo "  cost             - 成本追踪"
    echo "  memory           - 记忆检索"
    echo "  compaction       - 压缩管理"
    echo "  tools            - 工具追踪"
    echo "  permission       - 权限管理"
    echo "  coordinator      - Agent协调（仅本地记录）"
    echo "  dream            - 自动整理"
    echo "  slash             - 斜杠命令"
    echo "  budget           - Token预算"
    echo "  flags            - 功能开关"
    echo "  all-status       - 所有状态"
    echo "  help             - 显示帮助"
    echo ""
}

case "$1" in
    cost)
        $PYTHON "$TOOLS_DIR/cost_tracker.py"
        ;;
    memory)
        $PYTHON "$TOOLS_DIR/memory_relevance.py" scan
        ;;
    compaction)
        $PYTHON "$TOOLS_DIR/compaction_manager.py" status
        ;;
    tools)
        $PYTHON "$TOOLS_DIR/tool_tracker.py" summary
        ;;
    permission)
        $PYTHON "$TOOLS_DIR/permission_manager.py" list
        ;;
    coordinator)
        $PYTHON "$TOOLS_DIR/coordinator.py" list
        ;;
    dream)
        $PYTHON "$TOOLS_DIR/dream_consolidation.py" status
        ;;
    slash)
        $PYTHON "$TOOLS_DIR/slash_commands.py" help
        ;;
    budget)
        $PYTHON "$TOOLS_DIR/token_budget.py" status
        ;;
    flags)
        $PYTHON "$TOOLS_DIR/feature_flags.py" list
        ;;
    all-status)
        echo "=== 成本追踪 ===" && $PYTHON "$TOOLS_DIR/cost_tracker.py" | head -10
        echo ""
        echo "=== Token预算 ===" && $PYOLS_DIR/token_budget.py" status
        echo ""
        echo "=== 功能开关 ===" && $PYTHON "$TOOLS_DIR/feature_flags.py" list
        ;;
    help)
        show_help
        ;;
    *)
        show_help
        ;;
esac
