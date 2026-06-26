#!/bin/bash

# Dashform Credentials Setup Script
# This script uses the MCP get_user_info tool to cache credentials

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$SCRIPT_DIR/../credentials.json"
MCP_URL="https://getaiform.com/api/mcp"

echo "Dashform Credentials Setup..."


# Get session token from argument or prompt
if [ -n "$1" ]; then
    SESSION_TOKEN="$1"
else
    echo "Step 1: Get your session token"
    echo "1. Sign in to https://getaiform.com"
    echo "2. Open browser DevTools (F12)"
    echo "3. Go to Application → Cookies"
    echo "4. Find 'better-auth.session_token'"
    echo "5. Copy its value"
    echo ""
    read -p "Paste your session token: " SESSION_TOKEN
fi

if [ -z "$SESSION_TOKEN" ]; then
    echo "Error: Session token is required"
    exit 1
fi

echo ""
echo "Fetching your user information via MCP..."

# Call MCP get_user_info tool
RESPONSE=$(curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
            \"name\": \"get_user_info\",
            \"arguments\": {
                \"sessionToken\": \"$SESSION_TOKEN\"
            }
        }
    }")

# Check if response is valid
if [ -z "$RESPONSE" ]; then
    echo "Error: Failed to fetch user information"
    exit 1
fi

# Extract all user information from response
USER_ID=$(echo "$RESPONSE" | grep -o 'userId[^a-f0-9-]*[a-f0-9-]\{36\}' | grep -o '[a-f0-9-]\{36\}' | head -1)
ORG_ID=$(echo "$RESPONSE" | grep -o 'organizationId[^a-f0-9-]*[a-f0-9-]\{36\}' | grep -o '[a-f0-9-]\{36\}' | head -1)
USER_NAME=$(echo "$RESPONSE" | grep -o '"userName":"[^"]*"' | cut -d'"' -f4)
USER_EMAIL=$(echo "$RESPONSE" | grep -o '"userEmail":"[^"]*"' | cut -d'"' -f4)

if [ -z "$USER_ID" ] || [ -z "$ORG_ID" ]; then
    echo "Error: Could not extract user information"
    echo "Response: $RESPONSE"
    exit 1
fi

# Save credentials
mkdir -p "$(dirname "$CREDENTIALS_FILE")"
cat > "$CREDENTIALS_FILE" << JSON
{
  "userId": "$USER_ID",
  "organizationId": "$ORG_ID",
  "userName": "$USER_NAME",
  "userEmail": "$USER_EMAIL",
  "cachedAt": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
JSON

echo ""
echo "Credentials saved successfully!"
echo ""
echo "User: $USER_NAME ($USER_EMAIL)"
echo "User ID: $USER_ID"
echo "Organization ID: $ORG_ID"
echo ""
echo "You can now use the Dashform agent skill without manually providing credentials."
echo "Credentials are cached in: $CREDENTIALS_FILE"
