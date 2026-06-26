#!/bin/bash
#
# OpenClaw 技能包装器
# 用于调用实际的执行脚本
#

set -e  # 遇到错误立即退出

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 执行脚本路径
EXECUTE_SCRIPT="$SCRIPT_DIR/execute.sh"

# ==================================================
# 依赖检查
# ==================================================

# 检查 Bash 是否可用
if ! command -v bash &> /dev/null; then
    echo '{"success": false, "error": "BashNotFound", "message": "未找到 Bash。请安装 Bash >= 4.0"}' >&2
    exit 1
fi

# 检查 Bash 版本
BASH_VERSION_MAJOR=${BASH_VERSINFO[0]}
BASH_VERSION_MINOR=${BASH_VERSINFO[1]}
if [ "$BASH_VERSION_MAJOR" -lt 4 ]; then
    echo "{\"success\": false, \"error\": \"BashVersionTooOld\", \"message\": \"需要 Bash >= 4.0，当前版本：$BASH_VERSION\"}" >&2
    exit 1
fi

# ==================================================
# 文件检查
# ==================================================

if [ ! -f "$EXECUTE_SCRIPT" ]; then
    echo "{\"success\": false, \"error\": \"ExecuteScriptNotFound\", \"message\": \"未找到执行脚本：$EXECUTE_SCRIPT\"}" >&2
    exit 1
fi

# 检查执行权限
if [ ! -x "$EXECUTE_SCRIPT" ]; then
    chmod +x "$EXECUTE_SCRIPT"
fi

# ==================================================
# 调用执行脚本
# ==================================================

# 将输入传递给执行脚本
if [ $# -eq 0 ]; then
    # 没有参数，从 STDIN 读取
    bash "$EXECUTE_SCRIPT"
else
    # 有参数，传递第一个参数作为输入
    bash "$EXECUTE_SCRIPT" "$1"
fi

# 传递退出码
exit $?
