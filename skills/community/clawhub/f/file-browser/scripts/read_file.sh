#!/bin/bash
WORKSPACE="/home/alfred/.openclaw/workspace"
REL_PATH="$1"
FULL_PATH="$WORKSPACE/$REL_PATH"

# Sanitize
if [[ "$REL_PATH" == *'..'* || "$REL_PATH" == '/'* ]]; then
echo '{"success": false, "error": "Invalid path"}'
exit 1
fi

if [ ! -f "$FULL_PATH" ] || [ ! -r "$FULL_PATH" ]; then
echo '{"success": false, "error": "File not found or unreadable"}'
exit 1
fi

# Limit size (e.g., head -c 10240)
CONTENT=$(head -c 10240 "$FULL_PATH" | tr -d '\0')
echo "{\"success\": true, \"data\": \"$CONTENT\"}"
