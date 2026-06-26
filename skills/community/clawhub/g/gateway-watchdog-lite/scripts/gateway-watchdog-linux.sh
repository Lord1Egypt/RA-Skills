#!/bin/bash
# gateway-watchdog-linux.sh — Self-healing gateway recovery for Linux (Lite — no crash loop detection)
# Designed to run as a systemd user service (continuous loop with 120s sleep).
#
# Recovery log: /tmp/openclaw/gateway-watchdog.log
# Alerts: Telegram (optional) — set TELEGRAM_ID="" to disable
#
# Supplied by ConfusedUser.com — OpenClaw tools & skills
# Full version with crash loop detection: https://confuseduser.com

LOGFILE="/tmp/openclaw/gateway-watchdog.log"
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
            || [ -x "/usr/local/bin/gog" ] && echo "/usr/local/bin/gog" \
            || echo "")
        if [ -n "$GOG_BIN" ]; then
            "$GOG_BIN" telegram send --to "$TELEGRAM_ID" --text "$MSG" 2>/dev/null || true
        else
            log "ALERT: gog not found — Telegram alert not sent. Message: $MSG"
        fi
    fi
}

# --- Main loop (runs continuously under systemd) ---

log "Gateway Watchdog Lite started (Linux). Probing $PROBE_URL every 120 seconds."

while true; do
    # Check cooldown
    if [ -f "$RECOVERY_COOLDOWN_FILE" ]; then
        LAST=$(cat "$RECOVERY_COOLDOWN_FILE")
        NOW=$(date +%s)
        ELAPSED=$((NOW - LAST))
        if [ $ELAPSED -lt $COOLDOWN_SECONDS ]; then
            sleep 120
            continue
        fi
    fi

    # Probe gateway health
    HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$PROBE_URL" 2>/dev/null)

    if [ "$HTTP_STATUS" = "200" ] || [ "$HTTP_STATUS" = "301" ] || [ "$HTTP_STATUS" = "302" ]; then
        sleep 120
        continue
    fi

    # Gateway is down — attempt recovery
    log "Gateway probe failed (HTTP $HTTP_STATUS). Attempting recovery..."
    date +%s > "$RECOVERY_COOLDOWN_FILE"

    # Try openclaw-gateway systemd service first, otherwise pkill fallback
    if systemctl --user is-active --quiet openclaw-gateway 2>/dev/null; then
        systemctl --user restart openclaw-gateway 2>/dev/null
    else
        pkill -f "openclaw.*gateway" 2>/dev/null || true
        sleep 3
        log "WARNING: openclaw-gateway service not found — manual restart may be required"
    fi

    sleep 5

    # Re-probe
    HTTP_STATUS_AFTER=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$PROBE_URL" 2>/dev/null)

    if [ "$HTTP_STATUS_AFTER" = "200" ] || [ "$HTTP_STATUS_AFTER" = "301" ] || [ "$HTTP_STATUS_AFTER" = "302" ]; then
        log "Recovery SUCCESS — gateway is back up (HTTP $HTTP_STATUS_AFTER)"
        send_alert "⚡ Auto-recovery: Gateway was down and has been automatically restarted. Now healthy."
    else
        log "Recovery FAILED — gateway still down after restart attempt (HTTP $HTTP_STATUS_AFTER)"
        send_alert "🔴 Gateway auto-recovery FAILED. Manual restart needed: systemctl --user restart openclaw-gateway"
    fi

    sleep 120
done
