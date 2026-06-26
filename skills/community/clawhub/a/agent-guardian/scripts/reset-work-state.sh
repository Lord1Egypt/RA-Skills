#!/bin/bash
# 重置工作状态 + 消息队列（新会话启动时调用）
STATE_FILE="/tmp/agent-work-state.json"
NOW=$(date +%s)

cat > "$STATE_FILE" << EOF
{
  "current_task": "待命中",
  "status": "idle",
  "started_at": 0,
  "last_update": $NOW,
  "update_count": 0,
  "last_status_values": ["idle"],
  "error_count": 0,
  "last_report_at": 0
}
EOF

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$SCRIPT_DIR/msg-queue.py" reset 2>/dev/null

echo "OK: work state and message queue reset at $(date)"
