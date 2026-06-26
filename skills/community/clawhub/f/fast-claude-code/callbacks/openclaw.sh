#!/bin/bash
# OpenClaw Callback - Send callback via OpenClaw gateway call agent

set -euo pipefail

# Default values
STATUS="done"
MODE="single"
TASK=""
MESSAGE=""
OUTPUT=""
SESSION_KEY=""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --status)
            STATUS="$2"
            shift 2
            ;;
        --mode)
            MODE="$2"
            shift 2
            ;;
        --task)
            TASK="$2"
            shift 2
            ;;
        --message)
            MESSAGE="$2"
            shift 2
            ;;
        --output)
            OUTPUT="$2"
            shift 2
            ;;
        --session-key)
            SESSION_KEY="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build the summary instruction and task content
SUMMARY_INSTRUCTION="请总结以下 Claude Code 任务的执行结果，并回复用户："

# Build message with clear structure
MSG="$SUMMARY_INSTRUCTION

=== 任务信息 ===
模式: $MODE
状态: $STATUS
任务标识: $TASK"

# Append original task/command
MSG="$MSG

=== 用户请求 ===
$MESSAGE"

# Append output if provided
if [[ -n "$OUTPUT" ]]; then
    MSG="$MSG

=== 执行结果 ===
$OUTPUT"
else
    MSG="$MSG

=== 执行结果 ===
(无输出内容)"
fi

# Generate idempotencyKey from task parameters to prevent duplicate sends on retry
IDEMPOTENCY_KEY="${MODE}:${TASK}:$(date +%s)"

# Escape strings for JSON
escape_json() {
    local string="$1"
    string="${string//\\/\\\\}"
    string="${string//\"/\\\"}"
    string="${string//$'\n'/\\n}"
    string="${string//$'\r'/\\r}"
    string="${string//$'\t'/\\t}"
    printf '%s' "$string"
}

MSG_JSON=$(escape_json "$MSG")
SESSION_KEY_JSON=$(escape_json "$SESSION_KEY")
IDEMPOTENCY_KEY_JSON=$(escape_json "$IDEMPOTENCY_KEY")

# Build params JSON
PARAMS=$(cat << EOF
{"sessionKey":"$SESSION_KEY_JSON","message":"$MSG_JSON","idempotencyKey":"$IDEMPOTENCY_KEY_JSON"}
EOF
)

# Check if openclaw is available
if command -v openclaw &> /dev/null; then
    openclaw gateway call agent --params "$PARAMS"
else
    echo "Warning: openclaw not found, using echo instead"
    echo "$MSG"
fi
