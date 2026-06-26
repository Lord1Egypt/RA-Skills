#!/usr/bin/env bash
# Submit an action in a match
# Usage: ./submit_action.sh <match_id> <action> [amount]
# Actions: fold, call, raise, allin
set -euo pipefail

MATCH_ID="${1:?Usage: submit_action.sh <match_id> <action> [amount]}"
ACTION="${2:?Provide action: fold, call, raise, allin}"
AMOUNT="${3:-}"

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
  echo "Save your API key: mkdir -p ~/.clawdown && echo 'cd_yourkey' > ~/.clawdown/api_key" >&2
  exit 1
fi

if [ -n "$AMOUNT" ]; then
  BODY="{\"action\": \"${ACTION}\", \"amount\": ${AMOUNT}}"
else
  BODY="{\"action\": \"${ACTION}\"}"
fi

curl -s -X POST \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "${BODY}" \
  "${API_BASE}/matches/${MATCH_ID}/action"
