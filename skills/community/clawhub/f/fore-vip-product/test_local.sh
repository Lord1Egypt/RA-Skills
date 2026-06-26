#!/bin/bash

# Product MCP Skill - Local Test Script
# Tests the query_kl tool via MCP Server

API_BASE="https://api.fore.vip"
MCP_TOOLS_LIST="${API_BASE}/mcp/tools/list"
MCP_TOOLS_CALL="${API_BASE}/mcp/tools/call"

echo "======================================"
echo "Product Catalog MCP Skill - Test"
echo "======================================"
echo ""

# Test 1: Get Tools List
echo "Test 1: Getting tools list..."
echo "URL: ${MCP_TOOLS_LIST}"
echo ""

tools_list=$(curl -s "${MCP_TOOLS_LIST}")
echo "${tools_list}" | python3 -m json.tool 2>/dev/null || echo "${tools_list}"
echo ""

# Check if query_kl is in the list
if echo "${tools_list}" | grep -q "query_kl"; then
    echo "✅ query_kl tool found in tools list"
else
    echo "❌ query_kl tool NOT found in tools list"
    exit 1
fi
echo ""

# Test 2: Query all products (no tag filter)
echo "Test 2: Query all products (no tag filter)..."
echo ""

result=$(curl -s -X POST "${MCP_TOOLS_CALL}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "query_kl",
    "arguments": {
      "limit": 5,
      "skip": 0
    }
  }')

echo "${result}" | python3 -m json.tool 2>/dev/null || echo "${result}"
echo ""

# Check success
if echo "${result}" | grep -q '"success": true'; then
    echo "✅ Query all products successful"
else
    echo "❌ Query all products failed"
    exit 1
fi
echo ""

# Test 3: Query products by tag
echo "Test 3: Query products by tag (推荐)..."
echo ""

result=$(curl -s -X POST "${MCP_TOOLS_CALL}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "query_kl",
    "arguments": {
      "tag": "推荐",
      "limit": 10,
      "skip": 0
    }
  }')

echo "${result}" | python3 -m json.tool 2>/dev/null || echo "${result}"
echo ""

# Check success
if echo "${result}" | grep -q '"success": true'; then
    echo "✅ Query by tag successful"
else
    echo "❌ Query by tag failed"
    exit 1
fi
echo ""

# Test 4: Test pagination
echo "Test 4: Test pagination (skip=5, limit=3)..."
echo ""

result=$(curl -s -X POST "${MCP_TOOLS_CALL}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "query_kl",
    "arguments": {
      "limit": 3,
      "skip": 5
    }
  }')

echo "${result}" | python3 -m json.tool 2>/dev/null || echo "${result}"
echo ""

# Check success
if echo "${result}" | grep -q '"success": true'; then
    echo "✅ Pagination test successful"
else
    echo "❌ Pagination test failed"
    exit 1
fi
echo ""

# Test 5: Test invalid tool name
echo "Test 5: Test invalid tool name..."
echo ""

result=$(curl -s -X POST "${MCP_TOOLS_CALL}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "invalid_tool",
    "arguments": {}
  }')

echo "${result}" | python3 -m json.tool 2>/dev/null || echo "${result}"
echo ""

# Check error
if echo "${result}" | grep -q '"error"'; then
    echo "✅ Invalid tool error handling correct"
else
    echo "❌ Invalid tool error handling failed"
    exit 1
fi
echo ""

echo "======================================"
echo "All tests passed! ✅"
echo "======================================"
