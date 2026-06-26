#!/usr/bin/env bash
# claude-kill.sh — 终止 Claude Code 任务
#
# 用法: claude-kill.sh <task-id>

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/clawclau-lib.sh"

cc_require tmux jq

if [[ $# -lt 1 ]]; then
    echo "Usage: claude-kill.sh <task-id>" >&2; exit 1
fi

TASK_ID="$1"
SESSION=$(cc_tmux_session "$TASK_ID")

if tmux has-session -t "$SESSION" 2>/dev/null; then
    tmux kill-session -t "$SESSION"
    echo "已终止 tmux session '$SESSION'"
else
    echo "Session '$SESSION' 不存在（任务可能已完成）"
fi

if [[ -f "$CC_REGISTRY" ]]; then
    NOW=$(cc_now_ms)
    cc_task_update "$TASK_ID" \
        "{\"status\":\"killed\",\"killedAt\":$NOW}"
    echo "已更新注册表状态为 killed"
fi
