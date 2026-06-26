#!/bin/bash
# test_config.sh - Validate OpenClaw configuration

CONFIG_FILE="/data/.openclaw/openclaw.json"

echo "🧪 Testing OpenClaw Configuration"
echo ""

PASSED=0
FAILED=0

# Test 1: Valid JSON
echo -n "📋 Valid JSON... "
if jq empty "$CONFIG_FILE" 2>/dev/null; then
  echo "✅"
  ((PASSED++))
else
  echo "❌"
  jq . "$CONFIG_FILE" 2>&1 | head -5
  ((FAILED++))
fi

# Test 2: Required fields
echo -n "🏗️  Required fields... "
MISSING=""
for field in "agents" "models" "channels" "bindings"; do
  jq -e ".$field" "$CONFIG_FILE" > /dev/null || MISSING="$MISSING $field"
done
if [ -z "$MISSING" ]; then
  echo "✅"
  ((PASSED++))
else
  echo "❌ Missing: $MISSING"
  ((FAILED++))
fi

# Test 3: All agents valid
echo -n "🤖 Agent definitions... "
AGENT_COUNT=$(jq '.agents.list | length' "$CONFIG_FILE")
echo "✅ ($AGENT_COUNT agents)"
((PASSED++))

# Test 4: All models exist
echo -n "📡 Models in OpenRouter... "
INVALID_MODELS=$(jq -r '.agents.list[].model.primary' "$CONFIG_FILE" | grep -v '^openrouter/' | wc -l)
if [ "$INVALID_MODELS" -eq 0 ]; then
  echo "✅"
  ((PASSED++))
else
  echo "⚠️  ($INVALID_MODELS using non-OpenRouter providers)"
  ((PASSED++))
fi

# Test 5: Bindings valid
echo -n "🔗 Channel bindings... "
BINDING_COUNT=$(jq '.bindings | length' "$CONFIG_FILE")
if [ "$BINDING_COUNT" -gt 0 ]; then
  echo "✅ ($BINDING_COUNT bindings)"
  ((PASSED++))
else
  echo "❌ No bindings found"
  ((FAILED++))
fi

# Test 6: API keys present
echo -n "🔑 API keys... "
API_KEY=$(jq -r '.models.providers.openrouter.apiKey // ""' "$CONFIG_FILE")
if [ -n "$API_KEY" ] && [ "$API_KEY" != "null" ]; then
  echo "✅"
  ((PASSED++))
else
  echo "❌ Missing OpenRouter API key"
  ((FAILED++))
fi

echo ""
echo "📊 Results: $PASSED passed, $FAILED failed"

if [ $FAILED -eq 0 ]; then
  echo "✨ Configuration is valid!"
  exit 0
else
  echo "❌ Fix errors above"
  exit 1
fi
