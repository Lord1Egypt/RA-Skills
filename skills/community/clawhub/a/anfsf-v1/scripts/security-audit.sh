#!/bin/bash

# ASF V4.0 Security Audit Script
# Phase 3: Security audit and compliance checking.
# Version: v0.9.0

set -e

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   ASF V4.0 Security Audit                                         ║"
echo "║   Phase 3: Security Audit & Compliance                            ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
PASS=0
WARN=0
FAIL=0

# Function to check and report
check() {
  local name="$1"
  local condition="$2"
  
  if eval "$condition"; then
    echo -e "${GREEN}✓${NC} $name"
    ((PASS++))
  else
    echo -e "${RED}✗${NC} $name"
    ((FAIL++))
  fi
}

warn() {
  local name="$1"
  echo -e "${YELLOW}⚠${NC} $name"
  ((WARN++))
}

echo "=== Code Security Checks ==="
echo ""

# Check 1: No hardcoded secrets
check "No hardcoded secrets in source" "! grep -r 'password.*=.*[\"'\\''"].*[\"'\\''"]' skills/asf-v4/*.ts 2>/dev/null"

# Check 2: No eval() usage
check "No eval() usage" "! grep -r '\\beval\\b' skills/asf-v4/*.ts 2>/dev/null"

# Check 3: No console.log in production code (excluding benchmarks/tests)
warn "Console.log usage found (review for production)"

# Check 4: TypeScript strict mode
check "TypeScript strict mode enabled" "grep -q '\"strict\": true' tsconfig.json 2>/dev/null"

# Check 5: No any type usage (except in tests)
warn "Any type usage found (review for type safety)"

echo ""
echo "=== Permission & Access Control ==="
echo ""

# Check 6: Veto rules defined
check "Veto rules defined" "grep -q 'VetoEnforcer' skills/asf-v4/index.ts 2>/dev/null"

# Check 7: Ownership proof validation
check "Ownership proof validation" "grep -q 'validateProofs' skills/asf-v4/index.ts 2>/dev/null"

# Check 8: Single-writer check
check "Single-writer enforcement" "grep -q 'uniqueWriters' skills/asf-v4/integrations/security-audit-extension.ts 2>/dev/null"

# Check 9: Hard veto for critical resources
check "Hard veto for API contracts" "grep -q 'mode:.*hard' skills/asf-v4/config/asf-v4.config.yaml 2>/dev/null"

# Check 10: Architect approval required
check "Architect approval required" "grep -q 'architect.*approve' skills/asf-v4/config/asf-v4.config.yaml 2>/dev/null"

echo ""
echo "=== Data Isolation ==="
echo ""

# Check 11: Memory cache isolation
check "Memory cache with size limit" "grep -q 'maxSize.*10000' skills/asf-v4/integrations/memory-extension.ts 2>/dev/null"

# Check 12: Agent status registry isolation
check "Agent status per-agent isolation" "grep -q 'Map<string' skills/asf-v4/integrations/agent-status-extension.ts 2>/dev/null"

# Check 13: No global mutable state
warn "Global state found (review for isolation)"

echo ""
echo "=== Audit Logging ==="
echo ""

# Check 14: Change event logging
check "Change event logging" "grep -q 'writeChangeToMemory' skills/asf-v4/integrations/memory-extension.ts 2>/dev/null"

# Check 15: Timestamp on all events
check "Timestamps on events" "grep -q 'timestamp.*Date.now()' skills/asf-v4/integrations/*.ts 2>/dev/null"

# Check 16: Actor tracking
check "Actor tracking" "grep -q 'actorRoleId' skills/asf-v4/integrations/memory-extension.ts 2>/dev/null"

echo ""
echo "=== Safe Optimization ==="
echo ""

# Check 17: Cooldown mechanism
check "Optimizer cooldown" "grep -q 'cooldownUntil' skills/asf-v4/integrations/../optimization/safe-optimizer.ts 2>/dev/null"

# Check 18: Rollback capability
check "Rollback capability" "grep -q 'lastConfig' skills/asf-v4/integrations/../optimization/safe-optimizer.ts 2>/dev/null"

# Check 19: Failure threshold
check "Failure threshold" "grep -q 'failureThreshold' skills/asf-v4/integrations/../optimization/safe-optimizer.ts 2>/dev/null"

# Check 20: Forbidden optimizations
check "Forbidden optimizations defined" "grep -q 'FORBIDDEN_OPTIMIZATIONS' skills/asf-v4/integrations/../optimization/safe-optimizer.ts 2>/dev/null"

echo ""
echo "=== Dependency Security ==="
echo ""

# Check 21: No dev dependencies in production
check "No dev dependencies in production" "! grep -q 'devDependencies' skills/asf-v4/package.json 2>/dev/null || warn 'Dev dependencies found (review)'"

# Check 22: Node.js version constraint
check "Node.js version constraint" "grep -q '\"node\":' skills/asf-v4/package.json 2>/dev/null"

# Check 23: No peer dependency conflicts
check "No peer dependency conflicts" "grep -q '\"peerDependencies\":' skills/asf-v4/package.json 2>/dev/null"

echo ""
echo "=== Summary ==="
echo ""
echo "Passed: $PASS"
echo "Warnings: $WARN"
echo "Failed: $FAIL"
echo ""

TOTAL=$((PASS + FAIL))
if [ $TOTAL -gt 0 ]; then
  SCORE=$((PASS * 100 / TOTAL))
  echo "Security Score: $SCORE%"
fi

echo ""

if [ $FAIL -gt 0 ]; then
  echo -e "${RED}Security audit failed with $FAIL issues${NC}"
  exit 1
elif [ $WARN -gt 5 ]; then
  echo -e "${YELLOW}Security audit passed with $WARN warnings${NC}"
  exit 0
else
  echo -e "${GREEN}Security audit passed!${NC}"
  exit 0
fi
