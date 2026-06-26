#!/bin/bash
# Gateway Watchdog v2 — boot-aware, multi-layer resilience
# Run via launchd every 5 minutes
#
# Problem solved: v1 watchdog killed the gateway during its ~90s boot sequence,
# creating a restart loop where the gateway never finished initializing.
#
# Layers:
#   1. Boot grace period (process age check) — don't restart young processes
#   2. Progressive retry with backoff — 3 retries at 15s, 30s, 45s
#   3. Port-level check fallback — if HTTP fails, check if port is bound
#   4. Stale PID detection — catch zombie processes not serving traffic
#   5. Restart cooldown file — prevent multiple restarts within 10 min

GATEWAY_URL="http://127.0.0.1:18789"
LOG="$HOME/.openclaw/logs/watchdog.log"
COOLDOWN_FILE="/tmp/openclaw-gateway-restart-cooldown"
BOOT_GRACE_SECONDS=180       # 3 min grace for memory init
COOLDOWN_SECONDS=600         # 10 min between restart attempts
STALE_THRESHOLD_SECONDS=600  # 10 min: if process is old but port isn't bound, it's stale

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG"
}

check_http() {
    curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$GATEWAY_URL" 2>/dev/null
}

check_port_bound() {
    lsof -i :18789 -sTCP:LISTEN >/dev/null 2>&1
}

get_gateway_pid() {
    launchctl list ai.openclaw.gateway 2>/dev/null | grep '"PID"' | awk -F'"' '{print $NF}' | tr -d ' ;'
    # Fallback: parse from launchctl output
    launchctl list ai.openclaw.gateway 2>/dev/null | awk '/PID/ {gsub(/[^0-9]/,"",$NF); print $NF}'
}

get_process_age_seconds() {
    local pid=$1
    if [ -z "$pid" ] || [ "$pid" = "0" ]; then
        echo "0"
        return
    fi
    local start_time
    start_time=$(ps -p "$pid" -o lstart= 2>/dev/null)
    if [ -z "$start_time" ]; then
        echo "0"
        return
    fi
    local start_epoch
    start_epoch=$(date -j -f "%a %b %d %T %Y" "$start_time" "+%s" 2>/dev/null)
    if [ -z "$start_epoch" ]; then
        echo "0"
        return
    fi
    local now_epoch
    now_epoch=$(date "+%s")
    echo $(( now_epoch - start_epoch ))
}

is_in_cooldown() {
    if [ -f "$COOLDOWN_FILE" ]; then
        local cooldown_time
        cooldown_time=$(cat "$COOLDOWN_FILE" 2>/dev/null)
        local now
        now=$(date "+%s")
        if [ -n "$cooldown_time" ] && [ $(( now - cooldown_time )) -lt $COOLDOWN_SECONDS ]; then
            return 0  # still in cooldown
        fi
    fi
    return 1  # not in cooldown
}

set_cooldown() {
    date "+%s" > "$COOLDOWN_FILE"
}

restart_gateway() {
    log "ACTION: Restarting gateway via launchctl kickstart -k"
    launchctl kickstart -k "gui/$(id -u)/ai.openclaw.gateway" 2>&1 >> "$LOG"
    set_cooldown
}

# ─── Main Logic ───

# Ensure log directory exists
mkdir -p "$(dirname "$LOG")"

# Layer 1: Quick HTTP check
STATUS=$(check_http)
if [ "$STATUS" != "000" ] && [ -n "$STATUS" ]; then
    # Gateway is responding. All good.
    exit 0
fi

# Gateway not responding via HTTP. Investigate.
PID=$(get_gateway_pid)
AGE=$(get_process_age_seconds "$PID")

# Layer 2: Boot grace period
if [ -n "$PID" ] && [ "$PID" != "0" ] && [ "$AGE" -lt "$BOOT_GRACE_SECONDS" ]; then
    log "INFO: Gateway process $PID is ${AGE}s old (boot grace: ${BOOT_GRACE_SECONDS}s). Waiting for init to complete."
    exit 0
fi

# Layer 3: Port-level check (maybe HTTP is slow but port is bound)
if check_port_bound; then
    log "INFO: Port 18789 is bound but HTTP unresponsive. Process $PID age: ${AGE}s. Waiting (may be under load)."
    # Give it one more chance with a longer timeout
    RETRY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$GATEWAY_URL" 2>/dev/null)
    if [ "$RETRY_STATUS" != "000" ] && [ -n "$RETRY_STATUS" ]; then
        log "OK: Gateway recovered with longer timeout (status=$RETRY_STATUS)"
        exit 0
    fi
    # Port bound but not serving after 15s. If process is very old, it might be stuck.
    if [ "$AGE" -gt "$STALE_THRESHOLD_SECONDS" ]; then
        log "WARN: Port bound but HTTP dead for ${AGE}s. Stale process detected."
        # Fall through to restart logic
    else
        log "INFO: Port bound, process ${AGE}s old. Giving more time."
        exit 0
    fi
fi

# Layer 4: Progressive retry with backoff
log "WARN: Gateway unresponsive (status=$STATUS, PID=$PID, age=${AGE}s). Starting progressive retry..."

for DELAY in 15 30 45; do
    sleep $DELAY
    STATUS=$(check_http)
    if [ "$STATUS" != "000" ] && [ -n "$STATUS" ]; then
        log "OK: Gateway recovered after ${DELAY}s retry (status=$STATUS)"
        exit 0
    fi
    # Also check if port came up during wait
    if check_port_bound; then
        log "INFO: Port bound during retry. Giving more time."
        sleep 15
        STATUS=$(check_http)
        if [ "$STATUS" != "000" ] && [ -n "$STATUS" ]; then
            log "OK: Gateway recovered after port bind + wait (status=$STATUS)"
            exit 0
        fi
    fi
done

# Layer 5: Cooldown check before restart
if is_in_cooldown; then
    log "CRITICAL: Gateway still down but restart cooldown active. Last restart was <${COOLDOWN_SECONDS}s ago. Skipping to prevent restart loop."
    exit 1
fi

# All retries exhausted, not in cooldown. Restart.
log "ERROR: Gateway unresponsive after all retries (PID=$PID, age=${AGE}s). Restarting..."
restart_gateway

# Verify restart worked (with boot grace)
sleep 30
STATUS=$(check_http)
if [ "$STATUS" != "000" ] && [ -n "$STATUS" ]; then
    log "OK: Gateway restarted successfully (status=$STATUS)"
elif check_port_bound; then
    log "OK: Gateway restarting (port bound, HTTP pending). Will verify next cycle."
else
    log "CRITICAL: Gateway restart may have failed. Process still booting (3 min grace). Will re-check next cycle."
fi
