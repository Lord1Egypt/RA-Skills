#!/usr/bin/env bash
set -euo pipefail

API_BASE="https://api.copy-paste.cloud"
API_KEY="${COPYPASTE_API_KEY:?COPYPASTE_API_KEY is not set. Generate a key at https://copy-paste.cloud/developer}"

response=$(curl -sS --fail-with-body \
  -H "Authorization: Bearer ${API_KEY}" \
  "${API_BASE}/api/v1/pastes/recent")

count=$(echo "$response" | jq 'length')
if [[ "$count" -eq 0 ]]; then
  echo "No recent public pastes found."
  exit 0
fi

echo "=== Recent public pastes on copy-paste.cloud ==="
echo ""

echo "$response" | jq -r '.[] | [
  "ID:       " + .id,
  "Title:    " + (if .title then .title else "(untitled)" end),
  "Language: " + (if .language then .language else "plain text" end),
  "Author:   " + (if .authorName then .authorName else "anonymous" end),
  "Created:  " + .createdAt,
  "Tags:     " + (if (.tags | length) > 0 then (.tags | join(", ")) else "none" end),
  "URL:      https://copy-paste.cloud/" + .id,
  "Preview:  " + (.content | split("\n")[0] | .[0:120]) + (if (.content | length) > 120 then "…" else "" end),
  "---"
] | .[]'
