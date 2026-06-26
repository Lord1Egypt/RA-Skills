#!/bin/bash
# cPanel API Caller - Generic wrapper for cPanel/WHM API calls
# Usage: cpanel_api.sh <api_type> <endpoint> [params...]
# api_type: whm | uapi | cpanel2

set -e

# Configuration
CONFIG_FILE="${CPANEL_CONFIG:-$HOME/.cpanel/config.json}"
HOST="${CPANEL_HOST}"
TOKEN="${CPANEL_TOKEN}"
USER="${CPANEL_USER:-root}"

# Load config if exists
if [[ -f "$CONFIG_FILE" ]]; then
    HOST=$(jq -r '.host // empty' "$CONFIG_FILE" 2>/dev/null || echo "$HOST")
    TOKEN=$(jq -r '.token // empty' "$CONFIG_FILE" 2>/dev/null || echo "$TOKEN")
fi

# Validate
if [[ -z "$HOST" || -z "$TOKEN" ]]; then
    echo "Error: CPANEL_HOST and CPANEL_TOKEN must be set"
    echo "Set environment variables or create $CONFIG_FILE"
    exit 1
fi

# Arguments
API_TYPE="${1:-whm}"
ENDPOINT="${2}"
shift 2 2>/dev/null || true
PARAMS="$@"

# Build URL and auth header
case "$API_TYPE" in
    whm)
        URL="${HOST}/json-api/${ENDPOINT}"
        AUTH_HEADER="Authorization: whm ${TOKEN}"
        ;;
    uapi)
        URL="${HOST}/execute/${ENDPOINT}"
        AUTH_HEADER="Authorization: cpanel ${TOKEN}"
        ;;
    cpanel2)
        URL="${HOST}/json-api/cpanel2"
        AUTH_HEADER="Authorization: cpanel ${TOKEN}"
        ;;
    *)
        echo "Error: Invalid API type. Use: whm, uapi, or cpanel2"
        exit 1
        ;;
esac

# Append params
if [[ -n "$PARAMS" ]]; then
    URL="${URL}?${PARAMS}"
fi

# Make request
RESPONSE=$(curl -s -w "\n%{http_code}" -H "$AUTH_HEADER" "$URL")
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Output
if [[ "$HTTP_CODE" -eq 200 ]]; then
    echo "$BODY" | jq .
else
    echo "HTTP Error: $HTTP_CODE"
    echo "$BODY" | jq . 2>/dev/null || echo "$BODY"
    exit 1
fi