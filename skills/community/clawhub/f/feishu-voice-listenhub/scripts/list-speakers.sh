#!/usr/bin/env bash
# list-speakers.sh — List available ListenHub speakers
# Usage: list-speakers.sh [language]
#
# Required env:
#   LISTENHUB_API_KEY — ListenHub API key

set -euo pipefail

LANGUAGE="${1:-}"

: "${LISTENHUB_API_KEY:?Set LISTENHUB_API_KEY}"

API_BASE="https://api.marswave.ai/openapi/v1"

RESP=$(curl -sS "$API_BASE/speakers/list" \
  -H "Authorization: Bearer $LISTENHUB_API_KEY")

echo "$RESP" | python3 -c "
import sys,json
d=json.load(sys.stdin)
lang_filter='$LANGUAGE'
for item in d['data']['items']:
    if lang_filter and item['language'] != lang_filter:
        continue
    print(f\"{item['speakerId']:40s} {item['name']:10s} {item['gender']:6s} {item['language']}\")
"
