#!/bin/bash
# USDA FoodData Central API - Food Search
# Usage: fdc_search.sh "search query" [pageSize] [dataType]

# Configuration
API_BASE="https://api.nal.usda.gov/fdc/v1"

# Check for API key
if [ -z "$FDC_API_KEY" ]; then
    echo "❌ Error: FDC_API_KEY environment variable is not set."
    echo ""
    echo "To get an API key:"
    echo "1. Visit: https://fdc.nal.usda.gov/api-key-signup"
    echo "2. Fill out: First Name, Last Name, Email"
    echo "3. Check your email for the 40-character API key"
    echo "4. Add to ~/.openclaw/openclaw.json:"
    echo '   {"env": {"FDC_API_KEY": "your-api-key-here"}}'
    exit 1
fi

# Parse arguments
QUERY="$1"
PAGE_SIZE="${2:-10}"
DATA_TYPE="$3"

if [ -z "$QUERY" ]; then
    echo "Usage: fdc_search.sh \"search query\" [pageSize] [dataType]"
    echo "  dataType options: Branded, Foundation, Survey (FNDDS), SR Legacy"
    exit 1
fi

# Build JSON payload
if [ -n "$DATA_TYPE" ]; then
    JSON_PAYLOAD=$(jq -n \
        --arg query "$QUERY" \
        --argjson pageSize "$PAGE_SIZE" \
        --arg dataType "$DATA_TYPE" \
        '{query: $query, pageSize: $pageSize, dataType: [$dataType]}')
else
    JSON_PAYLOAD=$(jq -n \
        --arg query "$QUERY" \
        --argjson pageSize "$PAGE_SIZE" \
        '{query: $query, pageSize: $pageSize}')
fi

# Make API request
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -H "X-Api-Key: $FDC_API_KEY" \
    -d "$JSON_PAYLOAD" \
    "${API_BASE}/foods/search")

# Separate body and status code
HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | sed '$d')

# Check for errors
case "$HTTP_CODE" in
    200)
        # Success - process results
        ;;
    403)
        ERROR_CODE=$(echo "$BODY" | jq -r '.error.code // "UNKNOWN"' 2>/dev/null)
        if [ "$ERROR_CODE" = "API_KEY_MISSING" ]; then
            echo "❌ Error: API key is missing. Please set FDC_API_KEY environment variable."
        elif [ "$ERROR_CODE" = "API_KEY_INVALID" ]; then
            echo "❌ Error: API key is invalid. Please verify your API key."
        else
            echo "❌ Error: Authentication failed (HTTP 403)"
        fi
        exit 1
        ;;
    429)
        echo "❌ Error: Rate limit exceeded. You have made too many requests."
        echo "Please wait 1 hour before trying again."
        REMAINING=$(echo "$BODY" | jq -r '.headers["X-RateLimit-Remaining"] // "unknown"' 2>/dev/null)
        echo "Remaining requests: $REMAINING"
        exit 1
        ;;
    400)
        echo "❌ Error: Bad request (HTTP 400)"
        echo "$BODY" | jq -r '.error.message // .message // "Unknown error"' 2>/dev/null
        exit 1
        ;;
    *)
        echo "❌ Error: Unexpected HTTP status code: $HTTP_CODE"
        exit 1
        ;;
esac

# Parse and display results
echo "# Search Results: \"$QUERY\""
echo ""

TOTAL_HITS=$(echo "$BODY" | jq -r '.totalHits // 0')
echo "Total hits: $TOTAL_HITS"
echo ""

if [ "$TOTAL_HITS" -eq 0 ]; then
    echo "No foods found matching your search query."
    exit 0
fi

# Display results as a markdown table
echo "| FDC ID | Description | Data Type | Brand Owner |"
echo "|--------|-------------|-----------|-------------|"

echo "$BODY" | jq -r '.foods[] | [
    .fdcId,
    (.description | gsub("\\|"; "\\|")),
    .dataType,
    (.brandOwner // "N/A")
] | @tsv' 2>/dev/null | while IFS=$'\t' read -r fdcId description dataType brandOwner; do
    echo "| $fdcId | $description | $dataType | $brandOwner |"
done

echo ""
echo "To get full nutritional details, use: ./skills/fdc-api/scripts/fdc_food.sh <fdcId>"
