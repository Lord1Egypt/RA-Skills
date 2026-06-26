#!/usr/bin/env bash
#
# adguard-home/scripts/toggle_filtering.sh
# Enable or disable AdGuard Home DNS filtering
# Usage: ./toggle_filtering.sh true|false
#

set -uo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

log()  { echo -e "${CYAN}[adguard]${RESET} $*"; }
pass() { echo -e "${GREEN}✅ $*${RESET}"; }
err()  { echo -e "${RED}❌ $*${RESET}" >&2; }

# ── Config ─────────────────────────────────────────────────────────────────────
ADGUARD_USERNAME="${ADGUARD_USERNAME:?ADGUARD_USERNAME not set}"
ADGUARD_PASSWORD="${ADGUARD_PASSWORD:?ADGUARD_PASSWORD not set}"
ADGUARD_BASE_URL="${ADGUARD_BASE_URL:-http://localhost:3000}"

AUTH=$(echo -n "${ADGUARD_USERNAME}:${ADGUARD_PASSWORD}" | base64)

# ── Args ───────────────────────────────────────────────────────────────────────
ENABLE="${1:-}"

if [[ "$ENABLE" != "true" && "$ENABLE" != "false" ]]; then
  echo "Usage: $0 true|false"
  exit 1
fi

enabled_val=$([[ "$ENABLE" == "true" ]] && echo "true" || echo "false")

log "Setting DNS filtering to ${ENABLE}..."

response=$(curl -s -X POST "${ADGUARD_BASE_URL}/control/dns_config" \
  -H "Authorization: Basic ${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{\"filtering_enabled\":${enabled_val}}" 2>/dev/null)

if [[ $? -eq 0 ]]; then
  if [[ "$ENABLE" == "true" ]]; then
    pass "DNS filtering is now ENABLED"
  else
    pass "DNS filtering is now DISABLED"
    echo "⚠️  Warning: Disabling filtering means ads and trackers will resolve normally."
  fi
else
  err "Failed to update DNS config. Response: $response"
  exit 1
fi
