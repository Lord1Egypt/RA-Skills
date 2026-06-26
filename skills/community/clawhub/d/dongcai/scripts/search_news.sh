#!/bin/bash

# Check if query is provided
if [ -z "$1" ]; then
  echo "Usage: ./search_news.sh <query>"
  exit 1
fi

QUERY="$1"
APIKEY="$MX_APIKEY" # Assumes MX_APIKEY is set in environment or .env

if [ -z "$APIKEY" ]; then
  echo "Error: MX_APIKEY environment variable is not set."
  exit 1
fi

curl -X POST --location 'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
--header 'Content-Type: application/json' \
--header "apikey:$APIKEY" \
--data "{\"query\":\"$QUERY\"}"