#!/bin/bash
# OpenClaw Memory System — Heartbeat Check (Unix/Linux/macOS)
# Periodic routine: process cron inbox, check state, create daily file if needed

set -euo pipefail

WORKSPACE_PATH="${1:-.}"
WORKSPACE="$(cd "$WORKSPACE_PATH" && pwd)"
MEMORY_DIR="$WORKSPACE/memory"
INBOX_FILE="$MEMORY_DIR/cron-inbox.md"
STATE_FILE="$MEMORY_DIR/heartbeat-state.json"
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"

# Check for jq (optional — we'll write state JSON manually if not available)
JQ_AVAILABLE=false
if command -v jq &> /dev/null; then
    JQ_AVAILABLE=true
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting heartbeat check..."

# Ensure memory directory exists
if [ ! -d "$MEMORY_DIR" ]; then
    log "ERROR: Memory directory not found at $MEMORY_DIR"
    exit 1
fi

# 1. Ensure today's daily notes file exists
if [ ! -f "$TODAY_FILE" ]; then
    log "Creating daily notes file for today: $TODAY_FILE"
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    TEMPLATE="$(dirname "$SCRIPT_DIR")/templates/daily-notes.md"
    if [ -f "$TEMPLATE" ]; then
        sed "s/YYYY-MM-DD/$TODAY/g" "$TEMPLATE" > "$TODAY_FILE"
        log "Created from template"
    else
        echo "# $TODAY — Daily Notes" > "$TODAY_FILE"
        log "Created minimal daily notes file"
    fi
fi

# 2. Process cron inbox if entries exist
if [ -f "$INBOX_FILE" ]; then
    ENTRY_COUNT=$(grep -c "^## \[" "$INBOX_FILE" || true)
    if [ "$ENTRY_COUNT" -gt 0 ]; then
        log "Processing $ENTRY_COUNT cron inbox entries..."

        # Append to today's daily notes
        echo "" >> "$TODAY_FILE"
        echo "## $(date '+%H:%M') -- Cron Inbox Processing" >> "$TODAY_FILE"

        # Copy FULL entries (header + body), not just headers
        # Extract everything from each ## [ line to the next ## [ or EOF
        awk '
            /^## \[/ {
                if (buffer != "") {
                    print buffer
                    print ""
                }
                buffer = $0
                next
            }
            buffer != "" {
                buffer = buffer "\n" $0
            }
            END {
                if (buffer != "") print buffer
            }
        ' "$INBOX_FILE" >> "$TODAY_FILE"

        log "Appended inbox entries to daily notes"

        # Clear inbox (keep header)
        HEADER="# Cron Inbox\n\nCross-session message bus.\n\n---\n\n*Last processed: $(date '+%Y-%m-%d %H:%M')*\n"
        printf "%b" "$HEADER" > "$INBOX_FILE"
        log "Cleared cron inbox"
    else
        log "Inbox is empty"
    fi
else
    log "Inbox file not found — creating empty inbox"
    echo "# Cron Inbox" > "$INBOX_FILE"
fi

# 3. Update heartbeat state
if [ -f "$STATE_FILE" ]; then
    if [ "$JQ_AVAILABLE" = true ]; then
        TMP_STATE=$(mktemp)
        jq '.lastChecks.cronInbox = now | .version = "1.0.0"' "$STATE_FILE" > "$TMP_STATE"
        mv "$TMP_STATE" "$STATE_FILE"
        log "Updated heartbeat state"
    else
        # Manual JSON update without jq
        NOW=$(date +%s)
        sed -i.bak "s/\"cronInbox\": .*/\"cronInbox\": $NOW/" "$STATE_FILE"
        sed -i.bak "s/\"version\": .*/\"version\": \"1.0.0\"/" "$STATE_FILE"
        rm -f "$STATE_FILE.bak"
        log "Updated heartbeat state (no jq)"
    fi
else
    log "Creating new heartbeat state file"
    cat > "$STATE_FILE" << EOF
{
  "lastChecks": {
    "email": null,
    "calendar": null,
    "weather": null,
    "social": null,
    "cronInbox": $(date +%s)
  },
  "lastMaintenance": null,
  "lastMemoryExtraction": null,
  "lastWeeklyReview": null,
  "version": "1.0.0"
}
EOF
fi

log "Heartbeat check complete."
exit 0
