#!/bin/bash
# Website Monitor – Detect changes on websites
# Usage: website-monitor.sh check|add|list URL [NAME]

set -e
MONITOR_DIR="$HOME/.website-monitor"
mkdir -p "$MONITOR_DIR/sites"
mkdir -p "$MONITOR_DIR/history"

case "${1:-check}" in
    add)
        URL="$2"
        NAME="${3:-$(echo "$URL" | sed 's|https\?://||;s|[^a-zA-Z0-9]|_|g')}"
        echo "$URL" > "$MONITOR_DIR/sites/$NAME.url"
        echo "✅ Monitoring: $NAME ($URL)"
        ;;
    list)
        echo "📋 Monitored sites:"
        for f in "$MONITOR_DIR"/sites/*.url; do
            [ -f "$f" ] && echo "  - $(basename "$f" .url): $(cat "$f")"
        done
        ;;
    check)
        CHANGES=0
        for f in "$MONITOR_DIR"/sites/*.url; do
            [ -f "$f" ] || continue
            NAME=$(basename "$f" .url)
            URL=$(cat "$f")
            CURRENT=$(curl -s --max-time 30 "$URL" | md5sum | cut -d' ' -f1)
            PREV_FILE="$MONITOR_DIR/history/$NAME.md5"
            
            if [ -f "$PREV_FILE" ]; then
                PREV=$(cat "$PREV_FILE")
                if [ "$CURRENT" != "$PREV" ]; then
                    echo "🔔 CHANGE: $NAME ($URL)"
                    CHANGES=$((CHANGES + 1))
                fi
            else
                echo "📝 First check: $NAME"
            fi
            echo "$CURRENT" > "$PREV_FILE"
        done
        echo "✅ Checked. Changes: $CHANGES"
        ;;
    *)
        echo "Usage: website-monitor.sh [add|list|check]"
        ;;
esac
