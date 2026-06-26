#!/bin/bash
echo "=== CLAWHUB SKILL VALIDATION v1.1 ==="
echo "Now with bot detection awareness!"
echo ""

# Basic checks
[ -f "SKILL.md" ] && echo "✅ SKILL.md exists" || echo "❌ SKILL.md missing"

# Check for bot detection section
if grep -q "bot detection" SKILL.md -i; then
    echo "✅ Bot detection awareness included"
else
    echo "⚠️  Consider adding bot detection guidance"
fi

# Check for authentication options
if grep -q "Camo Fox" SKILL.md || grep -q "token" SKILL.md -i; then
    echo "✅ Authentication options documented"
else
    echo "❌ Missing authentication guidance"
fi

echo ""
echo "=== BOT DETECTION READINESS ==="
echo "For ClawHub publishing, ensure:"
echo "1. Camo Fox enabled (BrowserBase)"
echo "2. Residential proxies configured"
echo "3. Authentication tested before publishing"
echo ""
echo "Run: ./scripts/troubleshoot-auth.sh"
echo "For authentication troubleshooting"
