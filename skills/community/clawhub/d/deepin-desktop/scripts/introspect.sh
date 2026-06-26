#!/bin/bash
# Introspect all deepin D-Bus interfaces
DEST="$1"
PATH_STR="$2"
OUTPUT_DIR="/home/zane/.openclaw/workspace/skills/deepin-desktop/references"

if [ -z "$DEST" ] || [ -z "$PATH_STR" ]; then
  echo "Usage: $0 <service-name> <object-path>"
  exit 1
fi

SAFE=$(echo "$DEST.$PATH_STR" | tr '/' '_' | tr '.' '_')
FILE="$OUTPUT_DIR/${SAFE}.txt"

echo "Introspecting $DEST $PATH_STR..."
gdbus introspect --system --dest "$DEST" --object-path "$PATH_STR" > "$FILE" 2>&1
echo "Saved to $FILE ($(wc -l < "$FILE") lines)"
