#!/usr/bin/env bash
# test-connection.sh - Test Agnes Video API connection and configuration
# Usage: ./test-connection.sh

set -euo pipefail

API_CREATE="https://apihub.agnes-ai.com/v1/videos"
API_KEY="${ANGES_API_KEY:-${AGENT_ANGES_API_KEY:-}}"

echo "🔍 Testing Agnes Video V2.0 API Connection"
echo "==========================================="

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
    "model": "agnes-video-v2.0",
    "prompt": "A simple test video of a red ball bouncing",
    "mode": "ti2vid",
    "width": 512,
    "height": 512,
    "num_frames": 81,
    "frame_rate": 24
  }' \
  "$API_CREATE" 2>&1) || {
    echo "❌ Connection failed"
    echo "   Response: $RESPONSE"
    exit 1
  }

echo "✓ API connection successful"
echo ""

# Parse response
VIDEO_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['video_id'])" 2>/dev/null) || {
  echo "❌ Failed to parse response"
  echo "   Response: $RESPONSE"
  exit 1
}

echo "✓ Test video task created successfully"
echo "   Video ID: $VIDEO_ID"
echo ""
echo "✅ All tests passed! API is working correctly."
