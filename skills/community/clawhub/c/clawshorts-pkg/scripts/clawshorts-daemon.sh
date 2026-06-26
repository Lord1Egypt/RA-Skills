#!/bin/bash
#
# Fire TV Shorts Limiter Daemon (bash fallback)
# Delegates to Python daemon for production use.
#
set -euo pipefail

IPS="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON_DAEMON="${SCRIPT_DIR}/clawshorts-daemon.py"
STATE_DIR="${HOME}/.clawshorts"
LOG_DIR="${STATE_DIR}/logs"

# Threshold: video player width must be less than 80% of screen width to count
# as Shorts.  This is SHORTS_WIDTH_THRESHOLD (0.90) expressed as a percentage.
SHORTS_WIDTH_PCT=90

YOUTUBE_PKG="com.google.android.youtube.tv"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

log() {
    echo "[$(date '+%H:%M:%S')] $*"
}

validate_ip() {
    local ip="$1"
    # Delegate to Python validator for consistency with Python daemon
    python3 -c "
import sys, re
ip = '$ip'
if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
    sys.exit(1)
if any(int(o) > 255 for o in ip.split('.')):
    sys.exit(1)
" 2>/dev/null
}

for ip in $(echo "$IPS" | tr ',' ' '); do
    ip=$(echo "$ip" | xargs)
    if ! validate_ip "$ip"; then
        echo "Error: Invalid IP: $ip" >&2
        exit 1
    fi
done

mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="${LOG_DIR}/daemon.log"

get_state_file() {
    local ip="$1"
    local slug="${ip//./-}"
    echo "${STATE_DIR}/state-${slug}.txt"
}

get_session_file() {
    local ip="$1"
    local slug="${ip//./-}"
    echo "${STATE_DIR}/session-${slug}.txt"
}

check_adb() {
    adb devices 2>/dev/null | grep -q "^${1}:5555.*device$"
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

log "========================================="
log "Shorts Limiter (bash daemon)"
log "IPs: $IPS"
log "Threshold: ${SHORTS_WIDTH_PCT}% (matches Python daemon)"
log "========================================="

# Detect if Python daemon is available and prefer it
if [[ -x "$PYTHON_DAEMON" ]] && [[ "${FORCE_BASH_DAEMON:-}" != "1" ]]; then
    log "Using Python daemon: $PYTHON_DAEMON"
    exec python3 "$PYTHON_DAEMON" "$IPS" "$@"
fi

# Bash fallback (deprecated)
log "WARNING: Using bash daemon (deprecated). Prefer Python daemon."

while true; do
    for ip in $(echo "$IPS" | tr ',' ' '); do
        ip=$(echo "$ip" | xargs)
        if ! validate_ip "$ip"; then
            log "[SECURITY] Invalid IP: $ip"
            continue
        fi

        if ! check_adb "$ip"; then
            log "[ADB] OFF $ip"
            adb connect "$ip:5555" >/dev/null 2>&1
            continue
        fi

        log "[ADB] OK $ip"

        if adb -s "$ip:5555" shell dumpsys activity activities 2>/dev/null | grep -q youtube; then
            log "[WATCH] YouTube on $ip"

            adb -s "$ip:5555" shell uiautomator dump /sdcard/ui.xml 2>/dev/null
            adb -s "$ip:5555" pull /sdcard/ui.xml /tmp/ui.xml 2>/dev/null

            pct=$(python3 -c "
import re
try:
    c=open('/tmp/ui.xml').read()
    m=re.search(r'focused=\"true\"[^>]*bounds=\"\[(\d+),(\d+)\]\[(\d+),(\d+)\]\"',c)
    if not m:
        print(100)
    else:
        fw=int(m.group(3))-int(m.group(1))
        m=re.search(r'bounds=\"\[(\d+),(\d+)\]\[(\d+),(\d+)\]\"',c)
        if not m:
            print(100)
        else:
            sw=int(m.group(3))-int(m.group(1))
            print(int(fw/sw*100))
except:
    print(100)
" 2>/dev/null || echo "100")

            log "[RATIO] ${pct}%"

            # Use SHORTS_WIDTH_PCT as threshold (90 = 90% = SHORTS_WIDTH_THRESHOLD 0.90)
            if [[ "${pct}" -lt "${SHORTS_WIDTH_PCT}" ]]; then
                state_file=$(get_state_file "$ip")
                session_file=$(get_session_file "$ip")
                cnt=0 lim=5
                prev_session=""

                if [[ -f "$session_file" ]]; then
                    prev_session=$(cat "$session_file" 2>/dev/null || echo "")
                fi

                if [[ "$prev_session" = "1" ]]; then
                    log "[SHORTS] Same session, not counting again"
                else
                    echo "1" > "$session_file"

                    if [[ -f "$state_file" ]]; then
                        cnt=$(grep "^COUNT=" "$state_file" 2>/dev/null | head -1 | cut -d= -f2 || echo "0")
                        lim=$(grep "^LIMIT=" "$state_file" 2>/dev/null | head -1 | cut -d= -f2 || echo "5")
                    fi

                    if [[ "$cnt" -lt "$lim" ]]; then
                        cnt=$((cnt + 1))
                        cat > "$state_file" << EOF
DATE=$(date +%Y-%m-%d)
COUNT=$cnt
LIMIT=$lim
EOF
                        log "[SHORTS] #$cnt/$lim"

                        if [[ "$cnt" -ge "$lim" ]]; then
                            log "[LIMIT] Reached! Force-stopping YouTube..."
                            adb -s "$ip:5555" shell am force-stop "$YOUTUBE_PKG" 2>/dev/null || true
                        fi
                    else
                        adb -s "$ip:5555" shell am force-stop "$YOUTUBE_PKG" 2>/dev/null || true
                        log "[BLOCK] Limit reached"
                    fi
                fi
            else
                session_file=$(get_session_file "$ip")
                if [[ -f "$session_file" ]] && [[ "$(cat "$session_file" 2>/dev/null)" = "1" ]]; then
                    echo "0" > "$session_file"
                    log "[SHORTS] Exited Shorts view"
                fi
            fi
        fi
    done
    sleep 10
done
