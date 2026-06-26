#!/bin/bash
# OpenClaw Memory System — Automated Tests (Bash)
# Run: ./test-memory-system.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(dirname "$SCRIPT_DIR")"
TEST_WORKSPACE="$(mktemp -d)"

# Test results
PASSED=0
FAILED=0

# Check for jq
JQ_AVAILABLE=false
if command -v jq &> /dev/null; then
    JQ_AVAILABLE=true
fi

pass() {
    echo -e "\033[32m[PASS]\033[0m $1"
    PASSED=$((PASSED + 1))
}

fail() {
    echo -e "\033[31m[FAIL]\033[0m $1"
    if [ $# -ge 2 ]; then
        echo "       $2"
    fi
    FAILED=$((FAILED + 1))
}

assert_exists() {
    if [ ! -e "$1" ]; then
        fail "$2" "Expected to exist: $1"
        return 1
    fi
    return 0
}

assert_contains() {
    if ! grep -q "$2" "$1"; then
        fail "$3" "Pattern '$2' not found in $1"
        return 1
    fi
    return 0
}

assert_not_contains() {
    if grep -q "$2" "$1"; then
        fail "$3" "Pattern '$2' should NOT be in $1"
        return 1
    fi
    return 0
}

echo "========================================"
echo "OpenClaw Memory System — Test Suite"
echo "Test workspace: $TEST_WORKSPACE"
echo "========================================"

# === TEST 1: Installation ===
echo ""
echo "[TEST] Installation script creates correct structure"
INSTALL_SCRIPT="$SKILL_ROOT/scripts/install.sh"
if [ ! -f "$INSTALL_SCRIPT" ]; then
    fail "Install script exists" "Not found: $INSTALL_SCRIPT"
else
    cd "$TEST_WORKSPACE"
    bash "$INSTALL_SCRIPT" "$TEST_WORKSPACE"

    if assert_exists "$TEST_WORKSPACE/memory" "memory dir" &&
       assert_exists "$TEST_WORKSPACE/memory/diary" "diary dir" &&
       assert_exists "$TEST_WORKSPACE/memory/dreams" "dreams dir" &&
       assert_exists "$TEST_WORKSPACE/MEMORY.md" "MEMORY.md" &&
       assert_exists "$TEST_WORKSPACE/HEARTBEAT.md" "HEARTBEAT.md" &&
       assert_exists "$TEST_WORKSPACE/memory/cron-inbox.md" "cron-inbox.md" &&
       assert_exists "$TEST_WORKSPACE/memory/heartbeat-state.json" "heartbeat-state.json" &&
       assert_exists "$TEST_WORKSPACE/memory/platform-posts.md" "platform-posts.md" &&
       assert_exists "$TEST_WORKSPACE/memory/strategy-notes.md" "strategy-notes.md" &&
       assert_contains "$TEST_WORKSPACE/MEMORY.md" "About \[Your Name" "MEMORY.md template"; then
        pass "Installation script creates correct structure"
    fi
fi

# === TEST 2: Daily Notes ===
echo ""
echo "[TEST] Daily notes file is created and formatted correctly"
TODAY=$(date +%Y-%m-%d)
TODAY_FILE="$TEST_WORKSPACE/memory/$TODAY.md"

if assert_exists "$TODAY_FILE" "Today's daily notes file" &&
   assert_contains "$TODAY_FILE" "# $TODAY" "Daily notes header" &&
   assert_contains "$TODAY_FILE" "Session Start" "Session start section"; then
    pass "Daily notes file is created and formatted correctly"
fi

# === TEST 3: Cron Inbox Processing ===
echo ""
echo "[TEST] Cron inbox entries are processed into daily notes"
INBOX_FILE="$TEST_WORKSPACE/memory/cron-inbox.md"

# Add a test entry to inbox
cat >> "$INBOX_FILE" << EOF

## [$(date '+%Y-%m-%d %H:%M')] TestBot -- Test event
This is a test entry from a cron job.
It has multiple lines.
EOF

# Run heartbeat check
HEARTBEAT_SCRIPT="$SKILL_ROOT/scripts/heartbeat-check.sh"
if [ -f "$HEARTBEAT_SCRIPT" ]; then
    bash "$HEARTBEAT_SCRIPT" "$TEST_WORKSPACE"

    if assert_contains "$TODAY_FILE" "TestBot" "Inbox entry in daily notes" &&
       assert_contains "$TODAY_FILE" "Cron Inbox Processing" "Inbox processing section" &&
       assert_not_contains "$INBOX_FILE" "TestBot" "Inbox cleared"; then
        pass "Cron inbox entries are processed into daily notes"
    fi
else
    fail "Heartbeat script exists" "Not found: $HEARTBEAT_SCRIPT"
fi

# === TEST 4: Memory Extraction ===
echo ""
echo "[TEST] Significant entries are extracted to MEMORY.md"
MEMORY_FILE="$TEST_WORKSPACE/MEMORY.md"

# Add a significant entry to daily notes
cat >> "$TODAY_FILE" << EOF

## 14:30 -- Major Decision Made
We decided to switch from MongoDB to PostgreSQL for the project.
This is an important architectural decision that will affect scaling.
**Decision:** Use PostgreSQL with TimescaleDB extension.
EOF

# Run memory extraction
EXTRACT_SCRIPT="$SKILL_ROOT/scripts/memory-extract.sh"
if [ -f "$EXTRACT_SCRIPT" ]; then
    bash "$EXTRACT_SCRIPT" "$TEST_WORKSPACE"

    if assert_contains "$MEMORY_FILE" "Daily Extracts" "Extracts section in MEMORY.md" &&
       assert_contains "$MEMORY_FILE" "Major Decision Made" "Extracted entry title" &&
       assert_contains "$MEMORY_FILE" "PostgreSQL" "Extracted content" &&
       assert_contains "$TODAY_FILE" "Memory extraction completed" "Extraction marker"; then
        pass "Significant entries are extracted to MEMORY.md"
    fi
else
    fail "Memory extract script exists" "Not found: $EXTRACT_SCRIPT"
fi

# === TEST 5: Heartbeat State ===
echo ""
echo "[TEST] Heartbeat state file is updated correctly"
STATE_FILE="$TEST_WORKSPACE/memory/heartbeat-state.json"

if assert_exists "$STATE_FILE" "Heartbeat state file"; then
    if [ "$JQ_AVAILABLE" = true ]; then
        VERSION=$(jq -r '.version' "$STATE_FILE" 2>/dev/null || echo "unknown")
        if [ "$VERSION" = "1.0.0" ]; then
            pass "Heartbeat state file is updated correctly"
        else
            fail "Heartbeat state version" "Expected 1.0.0, got $VERSION"
        fi
    else
        # Check without jq — just verify file exists and contains version string
        if assert_contains "$STATE_FILE" "1.0.0" "Version in state file"; then
            pass "Heartbeat state file is updated correctly (no jq)"
        fi
    fi
fi

# === TEST 6: Cron Inbox Body Preservation ===
echo ""
echo "[TEST] Cron inbox entries preserve body text"
INBOX_FILE="$TEST_WORKSPACE/memory/cron-inbox.md"

# Add a test entry with body text
cat >> "$INBOX_FILE" << EOF

## [$(date '+%Y-%m-%d %H:%M')] BodyTestBot -- Entry with body
This is the body text that should be preserved.
It has multiple lines of content.
**Key detail:** ELO now 1450
EOF

# Run heartbeat check again
bash "$HEARTBEAT_SCRIPT" "$TEST_WORKSPACE"

if assert_contains "$TODAY_FILE" "BodyTestBot" "Inbox entry header in daily notes" &&
   assert_contains "$TODAY_FILE" "This is the body text that should be preserved." "Inbox entry body in daily notes" &&
   assert_contains "$TODAY_FILE" "ELO now 1450" "Inbox entry detail in daily notes"; then
    pass "Cron inbox entries preserve body text"
else
    fail "Cron inbox body preservation" "Body text was lost during inbox processing"
fi

# === TEST 6: Dry Run ===
echo ""
echo "[TEST] Installation dry run does not create files"
DRY_RUN_WORKSPACE="$(mktemp -d)"
bash "$INSTALL_SCRIPT" "$DRY_RUN_WORKSPACE" --dry-run

if [ ! -f "$DRY_RUN_WORKSPACE/MEMORY.md" ]; then
    pass "Installation dry run does not create files"
else
    fail "Dry run should not create files" "MEMORY.md exists after dry run"
fi
rm -rf "$DRY_RUN_WORKSPACE"

# === SUMMARY ===
echo ""
echo "========================================"
echo "Test Results"
echo "========================================"

echo ""
echo "Total: $((PASSED + FAILED)) | Passed: $PASSED | Failed: $FAILED"

# Cleanup
echo ""
echo "Cleaning up test workspace..."
rm -rf "$TEST_WORKSPACE"

if [ "$FAILED" -gt 0 ]; then
    echo ""
    echo -e "\033[31mSOME TESTS FAILED\033[0m"
    exit 1
else
    echo ""
    echo -e "\033[32mALL TESTS PASSED ✓\033[0m"
    exit 0
fi
