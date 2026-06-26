#!/bin/bash
# 智能路由技能Shell包装脚本 v2.0

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/main.py"

# 检查Python脚本是否存在
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "错误: 找不到Python脚本 $PYTHON_SCRIPT"
    exit 1
fi

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "错误: 需要Python3"
    exit 1
fi

# 执行Python脚本
python3 "$PYTHON_SCRIPT" "$@"

# 返回Python脚本的退出码
exit $?