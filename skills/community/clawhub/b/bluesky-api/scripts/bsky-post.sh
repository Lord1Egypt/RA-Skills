#!/usr/bin/env bash
set -euo pipefail

# Post to Bluesky via AT Protocol (requires app password)
# Usage: bsky-post.sh <handle> <app_password> <text>

HANDLE="${1:-${BSKY_HANDLE:-}}"
# Prefer env var for app password — never pass secrets as CLI args (visible in ps/history)
APP_PASSWORD="${BSKY_APP_PASSWORD:-}"
TEXT="${2:-}"

if [ -z "$HANDLE" ] || [ -z "$APP_PASSWORD" ] || [ -z "$TEXT" ]; then
  echo "Usage: BSKY_APP_PASSWORD=<password> bsky-post.sh <handle> <text>" >&2
  echo "  handle           — Bluesky handle (e.g. alice.bsky.social), or set BSKY_HANDLE" >&2
  echo "  text             — Post text (max 300 characters)" >&2
  echo "  BSKY_APP_PASSWORD — App password (env var, never pass as CLI arg)" >&2
  exit 1
fi

# Check post length using grapheme count (Bluesky's actual limit is 300 graphemes)
# Use Python if available for accurate Unicode grapheme counting, fall back to char count
if command -v python3 &>/dev/null; then
  GRAPHEME_COUNT=$(python3 -c "
import unicodedata, sys
text = sys.stdin.read()
# NFC normalize then count (approximation; full grapheme cluster counting needs 'grapheme' lib)
normalized = unicodedata.normalize('NFC', text)
print(len(normalized))
" <<< "$TEXT")
else
  GRAPHEME_COUNT=${#TEXT}
fi

if [ "$GRAPHEME_COUNT" -gt 300 ]; then
  echo "Error: post text is ${GRAPHEME_COUNT} graphemes (max 300)" >&2
  exit 1
fi

# Step 1: Authenticate
SESSION=$(curl -sf -X POST "https://bsky.social/xrpc/com.atproto.server.createSession" \
  -H "Content-Type: application/json" \
  -d "{\"identifier\": $(printf '%s' "$HANDLE" | jq -Rs .), \"password\": $(printf '%s' "$APP_PASSWORD" | jq -Rs .)}") || {
  echo "Error: authentication failed for '${HANDLE}'" >&2
  exit 1
}

ACCESS_TOKEN=$(echo "$SESSION" | jq -r '.accessJwt')
DID=$(echo "$SESSION" | jq -r '.did')

if [ "$ACCESS_TOKEN" = "null" ] || [ -z "$ACCESS_TOKEN" ]; then
  # Never print SESSION JSON — it contains accessJwt and DID
  ERROR_MSG=$(echo "$SESSION" | jq -r '.error // "unknown error"' 2>/dev/null || echo "unknown error")
  echo "Error: authentication failed — ${ERROR_MSG}" >&2
  exit 1
fi

# Step 2: Create the post
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%S.000Z)

RESULT=$(curl -sf -X POST "https://bsky.social/xrpc/com.atproto.repo.createRecord" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"repo\": $(printf '%s' "$DID" | jq -Rs .),
    \"collection\": \"app.bsky.feed.post\",
    \"record\": {
      \"\$type\": \"app.bsky.feed.post\",
      \"text\": $(printf '%s' "$TEXT" | jq -Rs .),
      \"createdAt\": \"${TIMESTAMP}\"
    }
  }") || {
  echo "Error: failed to create post" >&2
  exit 1
}

echo "Post created successfully!"
echo "$RESULT" | jq '{uri: .uri, cid: .cid}'
