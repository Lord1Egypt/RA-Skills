#!/bin/bash
# screenshot_and_send.sh - Take screenshot from PinchTab and send to Telegram
# Usage: ./screenshot_and_send.sh <tab_id> [telegram_chat_id]

set -e

TAB_ID="${1:-}"
TELEGRAM_CHAT_ID="${2:-}"
PINCHTAB_SERVER="${PINCHTAB_SERVER:-http://localhost:9867}"
PINCHTAB_TOKEN="${PINCHTAB_TOKEN:-}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"

if [ -z "$TAB_ID" ]; then
  echo "Usage: $0 <tab_id> [telegram_chat_id]"
  echo "Example: $0 62FD11183EA4F8B8DA24A57F6C0392C3 8522303961"
  exit 1
fi

if [ -z "$PINCHTAB_TOKEN" ]; then
  echo "ERROR: PINCHTAB_TOKEN not set. Export it first:"
  echo "export PINCHTAB_TOKEN='your_token_here'"
  exit 1
fi

# Create temp file for screenshot
TEMP_DIR=$(mktemp -d)
SCREENSHOT_FILE="$TEMP_DIR/screenshot.jpg"

echo "📸 Fetching screenshot from PinchTab for tab: $TAB_ID"

# Fetch screenshot from PinchTab
RESPONSE=$(curl -s "${PINCHTAB_SERVER}/tabs/${TAB_ID}/screenshot" \
  -H "Authorization: Bearer ${PINCHTAB_TOKEN}")

# Extract base64 from JSON response
BASE64_DATA=$(echo "$RESPONSE" | jq -r '.base64' 2>/dev/null)

if [ -z "$BASE64_DATA" ] || [ "$BASE64_DATA" = "null" ]; then
  echo "❌ Failed to get screenshot. Response: $RESPONSE"
  exit 1
fi

echo "✅ Screenshot fetched. Decoding base64..."

# Decode base64 to file
echo "$BASE64_DATA" | base64 -d > "$SCREENSHOT_FILE"

if [ ! -f "$SCREENSHOT_FILE" ]; then
  echo "❌ Failed to decode base64"
  exit 1
fi

FILE_SIZE=$(du -h "$SCREENSHOT_FILE" | cut -f1)
echo "✅ Screenshot saved: $SCREENSHOT_FILE ($FILE_SIZE)"

# Send to Telegram if chat_id provided
if [ -n "$TELEGRAM_CHAT_ID" ] && [ -n "$TELEGRAM_BOT_TOKEN" ]; then
  echo "📤 Sending to Telegram (chat: $TELEGRAM_CHAT_ID)..."
  
  TELE_RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendPhoto" \
    -F "chat_id=${TELEGRAM_CHAT_ID}" \
    -F "photo=@${SCREENSHOT_FILE}" \
    -F "caption=PinchTab Screenshot from tab ${TAB_ID}")
  
  if echo "$TELE_RESPONSE" | jq -e '.ok' >/dev/null 2>&1; then
    echo "✅ Sent to Telegram!"
  else
    echo "⚠️  Telegram send failed: $TELE_RESPONSE"
  fi
else
  echo "ℹ️  No Telegram config provided. Screenshot saved to: $SCREENSHOT_FILE"
  echo "   To send to Telegram, run:"
  echo "   export TELEGRAM_BOT_TOKEN='your_bot_token'"
  echo "   $0 $TAB_ID <chat_id>"
fi

# Optionally copy to workspace if in skill directory
if [ -d "/root/.openclaw/workspace/skills/pinchtab/assets" ]; then
  cp "$SCREENSHOT_FILE" "/root/.openclaw/workspace/skills/pinchtab/assets/last-screenshot.jpg"
  echo "📁 Copied to: /root/.openclaw/workspace/skills/pinchtab/assets/last-screenshot.jpg"
fi

echo "✨ Done!"
