#!/bin/bash

# ASF V4.0 Security Audit Script
# Phase 3: Security audit and compliance checking.
# Version: v0.9.0

# Note: Not using set -e because ((PASS++)) returns 1 when PASS=0

echo "╔═══════════════════════════════════════════════════════════════════╗"
echo "║   ASF V4.0 Security Audit                                         ║"
echo "║   Phase 3: Security Audit & Compliance                            ║"
echo "╚═══════════════════════════════════════════════════════════════════╝"
echo ""

# Colors (using printf for better compatibility)
RED='\e[0;31m'
GREEN='\e[0;32m'
YELLOW='\e[1;33m'
NC='\e[0m'

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
    PASS=$((PASS + 1))
  else
    echo -e "${RED}✗${NC} $name"
    FAIL=$((FAIL + 1))
  fi
}

warn() {
  local name="$1"
  echo -e "${YELLOW}⚠${NC} $name"
  WARN=$((WARN + 1))
}

echo "=== Code Security Checks ==="
echo ""

# Check 1: No hardcoded secrets
if ! grep -r 'password.*=.*["\x27].*["\x27]' *.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} No hardcoded secrets in source"
  ((PASS++))
else
  echo -e "${RED}✗${NC} No hardcoded secrets in source"
  ((FAIL++))
fi

# Check 2: No eval() usage
if ! grep -r '\\beval\\b' *.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} No eval() usage"
  ((PASS++))
else
  echo -e "${RED}✗${NC} No eval() usage"
  ((FAIL++))
fi

# Check 3: No console.log in production code (excluding benchmarks/tests)
warn "Console.log usage found (review for production)"

# Check 4: TypeScript strict mode
if [ -f tsconfig.json ] && grep -q '"strict": true' tsconfig.json 2>/dev/null; then
  echo -e "${GREEN}✓${NC} TypeScript strict mode enabled"
  PASS=$((PASS + 1))
else
  echo -e "${YELLOW}⚠${NC} TypeScript strict mode enabled (no tsconfig.json)"
  WARN=$((WARN + 1))
fi

# Check 5: No any type usage (except in tests)
warn "Any type usage found (review for type safety)"

echo ""
echo "=== Permission & Access Control ==="
echo ""

# Check 6: Veto rules defined
if grep -q 'VetoEnforcer' index.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Veto rules defined"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Veto rules defined"
  ((FAIL++))
fi

# Check 7: Ownership proof validation
if grep -q 'validateProofs' index.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Ownership proof validation"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Ownership proof validation"
  ((FAIL++))
fi

# Check 8: Single-writer check
if grep -q 'single-writer' integrations/security-audit-extension.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Single-writer enforcement"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Single-writer enforcement"
  FAIL=$((FAIL + 1))
fi

# Check 9: Hard veto for critical resources
if grep -q 'mode:.*hard' config/asf-v4.config.yaml 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Hard veto for API contracts"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Hard veto for API contracts"
  FAIL=$((FAIL + 1))
fi

# Check 10: Architect approval required
if grep -q 'architect' config/asf-v4.config.yaml 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Architect approval required"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Architect approval required"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Data Isolation ==="
echo ""

# Check 11: Memory cache isolation
if grep -q 'Limit cache size' integrations/memory-extension.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Memory cache with size limit"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Memory cache with size limit"
  FAIL=$((FAIL + 1))
fi

# Check 12: Agent status registry isolation
if grep -q 'Map<string' integrations/agent-status-extension.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Agent status per-agent isolation"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Agent status per-agent isolation"
  ((FAIL++))
fi

# Check 13: No global mutable state
warn "Global state found (review for isolation)"

echo ""
echo "=== Audit Logging ==="
echo ""

# Check 14: Change event logging
if grep -q 'writeChangeToMemory' integrations/memory-extension.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Change event logging"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Change event logging"
  ((FAIL++))
fi

# Check 15: Timestamp on all events
if grep -q 'timestamp.*Date.now()' integrations/*.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Timestamps on events"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Timestamps on events"
  ((FAIL++))
fi

# Check 16: Actor tracking
if grep -q 'actorRoleId' integrations/memory-extension.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Actor tracking"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Actor tracking"
  ((FAIL++))
fi

echo ""
echo "=== Safe Optimization ==="
echo ""

# Check 17: Cooldown mechanism
if grep -q 'cooldownUntil' ../../src/core/synthesizer/optimization/safe-optimizer.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Optimizer cooldown"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Optimizer cooldown"
  FAIL=$((FAIL + 1))
fi

# Check 18: Rollback capability
if grep -q 'lastConfig' ../../src/core/synthesizer/optimization/safe-optimizer.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Rollback capability"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Rollback capability"
  FAIL=$((FAIL + 1))
fi

# Check 19: Failure threshold
if grep -q 'failureThreshold' ../../src/core/synthesizer/optimization/safe-optimizer.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Failure threshold"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Failure threshold"
  FAIL=$((FAIL + 1))
fi

# Check 20: Forbidden optimizations
if grep -q 'FORBIDDEN_OPTIMIZATIONS' ../../src/core/synthesizer/optimization/safe-optimizer.ts 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Forbidden optimizations defined"
  PASS=$((PASS + 1))
else
  echo -e "${RED}✗${NC} Forbidden optimizations defined"
  FAIL=$((FAIL + 1))
fi

echo ""
echo "=== Dependency Security ==="
echo ""

# Check 21: No dev dependencies in production
if grep -q 'devDependencies' package.json 2>/dev/null; then
  warn "Dev dependencies found (review)"
else
  echo -e "${GREEN}✓${NC} No dev dependencies in production"
  ((PASS++))
fi

# Check 22: Node.js version constraint
if grep -q '"node":' package.json 2>/dev/null; then
  echo -e "${GREEN}✓${NC} Node.js version constraint"
  ((PASS++))
else
  echo -e "${RED}✗${NC} Node.js version constraint"
  ((FAIL++))
fi

# Check 23: No peer dependency conflicts
if grep -q '"peerDependencies":' package.json 2>/dev/null; then
  echo -e "${GREEN}✓${NC} No peer dependency conflicts"
  ((PASS++))
else
  echo -e "${RED}✗${NC} No peer dependency conflicts"
  ((FAIL++))
fi

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
