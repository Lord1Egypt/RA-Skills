#!/bin/bash
echo "=== CLAWHUB AUTHENTICATION TROUBLESHOOTING ==="
echo ""

# Check CLI version
echo "1. ClawHub CLI Version:"
clawhub -V 2>/dev/null || echo "  ❌ clawhub not found or version check failed"

# Check authentication
echo ""
echo "2. Authentication Status:"
clawhub whoami 2>&1 | head -5

# Check environment
echo ""
echo "3. Environment Check:"
echo "  CLAWHUB_TOKEN: ${CLAWHUB_TOKEN:-Not set}"
echo "  BROWSERBASE_CAMO_FOX: ${BROWSERBASE_CAMO_FOX:-Not set}"

# Check token files
echo ""
echo "4. Token Files:"
if [ -f ~/.clawhub/token ]; then
    echo "  ✅ ~/.clawhub/token exists"
    echo "  Size: $(wc -c < ~/.clawhub/token) bytes"
else
    echo "  ❌ ~/.clawhub/token not found"
fi

# Check for bot detection
echo ""
echo "5. Bot Detection Warning:"
echo "  If seeing 'Vercel Security Checkpoint', enable Camo Fox"
echo "  If 'clawhub login' times out, use manual token workflow"

echo ""
echo "=== RECOMMENDED ACTIONS ==="
echo "1. Enable Camo Fox in BrowserBase"
echo "2. Use residential proxies"
echo "3. Manual token: https://clawhub.ai/settings/tokens"
echo "4. Join Discord: https://discord.gg/clawd"
