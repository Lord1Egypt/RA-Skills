#!/usr/bin/env bash
# cleanup-zombie-browsers.sh — Detect and clean up zombie browser processes left by OpenClaw
#
# OpenClaw's browser tool (Playwright) launches Chrome/Chromium/Firefox instances.
# When the Gateway restarts, these child processes get orphaned (PPID becomes 1/systemd)
# and accumulate memory over time.
#
# SAFETY:
#   - Default mode: detect-only (no kill)
#   - Requires --kill to actually terminate processes
#   - Only targets current user's processes
#   - Only targets browsers with OpenClaw-specific user-data-dir
#   - Only targets orphaned processes (PPID=1 or PPID=systemd)
#   - Requires minimum age before killing (default: 1 hour)
#   - Sends SIGTERM first, SIGKILL only after grace period
#   - Full audit logging
#
# Usage:
#   ./cleanup-zombie-browsers.sh              # Detect only (safe, default)
#   ./cleanup-zombie-browsers.sh --kill       # Detect and terminate zombies
#   ./cleanup-zombie-browsers.sh --kill --min-age 7200  # Only kill processes older than 2h
#   ./cleanup-zombie-browsers.sh --json       # Output as JSON (for integration)

set -euo pipefail

# --- Defaults ---
ACTION="detect"
MIN_AGE_SECONDS=3600        # Only target processes alive > 1 hour
GRACE_PERIOD_SECONDS=10     # SIGTERM → wait → SIGKILL
OUTPUT_FORMAT="text"        # text or json
LOG_FILE="${OPENCLAW_ZOMBIE_LOG:-/tmp/openclaw/zombie-browser-cleanup.log}"
OPENCLAW_BROWSER_PATTERN=".openclaw/browser/"

# --- Parse args ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        --kill)       ACTION="kill"; shift ;;
        --min-age)    MIN_AGE_SECONDS="$2"; shift 2 ;;
        --grace)      GRACE_PERIOD_SECONDS="$2"; shift 2 ;;
        --json)       OUTPUT_FORMAT="json"; shift ;;
        --log)        LOG_FILE="$2"; shift 2 ;;
        --pattern)    OPENCLAW_BROWSER_PATTERN="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: $(basename "$0") [--kill] [--min-age SECONDS] [--grace SECONDS] [--json] [--log PATH]"
            echo ""
            echo "Detect (and optionally clean up) zombie browser processes left by OpenClaw."
            echo ""
            echo "Options:"
            echo "  --kill         Terminate detected zombie processes (default: detect only)"
            echo "  --min-age N    Only target processes older than N seconds (default: 3600)"
            echo "  --grace N      Seconds to wait between SIGTERM and SIGKILL (default: 10)"
            echo "  --json         Output results as JSON"
            echo "  --log PATH     Log file path (default: /tmp/openclaw/zombie-browser-cleanup.log)"
            echo "  --pattern STR  OpenClaw browser dir pattern (default: .openclaw/browser/)"
            echo ""
            echo "Safety: Without --kill, this script only reports. It never touches processes"
            echo "owned by other users or browsers not launched by OpenClaw."
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

mkdir -p "$(dirname "$LOG_FILE")"

# --- Logging ---
log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "$msg" >> "$LOG_FILE"
    if [[ "$OUTPUT_FORMAT" == "text" ]]; then
        echo "$msg"
    fi
}

# --- OS detection ---
detect_os() {
    case "$(uname -s)" in
        Linux*)  echo "linux" ;;
        Darwin*) echo "macos" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)       echo "unknown" ;;
    esac
}

OS="$(detect_os)"

# --- Browser process names by platform ---
get_browser_patterns() {
    case "$OS" in
        linux)
            echo "chrome chromium chromium-browser brave-browser microsoft-edge firefox"
            ;;
        macos)
            echo "Google Chrome Chromium Brave Browser Microsoft Edge Firefox"
            ;;
        *)
            echo "chrome chromium firefox"
            ;;
    esac
}

