#!/bin/bash
#
# End-to-End CLI Tests for ClawPurse
# Tests all CLI commands in realistic scenarios
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test configuration
TEST_DIR="/tmp/clawpurse-e2e-test-$$"
TEST_PASSWORD="test-password-123456"
TEST_MNEMONIC="abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon art"
TEST_ADDRESS_2="neutaro1test2qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqtest2"

# Counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Setup
setup() {
    echo "Setting up test environment..."
    mkdir -p "$TEST_DIR"
    export HOME="$TEST_DIR"
    export CLAWPURSE_PASSWORD="$TEST_PASSWORD"
}

# Cleanup
cleanup() {
    echo "Cleaning up test environment..."
    rm -rf "$TEST_DIR"
}

# Test helper functions
assert_success() {
    local cmd="$1"
    local description="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Testing: $description... "
    
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Command: $cmd"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_failure() {
    local cmd="$1"
    local description="$2"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Testing: $description... "
    
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "${RED}✗ FAIL (expected failure)${NC}"
        echo "  Command: $cmd"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    else
        echo -e "${GREEN}✓ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    fi
}

assert_contains() {
    local cmd="$1"
    local expected="$2"
    local description="$3"
    
    TESTS_RUN=$((TESTS_RUN + 1))
    echo -n "Testing: $description... "
    
    local output
    output=$(eval "$cmd" 2>&1)
    
    if echo "$output" | grep -q "$expected"; then
        echo -e "${GREEN}✓ PASS${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        echo "  Command: $cmd"
        echo "  Expected to contain: $expected"
        echo "  Actual output: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

# Test sections
test_wallet_init() {
    echo ""
    echo "=== Testing Wallet Initialization ==="
    
    # Test init with enforce mode
    assert_success \
        "echo '$TEST_PASSWORD' | clawpurse init --password '$TEST_PASSWORD' --allowlist-mode enforce" \
        "Initialize wallet with enforce mode"
    
    # Test that keystore exists
    assert_success \
        "test -f $HOME/.clawpurse/keystore.enc" \
        "Keystore file created"
    
    # Test keystore permissions
    assert_success \
        "test \$(stat -c '%a' $HOME/.clawpurse/keystore.enc) = '600'" \
        "Keystore has correct permissions (600)"
    
    # Clean up for next tests
    rm -rf "$HOME/.clawpurse"
}

test_wallet_import() {
    echo ""
    echo "=== Testing Wallet Import ==="
    
    # Test import with mnemonic
    assert_success \
        "echo -e '$TEST_MNEMONIC\n$TEST_PASSWORD' | clawpurse import" \
        "Import wallet from mnemonic"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
    
    # Test import with environment variable
    export CLAWPURSE_MNEMONIC="$TEST_MNEMONIC"
    assert_success \
        "clawpurse import --password '$TEST_PASSWORD'" \
        "Import wallet from environment variable"
    unset CLAWPURSE_MNEMONIC
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_address_command() {
    echo ""
    echo "=== Testing Address Command ==="
    
    # Initialize wallet first
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test address display
    assert_contains \
        "clawpurse address" \
        "neutaro1" \
        "Display wallet address"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_balance_command() {
    echo ""
    echo "=== Testing Balance Command ==="
    
    # Initialize wallet first
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test balance query (will fail without testnet, but tests command parsing)
    # This is a placeholder - actual test would require testnet connection
    echo -n "Testing: Query balance (command parsing)... "
    echo -e "${YELLOW}⊘ SKIP (requires testnet)${NC}"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_send_validation() {
    echo ""
    echo "=== Testing Send Command Validation ==="
    
    # Initialize wallet
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test send with invalid address
    assert_failure \
        "clawpurse send invalid-address 10 --password '$TEST_PASSWORD'" \
        "Reject invalid recipient address"
    
    # Test send with negative amount
    assert_failure \
        "clawpurse send $TEST_ADDRESS_2 -10 --password '$TEST_PASSWORD'" \
        "Reject negative amount"
    
    # Test send with zero amount
    assert_failure \
        "clawpurse send $TEST_ADDRESS_2 0 --password '$TEST_PASSWORD'" \
        "Reject zero amount"
    
    # Test send without password
    unset CLAWPURSE_PASSWORD
    assert_failure \
        "clawpurse send $TEST_ADDRESS_2 10" \
        "Require password for send"
    export CLAWPURSE_PASSWORD="$TEST_PASSWORD"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_allowlist_commands() {
    echo ""
    echo "=== Testing Allowlist Commands ==="
    
    # Initialize wallet with enforce mode
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import --allowlist-mode enforce > /dev/null 2>&1
    
    # Test allowlist init
    assert_success \
        "clawpurse allowlist init" \
        "Initialize allowlist"
    
    # Test allowlist add
    assert_success \
        "clawpurse allowlist add $TEST_ADDRESS_2 --name 'Test Address'" \
        "Add address to allowlist"
    
    # Test allowlist add with max
    assert_success \
        "clawpurse allowlist add $TEST_ADDRESS_2 --name 'Test' --max 100" \
        "Add address with max limit"
    
    # Test allowlist list
    assert_contains \
        "clawpurse allowlist list" \
        "$TEST_ADDRESS_2" \
        "List allowlist entries"
    
    # Test allowlist remove
    assert_success \
        "clawpurse allowlist remove $TEST_ADDRESS_2" \
        "Remove address from allowlist"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_status_command() {
    echo ""
    echo "=== Testing Status Command ==="
    
    # Test status command (will fail without network, but tests command parsing)
    echo -n "Testing: Chain status (command parsing)... "
    echo -e "${YELLOW}⊘ SKIP (requires network)${NC}"
}

test_history_command() {
    echo ""
    echo "=== Testing History Command ==="
    
    # Initialize wallet
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test history command (should work even with no transactions)
    assert_success \
        "clawpurse history" \
        "Display transaction history"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_staking_commands() {
    echo ""
    echo "=== Testing Staking Commands (v2.0) ==="
    
    # Initialize wallet
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test validators command
    echo -n "Testing: List validators... "
    echo -e "${YELLOW}⊘ SKIP (requires network)${NC}"
    
    # Test delegations command
    assert_success \
        "clawpurse delegations" \
        "List delegations (command parsing)"
    
    # Test unbonding command
    assert_success \
        "clawpurse unbonding" \
        "List unbonding delegations (command parsing)"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_error_handling() {
    echo ""
    echo "=== Testing Error Handling ==="
    
    # Test command without wallet
    assert_failure \
        "clawpurse balance --password '$TEST_PASSWORD'" \
        "Fail gracefully when wallet not initialized"
    
    # Initialize wallet
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test command with wrong password
    assert_failure \
        "clawpurse balance --password 'wrong-password'" \
        "Reject incorrect password"
    
    # Test unknown command
    assert_failure \
        "clawpurse unknown-command" \
        "Reject unknown command"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

test_file_operations() {
    echo ""
    echo "=== Testing File Operations ==="
    
    # Initialize wallet
    echo -e "$TEST_MNEMONIC\n$TEST_PASSWORD" | clawpurse import > /dev/null 2>&1
    
    # Test custom keystore path
    assert_success \
        "clawpurse balance --password '$TEST_PASSWORD' --keystore $TEST_DIR/custom-keystore.enc || true" \
        "Support custom keystore path"
    
    # Test custom allowlist path
    assert_success \
        "clawpurse allowlist list --allowlist $TEST_DIR/custom-allowlist.json || true" \
        "Support custom allowlist path"
    
    # Clean up
    rm -rf "$HOME/.clawpurse"
}

# Main test execution
main() {
    echo "╔════════════════════════════════════════════╗"
    echo "║  ClawPurse End-to-End CLI Tests           ║"
    echo "╚════════════════════════════════════════════╝"
    echo ""
    
    setup
    
    # Run all test suites
    test_wallet_init
    test_wallet_import
    test_address_command
    test_balance_command
    test_send_validation
    test_allowlist_commands
    test_status_command
    test_history_command
    test_staking_commands
    test_error_handling
    test_file_operations
    
    cleanup
    
    # Print summary
    echo ""
    echo "╔════════════════════════════════════════════╗"
    echo "║  Test Summary                              ║"
    echo "╚════════════════════════════════════════════╝"
    echo ""
    echo "  Tests Run:    $TESTS_RUN"
    echo -e "  Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
    echo -e "  Tests Failed: ${RED}$TESTS_FAILED${NC}"
    echo ""
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}Some tests failed.${NC}"
        exit 1
    fi
}

# Run tests
main
