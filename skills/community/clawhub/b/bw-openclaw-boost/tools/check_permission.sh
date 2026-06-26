#!/bin/bash
# 权限检查脚本
# 用法: check_permission.sh <tool> <command>
# 返回: 0=允许, 1=拒绝, 2=询问

TOOL="$1"
COMMAND="$2"
TOOLS_DIR="$(dirname "$0")"

if [ -z "$TOOL" ]; then
    echo "Usage: check_permission.sh <tool> <command>"
    exit 2
fi

# 调用 Python 权限管理器
RESULT=$(python3 "$TOOLS_DIR/permission_manager.py" check "$TOOL" "$COMMAND" 2>/dev/null)

case "$RESULT" in
    *"ALLOW"*)
        exit 0
        ;;
    *"DENY"*)
        echo "🚫 命令被拒绝: $COMMAND"
        exit 1
        ;;
    *)
        # ASK 或未知
        exit 2
        ;;
esac
