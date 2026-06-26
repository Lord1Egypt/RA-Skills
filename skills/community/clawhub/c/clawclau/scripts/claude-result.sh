#!/usr/bin/env bash
# claude-result.sh — 获取任务结果（从日志提取可读文本）
#
# 用法:
#   claude-result.sh <task-id>        # 提取可读文本
#   claude-result.sh <task-id> --raw  # 输出原始日志

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/clawclau-lib.sh"

cc_require jq

if [[ $# -lt 1 ]]; then
    echo "Usage: claude-result.sh <task-id> [--raw]" >&2
    exit 1
fi

TASK_ID="$1"
RAW="${2:-}"

if [[ ! -f "$CC_REGISTRY" ]]; then
    echo "ERROR: 注册表不存在" >&2; exit 1
fi

if ! cc_task_exists "$TASK_ID"; then
    echo "ERROR: 任务 '$TASK_ID' 不存在" >&2; exit 1
fi

LOG_FILE=$(cc_task_get "$TASK_ID" "log")
STATUS=$(cc_task_get "$TASK_ID" "status")

# 任务仍在运行：抓取 tmux 当前输出
SESSION=$(cc_tmux_session "$TASK_ID")
if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "=== 任务 $TASK_ID 正在运行（实时输出）==="
    tmux capture-pane -t "$SESSION" -p -S - 2>/dev/null || echo "(无输出)"
    exit 0
fi

if [[ ! -f "$LOG_FILE" ]]; then
    echo "ERROR: 日志文件不存在: $LOG_FILE" >&2
    exit 1
fi

echo "=== 任务 $TASK_ID [$STATUS] ==="

if [[ "$RAW" == "--raw" ]]; then
    cat "$LOG_FILE"
else
    TEXT=$(cc_extract_text "$LOG_FILE" 8000)
    if [[ -n "$TEXT" ]]; then
        echo "$TEXT"
    else
        echo "(日志存在但无可提取文本，使用 --raw 查看原始 stream-json)"
        echo ""
        echo "--- 原始日志前 50 行 ---"
        head -50 "$LOG_FILE"
    fi
fi
