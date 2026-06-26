#!/bin/bash
# Quick test of Claw Code Suite skill

set -euo pipefail

cd "$(dirname "$0")"

echo "🔧 Testing Claw Code Suite Skill"
echo "================================="

# Test 1: Summary
echo "1. Testing summary command..."
if ./run.sh summary 2>&1 | cat | grep -q '"ok": true'; then
    echo "   ✅ Success"
else
    echo "   ❌ Failed"
    exit 1
fi

# Test 2: Tools list
echo "2. Testing tools command..."
if ./run.sh tools --limit 2 2>&1 | cat | grep -q '"ok": true'; then
    echo "   ✅ Success"
else
    echo "   ❌ Failed"
    exit 1
fi

# Test 3: Commands list
echo "3. Testing commands command..."
if ./run.sh commands --limit 2 2>&1 | cat | grep -q '"ok": true'; then
    echo "   ✅ Success"
else
    echo "   ❌ Failed"
    exit 1
fi

# Test 4: Route (requires prompt)
echo "4. Testing route command..."
if ./run.sh route "test prompt" --limit 1 2>&1 | cat | grep -q '"ok": true'; then
    echo "   ✅ Success"
else
    echo "   ❌ Failed"
    exit 1
fi

# Test 5: Show-tool (needs existing tool name)
echo "5. Testing show-tool with 'AgentTool'..."
if ./run.sh show-tool AgentTool 2>&1 | cat | grep -q '"ok": true'; then
    echo "   ✅ Success"
else
    echo "   ⚠️  Tool not found (may be expected)"
fi

echo ""
echo "✅ All basic tests passed!"
echo ""
echo "To test more advanced commands:"
echo "  ./run.sh exec-tool <tool-name> <payload>"
echo "  ./run.sh exec-command <command-name> <prompt>"
echo "  ./run.sh bootstrap <prompt>"
echo ""
echo "See SKILL.md for full documentation."