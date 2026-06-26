#!/usr/bin/env bash
# =============================================================================
# astrill-watchdog.sh — Astrill VPN Watchdog for Ubuntu (deb GUI package)
# Version: 2.0.0
#
# Monitors Astrill StealthVPN via tun0 + ping. On failure, performs a full
# Astrill restart: pkill + setsid /autostart. Astrill auto-connects to the
# last used server. No sudo required at any point.
#
# On restart failure: logs prominently, resumes checking next cycle. Never exits.
#
# Usage: astrill-watchdog.sh {start|stop|status|once}
# Setup: run setup.sh once.
#
# Requirements:
#   - Ubuntu Linux, Astrill deb GUI package (/usr/local/Astrill/astrill)
#   - Tools: ping, ip, pgrep, pkill, setsid (Ubuntu defaults). No sudo.
#   - Active desktop session (DISPLAY/DBUS/WAYLAND) — required for relaunch.
# =============================================================================

# Intentionally NO set -e / set -o errexit.
# The watch loop must never exit on a non-zero command exit code. Every command
# that can fail is handled explicitly with || true or conditional checks.
# set -u and set -o pipefail are kept — those represent genuine programming
# errors, not expected runtime failures.
set -uo pipefail

# ── Config ────────────────────────────────────────────────────────────────────

CHECK_INTERVAL=30       # seconds between health checks
RECONNECT_WAIT=60       # seconds to wait after restart before checking health
PING_HOST="8.8.8.8"
PING_COUNT=3
PING_TIMEOUT=3          # per-ping timeout in seconds
LOG_MAX_LINES=5000      # rotate log when it exceeds this line count

ASTRILL_BIN="/usr/local/Astrill/astrill"
LOG_DIR="${XDG_STATE_HOME:-$HOME/.local/state}/astrill-watchdog"
LOG_FILE="$LOG_DIR/watchdog.log"
PID_FILE="$LOG_DIR/watchdog.pid"

# Desktop environment forwarded to Astrill on relaunch.
# setsid gives Astrill its own session so it can initialize its GUI/Wayland
# stack when launched from a systemd service (no controlling terminal).
DESKTOP_ENV=(
    DISPLAY="${DISPLAY:-:0}"
    DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:-unix:path=/run/user/$(id -u)/bus}"
    XDG_SESSION_TYPE="${XDG_SESSION_TYPE:-wayland}"
    WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-0}"
)

# ── Startup init ──────────────────────────────────────────────────────────────

# Resolve which user owns the running Astrill process. Falls back to the
# current user if Astrill is not yet running (e.g. watchdog starts before
# Astrill on login).
_resolve_astrill_user() {
    local pid
    pid="$(pgrep -f '/usr/local/Astrill/astrill' 2>/dev/null | head -1)" || true
    if [[ -n "$pid" ]]; then
        ps -p "$pid" -o user= 2>/dev/null | tr -d '[:space:]' || true
    fi
}
ASTRILL_USER="${ASTRILL_USER:-$(_resolve_astrill_user)}"
ASTRILL_USER="${ASTRILL_USER:-$(whoami)}"

# Ensure private log directory and files exist with correct permissions.
# dir 700, files 600 — logs contain VPN diagnostic info.
mkdir -p "$LOG_DIR"
chmod 700 "$LOG_DIR"
touch "$LOG_FILE" "$PID_FILE"
chmod 600 "$LOG_FILE" "$PID_FILE"

# ── Logging ───────────────────────────────────────────────────────────────────

log() {
    # Writes to log file only — never stdout — to avoid duplicate journal
    # entries when running under systemd (which captures stdout).
    local level="$1"; shift
    printf "[%s] [%-5s] %s\n" "$(date '+%Y-%m-%d %H:%M:%S')" "$level" "$*" >> "$LOG_FILE"
}

log_rotate() {
    # Trim log to last LOG_MAX_LINES lines when it grows too large.
    # Uses temp file + atomic mv to avoid truncating a file being tailed.
    local lines
    lines="$(wc -l < "$LOG_FILE" 2>/dev/null)" || return 0
    if (( lines > LOG_MAX_LINES )); then
        local tmp
        tmp="$(mktemp "$LOG_DIR/.log.XXXXXX")" || return 0
        if tail -n "$LOG_MAX_LINES" "$LOG_FILE" > "$tmp"; then
            mv "$tmp" "$LOG_FILE"
            chmod 600 "$LOG_FILE"
            log "INFO" "Log rotated (was ${lines} lines, kept last ${LOG_MAX_LINES})."
        else
            rm -f "$tmp"
        fi
    fi
}

