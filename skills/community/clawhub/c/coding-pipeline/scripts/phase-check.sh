#!/bin/bash
# coding-pipeline Phase Tracker
# Tracks current phase state in .pipeline-state/ and appends activity log
# Usage:
#   phase-check.sh get              — print current phase
#   phase-check.sh set <1|2|3|4>    — set current phase and log transition
#   phase-check.sh log <message>    — append a freeform log entry
#   phase-check.sh show             — print full activity log
#   phase-check.sh reset            — clear state (start of new task)

set -e

STATE_DIR=".pipeline-state"
STATE_FILE="${STATE_DIR}/current-phase"
LOG_FILE="${STATE_DIR}/activity.log"

usage() {
    cat << 'EOF'
Usage: phase-check.sh [command] [args]

Commands:
  get              Print current phase (1-4), or "none" if not set
  set <1|2|3|4>    Set the current phase and log the transition
  log <message>    Append a freeform log entry to the activity log
  show             Print the full activity log
  reset            Clear phase state (start of new task)
  -h, --help       Show this help
EOF
}

ensure_state_dir() {
    mkdir -p "$STATE_DIR"
}

timestamp() {
    date -u +"%Y-%m-%dT%H:%M:%SZ"
}

case "${1:-get}" in
    get)
        if [ -f "$STATE_FILE" ]; then
            cat "$STATE_FILE"
        else
            echo "none"
        fi
        ;;

    set)
        if [ -z "${2:-}" ]; then
            echo "Error: set requires a phase number (1-4)" >&2
            usage
            exit 1
        fi
        if ! [[ "$2" =~ ^[1-4]$ ]]; then
            echo "Error: phase must be 1, 2, 3, or 4" >&2
            exit 1
        fi
        ensure_state_dir
        previous="none"
        if [ -f "$STATE_FILE" ]; then
            previous=$(cat "$STATE_FILE")
        fi
        echo "$2" > "$STATE_FILE"
        echo "[$(timestamp)] Phase transition: $previous → $2" >> "$LOG_FILE"
        echo "Phase: $2"
        ;;

    log)
        shift
        if [ -z "${*:-}" ]; then
            echo "Error: log requires a message" >&2
            exit 1
        fi
        ensure_state_dir
        echo "[$(timestamp)] $*" >> "$LOG_FILE"
        ;;

    show)
        if [ -f "$LOG_FILE" ]; then
            cat "$LOG_FILE"
        else
            echo "No activity log yet. Start with 'phase-check.sh set 1'"
        fi
        ;;

    reset)
        if [ -d "$STATE_DIR" ]; then
            rm -f "$STATE_FILE" "$LOG_FILE"
            echo "Pipeline state reset."
        else
            echo "No state to reset."
        fi
        ;;

    -h|--help)
        usage
        exit 0
        ;;

    *)
        echo "Error: unknown command '$1'" >&2
        usage
        exit 1
        ;;
esac
