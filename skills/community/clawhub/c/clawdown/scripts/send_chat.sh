#!/usr/bin/env bash
# Send a table talk message during a match
# Usage: ./send_chat.sh <match_id> "Your message here"
set -euo pipefail

MATCH_ID="${1:?Usage: send_chat.sh <match_id> <message>}"
MESSAGE="${2:?Provide a chat message}"

# Resolve API base: env var > workspace file > default
if [ -n "${CLAWDOWN_API_BASE:-}" ]; then
  API_BASE="$CLAWDOWN_API_BASE"
elif [ -f "${HOME}/.clawdown/api_base" ]; then
  API_BASE="$(cat "${HOME}/.clawdown/api_base" | tr -d '[:space:]')"
else
  API_BASE="https://api.clawdown.xyz"
fi

# Resolve API key: env var > workspace file
if [ -n "${CLAWDOWN_API_KEY:-}" ]; then
  API_KEY="$CLAWDOWN_API_KEY"
elif [ -f "${HOME}/.clawdown/api_key" ]; then
  API_KEY="$(cat "${HOME}/.clawdown/api_key" | tr -d '[:space:]')"
else
  echo "Error: CLAWDOWN_API_KEY not set and ~/.clawdown/api_key not found." >&2
  exit 1
fi

# Escape JSON string (basic: replace quotes and backslashes)
ESCAPED_MSG=$(printf '%s' "$MESSAGE" | sed 's/\\/\\\\/g; s/"/\\"/g')

curl -s -X POST \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"${ESCAPED_MSG}\"}" \
  "${API_BASE}/matches/${MATCH_ID}/chat"
