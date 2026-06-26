#!/usr/bin/env bash
# claude-steer.sh — 向运行中的 Claude Code 发送纠偏消息
#
# 用法: claude-steer.sh <task-id> "<message>"
#
# 注意：
#   - 推荐用于 --steerable 模式（交互式）的任务
#   - Print 模式（claude -p）非交互，steer 无效
#     建议用 claude-kill.sh + claude-spawn.sh 以改进 prompt 重新派发

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/clawclau-lib.sh"

cc_require tmux jq

if [[ $# -lt 2 ]]; then
    echo "Usage: claude-steer.sh <task-id> \"<message>\"" >&2; exit 1
fi

TASK_ID="$1"
MESSAGE="$2"
SESSION=$(cc_tmux_session "$TASK_ID")

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "ERROR: tmux session '$SESSION' 不存在（任务未运行？）" >&2; exit 1
fi

# 检查模式，print 模式给出警告
if [[ -f "$CC_REGISTRY" ]]; then
    MODE=$(cc_task_get "$TASK_ID" "mode")
    if [[ "$MODE" == "print" ]]; then
        echo "WARNING: 任务 '$TASK_ID' 是 print 模式（非交互式），steer 可能无效" >&2
        echo "  建议: claude-kill.sh $TASK_ID 后以改进 prompt 重新派发" >&2
        echo ""
    fi
fi

# 发送消息到 tmux session
tmux send-keys -t "$SESSION" "$MESSAGE" Enter

# 记录到 steerLog
[[ -f "$CC_REGISTRY" ]] && cc_task_steer_log "$TASK_ID" "$MESSAGE"

echo "已发送消息到 '$SESSION'"
echo "  消息: $MESSAGE"
