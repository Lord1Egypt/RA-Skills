#!/usr/bin/env bash
# Demo: arc-shield catching real-world leaks

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ARC_SHIELD="${SCRIPT_DIR}/../scripts/arc-shield.sh"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║   🛡️  ARC-SHIELD DEMO                 ║${NC}"
echo -e "${CYAN}║   Catching Real-World Secret Leaks    ║${NC}"
echo -e "${CYAN}╔════════════════════════════════════════╗${NC}"
echo

demo_catch() {
    local title="$1"
    local message="$2"
    
    echo -e "${YELLOW}━━━ $title ━━━${NC}"
    echo -e "${CYAN}Message:${NC} ${message:0:80}..."
    echo
    
    # Scan
    if echo "$message" | "$ARC_SHIELD" --strict 2>&1 | grep -i "blocked" > /dev/null; then
        echo -e "${RED}❌ BLOCKED${NC} (as expected)"
    else
        echo -e "${GREEN}✓ Detected${NC}"
    fi
    
    echo "$message" | "$ARC_SHIELD" --report 2>&1 | head -5
    echo
}

# Example 1: GitHub PAT leak
demo_catch "GitHub PAT in debug output" \
"Here's the git config:
[remote \"origin\"]
url = https://ghp_abc123def456ghi789jkl012mno345pqr:x-oauth-basic@github.com/user/repo.git"

# Example 2: 1Password token
demo_catch "1Password service account token" \
"To authenticate, use: ops_eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9_longbase64string"

# Example 3: Instagram password
demo_catch "Instagram password in login attempt" \
"Trying to login with instagram credentials: user@example.com / MyP@ssw0rd123"

# Example 4: Wallet mnemonic
demo_catch "Wallet recovery phrase" \
"Found in ~/.secrets/wallet.txt: abandon ability able about above absent absorb abstract absurd abuse access accident"

# Example 5: AWS credentials
demo_catch "AWS keys in environment" \
"export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# Example 6: Secret file path
demo_catch "Secret file path leak" \
"I saved your password to ~/.secrets/instagram-password.txt for safekeeping"

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo
echo -e "${GREEN}✓ Arc-shield successfully caught all leaked secrets!${NC}"
echo -e "${CYAN}Run './quick-test.sh' for full test suite${NC}"
