#!/bin/bash
# send-notifications.sh - Send pending .notification files
# Uses swarm_notify() from config.sh for provider-agnostic delivery

source "$(dirname "$0")/config.sh"

LOG_FILE="${LOGS_DIR}/send-notifications.log"
log() { echo "[$(date '+%H:%M:%S')] $1" >> "$LOG_FILE"; }

find "$LOGS_DIR" -maxdepth 1 -type f -name "*.notification" | sort | while read -r NOTIF_FILE; do
    MSG=$(cat "$NOTIF_FILE" 2>/dev/null)
    [ -z "$MSG" ] && { log "skip empty: $NOTIF_FILE"; mv "$NOTIF_FILE" "${NOTIF_FILE}.sent"; continue; }

    if swarm_notify "$MSG"; then
        mv "$NOTIF_FILE" "${NOTIF_FILE}.sent"
        log "sent: $(basename "$NOTIF_FILE")"
    else
        log "failed: $(basename "$NOTIF_FILE") (will retry)"
    fi
done
