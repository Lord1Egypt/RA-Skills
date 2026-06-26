#!/bin/bash
# Обновление access_token через refresh_token

CLIENT_ID="${YANDEX_DIRECT_CLIENT_ID:-your_client_id_here}"
CLIENT_SECRET="${YANDEX_DIRECT_CLIENT_SECRET:-your_client_secret_here}"
REFRESH_TOKEN="${YANDEX_DIRECT_REFRESH_TOKEN:-your_refresh_token_here}"

RESPONSE=$(curl -s -X POST "https://oauth.yandex.com/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token" \
  -d "refresh_token=${REFRESH_TOKEN}" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}")

echo "$RESPONSE" | jq .

# Извлечение access_token
ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
echo "New Access Token: $ACCESS_TOKEN"