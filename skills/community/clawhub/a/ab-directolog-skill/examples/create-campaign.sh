#!/bin/bash
# Пример: создание новой кампании

ACCESS_TOKEN="${YANDEX_DIRECT_ACCESS_TOKEN:-your_access_token_here}"

curl -s -X POST "https://api.direct.yandex.com/json/v5/campaigns" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "add",
    "params": {
      "Campaigns": [
        {
          "Name": "Новая кампания 2026",
          "CampaignType": "TEXT",
          "DailyBudget": {
            "Amount": 50000
          },
          "StartDate": "2026-05-10",
          "TimeZone": "Europe/Moscow"
        }
      ]
    }
  }' | jq .