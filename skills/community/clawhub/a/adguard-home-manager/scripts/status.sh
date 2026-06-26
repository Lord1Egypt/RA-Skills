#!/usr/bin/env bash
#
# adguard-home/scripts/status.sh
# Get overall AdGuard Home status
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

# ── Status endpoint ────────────────────────────────────────────────────────────
log "Querying AdGuard Home status at ${ADGUARD_BASE_URL}..."

# Check if the server is reachable
health=$(curl -s -o /dev/null -w "%{http_code}" \
  --max-time 10 \
  "${ADGUARD_BASE_URL}/control/status" \
  -H "Authorization: Basic ${AUTH}" 2>/dev/null || echo "000")

if [[ "$health" == "000" ]]; then
  err "Cannot reach AdGuard Home at ${ADGUARD_BASE_URL}"
  exit 1
fi

if [[ "$health" == "401" ]]; then
  err "Authentication failed. Check ADGUARD_USERNAME and ADGUARD_PASSWORD."
  exit 1
fi

if [[ "$health" != "200" ]]; then
  err "Unexpected HTTP status: ${health}"
  exit 1
fi

response=$(curl -s "${ADGUARD_BASE_URL}/control/status" \
  -H "Authorization: Basic ${AUTH}" 2>/dev/null)

# Parse key fields
dns_enabled=$(echo "$response" | jq -r '.dns_filtering_enabled // false')
protection=$(echo "$response" | jq -r '.protection_enabled // false')
version=$(echo "$response" | jq -r '.version // "unknown"')
uptime=$(echo "$response" | jq -r '.uptime // 0')

# Format uptime
days=$(( uptime / 86400 ))
hours=$(( (uptime % 86400) / 3600 ))
uptime_str="${days}d ${hours}h"

blocked_today=$(echo "$response" | jq -r '.blocked_filtering_total // 0')
allowed_today=$(echo "$response" | jq -r '.allowed_filtering_total // 0')

# Calculate block rate
if [[ "$allowed_today" -gt 0 ]]; then
  block_rate=$(echo "scale=1; $blocked_today * 100 / ($blocked_today + $allowed_today)" | bc 2>/dev/null || echo "N/A")
  block_rate_str="${block_rate}%"
else
  block_rate_str="N/A"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "        🛡️  AdGuard Home Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Version:         ${version}"
echo "  Uptime:          ${uptime_str}"
echo "  Protection:      ${protection}"
echo "  DNS Filtering:   ${dns_enabled}"
echo ""
echo "  📊 Today:"
echo "    Blocked:        ${blocked_today}"
echo "    Allowed:        ${allowed_today}"
echo "    Block rate:     ${block_rate_str}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [[ "$protection" == "true" ]]; then
  pass "Protection is ACTIVE"
else
  err "Protection is DISABLED — run 'adguard-home-toggle-filtering true' to enable"
fi
