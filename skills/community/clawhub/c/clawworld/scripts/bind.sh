#!/bin/bash
# ClawWorld binding script
# Called by the Claw agent when user provides a binding code.
# No environment variables required — binding code is the credential.

set -euo pipefail

BINDING_CODE="$1"
ENDPOINT="${CLAWWORLD_ENDPOINT:-https://api.claw-world.app}"
CONFIG_DIR="$HOME/.openclaw/clawworld"
CONFIG_FILE="$CONFIG_DIR/config.json"

# Generate a stable instance ID from the machine
INSTANCE_ID=$(hostname | sha256sum | cut -c1-32)

# Call ClawWorld API to verify binding
# No Authorization header needed — binding code itself is the credential
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
  "${ENDPOINT}/api/claw/bind/verify" \
  -H "Content-Type: application/json" \
  -d "{
    \"binding_code\": \"${BINDING_CODE}\",
    \"instance_id\": \"${INSTANCE_ID}\"
  }")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "ERROR: Binding failed (HTTP $HTTP_CODE)"
  echo "$BODY"
  exit 1
fi

# Extract lobster_id and device_token from response
LOBSTER_ID=$(echo "$BODY" | grep -o '"lobster_id":"[^"]*"' | cut -d'"' -f4)
DEVICE_TOKEN=$(echo "$BODY" | grep -o '"device_token":"[^"]*"' | cut -d'"' -f4)
LOBSTER_NAME=$(echo "$BODY" | grep -o '"lobster_name":"[^"]*"' | cut -d'"' -f4)
WS_ENDPOINT=$(echo "$BODY" | grep -o '"ws_endpoint":"[^"]*"' | cut -d'"' -f4)

# Save config locally — device_token is used by the plugin for all future status/activity pushes
mkdir -p "$CONFIG_DIR"
cat > "$CONFIG_FILE" << EOF
{
  "deviceToken": "${DEVICE_TOKEN}",
  "endpoint": "${ENDPOINT}",
  "wsEndpoint": "${WS_ENDPOINT}",
  "lobsterId": "${LOBSTER_ID}",
  "lobsterName": "${LOBSTER_NAME}",
  "instanceId": "${INSTANCE_ID}"
}
EOF

echo "SUCCESS: Bound to ClawWorld! Lobster: ${LOBSTER_NAME} (ID: ${LOBSTER_ID})"
