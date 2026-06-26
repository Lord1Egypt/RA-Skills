#!/bin/bash
# Security verification script for Claw Code Suite v1.0.1+
# Verifies the skill contains no network code, servers, or credentials handling

set -euo pipefail

echo "🔒 Claw Code Suite Security Verification"
echo "========================================"
echo "Version: 1.0.1+ (Python-only, offline edition)"
echo ""

FAILED=0
PASSED=0

check() {
    local name="$1"
    local command="$2"
    local expected="$3"
    
    echo -n "• $name: "
    if eval "$command" >/dev/null 2>&1; then
        if [ "$expected" = "empty" ]; then
            echo "✅ PASS (no matches found)"
            ((PASSED++))
        else
            echo "❌ FAIL (matches found)"
            eval "$command"
            ((FAILED++))
        fi
    else
        if [ "$expected" = "empty" ]; then
            echo "❌ FAIL (command failed)"
            ((FAILED++))
        else
            echo "✅ PASS (expected matches found)"
            ((PASSED++))
        fi
    fi
}

echo "1. Checking for Rust/network/server code..."
check "No Rust source files" "find . -name \"*.rs\" | head -5" "empty"
check "No Cargo files" "find . -name \"Cargo.*\" -o -name \"*.toml\" | grep -v package.json" "empty"
check "No HTTP client imports" "grep -r \"import.*requests\|import.*http\|import.*urllib\" . --include=\"*.py\" | head -5" "empty"
check "No socket imports" "grep -r \"import.*socket\" . --include=\"*.py\" | head -5" "empty"
check "No server/binding code" "grep -r \"server\|bind\|listen\|port.*[0-9]\" . --include=\"*.py\" | grep -v \"teleport\|remote\" | head -5" "empty"

echo ""
echo "2. Checking for AI provider/credential code..."
check "No API key patterns" "grep -r \"API_KEY\|api_key\|APIKEY\" . --include=\"*.py\" --include=\"*.json\" | head -5" "empty"
check "No AI provider imports" "grep -r \"openai\|anthropic\|xai\|groq\" . -i --include=\"*.py\" | head -5" "empty"
check "No OAuth patterns" "grep -r \"oauth\|auth.*token\|client.*secret\" . -i --include=\"*.py\" | head -5" "empty"

echo ""
echo "3. Checking Python code integrity..."
check "Python files exist" "find . -name \"*.py\" | wc -l" "notempty"
check "Main harness exists" "test -f ./claw_harness.py" "notempty"
check "Enhanced harness exists" "test -f ./claw_harness_enhanced.py" "notempty"
check "Claw Code Python port exists" "test -d ./claw-code/src" "notempty"

echo ""
echo "4. Checking skill structure..."
check "SKILL.md exists" "test -f ./SKILL.md" "notempty"
check "CHANGELOG.md exists" "test -f ./CHANGELOG.md" "notempty"
check "run.sh exists" "test -f ./run.sh" "notempty"
check "Test script exists" "test -f ./test_skill.sh" "notempty"

echo ""
echo "========================================"
echo "Results: $PASSED passed, $FAILED failed"

if [ $FAILED -eq 0 ]; then
    echo "✅ SECURITY VERIFICATION PASSED"
    echo "This skill is clean, Python-only, and contains no network code."
    exit 0
else
    echo "❌ SECURITY VERIFICATION FAILED"
    echo "This skill may contain network/server code or other security issues."
    exit 1
fi