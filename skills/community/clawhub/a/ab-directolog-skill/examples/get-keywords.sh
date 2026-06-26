#!/bin/bash
# Пример: получить ключевые слова кампании

ACCESS_TOKEN="${YANDEX_DIRECT_ACCESS_TOKEN:-your_access_token_here}"
CAMPAIGN_ID="${1:-123456}"

curl -s -X POST "https://api.direct.yandex.com/json/v5/keywords" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"method\": \"get\",
    \"params\": {
      \"SelectionCriteria\": {
        \"CampaignIds\": [${CAMPAIGN_ID}]
      },
      \"FieldNames\": [\"Id\", \"Keyword\", \"Bid\", \"Competition\", \"Lowctrbid\", \"AvgCpc\"]
    }
  }" | jq .