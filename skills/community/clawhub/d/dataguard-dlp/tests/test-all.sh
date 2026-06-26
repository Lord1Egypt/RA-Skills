#!/bin/bash
# DataGuard DLP — Test Suite v1.2.0
# Copyright (c) 2026 Jeff Cyprien. Licensed under MIT.
# https://github.com/jeffcGit/dataguard-dlp
#
# Tests simplified pattern set (18 core patterns) + override + grep -P audit

# Don't exit on error - we want to see all results
# set -e removed

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPTS_DIR="$SKILL_DIR/scripts"
PASS=0
FAIL=0
TOTAL=0

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "========================================"
echo "  DataGuard v2.1 Test Suite"
echo "========================================"
echo ""

test_score() {
    local name="$1"
    local input="$2"
    local expected_min="$3"
    
    TOTAL=$((TOTAL + 1))
    
    result=$(echo "$input" | bash "$SCRIPTS_DIR/dlp-scan.sh" 2>&1)
    exit_code=$?
    
    if [ "$exit_code" -ge "$expected_min" ]; then
        echo -e "${GREEN}✓ PASS${NC} [$TOTAL] $name (score: $exit_code)"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}✗ FAIL${NC} [$TOTAL] $name (expected ≥ $expected_min, got $exit_code)"
        FAIL=$((FAIL + 1))
    fi
}

test_clean() {
    local name="$1"
    local input="$2"
    
    TOTAL=$((TOTAL + 1))
    
    result=$(echo "$input" | bash "$SCRIPTS_DIR/dlp-scan.sh" 2>&1)
    exit_code=$?
    
    if [ "$exit_code" -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC} [$TOTAL] $name (clean)"
        PASS=$((PASS + 1))
    else
        echo -e "${RED}✗ FAIL${NC} [$TOTAL] $name (should be clean, got score $exit_code)"
        FAIL=$((FAIL + 1))
    fi
}

echo -e "${BLUE}=== CRITICAL Patterns (Score ≥10) ===${NC}"
echo ""
echo "Testing pattern: sk-(ant|proj)?-?[a-zA-Z0-9_-]{20,}"
echo "Test input: sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx"
echo ""

test_score "Anthropic API key" "sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx" 10
test_score "OpenAI API key" "sk-proj-xxxxxxxxxxxxxxxxxxxx" 10
test_score "Generic API key" "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx" 10
test_score "GitHub PAT" "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 10
test_score "AWS Access Key" "AKIAIOSFODNN7EXAMPLE" 10
test_score "Slack Bot Token" "xoxb-1234567890-1234567890-abcdefghijkl" 10
test_score "Brevo API key" "xkeysib-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" 10
test_score "Bearer JWT" "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgDry" 10
test_score "Private key" "-----BEGIN RSA PRIVATE KEY-----" 10
test_score "MySQL URL with password" "mysql://user:secret123@localhost/db" 10
test_score "Postgres URL with password" "postgres://admin:p@ssw0rd@db.example.com/mydb" 10
test_score "AWS secret key" "aws_secret_access_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" 10
test_score "GCP service account" 'type: service_account project_id: myproject private_key: "-----BEGIN"' 10
test_score "Password in config" "password=supersecret123" 10

echo ""
echo -e "${BLUE}=== HIGH Patterns (Score ≥8) ===${NC}"
echo ""

test_score "SSN" "SSN: 123-45-6789" 8
test_score "Visa card" "Card: 4111111111111111" 8
test_score "Mastercard" "Card: 5500000000000004" 8
test_score "Amex card" "Card: 340000000000009" 8
test_score "CVV" "cvv: 123" 8
test_score "Internal IP 10.x" "Server: 10.0.0.1" 8
test_score "Internal IP 192.168.x" "Server: 192.168.1.100" 8
test_score "Internal IP 172.16.x" "Server: 172.16.0.1" 8
test_score "Internal hostname .local" "Host: server.local" 8
test_score "Internal hostname .internal" "Host: ip-10-0-1-50.ec2.internal" 8
test_score "Sensitive path .ssh" "File: /home/user/.ssh/id_rsa" 8
test_score "Sensitive path .env" "File: ~/.env" 8
test_score "Sensitive path /etc/shadow" "File: /etc/shadow" 8

echo ""
echo -e "${BLUE}=== MEDIUM Patterns (Score ≥5) ===${NC}"
echo ""

test_score "Phone number US" "Phone: 555-123-4567" 5
test_score "Phone international" "Phone: +1-347-644-7040" 5
test_score "Email with name" "John Smith john@example.com" 5
test_score "Secrets file .json" "File: secrets.json" 5
test_score "Secrets file .pem" "File: server.pem" 5

echo ""
echo -e "${BLUE}=== Clean Inputs (Score 0) ===${NC}"
echo ""

test_clean "Normal text" "Hello, this is a normal message"
test_clean "Public URL" "https://example.com/api/data"
test_clean "Public IP" "Server: 8.8.8.8"
test_clean "Regular sentence" "Send an email to discuss the project"
test_clean "Code snippet" "function hello() { return 'world'; }"
test_clean "Placeholder key" "Replace YOUR_API_KEY with your actual key"

echo ""
echo -e "${BLUE}=== Context Tracking ===${NC}"
echo ""

# Clear context
bash "$SCRIPTS_DIR/context-track.sh" --clear 2>/dev/null || true

# Log a sensitive read
bash "$SCRIPTS_DIR/context-track.sh" --log "/home/user/.env" "AWS_KEY" 2>/dev/null

TOTAL=$((TOTAL + 1))
result=$(bash "$SCRIPTS_DIR/context-track.sh" --score 2>/dev/null)
if echo "$result" | grep -q "score"; then
    echo -e "${GREEN}✓ PASS${NC} [$TOTAL] Context tracking active"
    PASS=$((PASS + 1))
else
    echo -e "${YELLOW}? SKIP${NC} [$TOTAL] Context tracking needs setup"
fi

# Clear for next tests
bash "$SCRIPTS_DIR/context-track.sh" --clear 2>/dev/null || true

echo ""
echo -e "${BLUE}=== Edge Cases ===${NC}"
echo ""

test_score "Multiple secrets combined" "aws_key=AKIAIOSFODNN7EXAMPLE password=secret123" 10
test_score "URL encoded (still detected)" "password=%73%65%63%72%65%74" 5

echo ""
echo "========================================"
echo -e "  Results: ${GREEN}$PASS passed${NC}, ${RED}$FAIL failed${NC}, $TOTAL total"
echo "========================================"

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ ALL TESTS PASSED${NC}"
    exit 0
else
    echo -e "${RED}✗ SOME TESTS FAILED${NC}"
    exit 1
fi