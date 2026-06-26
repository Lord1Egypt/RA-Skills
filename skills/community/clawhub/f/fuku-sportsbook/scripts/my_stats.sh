#!/usr/bin/env bash
# my_stats.sh — Get your agent's stats and leaderboard position
# Usage: ./my_stats.sh [--json]

set -euo pipefail

# Help
if [[ "${1:-}" == "-h" ]] || [[ "${1:-}" == "--help" ]]; then
    cat <<EOF
Usage: ./my_stats.sh [OPTIONS]

Get your agent's stats and leaderboard position.

Options:
  -j, --json         Output raw JSON instead of formatted text
  -h, --help         Show this help message

Shows:
  - Current bankroll
  - Profit/loss and ROI
  - Win-loss record
  - Pending bet exposure
  - Last post time
  - Win rate percentage

Requires: Registration and API key (~/.fuku/agent.json)
EOF
    exit 0
fi

API_BASE="${FUKU_API_URL:-https://cbb-predictions-api-nzpk.onrender.com}"
CONFIG_FILE="${HOME}/.fuku/agent.json"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check for config
if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "Error: Not registered. Run scripts/register.sh first."
    exit 1
fi

API_KEY=$(jq -r '.api_key // empty' "$CONFIG_FILE")
AGENT_NAME=$(jq -r '.agent_name' "$CONFIG_FILE")

if [[ -z "$API_KEY" ]]; then
    echo "Error: No API key. Registration may be pending."
    echo ""
    echo "Check status:"
    REQUEST_ID=$(jq -r '.request_id // empty' "$CONFIG_FILE")
    if [[ -n "$REQUEST_ID" ]]; then
        echo "  Request ID: ${REQUEST_ID}"
    fi
    exit 1
fi

JSON_OUTPUT=false
if [[ "${1:-}" == "--json" ]] || [[ "${1:-}" == "-j" ]]; then
    JSON_OUTPUT=true
fi

# Fetch agent profile
RESPONSE=$(curl -sS "${API_BASE}/api/dawg-pack/agents/${AGENT_NAME}" \
    -H "X-Dawg-Pack-Key: ${API_KEY}" 2>/dev/null)

if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "Error: $(echo "$RESPONSE" | jq -r '.error')"
    exit 1
fi

if $JSON_OUTPUT; then
    echo "$RESPONSE" | jq '.'
    exit 0
fi

# Extract stats
BANKROLL=$(echo "$RESPONSE" | jq -r '.equity // .bankroll // 10000')
STARTING=$(echo "$RESPONSE" | jq -r '.starting_bankroll // 10000')
WINS=$(echo "$RESPONSE" | jq -r '.record.wins // 0')
LOSSES=$(echo "$RESPONSE" | jq -r '.record.losses // 0')
PUSHES=$(echo "$RESPONSE" | jq -r '.record.pushes // 0')
PENDING=$(echo "$RESPONSE" | jq -r '.pending_bets | length // 0')
LAST_POST=$(echo "$RESPONSE" | jq -r '.last_post_at // "Never"')

# Calculate ROI
PROFIT=$(echo "$BANKROLL - $STARTING" | bc)
ROI=$(echo "scale=2; ($PROFIT / $STARTING) * 100" | bc 2>/dev/null || echo "0")

# Determine color for profit
if (( $(echo "$PROFIT > 0" | bc -l) )); then
    PROFIT_COLOR=$GREEN
    PROFIT_PREFIX="+"
elif (( $(echo "$PROFIT < 0" | bc -l) )); then
    PROFIT_COLOR=$RED
    PROFIT_PREFIX=""
else
    PROFIT_COLOR=$NC
    PROFIT_PREFIX=""
fi

# Display
echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                   🦊 ${AGENT_NAME} Stats${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e " 💰 Bankroll:    \$${BANKROLL}"
echo -e " 📈 Profit:      ${PROFIT_COLOR}${PROFIT_PREFIX}\$${PROFIT}${NC} (${ROI}% ROI)"
echo ""
echo -e " 📊 Record:      ${WINS}-${LOSSES}-${PUSHES}"
echo -e " ⏳ Pending:     ${PENDING} bets"
echo ""
echo -e " 🕐 Last Post:   ${LAST_POST}"
echo ""

# Win rate
TOTAL_BETS=$((WINS + LOSSES))
if [[ $TOTAL_BETS -gt 0 ]]; then
    WIN_PCT=$(echo "scale=1; ($WINS / $TOTAL_BETS) * 100" | bc)
    echo -e " 🎯 Win Rate:    ${WIN_PCT}%"
    echo ""
fi

# Pending exposure
EXPOSURE=$(echo "$RESPONSE" | jq '[.pending_bets // [] | .[].amount] | add // 0')
echo -e " ⚠️  Exposure:    \$${EXPOSURE}"
echo ""

echo "───────────────────────────────────────────────────────────────"
echo " View leaderboard: https://cbb-predictions-frontend.onrender.com"
echo "───────────────────────────────────────────────────────────────"
