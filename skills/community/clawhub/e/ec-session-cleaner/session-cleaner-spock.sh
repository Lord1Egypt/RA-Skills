#!/bin/bash
# Session Cleaner for Spock - Converts session JSONL to readable markdown
# Usage: node session-cleaner-spock.mjs <session-file.jsonl>
#        node session-cleaner-spock.mjs --all
#        node session-cleaner-spock.mjs --yesterday

SESSIONS_DIR="/home/user/.openclaw/agents/ada/sessions"
OUTPUT_DIR="/home/user/agent-workspace/memory/sessions"

mkdir -p "$OUTPUT_DIR"

cd /home/user/agent-workspace/scripts || exit 1

# Run with appropriate args, just targeting Spock's sessions
for file in "$SESSIONS_DIR"/*.jsonl; do
    [ -f "$file" ] || continue
    
    filename=$(basename "$file")
    session_id="${filename%%.*}"
    output_path="$OUTPUT_DIR/${session_id:0:8}_clean.md"
    
    # Skip if already processed
    [ -f "$output_path" ] && continue
    
    # Use the main cleaner with Spock's output dir
    node session-cleaner.mjs "$file" 2>/dev/null | tail -5
done

echo "Spock session cleanup complete. Files in: $OUTPUT_DIR"
