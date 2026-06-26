#!/bin/bash

OPENCLAW_HOME_DIR="${OPENCLAW_HOME_DIR:-$HOME/.openclaw}"
STATE_FILE="${STATE_FILE:-$OPENCLAW_HOME_DIR/state/rollback-pending.json}"
CONFIG_FILE="${CONFIG_FILE:-$OPENCLAW_HOME_DIR/openclaw.json}"
BACKUP_DIR="${BACKUP_DIR:-$OPENCLAW_HOME_DIR}"
LOG_FILE="${LOG_FILE:-$OPENCLAW_HOME_DIR/logs/rollback.log}"
LAUNCHD_LABEL="ai.openclaw.rollback"
GATEWAY_PORT="18789"
ROLLBACK_DELAY_MINUTES=10

mkdir -p "$BACKUP_DIR" "$(dirname "$STATE_FILE")" "$(dirname "$LOG_FILE")"

log() {
    local msg="[$(date -Iseconds)] $1"
    echo "$msg" >> "$LOG_FILE"
    echo "$1"
}

usage() {
    cat <<'EOF'
Usage:
  auto-rollback.sh start [--reason "description"]
  auto-rollback.sh start "description"
  auto-rollback.sh cancel
  auto-rollback.sh status
EOF
}

require_bin() {
    command -v "$1" >/dev/null 2>&1 || {
        log "❌ Missing required command: $1"
        exit 1
    }
}

write_state_file() {
    local backup_file="$1"
    local rollback_time="$2"
    local reason="$3"

    jq -n \
        --arg backup_file "$backup_file" \
        --arg launchd_label "$LAUNCHD_LABEL" \
        --arg created_at "$(date -Iseconds)" \
        --arg rollback_at "$rollback_time" \
        --arg reason "$reason" \
        '{
          backup_file: $backup_file,
          launchd_label: $launchd_label,
          created_at: $created_at,
          rollback_at: $rollback_at,
          reason: $reason
        }' > "$STATE_FILE"
}

resolve_openclaw_cmd() {
    if command -v openclaw >/dev/null 2>&1; then
        command -v openclaw
        return 0
    fi

    if [ -x /opt/homebrew/bin/openclaw ]; then
        echo /opt/homebrew/bin/openclaw
        return 0
    fi

    if [ -x /usr/local/bin/openclaw ]; then
        echo /usr/local/bin/openclaw
        return 0
    fi

    return 1
}

OPENCLAW_CMD="$(resolve_openclaw_cmd)" || {
    log "❌ Unable to find 'openclaw' in PATH, /opt/homebrew/bin, or /usr/local/bin"
    exit 1
}

check_gateway_health() {
    if ! pgrep -f "openclaw.*gateway" >/dev/null 2>&1; then
        return 1
    fi

    local max_attempts="${1:-30}"
    local attempt=0
    while [ "$attempt" -lt "$max_attempts" ]; do
        if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$GATEWAY_PORT/health" 2>/dev/null | grep -q "200"; then
            return 0
        fi
        sleep 1
        attempt=$((attempt + 1))
    done

    return 1
}

ensure_no_pending_rollback() {
    if [ -f "$STATE_FILE" ]; then
        log "❌ A rollback is already pending"
        log "ℹ️  Run '$0 status' or '$0 cancel' before starting a new one"
        exit 1
    fi
}

