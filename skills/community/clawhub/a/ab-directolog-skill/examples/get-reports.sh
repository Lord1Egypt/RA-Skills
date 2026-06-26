#!/bin/bash
# Пример: получить отчёт по кампаниям за период

ACCESS_TOKEN="${YANDEX_DIRECT_ACCESS_TOKEN:-your_access_token_here}"
DATE_FROM="${1:-2026-05-01}"
DATE_TO="${2:-2026-05-06}"

curl -s -X POST "https://api.direct.yandex.com/json/v5/reports" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d "{
    \"method\": \"get\",
    \"params\": {
      \"SelectionCriteria\": {
        \"DateFrom\": \"${DATE_FROM}\",
        \"DateTo\": \"${DATE_TO}\"
      },
      \"FieldNames\": [
        \"CampaignName\",
        \"Clicks\",
        \"Impressions\",
        \"Cost\",
        \"ConversionRate\",
        \"AvgCpc\",
        \"AvgCpm\"
      ],
      \"ReportType\": \"CAMPAIGN_PERFORMANCE_REPORT\",
      \"DateRangeType\": \"CUSTOM_DATE\"
    }
  }" | jq .