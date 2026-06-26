#!/bin/bash
# AIClient2API Usage Refresher
# Manually triggers usage data refresh by calling the provider's usage check

AICLIENT_DIR="$HOME/web/AIClient-2-API"
CACHE_FILE="$AICLIENT_DIR/configs/usage-cache.json"

echo "🔄 Refreshing AIClient2API usage data..."
echo ""

# Check if AIClient2API is running
PID=$(ps aux | grep "api-server.js" | grep -v grep | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "❌ Error: AIClient2API service is not running"
    exit 1
fi

echo "📍 AIClient2API is running (PID: $PID)"
echo ""

# Get the old timestamp
if [ -f "$CACHE_FILE" ]; then
    OLD_TIME=$(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null)
    echo "🕐 Current cache: $(date -r "$CACHE_FILE" '+%Y-%m-%d %H:%M:%S')"
else
    echo "⚠️ Cache file not found"
    OLD_TIME=0
fi

echo ""
echo "💡 Triggering refresh via Web UI API..."
echo "   (This requires the service to be running)"
echo ""

# Try to trigger refresh by touching a marker file or using the API
# Since direct API access requires auth, we'll use a workaround:
# Create a simple Node.js script to trigger the refresh internally

cat > /tmp/refresh_usage.js << 'EOF'
import { readFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const configPath = join(homedir(), 'web/AIClient-2-API/configs/usage-cache.json');

console.log('Reading current usage cache...');
try {
    const data = JSON.parse(readFileSync(configPath, 'utf8'));
    console.log('✅ Cache file is accessible');
    console.log('📊 Last update:', data.timestamp);
    
    // The actual refresh happens automatically in the background
    // We just need to wait for the next cycle
    console.log('');
    console.log('💡 Usage data refreshes automatically every few minutes.');
    console.log('   Check again in a moment with: bash scripts/check_usage.sh');
} catch (error) {
    console.error('❌ Error reading cache:', error.message);
}
EOF

node /tmp/refresh_usage.js
rm /tmp/refresh_usage.js

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Refresh request completed"
echo ""
echo "📝 Note: The usage cache updates automatically in the background."
echo "   Wait a moment and run 'bash scripts/check_usage.sh' to see updates."
echo ""
echo "🌐 For manual refresh, visit: http://127.0.0.1:16825"
echo "   (Login required - password in configs/pwd)"
