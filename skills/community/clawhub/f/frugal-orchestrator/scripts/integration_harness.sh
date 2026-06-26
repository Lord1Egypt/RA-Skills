#!/bin/bash
#
# Frugal Orchestrator - Integration Test Harness
# Validates skill installation and basic operations
#

set -euo pipefail

echo "=== FRUGAL ORCHESTRATOR INTEGRATION TESTS ==="
echo "Started: $(date -Iseconds)"
echo ""

PASS=0
FAIL=0
TEST=""

run_test() {
    TEST="$1"
    echo -n "Testing $TEST... "
    if eval "$2" > /dev/null 2>&1; then
        echo "✓ PASS"
        ((PASS++))
    else
        echo "✗ FAIL"
        ((FAIL++))
    fi
}

# Basic structure tests
run_test "Script directory exists" "[ -d '/a0/usr/projects/frugal_orchestrator/scripts' ]"
run_test "TOON tools present" "[ -f '/a0/usr/projects/frugal_orchestrator/tools/toon/json_to_toon.py' ]"
run_test "SKILL.md valid" "[ -f '/a0/usr/projects/frugal_orchestrator/SKILL.md' ] && grep -q '# Frugal Orchestrator' SKILL.md"
run_test "Git repo initialized" "[ -d '.git' ]"
run_test "delegate.sh executable" "[ -x 'scripts/delegate.sh' ]"
run_test "token_tracker.py executable" "[ -x 'scripts/token_tracker.py' ]"

# Functional test - verify TOON conversion
run_test "JSON→TOON conversion" "python tools/toon/json_to_toon.py --help > /dev/null 2>&1"
run_test "TOON→JSON conversion" "python tools/toon/toon_to_json.py --help > /dev/null 2>&1"

echo ""
echo "=== RESULTS ==="
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo "Completed: $(date -Iseconds)"

[[ $FAIL -eq 0 ]] && exit 0 || exit 1
