#!/bin/bash
# Codex Runner - Log command

TASK_NAME=${1:-codex-task}
LOG_FILE=~/.codex-logs/codex-$TASK_NAME.log

if [ -f "$LOG_FILE" ]; then
    echo "=== 日志: $LOG_FILE ==="
    tail -50 "$LOG_FILE"
else
    echo "日志文件不存在: $LOG_DIR/codex-$TASK_NAME.log"
fi
