#!/bin/bash
# Session Logging Cleanup Script
# Removes session files older than 7 days

SESSIONS_DIR="${SESSIONS_DIR:-$HOME/.openclaw/workspace/sessions}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
LOG_FILE="${LOG_FILE:-$HOME/.openclaw/workspace/logs/session-cleanup.log}"

# Create log directory if needed
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$SESSIONS_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting session cleanup..." >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Sessions dir: $SESSIONS_DIR" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Retention: $RETENTION_DAYS days" >> "$LOG_FILE"

# Count files before
BEFORE=$(find "$SESSIONS_DIR" -name "*.md" -type f 2>/dev/null | wc -l)

# Delete files older than retention period
find "$SESSIONS_DIR" -name "*.md" -type f -mtime +$RETENTION_DAYS -delete -print 2>/dev/null | while read -r file; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Deleted: $file" >> "$LOG_FILE"
done

# Count deleted
AFTER=$(find "$SESSIONS_DIR" -name "*.md" -type f 2>/dev/null | wc -l)
DELETED=$((BEFORE - AFTER))

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleanup complete. Deleted $DELETED files ($BEFORE -> $AFTER)" >> "$LOG_FILE"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] ---" >> "$LOG_FILE"
