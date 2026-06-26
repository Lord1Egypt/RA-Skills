#!/bin/bash
# Verify Gomboc skill setup

set -e

echo "🔍 Verifying Gomboc Skill Setup"
echo "================================"
echo ""

# Check token
if [ -z "$GOMBOC_PAT" ]; then
    echo "❌ GOMBOC_PAT not set"
    echo "   Get a token at: https://app.gomboc.ai/settings/tokens"
    exit 1
fi

echo "✅ GOMBOC_PAT is set"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check CLI exists
if [ ! -f "scripts/cli-wrapper.py" ]; then
    echo "❌ scripts/cli-wrapper.py not found"
    exit 1
fi

echo "✅ CLI wrapper found"

# Test token with API
echo ""
echo "🌐 Testing Gomboc API connection..."

RESPONSE=$(python3 << 'PYEOF'
import urllib.request
import urllib.error
import json
import os

token = os.getenv("GOMBOC_PAT")
url = "https://api.app.gomboc.ai/graphql"

try:
    query = '{"query": "{ __typename }"}'
    req = urllib.request.Request(
        url,
        data=query.encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=10) as response:
        result = json.loads(response.read())
        if "errors" in result:
            print("FAIL")
        else:
            print("OK")
except Exception as e:
    print(f"FAIL")
PYEOF
)

if [ "$RESPONSE" = "OK" ]; then
    echo "✅ API connection successful"
else
    echo "❌ API connection failed"
    echo "   Check your GOMBOC_PAT token"
    exit 1
fi

echo ""
echo "================================"
echo "✅ Setup verification complete!"
echo ""
echo "You're ready to use Gomboc:"
echo "  python scripts/cli-wrapper.py scan --path ./src"
