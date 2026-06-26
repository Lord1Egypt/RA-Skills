#!/bin/bash
# Test Runner

echo "🧪 Running Cognitive Brain Test Suite"
echo "====================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

run_test() {
  local test_file=$1
  local test_name=$2

  echo -e "\n📋 $test_name"
  echo "----------------------------------------"

  if node "$test_file"; then
    echo -e "${GREEN}✓ $test_name passed${NC}"
    ((PASSED++))
  else
    echo -e "${RED}✗ $test_name failed${NC}"
    ((FAILED++))
  fi
}

# Setup
node tests/setup.cjs

# Run all test files
run_test "tests/db.test.cjs" "Database Tests"
run_test "tests/memory.test.cjs" "Memory Tests"
run_test "tests/repository.test.cjs" "Repository Tests"
run_test "tests/service.test.cjs" "Service Tests"
run_test "tests/v5.test.cjs" "V5 Architecture Tests"
run_test "tests/api.test.cjs" "API Tests"

# Summary
echo -e "\n====================================="
echo "📊 Test Summary"
echo "====================================="
echo -e "${GREEN}Passed: $PASSED${NC}"
echo -e "${RED}Failed: $FAILED${NC}"
echo "Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
  echo -e "\n${GREEN}✅ All tests passed!${NC}"
  exit 0
else
  echo -e "\n${RED}❌ Some tests failed${NC}"
  exit 1
fi
