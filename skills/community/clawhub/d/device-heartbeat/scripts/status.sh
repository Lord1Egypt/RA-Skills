#!/bin/bash
# 本地快速查看心跳状态（无需 API key）
# 用法: status.sh

LABEL="ai.openclaw.device-heartbeat"
STATE_FILE="${HOME}/.openclaw/logs/heartbeat-state.json"
LOG_FILE="${HOME}/.openclaw/logs/heartbeat.log"

echo "=== Device Heartbeat Status ==="
echo ""

# 服务状态
if launchctl list | grep -q "$LABEL" 2>/dev/null; then
  PID=$(launchctl list | grep "$LABEL" | awk '{print $1}')
  echo "Service: ✅ running (PID: $PID)"
else
  echo "Service: ❌ not running"
fi
echo ""

# 状态文件
if [ -f "$STATE_FILE" ]; then
  echo "State:"
  cat "$STATE_FILE"
  echo ""
fi

# 最近日志
if [ -f "$LOG_FILE" ]; then
  echo "Recent logs:"
  tail -5 "$LOG_FILE"
fi
