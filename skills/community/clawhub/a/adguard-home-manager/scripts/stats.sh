#!/usr/bin/env bash
#
# adguard-home/scripts/stats.sh
# Get AdGuard Home filtering statistics
# Usage: ./stats.sh [hour|day|week|month|year]
#

set -uo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
RESET='\033[0m'

log() { echo -e "${CYAN}[adguard]${RESET} $*"; }

# ── Config ─────────────────────────────────────────────────────────────────────
ADGUARD_USERNAME="${ADGUARD_USERNAME:?ADGUARD_USERNAME not set}"
ADGUARD_PASSWORD="${ADGUARD_PASSWORD:?ADGUARD_PASSWORD not set}"
ADGUARD_BASE_URL="${ADGUARD_BASE_URL:-http://localhost:3000}"

AUTH=$(echo -n "${ADGUARD_USERNAME}:${ADGUARD_PASSWORD}" | base64)

# ── Args ───────────────────────────────────────────────────────────────────────
PERIOD="${1:-day}"

log "Fetching ${PERIOD} stats..."

response=$(curl -s "${ADGUARD_BASE_URL}/control/stats" \
  -H "Authorization: Basic ${AUTH}" \
  -d "{\"period\":\"${PERIOD}\"}" \
  -H "Content-Type: application/json" 2>/dev/null)

if echo "$response" | jq -e '. // empty' >/dev/null 2>&1; then
  :
else
  echo "Error fetching stats: $response"
  exit 1
fi

# Extract values
total_dns=$(echo "$response" | jq -r '.dns_queries_total // 0')
blocked_dns=$(echo "$response" | jq -r '.blocked_total // 0')
replaced=$(echo "$response" | jq -r '.replaced_total // 0')
num_blocked_filtering=$(echo "$response" | jq -r '.num_blocked_filtering // 0')
num_allowed_filtering=$(echo "$response" | jq -r '.num_allowed_filtering // 0')
blocked_domains=$(echo "$response" | jq -r '.blocked_domains // [] | length')
top_blocked=$(echo "$response" | jq -r '.top_blocked_domains // []')

block_rate=$(echo "scale=1; $num_blocked_filtering * 100 / ($num_blocked_filtering + $num_allowed_filtering)" 2>/dev/null | grep -v error || echo "0.0")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "     📊 AdGuard Stats — ${PERIOD}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Total DNS queries:  ${total_dns}"
echo "  Blocked:            ${num_blocked_filtering}"
echo "  Allowed:            ${num_allowed_filtering}"
echo "  Block rate:         ${block_rate}%"
echo ""
echo "  Top blocked domains:"
if [[ $(echo "$top_blocked" | jq 'length') -gt 0 ]]; then
  echo "$top_blocked" | jq -r '.[:10] | .[] | "    \(.domain) — \(.count)x"'
else
  echo "    (none in this period)"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
