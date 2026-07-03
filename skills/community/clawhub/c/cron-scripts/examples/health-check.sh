#!/usr/bin/env bash
# name: health-check-example
# schedule: */10 * * * *
# tz: UTC
# timeout: 30
#
# Example: ping a URL every 10 minutes, send Telegram alert on failure.
# Replace URL and CHAT_ID with your own values.

URL="https://example.com/health"
CHAT_ID="YOUR_TELEGRAM_CHAT_ID"   # e.g. 79151284
OPENCLAW_PORT="${OPENCLAW_PORT:-3000}"

HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" --max-time 10 "$URL" 2>/dev/null || echo "000")

if [ "$HTTP_CODE" != "200" ]; then
  curl -sf -X POST "http://localhost:${OPENCLAW_PORT}/api/announce" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"⚠️ Health check failed: $URL returned HTTP $HTTP_CODE\", \"channel\": \"telegram\", \"to\": \"$CHAT_ID\"}" \
    > /dev/null
fi
