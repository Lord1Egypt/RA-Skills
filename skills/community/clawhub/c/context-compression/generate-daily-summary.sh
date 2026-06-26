#!/bin/bash
# Generate Daily Summary from Daily Notes
# This script runs OUTSIDE of OpenClaw agent context
# Reads from memory/YYYY-MM-DD.md, compresses, saves to memory/summaries/

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
MEMORY_DIR="$WORKSPACE/memory"
SUMMARIES_DIR="$MEMORY_DIR/summaries"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/logs/summary.log}"

# Ensure directories exist
mkdir -p "$SUMMARIES_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
    echo "$1"
}

# Get today's date
TODAY=$(date '+%Y-%m-%d')
YESTERDAY=$(date -d "yesterday" '+%Y-%m-%d' 2>/dev/null || date -v-1d '+%Y-%m-%d' 2>/dev/null)

DAILY_NOTE="$MEMORY_DIR/$TODAY.md"
SUMMARY_FILE="$SUMMARIES_DIR/$TODAY.md"

log "=== Daily Summary Generation ==="
log "Date: $TODAY"

# Check if daily note exists
if [ ! -f "$DAILY_NOTE" ]; then
    log "No daily note found for today: $DAILY_NOTE"
    exit 0
fi

# Check if summary already exists and is recent (within 4 hours)
if [ -f "$SUMMARY_FILE" ]; then
    summary_age=$((($(date +%s) - $(stat -c%Y "$SUMMARY_FILE" 2>/dev/null || stat -f%m "$SUMMARY_FILE")) / 3600))
    if [ "$summary_age" -lt 4 ]; then
        log "Summary already exists and is recent ($summary_age hours old), skipping"
        exit 0
    fi
fi

# Read daily note
NOTE_CONTENT=$(cat "$DAILY_NOTE")
NOTE_LINES=$(echo "$NOTE_CONTENT" | wc -l)
NOTE_CHARS=${#NOTE_CONTENT}

log "Daily note: $NOTE_LINES lines, $NOTE_CHARS chars"

# Create summary
# For now, we just copy the daily note as the summary
# In a production system, this would use an LLM to compress

cat > "$SUMMARY_FILE" << EOF
# Summary - $TODAY

## Source
- Original: memory/$TODAY.md
- Generated: $(date '+%Y-%m-%d %H:%M:%S')
- Original size: $NOTE_LINES lines, $NOTE_CHARS chars

## Content

$NOTE_CONTENT
EOF

log "Summary generated: $SUMMARY_FILE"

# Clean up old summaries (keep last 30 days)
find "$SUMMARIES_DIR" -name "*.md" -mtime +30 -delete 2>/dev/null
log "Cleaned up summaries older than 30 days"
