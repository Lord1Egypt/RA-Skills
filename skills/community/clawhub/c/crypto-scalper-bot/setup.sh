#!/bin/bash
# Setup Verification Script
# Run this after creating env files

echo "======================================"
echo "🔍 CRYPTO TRADING SETUP VERIFICATION"
echo "======================================"

# Check env files
echo ""
echo "📁 Checking env files..."

if [ -f "binance.env" ]; then
    source binance.env
    if [ -n "$BINANCE_API_KEY" ] && [ -n "$BINANCE_API_SECRET" ]; then
        echo "✅ binance.env: Found (${BINANCE_API_KEY:0:10}...)"
    else
        echo "❌ binance.env: Empty values!"
    fi
else
    echo "❌ binance.env: Not found!"
fi

if [ -f "telegram.env" ]; then
    source telegram.env
    if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
        echo "✅ telegram.env: Found"
    else
        echo "❌ telegram.env: Empty values!"
    fi
else
    echo "⚠️  telegram.env: Not found (optional)"
fi

# Check Python
echo ""
echo "🐍 Checking Python..."
python3 --version || echo "❌ Python not found!"

# Check dependencies
echo ""
echo "📦 Checking dependencies..."
python3 -c "import requests" 2>/dev/null && echo "✅ requests" || echo "❌ requests not installed (pip3 install requests)"

# Try to fetch balance
echo ""
echo "🌐 Testing Binance connection..."
if [ -f "binance.env" ]; then
    source binance.env
    python3 << 'PYEOF'
import os, requests, hmac, hashlib, time
for env_file in ['binance.env']:
    with open(env_file) as f:
        for line in f:
            if '=' in line:
                k, v = line.strip().split('=', 1)
                os.environ[k] = v

api_key = os.environ.get('BINANCE_API_KEY', '')
api_secret = os.environ.get('BINANCE_API_SECRET', '')

if not api_key or not api_secret:
    print("❌ Missing credentials")
    exit(1)

def get_sig(q):
    return hmac.new(api_secret.encode(), q.encode(), hashlib.sha256).hexdigest()

ts = int(time.time() * 1000)
q = f"timestamp={ts}&recvWindow=5000&signature={get_sig(q)}"
url = f"https://fapi.binance.com/fapi/v2/account?{q}&timestamp={ts}&recvWindow=5000&signature={get_sig(q)}"
headers = {'X-MBX-APIKEY': api_key}

try:
    r = requests.get(f"https://fapi.binance.com/fapi/v2/account?timestamp={ts}&recvWindow=5000&signature={get_sig(f'timestamp={ts}&recvWindow=5000')}", headers=headers, timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Balance: ${float(data.get('availableBalance', 0)):.2f}")
    else:
        print(f"❌ API Error: {r.status_code}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
PYEOF
fi

echo ""
echo "======================================"
echo "Setup check complete!"
echo "======================================"
