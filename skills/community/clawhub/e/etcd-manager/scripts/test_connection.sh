#!/bin/bash
# Test etcd connection script

set -euo pipefail

ENDPOINTS="${1:-127.0.0.1:2379}"

echo "🔍 Testing etcd connection to: $ENDPOINTS"
echo "========================================"

# Test 1: Check endpoint health
echo ""
echo "1. Checking endpoint health..."
if etcdctl --endpoints="$ENDPOINTS" endpoint health 2>/dev/null; then
    echo "✅ Endpoint is healthy"
else
    echo "❌ Endpoint is not healthy"
    exit 1
fi

# Test 2: Get etcd version
echo ""
echo "2. Getting etcd version..."
etcdctl --endpoints="$ENDPOINTS" version

# Test 3: Test basic operations
echo ""
echo "3. Testing basic operations..."

TEST_KEY="/etcd-skill-test-$(date +%s)"
TEST_VALUE="test-value-$(date +%s)"

echo "   Test key: $TEST_KEY"
echo "   Test value: $TEST_VALUE"

# Put test value
echo "   a) Putting test value..."
etcdctl --endpoints="$ENDPOINTS" put "$TEST_KEY" "$TEST_VALUE"

# Get test value
echo "   b) Getting test value..."
etcdctl --endpoints="$ENDPOINTS" get "$TEST_KEY"

# List test key
echo "   c) Listing test key..."
etcdctl --endpoints="$ENDPOINTS" get "$TEST_KEY" --prefix --keys-only

# Delete test value
echo "   d) Deleting test value..."
etcdctl --endpoints="$ENDPOINTS" del "$TEST_KEY"

# Verify deletion
echo "   e) Verifying deletion..."
etcdctl --endpoints="$ENDPOINTS" get "$TEST_KEY" 2>/dev/null || echo "   ✅ Key successfully deleted"

echo ""
echo "🎉 All tests passed! etcd connection is working correctly."