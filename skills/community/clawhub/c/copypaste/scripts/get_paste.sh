#!/usr/bin/env bash
set -euo pipefail

API_BASE="https://api.copy-paste.cloud"

if [[ $# -lt 1 ]]; then
  echo "Usage: get_paste.sh <paste-id> [password]" >&2
  exit 1
fi

PASTE_ID="$1"
PASSWORD="${2:-}"

# Validate rough UUID shape to avoid path traversal
if ! [[ "$PASTE_ID" =~ ^[0-9a-fA-F-]{36}$ ]]; then
  echo "Error: paste-id must be a UUID (e.g. 3f2a1c9e-0000-0000-0000-000000000000)" >&2
  exit 1
fi

URL="${API_BASE}/api/v1/pastes/${PASTE_ID}"
if [[ -n "$PASSWORD" ]]; then
  URL="${URL}?password=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$PASSWORD")"
fi

# Include API key if available (needed for private/group pastes)
AUTH_HEADER=""
if [[ -n "${COPYPASTE_API_KEY:-}" ]]; then
  AUTH_HEADER="-H Authorization: Bearer ${COPYPASTE_API_KEY}"
fi

response=$(curl -sS --fail-with-body \
  ${AUTH_HEADER:+-H "Authorization: Bearer ${COPYPASTE_API_KEY:-}"} \
  "$URL")

title=$(echo "$response"    | jq -r 'if .title then .title else "(untitled)" end')
language=$(echo "$response" | jq -r 'if .language then .language else "plain text" end')
author=$(echo "$response"   | jq -r 'if .authorName then .authorName else "anonymous" end')
created=$(echo "$response"  | jq -r '.createdAt')
expires=$(echo "$response"  | jq -r 'if .expiresAt then .expiresAt else "never" end')
bar=$(echo "$response"      | jq -r 'if .burnAfterRead then "yes (this was the last view)" else "no" end')
tags=$(echo "$response"     | jq -r 'if (.tags | length) > 0 then (.tags | join(", ")) else "none" end')
content=$(echo "$response"  | jq -r '.content')

echo "=== Paste: ${title} ==="
echo "ID:             ${PASTE_ID}"
echo "Language:       ${language}"
echo "Author:         ${author}"
echo "Created:        ${created}"
echo "Expires:        ${expires}"
echo "Burn-after-read:${bar}"
echo "Tags:           ${tags}"
echo "URL:            https://copy-paste.cloud/${PASTE_ID}"
echo ""
echo "--- Content ---"
echo "$content"
