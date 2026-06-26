#!/bin/bash
# Bright Data Web Scraping Script
# Requires: BRIGHTDATA_API_KEY, BRIGHTDATA_UNLOCKER_ZONE set in environment
# Usage: bash scrape.sh "url"

URL="$1"

if [ -z "$URL" ]; then
  echo "Error: URL is required"
  echo "Usage: $0 \"url\""
  exit 1
fi

if [ -z "$BRIGHTDATA_API_KEY" ] || [ -z "$BRIGHTDATA_UNLOCKER_ZONE" ]; then
  echo "Error: Please set BRIGHTDATA_API_KEY and BRIGHTDATA_UNLOCKER_ZONE environment variables"
  exit 1
fi

# Use Bright Data Web Unlocker to fetch the page and convert to markdown
RESPONSE=$(curl -s -H "Authorization: Bearer $BRIGHTDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"zone\":\"$BRIGHTDATA_UNLOCKER_ZONE\",\"url\":\"$URL\",\"format\":\"markdown\"}" \
  https://api.brightdata.com/request)

# Check if we got a response
if [ -z "$RESPONSE" ]; then
  echo "Error: No response from Bright Data API"
  exit 1
fi

# Output the markdown content
echo "$RESPONSE"