# ── Health checks ─────────────────────────────────────────────────────────────

tun_up() {
    # Returns 0 if tun0 exists and is UP or UNKNOWN.
    local state
    state="$(ip link show tun0 2>/dev/null)" || return 1
    [[ "$state" =~ state[[:space:]]+(UP|UNKNOWN) ]]
}

internet_ok() {
    ping -c "$PING_COUNT" -W "$PING_TIMEOUT" "$PING_HOST" &>/dev/null
}

stealth_healthy() {
    tun_up && internet_ok
}

astrill_running() {
    pgrep -u "$ASTRILL_USER" -f '/usr/local/Astrill/astrill' &>/dev/null
}

# ── Reconnect ─────────────────────────────────────────────────────────────────

_restart_astrill() {
    # Kill entire Astrill process tree, then relaunch with /autostart.
    # Root-owned children (asproxy, asovpnc) die with the parent — no sudo needed.
    log "INFO" "  → Restarting Astrill via setsid /autostart"

    pkill -u "$ASTRILL_USER" -f '/usr/local/Astrill/astrill' 2>/dev/null || true
    sleep 4  # allow process tree to exit cleanly before relaunch

    if [[ ! -x "$ASTRILL_BIN" ]]; then
        log "ERROR" "  Astrill binary missing or not executable: ${ASTRILL_BIN}"
        return 1
    fi

    env "${DESKTOP_ENV[@]}" setsid "$ASTRILL_BIN" /autostart &>/dev/null &
    log "INFO" "  Astrill relaunched (PID $!)."
}

stealth_reconnect() {
    # Perform one full restart, wait RECONNECT_WAIT seconds, return health status.
    log "WARN" "StealthVPN down — restarting Astrill."

    ( _restart_astrill ) || log "WARN" "  _restart_astrill exited non-zero — continuing to wait."

    log "INFO" "  Waiting ${RECONNECT_WAIT}s for StealthVPN to recover…"
    sleep "$RECONNECT_WAIT"

    if stealth_healthy; then
        log "INFO" "StealthVPN restored."
        return 0
    fi

    log "ERROR" "StealthVPN still unhealthy after restart."
    return 1
}

# ── Watch loop ────────────────────────────────────────────────────────────────

watch_loop() {
    echo "$$" > "$PID_FILE"
    chmod 600 "$PID_FILE"
    log "INFO" "Watchdog started (PID=$$, user=${ASTRILL_USER}, interval=${CHECK_INTERVAL}s)."

    local was_healthy=true
    local consecutive_failures=0

    while true; do
        log_rotate

        if stealth_healthy; then
            if [[ "$was_healthy" == false ]]; then
                log "INFO" "StealthVPN healthy again (was down for ${consecutive_failures} check(s))."
                was_healthy=true
                consecutive_failures=0
            else
                log "DEBUG" "StealthVPN healthy."
            fi
        else
            (( consecutive_failures++ )) || true

            if [[ "$was_healthy" == true ]]; then
                local tun_state ping_state astrill_state
                tun_state=$(    tun_up         && echo "UP"  || echo "DOWN")
                ping_state=$(   internet_ok    && echo "OK"  || echo "FAIL")
                astrill_state=$(astrill_running && echo "YES" || echo "NO")
                log "WARN" "StealthVPN FAILED. tun0=${tun_state} ping=${ping_state} astrill=${astrill_state}"
                was_healthy=false
            else
                log "WARN" "StealthVPN still down (failure streak: ${consecutive_failures})."
            fi

            if stealth_reconnect; then
                was_healthy=true
                consecutive_failures=0
            else
                log "ERROR" "══════════════════════════════════════════════"
                log "ERROR" "CRITICAL: StealthVPN restart failed. No internet."
                log "ERROR" "Resuming checks in ${CHECK_INTERVAL}s."
                log "ERROR" "══════════════════════════════════════════════"
            fi
        fi

        sleep "$CHECK_INTERVAL"
    done
}

# ── Commands ──────────────────────────────────────────────────────────────────

