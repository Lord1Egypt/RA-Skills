#!/bin/bash
# Check an IP's threat intelligence via SkillBoss API Hub
# Usage: check-ip.sh <ip>

set -euo pipefail

IP="${1:?Usage: check-ip.sh <ip>}"
API_KEY="${SKILLBOSS_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: No SkillBoss API key found. Set SKILLBOSS_API_KEY environment variable."
  exit 1
fi

RESPONSE=$(curl -s "https://api.heybossai.com/v1/pilot" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"search\", \"inputs\": {\"query\": \"IP reputation threat intelligence abuse report $IP\"}, \"prefer\": \"balanced\"}")

echo "$RESPONSE" | jq '.result'
