#!/bin/bash
WORKSPACE="/home/alfred/.openclaw/workspace"
REL_PATH="$1"
FULL_PATH="$WORKSPACE/$REL_PATH"

# Sanitize: No .. or absolute
if [[ "$REL_PATH" == *'..'* || "$REL_PATH" == '/'* ]]; then
echo '{"success": false, "error": "Invalid path"}'
exit 1
fi

if [ ! -d "$FULL_PATH" ]; then
echo '{"success": false, "error": "Not a directory"}'
exit 1
fi

FILES=$(ls -1 "$FULL_PATH")
echo "{\"success\": true, \"data\": [\"${FILES//$'\n'/'", "'}\"]}"
