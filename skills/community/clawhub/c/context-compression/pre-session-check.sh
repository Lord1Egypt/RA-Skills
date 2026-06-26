#!/bin/bash
# Pre-session Context Check
# Lightweight check that runs BEFORE context is loaded
# This is the "hook" approach - called by OpenClaw before loading session

SESSIONS_DIR="${SESSIONS_DIR:-$HOME/.openclaw/agents/main/sessions}"
MAX_SESSION_LINES=2000
MAX_TOTAL_UNITS=70000  # Leave buffer for other context layers

# Quick char estimation (1 char ≈ 3 bytes)
estimate_units() {
    local bytes=$1
    echo $((bytes / 3))
}

# Check total session size
total_bytes=0
for f in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$f" ] || continue
    [ -f "${f}.lock" ] && continue
    bytes=$(stat -c%s "$f" 2>/dev/null || stat -f%z "$f" 2>/dev/null || echo 0)
    total_bytes=$((total_bytes + bytes))
done

total_units=$(estimate_units $total_bytes)

# If under threshold, no action needed
if [ "$total_units" -lt "$MAX_TOTAL_UNITS" ]; then
    echo "OK: Total session chars ~$total_units (under $MAX_TOTAL_UNITS)"
    exit 0
fi

# Need truncation - this should trigger the external truncation service
echo "TRUNCATE_NEEDED: Total session chars ~$total_units exceeds $MAX_TOTAL_UNITS"

# Option 1: Call the external truncation script directly
# This runs OUTSIDE of agent context
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/truncate-sessions-safe.sh"

# Option 2: Signal to a background service
# touch /tmp/truncation-signal

exit 0
