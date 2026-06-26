#!/usr/bin/env bash
# claude-monitor.sh — 批量检查所有任务，更新状态，发送通知
#
# 用法: claude-monitor.sh
# 建议通过 cron 每 10 分钟运行一次:
#   */10 * * * * /Users/yjj/.openclaw/workspace/scripts/claude-monitor.sh >> /tmp/clawclau-monitor.log 2>&1
#
# 功能：
# - 检查所有 running 任务的 tmux session 是否存活
# - session 结束后更新状态（done/failed）并通知小八
# - 检查超时，超时后终止 session 并通知
# - 作为后台 completion detector 的安全兜底

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/clawclau-lib.sh"

export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.openclaw/bin:$PATH"

cc_require tmux jq

TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
echo "[$TIMESTAMP] claude-monitor 开始检查..."

if [[ ! -f "$CC_REGISTRY" ]]; then
    echo "注册表不存在，跳过。"
    exit 0
fi

# 获取所有 running 状态的任务
RUNNING_TASKS=$(jq -r '.[] | select(.status == "running") | .id' \
    "$CC_REGISTRY" 2>/dev/null || echo "")

if [[ -z "$RUNNING_TASKS" ]]; then
    echo "无运行中任务，退出。"
    exit 0
fi

NOTIFIED=0

for TASK_ID in $RUNNING_TASKS; do
    SESSION=$(cc_tmux_session "$TASK_ID")

    if tmux has-session -t "$SESSION" 2>/dev/null; then
        # Session 仍存活，检查超时
        STARTED=$(cc_task_get "$TASK_ID" "startedAt")
        TIMEOUT=$(cc_task_get "$TASK_ID" "timeout")
        TIMEOUT="${TIMEOUT:-600}"
        NOW=$(date +%s000)
        ELAPSED=$(( (NOW - STARTED) / 1000 ))

        if [[ "$ELAPSED" -gt "$TIMEOUT" ]]; then
            echo "  TIMEOUT: $TASK_ID (已运行 ${ELAPSED}s > 超时 ${TIMEOUT}s)"
            tmux kill-session -t "$SESSION" 2>/dev/null || true
            sleep 1
            cc_task_update "$TASK_ID" \
                "{\"status\":\"timeout\",\"completedAt\":$NOW}"
            cc_notify "[monitor] 任务 $TASK_ID 超时（${TIMEOUT}s），已终止"
            NOTIFIED=$((NOTIFIED + 1))
        else
            echo "  RUNNING: $TASK_ID (已运行 ${ELAPSED}s / ${TIMEOUT}s)"
        fi
    else
        # Session 已结束，更新状态
        LOG_FILE=$(cc_task_get "$TASK_ID" "log")
        NOW=$(date +%s000)

        if [[ -s "$LOG_FILE" ]]; then
            STATUS="done"
        else
            STATUS="failed"
        fi

        cc_task_update "$TASK_ID" \
            "{\"status\":\"$STATUS\",\"completedAt\":$NOW}"

        SNIPPET=$(cc_extract_text "$LOG_FILE" 300)

        if [[ "$STATUS" == "done" ]]; then
            MSG="[monitor][完成] 任务 $TASK_ID"
            [[ -n "$SNIPPET" ]] && MSG+=$'\n'"摘要: ${SNIPPET:0:200}"
            cc_notify "$MSG"
        else
            cc_notify "[monitor][失败] 任务 $TASK_ID（日志为空）"
        fi

        NOTIFIED=$((NOTIFIED + 1))
        echo "  COMPLETED: $TASK_ID [$STATUS]"
    fi
done

echo "Monitor 完成，共处理 $NOTIFIED 个任务状态变更。"
