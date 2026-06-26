#!/bin/bash
# ClawWorld unbind script
# Called by the Claw agent when user requests to disconnect from ClawWorld.
# Reads device_token and lobster_id from config.json — no arguments required.

set -euo pipefail

CONFIG_DIR="$HOME/.openclaw/clawworld"
CONFIG_FILE="$CONFIG_DIR/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: Not bound to ClawWorld (config.json not found)"
  exit 1
fi

DEVICE_TOKEN=$(grep -o '"deviceToken": "[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
LOBSTER_ID=$(grep -o '"lobsterId": "[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)
ENDPOINT=$(grep -o '"endpoint": "[^"]*"' "$CONFIG_FILE" | cut -d'"' -f4)

if [ -z "$DEVICE_TOKEN" ] || [ -z "$LOBSTER_ID" ] || [ -z "$ENDPOINT" ]; then
  echo "ERROR: config.json is missing required fields (deviceToken, lobsterId, endpoint)"
  exit 1
fi

RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "${ENDPOINT}/api/claw/unbind" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEVICE_TOKEN}" \
  -d "{\"lobster_id\": \"${LOBSTER_ID}\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "ERROR: Unbind failed (HTTP $HTTP_CODE)"
  echo "$BODY"
  exit 1
fi

# Remove local config — device_token is no longer valid
rm -f "$CONFIG_FILE"

echo "SUCCESS: Disconnected from ClawWorld. Your lobster has gone offline."
