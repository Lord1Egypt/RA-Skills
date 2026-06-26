#!/usr/bin/env bash
set -euo pipefail

# Integration Test Suite for Email Automation Skill
# Validates end-to-end workflow

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASSED=0
FAILED=0

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_pass() {
  echo -e "${GREEN}✓${NC} $1"
  PASSED=$((PASSED + 1))
}

log_fail() {
  echo -e "${RED}✗${NC} $1"
  FAILED=$((FAILED + 1))
}

log_info() {
  echo -e "${YELLOW}→${NC} $1"
}

echo "========================================="
echo "Email Automation Skill - Integration Test"
echo "========================================="
echo ""

# Test 1: Directory structure
log_info "Test 1: Checking directory structure..."
if [[ -d "$SCRIPT_DIR/lib" ]] && \
   [[ -d "$SCRIPT_DIR/templates" ]] && \
   [[ -f "$SCRIPT_DIR/create-sequence.sh" ]] && \
   [[ -f "$SCRIPT_DIR/monitor-sequences.sh" ]]; then
  log_pass "Directory structure is correct"
else
  log_fail "Directory structure is incomplete"
fi

# Test 2: Scripts are executable
log_info "Test 2: Checking script permissions..."
if [[ -x "$SCRIPT_DIR/create-sequence.sh" ]] && \
   [[ -x "$SCRIPT_DIR/monitor-sequences.sh" ]]; then
  log_pass "Scripts are executable"
else
  log_fail "Scripts are not executable"
fi

# Test 3: Templates exist
log_info "Test 3: Checking email templates..."
TEMPLATE_COUNT=$(find "$SCRIPT_DIR/templates" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
if [[ "$TEMPLATE_COUNT" -ge 3 ]]; then
  log_pass "Found $TEMPLATE_COUNT email templates"
else
  log_fail "Missing email templates (found: $TEMPLATE_COUNT, expected: ≥3)"
fi

# Test 4: Create test sequence (dry run)
log_info "Test 4: Creating test sequence..."
TEST_OUTPUT="/tmp/test-sequence-$$.json"
if "$SCRIPT_DIR/create-sequence.sh" \
    --type welcome \
    --product "Test Product" \
    --emails 3 \
    --delay-days "0,3,7" \
    --output "$TEST_OUTPUT" >/dev/null 2>&1; then
  
  if [[ -f "$TEST_OUTPUT" ]] && jq -e '.sequenceName' "$TEST_OUTPUT" >/dev/null 2>&1; then
    log_pass "Sequence creation works (valid JSON output)"
    rm -f "$TEST_OUTPUT"
  else
    log_fail "Sequence file created but invalid JSON"
  fi
else
  log_fail "Sequence creation failed"
fi

# Test 5: API wrapper loads
log_info "Test 5: Checking API wrapper..."
if source "$SCRIPT_DIR/lib/convertkit-api.sh" 2>/dev/null; then
  if declare -F check_convertkit_auth >/dev/null 2>&1; then
    log_pass "ConvertKit API wrapper loaded"
  else
    log_fail "ConvertKit API wrapper missing functions"
  fi
else
  log_fail "ConvertKit API wrapper failed to load"
fi

# Test 6: ConvertKit API connection (if key is set)
if [[ -n "${CONVERTKIT_API_SECRET:-}" ]]; then
  log_info "Test 6: Testing ConvertKit API connection..."
  source "$SCRIPT_DIR/lib/convertkit-api.sh"
  if convertkit_test_connection >/dev/null 2>&1; then
    log_pass "ConvertKit API connection successful"
  else
    log_fail "ConvertKit API connection failed"
  fi
else
  log_info "Test 6: Skipped (CONVERTKIT_API_SECRET not set)"
fi

# Test 7: SKILL.md exists and is valid
log_info "Test 7: Checking skill documentation..."
if [[ -f "$SCRIPT_DIR/SKILL.md" ]]; then
  LINE_COUNT=$(wc -l < "$SCRIPT_DIR/SKILL.md" | tr -d ' ')
  if [[ "$LINE_COUNT" -gt 100 ]]; then
    log_pass "SKILL.md exists and is comprehensive ($LINE_COUNT lines)"
  else
    log_fail "SKILL.md exists but seems incomplete ($LINE_COUNT lines)"
  fi
else
  log_fail "SKILL.md not found"
fi

# Summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "${GREEN}Passed:${NC} $PASSED"
echo -e "${RED}Failed:${NC} $FAILED"
echo ""

if [[ "$FAILED" -eq 0 ]]; then
  echo -e "${GREEN}✓ All tests passed!${NC}"
  echo ""
  echo "Skill is ready to use:"
  echo "  1. Set CONVERTKIT_API_SECRET environment variable"
  echo "  2. Run: ./create-sequence.sh --type welcome --product 'Your Product'"
  echo "  3. Monitor: ./monitor-sequences.sh"
  exit 0
else
  echo -e "${RED}✗ Some tests failed${NC}"
  echo "Please fix the issues above before using the skill."
  exit 1
fi