cmd_start() {
    if [[ -f "$PID_FILE" ]]; then
        local old
        old="$(cat "$PID_FILE" 2>/dev/null)" || old=""
        if [[ -n "$old" ]] && kill -0 "$old" 2>/dev/null; then
            echo "Watchdog already running (PID ${old})."
            exit 0
        fi
        rm -f "$PID_FILE"
    fi

    local orphans
    orphans="$(pgrep -f 'astrill-watchdog.sh _loop' 2>/dev/null || true)"
    if [[ -n "$orphans" ]]; then
        echo "Cleaning up orphaned loop processes: ${orphans}"
        echo "$orphans" | xargs kill 2>/dev/null || true
        sleep 1
    fi

    nohup bash "$0" _loop >> "$LOG_FILE" 2>&1 &
    local new_pid="$!"
    echo "$new_pid" > "$PID_FILE"
    chmod 600 "$PID_FILE"
    echo "Watchdog started (PID ${new_pid}). Log: ${LOG_FILE}"
}

cmd_stop() {
    local killed=0

    if [[ -f "$PID_FILE" ]]; then
        local pid
        pid="$(cat "$PID_FILE" 2>/dev/null)" || pid=""
        if [[ -n "$pid" ]] && kill "$pid" 2>/dev/null; then
            echo "Watchdog (PID ${pid}) stopped."
            killed=1
        fi
        rm -f "$PID_FILE"
    fi

    local orphans
    orphans="$(pgrep -f 'astrill-watchdog.sh _loop' 2>/dev/null || true)"
    if [[ -n "$orphans" ]]; then
        echo "$orphans" | xargs kill 2>/dev/null || true
        echo "Killed orphaned loop processes: ${orphans}"
        killed=1
    fi

    [[ $killed -eq 0 ]] && echo "No watchdog was running."
    return 0
}

cmd_status() {
    local tun_info ping_state astrill_info health_state watcher_state

    if tun_up; then
        local tun_ip
        tun_ip="$(ip addr show tun0 2>/dev/null | awk '/inet /{print $2}' | head -1)"
        tun_info="UP (${tun_ip:-no IP})"
    else
        tun_info="DOWN"
    fi

    ping_state=$(internet_ok && echo "OK" || echo "FAILED")

    if astrill_running; then
        astrill_info="$(pgrep -u "$ASTRILL_USER" -f '/usr/local/Astrill/astrill' \
            | head -1 \
            | xargs -I{} ps -p {} -o pid=,etime= 2>/dev/null \
            | awk '{print "PID "$1", up "$2}')"
        astrill_info="${astrill_info:-running (PID unknown)}"
    else
        astrill_info="NOT RUNNING"
    fi

    health_state=$(stealth_healthy && echo "HEALTHY ✓" || echo "DEGRADED ✗")

    local loops
    loops="$(pgrep -f 'astrill-watchdog.sh _loop' 2>/dev/null || true)"
    if [[ -n "$loops" ]]; then
        watcher_state="running (PID $(echo "$loops" | tr '\n' ' ' | sed 's/ $//'))"
        local pid_file_val
        pid_file_val="$(cat "$PID_FILE" 2>/dev/null || true)"
        if [[ -n "$pid_file_val" ]] && ! echo "$loops" | grep -qF "$pid_file_val"; then
            watcher_state+=" ⚠  PID mismatch — run: stop then start"
        fi
    else
        watcher_state="NOT RUNNING"
    fi

    printf "user:     %s\ntun0:     %s\nping:     %s\nastrill:  %s\nstatus:   %s\nwatchdog: %s\nlog:      %s\n" \
        "$ASTRILL_USER" "$tun_info" "$ping_state" "$astrill_info" \
        "$health_state" "$watcher_state" "$LOG_FILE"

    echo ""
    echo "--- last 20 log lines ---"
    tail -n 20 "$LOG_FILE" 2>/dev/null || echo "(no log yet)"
}

cmd_once() {
    if stealth_healthy; then
        log "INFO" "once: StealthVPN healthy — nothing to do."
        echo "StealthVPN healthy."
    else
        log "WARN" "once: StealthVPN unhealthy — attempting restart."
        echo "StealthVPN unhealthy — restarting…"
        stealth_reconnect || true
    fi
}

# ── Entrypoint ────────────────────────────────────────────────────────────────

case "${1:-}" in
    start)  cmd_start  ;;
    stop)   cmd_stop   ;;
    status) cmd_status ;;
    once)   cmd_once   ;;
    _loop)  watch_loop ;;
    *)
        echo "Usage: $(basename "$0") {start|stop|status|once}"
        exit 1
        ;;
esac
