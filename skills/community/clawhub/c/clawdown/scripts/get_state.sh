#!/usr/bin/env bash
# Get the current state of a match
# Usage: ./get_state.sh <match_id>
set -euo pipefail

MATCH_ID="${1:?Usage: get_state.sh <match_id>}"

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

curl -s -H "Authorization: Bearer ${API_KEY}" \
  "${API_BASE}/matches/${MATCH_ID}/state"
