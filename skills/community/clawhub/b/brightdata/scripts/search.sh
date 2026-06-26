#!/bin/bash
# Bright Data Google Search Script using SERP API
# Requires: BRIGHTDATA_API_KEY, BRIGHTDATA_SERP_ZONE set in environment
# Usage: bash search.sh "query" [cursor]

QUERY="$1"
CURSOR="${2:-0}"

if [ -z "$QUERY" ]; then
  echo "Error: Query is required"
  echo "Usage: $0 \"search query\" [cursor]"
  exit 1
fi

if [ -z "$BRIGHTDATA_API_KEY" ] || [ -z "$BRIGHTDATA_SERP_ZONE" ]; then
  echo "Error: Please set BRIGHTDATA_API_KEY and BRIGHTDATA_SERP_ZONE environment variables"
  exit 1
fi

# Construct Google search URL
URL="https://www.google.com/search?q=$(echo "$QUERY" | sed 's/ /+/g')&hl=en&gl=us&num=10&start=$((CURSOR * 10))"

# Use Bright Data SERP API to get structured results
RESPONSE=$(curl -s -X POST https://api.brightdata.com/request \
  -H "Authorization: Bearer $BRIGHTDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"zone\": \"$BRIGHTDATA_SERP_ZONE\",
    \"url\": \"$URL\",
    \"format\": \"json\",
    \"data_format\": \"parsed_light\"
  }")

# Check if we got a response
if [ -z "$RESPONSE" ] || [ "$RESPONSE" = "{}" ]; then
  echo "Error: No response from Bright Data SERP API"
  exit 1
fi

# Output the JSON response
echo "$RESPONSE"