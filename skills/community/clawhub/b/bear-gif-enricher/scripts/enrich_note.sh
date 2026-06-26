#!/usr/bin/env bash
set -euo pipefail

NOTE_ID="${1:?Usage: $0 <note-id>}"
TOKEN_FILE="${GRIZZLY_TOKEN_FILE:-$HOME/.config/grizzly/token}"
TENOR_KEY="${TENOR_API_KEY:-}"
GIPHY_KEY="${GIPHY_API_KEY:-$GIPHY_API_KEY}"

# 1. Read note content
NOTE_JSON=$(grizzly open-note --id "$NOTE_ID" --enable-callback --json --token-file "$TOKEN_FILE")
TITLE=$(echo "$NOTE_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title',''))" 2>/dev/null || echo "")
TEXT=$(echo "$NOTE_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('text',''))" 2>/dev/null || echo "")

# 2. Extract topic: prefer title, then first line
TOPIC="${TITLE:-}"
if [ -z "$TOPIC" ]; then
    TOPIC=$(echo "$TEXT" | head -1 | sed 's/^#\+ *//')
fi
TOPIC=$(echo "$TOPIC" | tr ' ' '+' | head -c 80)

if [ -z "$TOPIC" ]; then
    echo "ERROR: Could not extract topic from note $NOTE_ID"
    exit 1
fi

# 3. Search for a GIF
GIF_URL=""

if [ -n "$TENOR_KEY" ]; then
    GIF_URL=$(curl -sf "https://tenor.googleapis.com/v2/search?q=${TOPIC}&key=${TENOR_KEY}&limit=1&media_filter=gif" \
        | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['results'][0]['media_formats']['gif']['url'])" 2>/dev/null || echo "")
fi

if [ -z "$GIF_URL" ] && [ -n "$GIPHY_KEY" ]; then
    GIF_URL=$(curl -sf "https://api.giphy.com/v1/gifs/search?q=${TOPIC}&api_key=${GIPHY_KEY}&limit=1&rating=g" \
        | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['images']['original']['url'])" 2>/dev/null || echo "")
fi

if [ -z "$GIF_URL" ]; then
    echo "ERROR: No GIF found for topic: $TOPIC"
    exit 1
fi

# 4. Append GIF to note
GIF_MD="

![${TOPIC//+/ }](${GIF_URL})
"
echo "$GIF_MD" | grizzly add-text --id "$NOTE_ID" --mode append --token-file "$TOKEN_FILE"

# 5. Swap tags: remove 待整理, add 已整理
DONE_TAG="${RESEARCH_DONE_TAG:-已整理}"
PENDING_TAG="${RESEARCH_TAG:-待整理}"
# Remove old tag
grizzly delete-tag --name "$PENDING_TAG" --id "$NOTE_ID" --token-file "$TOKEN_FILE" 2>/dev/null || true
# Add new tag
echo "" | grizzly create --title "$(echo "$NOTE_JSON" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('title',''))" 2>/dev/null)" --tag "$DONE_TAG" 2>/dev/null || true

echo "OK: Enriched note $NOTE_ID with GIF for topic: ${TOPIC//+/ }"
