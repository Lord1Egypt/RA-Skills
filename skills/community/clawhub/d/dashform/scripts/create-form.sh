#!/bin/bash

# Create Form Script
# Reads form JSON data and calls MCP to create the form

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CREDENTIALS_FILE="$SCRIPT_DIR/../credentials.json"
MCP_URL="https://getaiform.com/api/mcp"

# Check if JSON file path is provided
if [ -z "$1" ]; then
    echo "Error: JSON file path is required"
    echo "Usage: $0 <path-to-form-json>"
    exit 1
fi

FORM_JSON_FILE="$1"

# Check if JSON file exists
if [ ! -f "$FORM_JSON_FILE" ]; then
    echo "Error: JSON file not found: $FORM_JSON_FILE"
    exit 1
fi

# Check if credentials exist
if [ ! -f "$CREDENTIALS_FILE" ]; then
    echo "Error: Credentials not found. Please run setup-credentials.sh first."
    exit 1
fi

echo "Dashform Form Creation..."

# Read credentials
USER_ID=$(grep -o '"userId": "[^"]*"' "$CREDENTIALS_FILE" | cut -d'"' -f4)
ORG_ID=$(grep -o '"organizationId": "[^"]*"' "$CREDENTIALS_FILE" | cut -d'"' -f4)

if [ -z "$USER_ID" ] || [ -z "$ORG_ID" ]; then
    echo "Error: Could not read credentials from $CREDENTIALS_FILE"
    exit 1
fi

echo "Using credentials:"
echo "  User ID: $USER_ID"
echo "  Organization ID: $ORG_ID"
echo ""

# Read form JSON
FORM_DATA=$(cat "$FORM_JSON_FILE")

# Check if jq is available for JSON merging
if command -v jq &> /dev/null; then
    # Use jq to merge credentials into form data
    MERGED_DATA=$(echo "$FORM_DATA" | jq --arg uid "$USER_ID" --arg oid "$ORG_ID" '. + {userId: $uid, organizationId: $oid}')
else
    # Fallback: manual JSON construction (basic, may not handle all cases)
    # Remove trailing } from form data and add credentials
    FORM_DATA_TRIMMED=$(echo "$FORM_DATA" | sed 's/}[[:space:]]*$//')
    MERGED_DATA="${FORM_DATA_TRIMMED}, \"userId\": \"$USER_ID\", \"organizationId\": \"$ORG_ID\"}"
fi

echo "Creating form..."
echo ""

# Call MCP create_form tool
RESPONSE=$(curl -s -X POST "$MCP_URL" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
            \"name\": \"create_form\",
            \"arguments\": $MERGED_DATA
        }
    }")

# Check if response is valid
if [ -z "$RESPONSE" ]; then
    echo "Error: Failed to create form"
    exit 1
fi

# Extract form ID and URLs from SSE response
# Response format: data: {"result":{"content":[{"type":"text","text":"..."}]}}
FORM_ID=$(echo "$RESPONSE" | grep -o '\\"formId\\": \\"[a-f0-9-]*\\"' | grep -o '[a-f0-9-]\{36\}' | head -1)
SHARE_URL=$(echo "$RESPONSE" | grep -o '\\"shareUrl\\": \\"[^\\]*\\"' | sed 's/\\"shareUrl\\": \\"\(.*\)\\"/\1/')
EDIT_URL=$(echo "$RESPONSE" | grep -o '\\"editUrl\\": \\"[^\\]*\\"' | sed 's/\\"editUrl\\": \\"\(.*\)\\"/\1/')

if [ -z "$FORM_ID" ]; then
    echo "Error: Could not create form"
    echo "Response: $RESPONSE"
    exit 1
fi

echo "Form created successfully!"
echo ""
echo "Form ID: $FORM_ID"
echo ""
echo "Share URL: $SHARE_URL"
echo "   (Share this link with your respondents)"
echo ""
echo "Edit URL: $EDIT_URL"
echo "   (Use this to customize your form)"
echo ""
