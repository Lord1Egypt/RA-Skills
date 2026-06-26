#!/bin/bash
# ============================================
# Confucius Debug — AI Analysis
# ============================================
#
# Security Manifest:
#   ENV accessed: CONFUCIUS_LOBSTER_ID (required, for identification)
#   External endpoints: https://api.washinmura.jp/api/v2/debug-ai
#   Files: none (read-only API call)
#   Side effects: solution saved to YanHui KB (free)
#
# Usage:
#   bash analyze.sh "error description" "optional: error message/stack trace"

set -euo pipefail

DESC="${1:?Usage: analyze.sh \"error description\" \"error message (optional)\"}"
MSG="${2:-}"
LOBSTER_ID="${CONFUCIUS_LOBSTER_ID:?Set CONFUCIUS_LOBSTER_ID env var first}"
API_URL="https://api.washinmura.jp/api/v2/debug-ai"

echo "🧙 Confucius is analyzing... (free, ~6 seconds)"
echo ""

BODY=$(jq -n \
  --arg desc "$DESC" \
  --arg msg "$MSG" \
  --arg lid "$LOBSTER_ID" \
  '{error_description: $desc, error_message: $msg, lobster_id: $lid, channel: "clawhub"}')

RESPONSE=$(curl -s --max-time 30 -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -d "$BODY") || {
  echo "❌ Cannot reach Confucius API (api.washinmura.jp). Check your internet or try again later."
  exit 1
}

# 檢查回傳是否有效
if echo "$RESPONSE" | jq -e '.yanhui' >/dev/null 2>&1; then
  echo "$RESPONSE" | jq -r '
    "🔍 Root Cause: \(.yanhui.root_cause // "N/A")\n" +
    "🔧 Fix: \(.yanhui.fix_description // "N/A")\n" +
    "📝 Patch:\n\(.yanhui.fix_patch // "N/A")\n" +
    "💰 Cost: \(.yanhui.cost // "N/A")\n" +
    "📊 Confidence: \(.yanhui.confidence // "N/A")"
  '
elif echo "$RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
  echo "❌ $(echo "$RESPONSE" | jq -r '.error')"
else
  echo "❌ Unexpected response from Confucius API:"
  echo "$RESPONSE" | jq . 2>/dev/null || echo "$RESPONSE"
fi
