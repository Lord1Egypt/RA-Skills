#!/bin/bash
# Chrome CDP Launcher - Opens Chrome with debug port
# Run ONCE, keep it open for 24/7 access

echo "🚀 Starting Chrome with Debug Port..."

# Kill existing Chrome
pkill -9 "Google Chrome" 2>/dev/null
sleep 2

# Launch Chrome with debug port
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="/tmp/chrome-cdp" \
  --no-first-run \
  --no-default-browser-check &

sleep 4

# Verify
if curl -s --max-time 3 http://localhost:9222/json/version > /dev/null 2>&1; then
    echo "✅ Chrome CDP running on http://localhost:9222"
    echo "📌 Keep this Chrome window open!"
    echo ""
    echo "Test with:"
    echo "  curl -s http://localhost:9222/json/version | head"
else
    echo "❌ Chrome CDP failed to start"
    echo "Try manually:"
    echo '  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222'
fi
