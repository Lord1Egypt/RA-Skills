#!/bin/bash
#
# CtrlZ Skill Test Suite
# Test all major features
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CTRLZ_SCRIPT="$SCRIPT_DIR/../ctrlz.sh"
TEST_DIR="/tmp/ctrlz_test_$(date +%s)"
DB_PATH="$TEST_DIR/test.db"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0

# Test function
run_test() {
  local test_name="$1"
  local test_cmd="$2"
  local expected_result="${3:-}"
  
  echo -n "Testing: $test_name ... "
  
  if eval "$test_cmd"; then
    echo -e "${GREEN}✓ PASSED${NC}"
    ((PASSED++))
  else
    echo -e "${RED}✗ FAILED${NC}"
    ((FAILED++))
  fi
}

# Initialize test environment
setup() {
  echo "=== Initializing Test Environment ==="
  mkdir -p "$TEST_DIR"
  export CTRLZ_DB="$DB_PATH"
  bash "$CTRLZ_SCRIPT" init > /dev/null 2>&1
  echo "Test directory: $TEST_DIR"
  echo "Database: $DB_PATH"
  echo ""
}

# Cleanup test environment
teardown() {
  echo ""
  echo "=== Cleaning Up Test Environment ==="
  rm -rf "$TEST_DIR"
  echo "Cleaned up"
}

# ============ Test Cases ============

test_init() {
  echo "=== Test 1: Database Initialization ==="
  run_test "Database initialization" "bash '$CTRLZ_SCRIPT' init | grep -q 'initialized'"
  run_test "Database file exists" "test -f '$DB_PATH'"
}

test_start_session() {
  echo ""
  echo "=== Test 2: Start Session ==="
  
  local result=$(bash "$CTRLZ_SCRIPT" start "Test session")
  run_test "Create session" "echo '$result' | jq -e '.session_id' > /dev/null"
  
  local session_id=$(echo "$result" | jq -r '.session_id')
  run_test "Session ID valid" "test -n '$session_id' && test '$session_id' != 'null'"
}

test_record_file_edit() {
  echo ""
  echo "=== Test 3: Record File Edit ==="
  
  # Create test file
  echo "Original content" > "$TEST_DIR/test_file.txt"
  
  # Start session
  local session_id=$(bash "$CTRLZ_SCRIPT" start "File edit test" | jq -r '.session_id')
  
  # Record operation
  run_test "Record file edit" "bash '$CTRLZ_SCRIPT' record '$session_id' file_edit '$TEST_DIR/test_file.txt' | jq -e '.recorded' > /dev/null"
  
  # Modify file
  echo "Modified content" > "$TEST_DIR/test_file.txt"
  
  # Verify backup exists
  run_test "Backup file exists" "test -f ~/.openclaw/skills/ctrlz/backups/*_test_file.txt"
}

test_undo_file_edit() {
  echo ""
  echo "=== Test 4: Undo File Edit ==="
  
  # Create and modify file
  echo "Original content" > "$TEST_DIR/undo_test.txt"
  local session_id=$(bash "$CTRLZ_SCRIPT" start "Undo test" | jq -r '.session_id')
  bash "$CTRLZ_SCRIPT" record "$session_id" file_edit "$TEST_DIR/undo_test.txt" > /dev/null
  echo "Modified content" > "$TEST_DIR/undo_test.txt"
  
  # Verify modification
  run_test "File was modified" "grep -q 'Modified content' '$TEST_DIR/undo_test.txt'"
  
  # Execute undo
  run_test "Execute undo" "bash '$CTRLZ_SCRIPT' undo | jq -e '.undone' > /dev/null"
  
  # Verify restored
  run_test "File restored" "grep -q 'Original content' '$TEST_DIR/undo_test.txt'"
}

test_record_file_write() {
  echo ""
  echo "=== Test 5: Record File Write ==="
  
  local session_id=$(bash "$CTRLZ_SCRIPT" start "File write test" | jq -r '.session_id')
  
  # Write new file
  echo "New file content" > "$TEST_DIR/new_file.txt"
  
  run_test "Record file write" "bash '$CTRLZ_SCRIPT' record '$session_id' file_write '$TEST_DIR/new_file.txt' | jq -e '.recorded' > /dev/null"
}