parse_start_reason() {
    if [ $# -eq 0 ]; then
        echo "manual config change"
        return 0
    fi

    case "$1" in
        --reason)
            if [ $# -lt 2 ] || [ -z "$2" ]; then
                log "❌ Missing value for --reason"
                exit 1
            fi
            echo "$2"
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            printf '%s\n' "$*"
            ;;
    esac
}

write_rollback_script() {
    local rollback_script="$1"
    local backup_file="$2"

    cat > "$rollback_script" <<EOF
#!/bin/bash

OPENCLAW_HOME_DIR="$OPENCLAW_HOME_DIR"
STATE_FILE="$STATE_FILE"
LOG_FILE="$LOG_FILE"
GATEWAY_PORT="$GATEWAY_PORT"
LAUNCHD_LABEL="$LAUNCHD_LABEL"
OPENCLAW_CMD="$OPENCLAW_CMD"
BACKUP_FILE="$backup_file"

log() {
    local msg="[\$(date -Iseconds)] \$1"
    echo "\$msg" >> "\$LOG_FILE"
    echo "\$1"
}

check_gateway_health() {
    if ! pgrep -f "openclaw.*gateway" >/dev/null 2>&1; then
        return 1
    fi

    if curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:\$GATEWAY_PORT/health" 2>/dev/null | grep -q "200"; then
        return 0
    fi

    return 1
}

log "🚨 rollback task started"

if check_gateway_health; then
    log "✅ Gateway is already healthy, cancelling rollback"
    rm -f "\$STATE_FILE" "\$OPENCLAW_HOME_DIR/\$LAUNCHD_LABEL.plist" "\$OPENCLAW_HOME_DIR/.rollback_execute.sh"
    exit 0
fi

log "❌ Gateway still unhealthy, restoring backup: \$BACKUP_FILE"
cp "\$BACKUP_FILE" "$CONFIG_FILE" || {
    log "❌ Failed to restore backup"
    exit 1
}

log "🔄 Restarting Gateway"
"\$OPENCLAW_CMD" gateway restart || log "❌ Gateway restart command failed"

sleep 5
if check_gateway_health; then
    log "🎉 Rollback completed and Gateway is healthy"
else
    log "⚠️ Rollback completed but Gateway is still unhealthy"
fi

rm -f "\$STATE_FILE" "\$OPENCLAW_HOME_DIR/\$LAUNCHD_LABEL.plist" "\$0"
EOF

    chmod +x "$rollback_script"
}

cmd_start() {
    require_bin jq
    require_bin launchctl
    require_bin curl
    require_bin plutil

    ensure_no_pending_rollback

    local reason
    reason="$(parse_start_reason "$@")"

    local backup_file="$BACKUP_DIR/openclaw.json.$(date +%Y%m%d-%H%M%S)"
    local plist_file="$OPENCLAW_HOME_DIR/$LAUNCHD_LABEL.plist"
    local rollback_script="$OPENCLAW_HOME_DIR/.rollback_execute.sh"
    local rollback_time
    local rollback_min
    local rollback_hour
    local rollback_day
    local rollback_month
    local rollback_year

    [ -f "$CONFIG_FILE" ] || {
        log "❌ Config file not found: $CONFIG_FILE"
        exit 1
    }

    cp "$CONFIG_FILE" "$backup_file" || {
        log "❌ Failed to back up openclaw.json"
        exit 1
    }
    log "✅ Config backed up: $backup_file"

    rollback_time="$(date -v+"${ROLLBACK_DELAY_MINUTES}"M '+%Y-%m-%d %H:%M:%S %z')"
    rollback_min="$(date -v+"${ROLLBACK_DELAY_MINUTES}"M '+%M')"
    rollback_hour="$(date -v+"${ROLLBACK_DELAY_MINUTES}"M '+%H')"
    rollback_day="$(date -v+"${ROLLBACK_DELAY_MINUTES}"M '+%d')"
    rollback_month="$(date -v+"${ROLLBACK_DELAY_MINUTES}"M '+%m')"
    rollback_year="$(date -v+"${ROLLBACK_DELAY_MINUTES}"M '+%Y')"

    write_rollback_script "$rollback_script" "$backup_file"

    cat > "$plist_file" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$LAUNCHD_LABEL</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$rollback_script</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Minute</key>
        <integer>$rollback_min</integer>
        <key>Hour</key>
        <integer>$rollback_hour</integer>
        <key>Day</key>
        <integer>$rollback_day</integer>
        <key>Month</key>
        <integer>$rollback_month</integer>
        <key>Year</key>
        <integer>$rollback_year</integer>
    </dict>
    <key>RunAtLoad</key>
    <false/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
        <key>HOME</key>
        <string>$HOME</string>
    </dict>
</dict>
</plist>
EOF

    plutil -lint "$plist_file" >/dev/null || {
        log "❌ Generated launchd plist is invalid: $plist_file"
        rm -f "$plist_file" "$rollback_script"
        exit 1
    }

    log "✅ launchd job created: $plist_file"
    log "⏰ Rollback scheduled for: $rollback_time"

    launchctl load "$plist_file" 2>/dev/null && log "✅ launchd job loaded" || log "⚠️ launchd load failed or job already exists"

    write_state_file "$backup_file" "$rollback_time" "$reason" || {
        log "❌ Failed to write state file"
        rm -f "$plist_file" "$rollback_script"
        exit 1
    }

    log "✅ State file written: $STATE_FILE"
    log "📋 Next step: $OPENCLAW_CMD gateway restart"
    log "⚠️ If Gateway stays unhealthy, rollback will run in ${ROLLBACK_DELAY_MINUTES} minutes"
    log "✅ If Gateway becomes healthy and BOOT.md integration is absent, cancel manually: $0 cancel"
}

cmd_cancel() {
    require_bin jq
    require_bin launchctl

    if [ ! -f "$STATE_FILE" ]; then
        log "ℹ️  No pending rollback"
        exit 0
    fi

    local launchd_label
    local plist_file

    launchd_label="$(jq -r '.launchd_label' "$STATE_FILE")"
    plist_file="$OPENCLAW_HOME_DIR/$launchd_label.plist"

    launchctl unload "$plist_file" 2>/dev/null && log "✅ launchd job unloaded" || log "⚠️ launchd unload failed or job already ran"
    rm -f "$plist_file" "$OPENCLAW_HOME_DIR/.rollback_execute.sh" "$STATE_FILE"
    log "✅ Pending rollback cancelled"
}

cmd_status() {
    require_bin jq
    require_bin launchctl

    if [ ! -f "$STATE_FILE" ]; then
        echo "ℹ️  No pending rollback"
        exit 0
    fi

    echo "📋 Pending rollback:"
    jq '.' "$STATE_FILE"
    echo ""

    if launchctl list | grep -q "$(jq -r '.launchd_label' "$STATE_FILE")"; then
        echo "✅ launchd job: loaded"
    else
        echo "⚠️ launchd job: not loaded"
    fi

    if check_gateway_health 1; then
        echo "✅ Gateway: healthy"
    else
        echo "❌ Gateway: unhealthy"
    fi
}

case "$1" in
    start)
        shift
        cmd_start "$@"
        ;;
    cancel)
        cmd_cancel
        ;;
    status)
        cmd_status
        ;;
    -h|--help|"")
        usage
        ;;
    *)
        usage
        exit 1
        ;;
esac