# --- Get process info ---
# Returns: PID PPID ELAPSED_SECONDS RSS_KB CMDLINE
get_openclaw_browser_procs() {
    local current_user
    current_user="$(whoami)"
    local now
    now="$(date +%s)"

    if [[ "$OS" == "linux" ]]; then
        # Find all browser-like processes owned by current user
        ps -u "$current_user" -o pid=,ppid=,lstart=,rss=,args= 2>/dev/null | while read -r pid ppid lstart_rest; do
            # lstart is like "Fri Mar  4 18:29:00 2026", followed by rss and args
            # Use a more reliable parsing approach
            :
        done

        # Alternative: use /proc for precise info
        for pid_dir in /proc/[0-9]*; do
            local pid="${pid_dir##*/}"

            # Must be owned by current user
            local proc_owner
            proc_owner="$(stat -c '%U' "$pid_dir" 2>/dev/null)" || continue
            [[ "$proc_owner" == "$current_user" ]] || continue

            # Read cmdline
            local cmdline
            cmdline="$(tr '\0' ' ' < "$pid_dir/cmdline" 2>/dev/null)" || continue

            # Must be a browser process
            local is_browser=false
            for browser in chrome chromium brave msedge firefox; do
                if [[ "$cmdline" == *"/$browser "* ]] || [[ "$cmdline" == *"/$browser-"* ]]; then
                    is_browser=true
                    break
                fi
            done
            [[ "$is_browser" == true ]] || continue

            # Must have OpenClaw browser pattern in cmdline
            [[ "$cmdline" == *"$OPENCLAW_BROWSER_PATTERN"* ]] || continue

            # Get PPID
            local ppid
            ppid="$(awk '{print $4}' "$pid_dir/stat" 2>/dev/null)" || continue

            # Get process start time and calculate age
            local start_time_ticks
            start_time_ticks="$(awk '{print $22}' "$pid_dir/stat" 2>/dev/null)" || continue
            local clk_tck
            clk_tck="$(getconf CLK_TCK)"
            local boot_time
            boot_time="$(awk '/^btime/ {print $2}' /proc/stat)"
            local start_epoch=$(( boot_time + start_time_ticks / clk_tck ))
            local age_seconds=$(( now - start_epoch ))

            # Get RSS in KB
            local rss_kb
            rss_kb="$(awk '{print $2}' "$pid_dir/statm" 2>/dev/null)" || continue
            rss_kb=$(( rss_kb * 4 ))  # pages to KB (assuming 4KB pages)

            echo "$pid $ppid $age_seconds $rss_kb $cmdline"
        done

    elif [[ "$OS" == "macos" ]]; then
        ps -u "$current_user" -o pid=,ppid=,etime=,rss=,command= 2>/dev/null | while IFS= read -r line; do
            local pid ppid etime rss cmdline
            read -r pid ppid etime rss cmdline <<< "$line"

            # Must have OpenClaw browser pattern
            [[ "$cmdline" == *"$OPENCLAW_BROWSER_PATTERN"* ]] || continue

            # Must be a browser
            local is_browser=false
            for browser in "Google Chrome" Chromium Brave Firefox "Microsoft Edge"; do
                if [[ "$cmdline" == *"$browser"* ]]; then
                    is_browser=true
                    break
                fi
            done
            [[ "$is_browser" == true ]] || continue

            # Parse elapsed time (DD-HH:MM:SS or HH:MM:SS or MM:SS)
            local age_seconds=0
            if [[ "$etime" == *-* ]]; then
                local days="${etime%%-*}"
                local rest="${etime#*-}"
                IFS=: read -r h m s <<< "$rest"
                age_seconds=$(( days*86400 + 10#$h*3600 + 10#$m*60 + 10#$s ))
            elif [[ "$etime" == *:*:* ]]; then
                IFS=: read -r h m s <<< "$etime"
                age_seconds=$(( 10#$h*3600 + 10#$m*60 + 10#$s ))
            else
                IFS=: read -r m s <<< "$etime"
                age_seconds=$(( 10#$m*60 + 10#$s ))
            fi

            echo "$pid $ppid $age_seconds $rss $cmdline"
        done
    fi
}

# --- Check if PPID indicates orphan ---
is_orphaned() {
    local ppid="$1"

    if [[ "$OS" == "linux" ]]; then
        # PPID=1 (init/systemd) means orphaned
        [[ "$ppid" -eq 1 ]] && return 0

        # Also check if PPID belongs to systemd --user (common on modern Linux)
        local ppid_cmdline
        ppid_cmdline="$(tr '\0' ' ' < "/proc/$ppid/cmdline" 2>/dev/null)" || return 0
        [[ "$ppid_cmdline" == *"systemd --user"* ]] && return 0

    elif [[ "$OS" == "macos" ]]; then
        [[ "$ppid" -eq 1 ]] && return 0
    fi

    return 1
}

# --- Format duration ---
format_duration() {
    local seconds="$1"
    if (( seconds >= 86400 )); then
        echo "$(( seconds / 86400 ))d $(( (seconds % 86400) / 3600 ))h"
    elif (( seconds >= 3600 )); then
        echo "$(( seconds / 3600 ))h $(( (seconds % 3600) / 60 ))m"
    elif (( seconds >= 60 )); then
        echo "$(( seconds / 60 ))m $(( seconds % 60 ))s"
    else
        echo "${seconds}s"
    fi
}

# --- Main ---
log "=== Zombie browser cleanup started (mode: $ACTION, min-age: ${MIN_AGE_SECONDS}s, os: $OS) ==="

if [[ "$OS" == "unknown" ]] || [[ "$OS" == "windows" ]]; then
    log "WARNING: $OS is not fully supported yet. Only Linux and macOS are supported."
    exit 0
fi

# Collect zombie candidates
declare -a zombie_pids=()
declare -a zombie_info=()
total_rss_kb=0
total_found=0

while IFS= read -r line; do
    [[ -z "$line" ]] && continue

    read -r pid ppid age_seconds rss_kb rest <<< "$line"

    total_found=$((total_found + 1))

    # Check: must be orphaned (PPID=1 or systemd)
    if ! is_orphaned "$ppid"; then
        continue
    fi

    # Check: must be old enough
    if (( age_seconds < MIN_AGE_SECONDS )); then
        log "SKIP PID $pid: age $(format_duration $age_seconds) < minimum $(format_duration $MIN_AGE_SECONDS)"
        continue
    fi

    zombie_pids+=("$pid")

    # Sum up RSS of this process + all its descendants
    tree_rss_kb=$rss_kb
    if [[ "$OS" == "linux" ]]; then
        for child_stat in /proc/[0-9]*/stat; do
            child_ppid="$(awk '{print $4}' "$child_stat" 2>/dev/null)" || continue
            child_pid="$(awk '{print $1}' "$child_stat" 2>/dev/null)" || continue
            # Check if child belongs to this process tree (direct or indirect)
            check_pid="$child_ppid"
            for _ in 1 2 3 4 5; do
                if [[ "$check_pid" == "$pid" ]]; then
                    child_rss="$(awk '{print $2}' "/proc/$child_pid/statm" 2>/dev/null)" || break
                    tree_rss_kb=$(( tree_rss_kb + child_rss * 4 ))
                    break
                fi
                [[ -f "/proc/$check_pid/stat" ]] || break
                check_pid="$(awk '{print $4}' "/proc/$check_pid/stat" 2>/dev/null)" || break
            done
        done
    fi

    rss_mb=$(( tree_rss_kb / 1024 ))
    zombie_info+=("PID=$pid PPID=$ppid age=$(format_duration $age_seconds) mem=${rss_mb}MB (tree)")
    total_rss_kb=$((total_rss_kb + tree_rss_kb))

done < <(get_openclaw_browser_procs)

zombie_count=${#zombie_pids[@]}
total_rss_mb=$((total_rss_kb / 1024))

log "Found $total_found OpenClaw browser processes, $zombie_count are zombies (${total_rss_mb}MB total)"

# --- Report ---
if [[ "$OUTPUT_FORMAT" == "json" ]]; then
    echo "{"
    echo "  \"total_openclaw_browsers\": $total_found,"
    echo "  \"zombie_count\": $zombie_count,"
    echo "  \"zombie_memory_mb\": $total_rss_mb,"
    echo "  \"action\": \"$ACTION\","
    echo "  \"zombies\": ["
    for i in "${!zombie_info[@]}"; do
        comma=","
        [[ $i -eq $((zombie_count - 1)) ]] && comma=""
        echo "    \"${zombie_info[$i]}\"$comma"
    done
    echo "  ]"
    echo "}"
else
    for info in "${zombie_info[@]}"; do
        log "  ZOMBIE: $info"
    done
fi

# --- Kill if requested ---
if [[ "$ACTION" == "kill" ]] && [[ $zombie_count -gt 0 ]]; then
    log "Terminating $zombie_count zombie processes..."

    for pid in "${zombie_pids[@]}"; do
        # Verify process still exists and still matches criteria before killing
        if [[ "$OS" == "linux" ]] && [[ -d "/proc/$pid" ]]; then
            verify_cmdline="$(tr '\0' ' ' < "/proc/$pid/cmdline" 2>/dev/null)" || continue
            if [[ "$verify_cmdline" != *"$OPENCLAW_BROWSER_PATTERN"* ]]; then
                log "SKIP PID $pid: re-verification failed (cmdline changed)"
                continue
            fi
        fi

        # Count child processes that will also be terminated
        child_count=0
        if [[ "$OS" == "linux" ]]; then
            child_count=$(grep -r "PPid:.*$pid" /proc/[0-9]*/status 2>/dev/null | wc -l || echo 0)
        fi

        # SIGTERM the process group (kills main + all children)
        log "Sending SIGTERM to PID $pid (+ ~$child_count child processes)"
        kill -TERM -- "-$(ps -o pgid= -p "$pid" 2>/dev/null | tr -d ' ')" 2>/dev/null \
            || kill -TERM "$pid" 2>/dev/null \
            || { log "PID $pid already gone"; continue; }

        # Wait for graceful exit
        waited=0
        while (( waited < GRACE_PERIOD_SECONDS )); do
            if ! kill -0 "$pid" 2>/dev/null; then
                log "PID $pid and children terminated gracefully"
                break
            fi
            sleep 1
            waited=$((waited + 1))
        done

        # SIGKILL if still alive
        if kill -0 "$pid" 2>/dev/null; then
            log "PID $pid did not exit after ${GRACE_PERIOD_SECONDS}s, sending SIGKILL"
            kill -KILL -- "-$(ps -o pgid= -p "$pid" 2>/dev/null | tr -d ' ')" 2>/dev/null \
                || kill -KILL "$pid" 2>/dev/null || true
        fi
    done

    log "Cleanup complete. Freed approximately ${total_rss_mb}MB"
elif [[ "$ACTION" == "detect" ]] && [[ $zombie_count -gt 0 ]]; then
    log "Run with --kill to terminate these zombie processes"
fi

log "=== Zombie browser cleanup finished ==="

# Exit code: 0 = no zombies or cleaned, 1 = zombies detected (detect mode)
if [[ "$ACTION" == "detect" ]] && [[ $zombie_count -gt 0 ]]; then
    exit 1
fi
exit 0
