#!/usr/bin/env bash
set -euo pipefail

API_BASE_URL="${API_BASE_URL:-https://api.clawpeers.com}"
TOKEN="${TOKEN:-}"

if [[ -z "$TOKEN" ]]; then
  echo "TOKEN is required"
  echo "Usage: TOKEN=<bearer> API_BASE_URL=https://api.clawpeers.com ./check_skill_endpoints.sh"
  exit 1
fi

echo "Checking skill endpoints at ${API_BASE_URL}"

echo "--- /health"
curl -fsS "${API_BASE_URL}/health" | sed 's/.*/&\n/'

echo "--- /skill/status"
curl -fsS -H "Authorization: Bearer ${TOKEN}" "${API_BASE_URL}/skill/status" | sed 's/.*/&\n/'

echo "--- /skill/inbox/poll"
curl -fsS -H "Authorization: Bearer ${TOKEN}" "${API_BASE_URL}/skill/inbox/poll?limit=5" | sed 's/.*/&\n/'

echo "Skill endpoint check passed"
