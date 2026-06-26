#!/bin/bash
# OpenClaw Memory System - Nightly Memory Extraction (Unix/Linux/macOS)
# Extracts durable facts from daily notes and appends them to MEMORY.md

set -euo pipefail

WORKSPACE_PATH="${1:-.}"
WORKSPACE="$(cd "$WORKSPACE_PATH" && pwd)"
MEMORY_DIR="$WORKSPACE/memory"
MEMORY_FILE="$WORKSPACE/MEMORY.md"

# Check for jq (optional - we'll write state JSON manually if not available)
JQ_AVAILABLE=false
if command -v jq &> /dev/null; then
    JQ_AVAILABLE=true
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "Starting nightly memory extraction..."

# Check if memory directory exists
if [ ! -d "$MEMORY_DIR" ]; then
    log "ERROR: Memory directory not found at $MEMORY_DIR"
    exit 1
fi

# Check if MEMORY.md exists
if [ ! -f "$MEMORY_FILE" ]; then
    log "WARNING: MEMORY.md not found. Creating from template..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    TEMPLATE="$(dirname "$SCRIPT_DIR")/templates/MEMORY.md"
    if [ -f "$TEMPLATE" ]; then
        cp "$TEMPLATE" "$MEMORY_FILE"
        log "Created MEMORY.md from template"
    else
        log "ERROR: Template not found. Cannot create MEMORY.md."
        exit 1
    fi
fi

# Find today's daily notes file
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$MEMORY_DIR/$TODAY.md"

if [ ! -f "$TODAY_FILE" ]; then
    log "No daily notes found for today ($TODAY). Nothing to extract."
    exit 0
fi

log "Reading daily notes: $TODAY_FILE"

# Extract significant entries using grep for keywords
SIGNIFICANCE_KEYWORDS="decided|decision|lesson learned|important|breakthrough|milestone|completed|shipped|launched|fixed|solved|agreed|confirmed|approved|rejected|failed|error|new project|started|created|deployed|published"

# Find entries (lines starting with ## HH:MM)
ENTRIES=$(grep -n "^## [0-9]\{2\}:[0-9]\{2\} --" "$TODAY_FILE" || true)

if [ -z "$ENTRIES" ]; then
    log "No timestamped entries found in daily notes."
    exit 0
fi

# Build extract section
EXTRACT_SECTION="\n## Daily Extracts - $TODAY\n"
EXTRACT_COUNT=0

# Process each entry
while IFS= read -r line; do
    LINENO=$(echo "$line" | cut -d: -f1)
    TITLE=$(echo "$line" | sed 's/^## [0-9]\{2\}:[0-9]\{2\} -- //')

    # Extract entry body (from this line to next ## or EOF) - using portable sed
    BODY=$(sed -n "${LINENO},/^## [0-9]\{2\}:[0-9]\{2\} -- /p" "$TODAY_FILE" | sed '$d' | tail -n +2)

    # Check if significant
    if echo "$TITLE $BODY" | grep -qiE "$SIGNIFICANCE_KEYWORDS"; then
        EXTRACT_SECTION="$EXTRACT_SECTION\n### $TITLE\n- **Date:** $TODAY\n- **Details:** $BODY\n"
        EXTRACT_COUNT=$((EXTRACT_COUNT + 1))
    fi
done <<< "$ENTRIES"

if [ "$EXTRACT_COUNT" -eq 0 ]; then
    log "No significant entries found for extraction."
    exit 0
fi

# Append to MEMORY.md
printf "%b\n" "$EXTRACT_SECTION" >> "$MEMORY_FILE"
log "Appended $EXTRACT_COUNT extracts to MEMORY.md"

# Mark as extracted
MARKER="\n\n---\n*Memory extraction completed at $(date '+%H:%M')*"
printf "%b\n" "$MARKER" >> "$TODAY_FILE"
log "Marked daily notes as extracted"

# Update heartbeat state
STATE_FILE="$MEMORY_DIR/heartbeat-state.json"
if [ -f "$STATE_FILE" ]; then
    if [ "$JQ_AVAILABLE" = true ]; then
        TMP_STATE=$(mktemp)
        jq '.lastMemoryExtraction = now | .version = "1.0.0"' "$STATE_FILE" > "$TMP_STATE"
        mv "$TMP_STATE" "$STATE_FILE"
        log "Updated heartbeat state"
    else
        # Manual JSON update without jq
        NOW=$(date +%s)
        sed -i.bak "s/\"lastMemoryExtraction\": .*/\"lastMemoryExtraction\": $NOW/" "$STATE_FILE"
        sed -i.bak "s/\"version\": .*/\"version\": \"1.0.0\"/" "$STATE_FILE"
        rm -f "$STATE_FILE.bak"
        log "Updated heartbeat state (no jq)"
    fi
fi

log "Nightly memory extraction complete."
exit 0
