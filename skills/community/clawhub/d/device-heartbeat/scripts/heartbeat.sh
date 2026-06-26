#!/bin/bash
# Device Heartbeat - 定期上报心跳到 healthchecks.io
# 用法: heartbeat.sh <PING_URL> [INTERVAL_SECONDS]

PING_URL="${1:?Usage: heartbeat.sh <PING_URL> [INTERVAL_SECONDS]}"
INTERVAL="${2:-180}"
STATE_FILE="${HOME}/.openclaw/logs/heartbeat-state.json"
LOG_FILE="${HOME}/.openclaw/logs/heartbeat.log"
MAX_LOG_LINES=500
FAIL_COUNT=0

log() {
  echo "[heartbeat] $(date '+%Y-%m-%d %H:%M:%S') $1"
  # 日志轮转：超过 MAX_LOG_LINES 行则截断保留最后一半
  if [ -f "$LOG_FILE" ]; then
    LINE_COUNT=$(wc -l < "$LOG_FILE" 2>/dev/null || echo 0)
    if [ "$LINE_COUNT" -gt "$MAX_LOG_LINES" ]; then
      KEEP=$((MAX_LOG_LINES / 2))
      tail -n "$KEEP" "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
    fi
  fi
}

update_state() {
  local status="$1"
  local now=$(date '+%Y-%m-%dT%H:%M:%S%z')
  mkdir -p "$(dirname "$STATE_FILE")"
  cat > "$STATE_FILE" << EOF
{
  "status": "$status",
  "last_check": "$now",
  "fail_count": $FAIL_COUNT,
  "ping_url_hash": "$(echo -n "$PING_URL" | shasum -a 256 | cut -c1-16)",
  "interval": $INTERVAL
}
EOF
}

log "Starting device heartbeat (interval: ${INTERVAL}s)"

while true; do
  HTTP_CODE=$(curl -fsS --retry 2 --max-time 10 -o /dev/null -w "%{http_code}" "$PING_URL" 2>/dev/null)
  if [ "$HTTP_CODE" = "200" ]; then
    if [ "$FAIL_COUNT" -gt 0 ]; then
      log "✅ RECOVERED after $FAIL_COUNT failures"
    else
      log "✅ ping ok"
    fi
    FAIL_COUNT=0
    update_state "up"
  else
    FAIL_COUNT=$((FAIL_COUNT + 1))
    log "❌ ping failed (HTTP $HTTP_CODE, fail #$FAIL_COUNT)"
    update_state "down"
  fi
  sleep "$INTERVAL"
done
