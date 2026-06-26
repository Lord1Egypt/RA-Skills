#!/bin/bash
# Пример: получить список кампаний через Yandex.Direct API v5

ACCESS_TOKEN="${YANDEX_DIRECT_ACCESS_TOKEN:-your_access_token_here}"

curl -s -X POST "https://api.direct.yandex.com/json/v5/campaigns" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "get",
    "params": {
      "SelectionCriteria": {},
      "FieldNames": ["Id", "Name", "Status", "DailyBudget", "AvgCpc", "Impressions", "Clicks"],
      "Page": {
        "Limit": 100,
        "Offset": 0
      }
    }
  }' | jq .