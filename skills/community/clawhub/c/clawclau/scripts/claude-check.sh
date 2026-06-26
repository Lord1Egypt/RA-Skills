#!/usr/bin/env bash
# claude-check.sh — 检查 Claude Code 任务状态（确定性，不消耗 token）
#
# 用法:
#   claude-check.sh              # 列出所有任务
#   claude-check.sh <task-id>    # 查看单个任务详情

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/clawclau-lib.sh"

cc_require tmux jq

if [[ ! -f "$CC_REGISTRY" ]]; then
    echo "暂无任务注册表。先运行 claude-spawn.sh。"
    exit 0
fi

# ── 单个任务 ───────────────────────────────────────────────────────────────
if [[ $# -ge 1 ]]; then
    TASK_ID="$1"

    if ! cc_task_exists "$TASK_ID"; then
        echo "ERROR: 任务 '$TASK_ID' 不在注册表中" >&2; exit 1
    fi

    TASK_JSON=$(jq -r --arg id "$TASK_ID" '.[] | select(.id == $id)' "$CC_REGISTRY")
    SESSION=$(cc_tmux_session "$TASK_ID")

    # tmux 存活是 running 的最终判据
    STATUS=$(echo "$TASK_JSON" | jq -r '.status')
    tmux has-session -t "$SESSION" 2>/dev/null && STATUS="running"

    MODE=$(echo "$TASK_JSON"     | jq -r '.mode // "print"')
    PROMPT=$(echo "$TASK_JSON"   | jq -r '.prompt // ""')
    WORKDIR=$(echo "$TASK_JSON"  | jq -r '.workdir // ""')
    STARTED=$(echo "$TASK_JSON"  | jq -r '.startedAt // 0')
    TIMEOUT=$(echo "$TASK_JSON"  | jq -r '.timeout // 600')
    LOG=$(echo "$TASK_JSON"      | jq -r '.log // ""')
    RETRIES=$(echo "$TASK_JSON"  | jq -r '.retryCount // 0')
    MAX_R=$(echo "$TASK_JSON"    | jq -r '.maxRetries // 3')
    PARENT=$(echo "$TASK_JSON"   | jq -r '.parentTaskId // ""')
    INTERVAL=$(echo "$TASK_JSON" | jq -r '.interval // 0')

    START_HUMAN=$(date -r "$((STARTED / 1000))" "+%Y-%m-%d %H:%M:%S" 2>/dev/null \
        || echo "$STARTED")

    echo "══════════════════════════════════════"
    echo "任务:     $TASK_ID"
    echo "状态:     $STATUS"
    echo "模式:     $MODE"
    echo "Session:  $SESSION"
    echo "开始:     $START_HUMAN"
    echo "超时:     ${TIMEOUT}s"
    echo "重试:     $RETRIES / $MAX_R"
    echo "进度汇报: $([ "$INTERVAL" -gt 0 ] && echo "每 ${INTERVAL}s" || echo "关闭")"
    [[ -n "$PARENT" && "$PARENT" != "null" ]] && echo "父任务:   $PARENT"
    echo "工作目录: $WORKDIR"
    echo "日志:     $LOG"
    echo "Prompt:   ${PROMPT:0:120}..."
    echo ""

    if [[ "$STATUS" == "running" ]]; then
        echo "── 实时输出 (tmux) ─────────────────────"
        tmux capture-pane -t "$SESSION" -p 2>/dev/null | tail -15 || echo "(空)"
    elif [[ -n "$LOG" && -f "$LOG" ]]; then
        echo "── 结果摘要 ────────────────────────────"
        TEXT=$(cc_extract_text "$LOG" 1000)
        if [[ -n "$TEXT" ]]; then
            echo "$TEXT"
        else
            echo "(日志存在但无可提取文本，用 claude-result.sh --raw 查看原始日志)"
        fi
    fi

    # steer 历史
    STEER_COUNT=$(echo "$TASK_JSON" | jq '.steerLog | length' 2>/dev/null || echo 0)
    if [[ "$STEER_COUNT" -gt 0 ]]; then
        echo ""
        echo "── Steer 历史 ($STEER_COUNT 条) ──────────"
        echo "$TASK_JSON" | jq -r '.steerLog[] | "  [\(.at)] \(.message)"' 2>/dev/null
    fi
    echo "══════════════════════════════════════"

# ── 所有任务 ───────────────────────────────────────────────────────────────
else
    TOTAL=$(jq 'length' "$CC_REGISTRY" 2>/dev/null || echo 0)

    if [[ "$TOTAL" -eq 0 ]]; then
        echo "暂无任务记录。"
        exit 0
    fi

    echo "══ ClawClau 任务列表 ($TOTAL 条) ═══════════════"
    printf "%-24s %-12s %-8s %-7s %s\n" "ID" "状态" "重试" "超时" "开始时间"
    echo "──────────────────────────────────────────────────────"

    jq -r '.[] | [.id, .status,
        ((.retryCount // 0 | tostring) + "/" + (.maxRetries // 3 | tostring)),
        ((.timeout // 600) | tostring),
        (.startedAt | . / 1000 | floor | tostring)] | @tsv' \
        "$CC_REGISTRY" 2>/dev/null \
    | while IFS=$'\t' read -r id status retries timeout started_ts; do
        SESSION=$(cc_tmux_session "$id")
        tmux has-session -t "$SESSION" 2>/dev/null && status="running"
        START_HUMAN=$(date -r "$started_ts" "+%m-%d %H:%M" 2>/dev/null \
            || echo "$started_ts")
        printf "%-24s %-12s %-8s %-7s %s\n" \
            "$id" "$status" "$retries" "${timeout}s" "$START_HUMAN"
    done

    echo ""
    RUNNING=$(jq '[.[] | select(.status == "running")] | length' \
        "$CC_REGISTRY" 2>/dev/null || echo 0)
    DONE=$(jq '[.[] | select(.status == "done")] | length' \
        "$CC_REGISTRY" 2>/dev/null || echo 0)
    FAILED=$(jq '[.[] | select(.status == "failed" or .status == "timeout")] | length' \
        "$CC_REGISTRY" 2>/dev/null || echo 0)
    echo "汇总: $RUNNING 运行中, $DONE 已完成, $FAILED 失败/超时"
fi
