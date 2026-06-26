#!/bin/bash
# gateway-watchdog.sh — Self-healing gateway recovery (Lite — no crash loop detection)
# Checks if the OC gateway is alive and recovers it if not.
# Designed to be run by a launchd watchdog every 2 minutes (macOS).
#
# Recovery log: /tmp/openclaw/gateway-watchdog.log
# Alerts: Telegram (optional) — set TELEGRAM_ID="" to disable
#
# Supplied by ConfusedUser.com — OpenClaw tools & skills
# Full version with crash loop detection: https://confuseduser.com

LOGFILE="/tmp/openclaw/gateway-watchdog.log"
PLIST="$HOME/Library/LaunchAgents/ai.openclaw.gateway.plist"
PROBE_URL="http://127.0.0.1:YOUR_OC_PORT"
TELEGRAM_ID="YOUR_TELEGRAM_ID"          # Set to "" to disable Telegram alerts
RECOVERY_COOLDOWN_FILE="/tmp/openclaw/watchdog-last-recovery"
COOLDOWN_SECONDS=300       # 5 minutes between recovery attempts

mkdir -p /tmp/openclaw

log() {
    echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $1" >> "$LOGFILE"
}

# --- Alert: Telegram optional, always logs ---
send_alert() {
    local MSG="$1"
    log "ALERT: $MSG"
    if [ -n "$TELEGRAM_ID" ]; then
        local GOG_BIN
        GOG_BIN=$(command -v gog 2>/dev/null \
            || [ -x "/opt/homebrew/bin/gog" ] && echo "/opt/homebrew/bin/gog" \
            || [ -x "/usr/local/bin/gog" ] && echo "/usr/local/bin/gog" \
            || echo "")
        if [ -n "$GOG_BIN" ]; then
            "$GOG_BIN" telegram send --to "$TELEGRAM_ID" --text "$MSG" 2>/dev/null || true
        else
            log "ALERT: gog not found — Telegram alert not sent. Message: $MSG"
        fi
    fi
}

# --- Main flow ---

# Check cooldown
if [ -f "$RECOVERY_COOLDOWN_FILE" ]; then
    LAST=$(cat "$RECOVERY_COOLDOWN_FILE")
    NOW=$(date +%s)
    ELAPSED=$((NOW - LAST))
    if [ $ELAPSED -lt $COOLDOWN_SECONDS ]; then
        exit 0
    fi
fi

# Probe gateway health
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$PROBE_URL" 2>/dev/null)

if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "301" ] || [ "$HTTP_STATUS" = "302" ]; then
    exit 0
fi

# Gateway is down — attempt recovery
log "Gateway probe failed (HTTP $HTTP_STATUS). Attempting recovery..."
date +%s > "$RECOVERY_COOLDOWN_FILE"

launchctl bootout "gui/$UID/ai.openclaw.gateway" 2>/dev/null
sleep 3
launchctl bootstrap "gui/$UID" "$PLIST" 2>/dev/null
sleep 5

# Re-probe
HTTP_STATUS_AFTER=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$PROBE_URL" 2>/dev/null)

if [ "$HTTP_STATUS_AFTER" = "200" ] || [ "$HTTP_STATUS_AFTER" = "301" ] || [ "$HTTP_STATUS_AFTER" = "302" ]; then
    log "Recovery SUCCESS — gateway is back up (HTTP $HTTP_STATUS_AFTER)"
    send_alert "⚡ Auto-recovery: Gateway was down and has been automatically restarted. Now healthy."
else
    log "Recovery FAILED — gateway still down after restart attempt (HTTP $HTTP_STATUS_AFTER)"
    send_alert "🔴 Gateway auto-recovery FAILED. Manual restart needed: launchctl bootout gui/\$UID/ai.openclaw.gateway && sleep 2 && launchctl bootstrap gui/\$(id -u) ~/Library/LaunchAgents/ai.openclaw.gateway.plist"
fi

exit 0
