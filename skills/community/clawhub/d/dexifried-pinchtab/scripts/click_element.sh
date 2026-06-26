#!/bin/bash

URL="http://localhost:9867/click"
TOKEN="b6a91002205211861a1840bc7d1f55e98757ba635436b5a7"

if [ -z "$1" ]; then
  echo "Usage: $0 <css_selector>"
  exit 1
fi

data=$(jq -n --arg selector "$1" '{selector: $selector}')

curl -X POST "$URL" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d "$data"