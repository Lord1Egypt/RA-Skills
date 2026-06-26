#!/usr/bin/env bash
# openclaw-gatewaykeeper: Health check and auto-restart for OpenClaw gateway
# Run via cron every 15 minutes

set -euo pipefail

OPENCLAW_WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
LOG_DIR="$OPENCLAW_WORKSPACE/logs"
RECOVERY_FILE="$LOG_DIR/gateway-recovery.json"
LOG_FILE="$LOG_DIR/openclaw-gatewaykeeper.log"

mkdir -p "$LOG_DIR"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S')  $1" >> "$LOG_FILE"; }

# Check gateway status
if status_output=$(openclaw gateway status 2>&1); then
    if echo "$status_output" | grep -qiE "running|alive|ok|active"; then
        log "OK: Gateway is running"
        exit 0
    fi
fi

# Gateway is down
log "WARN: Gateway appears down. Attempting restart..."
crash_time=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

if openclaw gateway start >/dev/null 2>&1; then
    sleep 5
    if verify=$(openclaw gateway status 2>&1) && echo "$verify" | grep -qiE "running|alive|ok|active"; then
        log "OK: Gateway restarted successfully"
        cat > "$RECOVERY_FILE" << EOF
{
  "crashed_at": "$crash_time",
  "restarted_at": "$(date -u '+%Y-%m-%dT%H:%M:%SZ')",
  "restarted_by": "openclaw-gatewaykeeper"
}
EOF
        log "OK: Recovery file written"
    else
        log "ERROR: Gateway restart failed"
    fi
else
    log "ERROR: Restart attempt failed"
fi