test_record_dir_create() {
  echo ""
  echo "=== Test 6: Record Directory Create ==="
  
  local session_id=$(bash "$CTRLZ_SCRIPT" start "Directory create test" | jq -r '.session_id')
  
  # Create directory
  mkdir -p "$TEST_DIR/new_directory"
  
  run_test "Record directory create" "bash '$CTRLZ_SCRIPT' record '$session_id' dir_create '$TEST_DIR/new_directory' | jq -e '.recorded' > /dev/null"
}

test_stack_size() {
  echo ""
  echo "=== Test 7: Stack Size Setting ==="
  
  run_test "Set stack size to 3" "bash '$CTRLZ_SCRIPT' set-stack 3 | jq -e '.max_stack_size == 3' > /dev/null"
  
  local size=$(bash "$CTRLZ_SCRIPT" get-stack | jq -r '.max_stack_size')
  run_test "Get stack size" "test '$size' = '3'"
  
  # Restore default
  bash "$CTRLZ_SCRIPT" set-stack 1 > /dev/null
}

test_multiple_undo() {
  echo ""
  echo "=== Test 8: Multiple Undo ==="
  
  # Create 3 sessions
  for i in 1 2 3; do
    local session_id=$(bash "$CTRLZ_SCRIPT" start "Session $i" | jq -r '.session_id')
    echo "Content $i" > "$TEST_DIR/multi_$i.txt"
    bash "$CTRLZ_SCRIPT" record "$session_id" file_write "$TEST_DIR/multi_$i.txt" > /dev/null
  done
  
  # Verify list
  local count=$(bash "$CTRLZ_SCRIPT" list 10 | grep -c "Session")
  run_test "List multiple sessions" "test '$count' -ge 3"
  
  # Undo 2
  run_test "Undo 2 sessions" "bash '$CTRLZ_SCRIPT' undo 2 | jq -e '.undone == 2' > /dev/null"
}

test_stats() {
  echo ""
  echo "=== Test 9: Statistics ==="
  
  local stats=$(bash "$CTRLZ_SCRIPT" stats)
  run_test "Get statistics" "echo '$stats' | jq -e '.active_sessions' > /dev/null"
  run_test "Stats include max_stack_size" "echo '$stats' | jq -e '.max_stack_size' > /dev/null"
}

test_clear() {
  echo ""
  echo "=== Test 10: Clear Records ==="
  
  # Create some records first
  local session_id=$(bash "$CTRLZ_SCRIPT" start "To be cleared" | jq -r '.session_id')
  bash "$CTRLZ_SCRIPT" record "$session_id" file_write "$TEST_DIR/clear_test.txt" > /dev/null
  
  # Clear
  run_test "Clear all records" "bash '$CTRLZ_SCRIPT' clear | jq -e '.cleared' > /dev/null"
  
  # Verify
  local count=$(bash "$CTRLZ_SCRIPT" stats | jq -r '.total_sessions')
  run_test "Records cleared" "test '$count' = '0'"
}

test_no_more_undo() {
  echo ""
  echo "=== Test 11: No More Undo ==="
  
  # Clear then try to undo
  bash "$CTRLZ_SCRIPT" clear > /dev/null 2>&1
  
  run_test "No undo returns error" "! bash '$CTRLZ_SCRIPT' undo | jq -e '.error' > /dev/null 2>&1"
}

# ============ Main Program ============

main() {
  echo "========================================"
  echo "     CtrlZ Skill Test Suite"
  echo "========================================"
  echo ""
  
  setup
  
  # Run all tests
  test_init
  test_start_session
  test_record_file_edit
  test_undo_file_edit
  test_record_file_write
  test_record_dir_create
  test_stack_size
  test_multiple_undo
  test_stats
  test_clear
  test_no_more_undo
  
  # Show results
  echo ""
  echo "========================================"
  echo "           Test Results"
  echo "========================================"
  echo -e "${GREEN}Passed: $PASSED${NC}"
  echo -e "${RED}Failed: $FAILED${NC}"
  echo "========================================"
  
  teardown
  
  if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
  else
    echo -e "${RED}Some tests failed${NC}"
    exit 1
  fi
}

main "$@"
