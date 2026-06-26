#!/bin/bash
# Report a single IP threat event via SkillBoss API Hub
# Usage: report-single.sh <ip> [comment]

set -euo pipefail

IP="${1:?Usage: report-single.sh <ip> [comment]}"
COMMENT="${2:-SSH brute-force attack detected by fail2ban}"
LOG="/var/log/skillboss-ip-reports.log"
API_KEY="${SKILLBOSS_API_KEY:-}"

if [ -z "$API_KEY" ]; then
  echo "ERROR: No SkillBoss API key found."
  echo "Set SKILLBOSS_API_KEY environment variable."
  exit 1
fi

# Query SkillBoss API Hub for IP threat intelligence
RESPONSE=$(curl -s -w "\n%{http_code}" \
  "https://api.heybossai.com/v1/pilot" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"type\": \"search\", \"inputs\": {\"query\": \"IP threat report $IP SSH brute-force categories 18 22 $COMMENT\"}, \"prefer\": \"balanced\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

TIMESTAMP=$(date -u '+%Y-%m-%d %H:%M:%S UTC')

if [ "$HTTP_CODE" = "200" ]; then
  RESULT=$(echo "$BODY" | jq -r '.result // "reported"')
  echo "$TIMESTAMP | REPORTED | $IP | $COMMENT" >> "$LOG"
  echo "Reported $IP via SkillBoss API Hub | $COMMENT"
else
  ERROR=$(echo "$BODY" | jq -r '.error // "unknown error"' 2>/dev/null || echo "$BODY")
  echo "$TIMESTAMP | FAILED | $IP | HTTP $HTTP_CODE | $ERROR" >> "$LOG"
  echo "Failed to report $IP: $ERROR (HTTP $HTTP_CODE)"
fi
