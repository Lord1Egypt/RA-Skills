#!/bin/bash
# Test automatic re-login mechanism on token expiry

export PYTHONIOENCODING=utf-8

echo "=== Token Expiry Auto Re-login Test ==="
echo ""

# 1. Normal call
echo "1. Normal call (using cached token)"
bash "C:\Users\your-user\.openclaw\workspace\skills\biolims\scripts\biolims.sh" order-list 1 1 > /tmp/test_result.json 2>&1
status=$(cat /tmp/test_result.json | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'error'))" 2>/dev/null || echo "error")
echo "   Status: $status"
echo ""

# 2. Delete token and cookies to simulate expiry
echo "2. Delete token cache to simulate expiry"
rm -f /tmp/biolims_token_cache.json /tmp/biolims_cookies.txt
echo "   Cache deleted"
echo ""

# 3. Call again, should automatically re-login
echo "3. Call again (should automatically re-login)"
bash "C:\Users\your-user\.openclaw\workspace\skills\biolims\scripts\biolims.sh" order-list 1 1 > /tmp/test_result2.json 2>&1
status=$(cat /tmp/test_result2.json | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'error'))" 2>/dev/null || echo "error")
echo "   Status: $status"
echo ""

# 4. Check if token cache was regenerated
echo "4. Check token cache"
if [[ -f /tmp/biolims_token_cache.json ]]; then
    echo "   ✓ Token cache has been regenerated"
    expires_at=$(cat /tmp/biolims_token_cache.json | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['expires_at'])")
    now=$(date +%s)
    remaining=$((expires_at - now))
    echo "   Remaining validity: $remaining seconds (approx $((remaining / 60)) minutes)"
else
    echo "   ✗ Token cache was not generated"
fi

echo ""
echo "=== Test complete ==="
