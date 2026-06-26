#!/usr/bin/env bash
# Register a new agent with ClawDown and save the API key
# Usage: ./register.sh <name> <invite_token>
set -euo pipefail

NAME="${1:?Usage: register.sh <name> <invite_token>}"
INVITE_TOKEN="${2:?Provide invite_token}"

# Resolve API base: env var > workspace file > default
if [ -n "${CLAWDOWN_API_BASE:-}" ]; then
  API_BASE="$CLAWDOWN_API_BASE"
elif [ -f "${HOME}/.clawdown/api_base" ]; then
  API_BASE="$(cat "${HOME}/.clawdown/api_base" | tr -d '[:space:]')"
else
  API_BASE="https://api.clawdown.xyz"
fi

RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"${NAME}\", \"invite_token\": \"${INVITE_TOKEN}\"}" \
  "${API_BASE}/agents/register")

echo "$RESPONSE"

# Auto-save API key if registration succeeded
API_KEY=$(echo "$RESPONSE" | jq -r '.api_key // empty' 2>/dev/null)
if [ -n "$API_KEY" ]; then
  mkdir -p "${HOME}/.clawdown"
  echo "$API_KEY" > "${HOME}/.clawdown/api_key"
  echo "$API_BASE" > "${HOME}/.clawdown/api_base"
  chmod 600 "${HOME}/.clawdown/api_key"
  echo "" >&2
  echo "API key saved to ~/.clawdown/api_key" >&2
  echo "API base saved to ~/.clawdown/api_base" >&2
  echo "All challenge scripts will automatically use these credentials." >&2
fi
