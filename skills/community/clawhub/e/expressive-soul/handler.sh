#!/bin/bash
# handler.sh — 每次对话后自动触发，记录对话内容用于23:00复盘
# 触发时机：每次AI回复后

_SELF_DIR="$(cd "$(dirname "$0")" && pwd)"
MEMORY_DIR="$_SELF_DIR/memory/daily"

mkdir -p "$MEMORY_DIR"

TODAY=$(date -u +%Y-%m-%d)
LOG_FILE="$MEMORY_DIR/${TODAY}.jsonl"

# 接收 stdin 输入（JSON格式：message + result）
if [ -p /dev/stdin ]; then
    INPUT=$(cat -)
else
    INPUT="{}"
fi

# 追加到今日日志
echo "$INPUT" | jq -c ". + {timestamp: \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" >> "$LOG_FILE" 2>/dev/null

echo "logged" >&2
