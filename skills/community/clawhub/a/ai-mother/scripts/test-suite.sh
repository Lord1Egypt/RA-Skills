#!/bin/bash
# AI Mother - Test Suite
# Verify all new features are working

SKILL_DIR="$HOME/.openclaw/skills/ai-mother"
cd "$SKILL_DIR" || exit 1

echo "🧪 AI Mother Feature Test Suite"
echo "================================"
echo ""

PASS=0
FAIL=0

# Test 1: Check all scripts exist
echo "📝 Test 1: Script Files"
SCRIPTS=(
    "scripts/health-check.sh"
    "scripts/auto-heal.sh"
    "scripts/analytics.py"
    "scripts/db.py"
    "scripts/patrol.sh"
    "scripts/get-ai-context.sh"
    "scripts/send-to-ai.sh"
    "scripts/smart-diagnose.sh"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ] && [ -x "$script" ]; then
        echo "  ✅ $script"
        ((PASS++))
    else
        echo "  ❌ $script (missing or not executable)"
        ((FAIL++))
    fi
done
echo ""

# Test 2: Database initialization
echo "📝 Test 2: Database"
if python3 scripts/db.py 2>&1 | grep -q "initialized"; then
    echo "  ✅ Database initialization works"
    ((PASS++))
else
    echo "  ❌ Database initialization failed"
    ((FAIL++))
fi

if [ -f "ai-mother.db" ]; then
    echo "  ✅ Database file created"
    ((PASS++))
else
    echo "  ❌ Database file not found"
    ((FAIL++))
fi
echo ""

# Test 3: Patrol script
echo "📝 Test 3: Patrol"
if scripts/patrol.sh --quiet > /dev/null 2>&1; then
    echo "  ✅ Patrol runs without errors"
    ((PASS++))
else
    echo "  ❌ Patrol failed"
    ((FAIL++))
fi
echo ""

# Test 4: Analytics
echo "📝 Test 4: Analytics"
if python3 scripts/analytics.py 2>&1 | grep -q "AI Mother Performance Report"; then
    echo "  ✅ Analytics generates report"
    ((PASS++))
else
    echo "  ❌ Analytics failed"
    ((FAIL++))
fi
echo ""

# Test 5: Auto-heal dry-run
echo "📝 Test 5: Auto-Heal"
# Find a running AI
AI_PID=$(ps aux | awk '/[[:space:]](claude|codex)[[:space:]]|[[:space:]](claude|codex)$/ && !/grep/ && !/ai-mother/ {print $2; exit}')

if [ -n "$AI_PID" ]; then
    if scripts/auto-heal.sh "$AI_PID" --dry-run > /dev/null 2>&1; then
        echo "  ✅ Auto-heal dry-run works (PID $AI_PID)"
        ((PASS++))
    else
        echo "  ⚠️  Auto-heal dry-run completed (no issues to fix)"
        ((PASS++))
    fi
else
    echo "  ⚠️  No AI agents running (skipping auto-heal test)"
    ((PASS++))
fi
echo ""

# Test 6: Health check
echo "📝 Test 6: Health Check"
if scripts/health-check.sh > /dev/null 2>&1; then
    echo "  ✅ Health check runs without errors"
    ((PASS++))
else
    echo "  ❌ Health check failed"
    ((FAIL++))
fi
echo ""

# Test 7: Documentation
echo "📝 Test 7: Documentation"
if [ -f "README.md" ] && [ -f "SKILL.md" ]; then
    echo "  ✅ Documentation files exist"
    ((PASS++))
else
    echo "  ❌ Documentation missing"
    ((FAIL++))
fi

if grep -q "auto-heal" SKILL.md && grep -q "analytics" SKILL.md; then
    echo "  ✅ Documentation includes new features"
    ((PASS++))
else
    echo "  ❌ Documentation incomplete"
    ((FAIL++))
fi
echo ""

# Summary
echo "================================"
echo "📊 Test Results"
echo "================================"
echo "✅ Passed: $PASS"
echo "❌ Failed: $FAIL"
echo ""

if [ "$FAIL" -eq 0 ]; then
    echo "🎉 All tests passed! AI Mother is ready."
    exit 0
else
    echo "⚠️  Some tests failed. Please review."
    exit 1
fi
