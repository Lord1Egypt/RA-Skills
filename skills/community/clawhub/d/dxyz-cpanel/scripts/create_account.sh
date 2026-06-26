#!/bin/bash
# Create cPanel Account
# Usage: create_account.sh <username> <domain> <password> [plan]

set -e

USERNAME="${1:?Username required}"
DOMAIN="${2:?Domain required}"
PASSWORD="${3:?Password required}"
PLAN="${4:-default}"

# Load config
source "$(dirname "$0")/cpanel_api.sh" 2>/dev/null || true

HOST="${CPANEL_HOST:?CPANEL_HOST not set}"
TOKEN="${CPANEL_TOKEN:?CPANEL_TOKEN not set}"

# Create account
echo "Creating account: $USERNAME ($DOMAIN)..."

RESPONSE=$(curl -s -H "Authorization: whm $TOKEN" \
    "${HOST}/json-api/createacct?api.version=1&username=${USERNAME}&domain=${DOMAIN}&password=${PASSWORD}&plan=${PLAN}")

# Parse response
RESULT=$(echo "$RESPONSE" | jq -r '.metadata.result // empty')
if [[ "$RESULT" == "1" ]]; then
    echo "✓ Account created successfully"
    echo "$RESPONSE" | jq '.data'
else
    echo "✗ Failed to create account"
    echo "$RESPONSE" | jq '.metadata.reason // .'
    exit 1
fi