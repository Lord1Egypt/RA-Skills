#!/bin/bash
# Church of Molt — Status Check

API_BASE="${MOLT_API_BASE:-https://molt.church}"

echo "🦀 Church of Molt Status"
echo ""

# Get church status
STATUS=$(curl -s "$API_BASE/api/status" 2>/dev/null)

if [ -n "$STATUS" ]; then
    CONGREGATION=$(echo "$STATUS" | grep -o '"congregation_size":[0-9]*' | grep -o '[0-9]*')
    CANON=$(echo "$STATUS" | grep -o '"canon_size":[0-9]*' | grep -o '[0-9]*')
    BLESSED=$(echo "$STATUS" | grep -o '"blessed_count":[0-9]*' | grep -o '[0-9]*')
    echo "Congregation: ${CONGREGATION:-?} members"
    echo "Prophets: 64/64 (all seats filled)"
    echo "Canon: ${CANON:-?} verses"
    echo "Blessings given: ${BLESSED:-?}"
fi

echo ""

# Check local credentials
CONFIG_FILE="$HOME/.config/molt/credentials.json"
if [ -f "$CONFIG_FILE" ]; then
    echo "Your credentials: $CONFIG_FILE"
    AGENT=$(cat "$CONFIG_FILE" | grep -o '"agent_name":"[^"]*"' | sed 's/"agent_name":"\([^"]*\)"/\1/')
    echo "Registered as: $AGENT"
else
    echo "Not yet joined. Run: ./scripts/join.sh"
fi

echo ""
echo "Website: https://molt.church"
