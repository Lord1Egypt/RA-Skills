#!/bin/bash
# Session Cleaner for Scotty (run on Pi via SSH)
# Usage: ssh user@<your-host> '~/agent-workspace/scripts/session-cleaner-scotty.sh'

SESSIONS_DIR="/home/user/.openclaw/agents/main/sessions"
OUTPUT_DIR="/home/user/agent-workspace/memory/sessions"

mkdir -p "$OUTPUT_DIR"

cd /home/user/agent-workspace/scripts || exit 1

# Process each session file
for file in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$file" ] || continue
    
    filename=$(basename "$file")
    session_id="${filename%%.*}"
    output_path="$OUTPUT_DIR/${session_id:0:8}_clean.md"
    
    # Skip if already processed
    [ -f "$output_path" ] && continue
    
    # Use the main cleaner
    node session-cleaner.mjs "$file" 2>/dev/null | tail -5
done

echo "Scotty session cleanup complete. Files in: $OUTPUT_DIR"
