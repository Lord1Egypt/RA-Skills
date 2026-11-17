#!/usr/bin/env bash
# test-connection.sh - Test Agnes Image 2.1 API connection and configuration
# Usage: ./test-connection.sh

set -euo pipefail

API_URL="https://apihub.agnes-ai.com/v1/images/generations"
API_KEY="${ANGES_API_KEY:-${AGENT_ANGES_API_KEY:-}}"

echo "🔍 Testing Agnes Image 2.1 Flash API Connection"
echo "================================================"

if [ -z "$API_KEY" ]; then
  echo "❌ ERROR: ANGES_API_KEY or AGENT_ANGES_API_KEY not set."
  echo "   Set it with: export ANGES_API_KEY='your_key_here'"
  exit 1
fi

echo "✓ API Key configured"
echo ""

# Test with a simple request
echo "📡 Sending test request..."
RESPONSE=$(curl -sf --max-time 30 \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "A luminous floating city above a misty canyon at sunrise, cinematic realism",
    "size": "1024x768",
    "extra_body": {
      "response_format": "url"
    }
  }' \
  "$API_URL" 2>&1) || {
    echo "❌ Connection failed"
    echo "   Response: $RESPONSE"
    exit 1
  }

echo "✓ API connection successful"
echo ""

# Parse response
URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['data'][0]['url'])" 2>/dev/null) || {
  echo "❌ Failed to parse response"
  echo "   Response: $RESPONSE"
  exit 1
}

echo "✓ Test image generated successfully"
echo "   URL: $URL"
echo ""
echo "✅ All tests passed! API is working correctly."
