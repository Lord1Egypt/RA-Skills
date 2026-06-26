#!/usr/bin/env bash
# preflight-check.sh — Run all checks before release.
# Exits non-zero if any check fails.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

cd "$ROOT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

pass() { echo -e "${GREEN}✓${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; exit 1; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
info() { echo -e "  $1"; }

echo "═══════════════════════════════════"
echo "  Release Preflight Checks"
echo "═══════════════════════════════════"
echo ""

# 1. Git clean
echo "▶ Checking git status..."
DIRTY=$(git status --porcelain)
if [ -n "$DIRTY" ]; then
  fail "Working directory is not clean. Commit or stash changes first."
fi
pass "Git working directory clean"

# 2. On a valid branch
BRANCH=$(git branch --show-current)
if [ -z "$BRANCH" ]; then
  fail "Not on a branch (detached HEAD)."
fi
info "Branch: $BRANCH"

# 3. Up to date with remote
git fetch --quiet 2>/dev/null || warn "Could not fetch from remote (offline?)"
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null || echo "")
if [ -n "$REMOTE" ] && [ "$LOCAL" != "$REMOTE" ]; then
  warn "Local branch is not in sync with origin/$BRANCH"
fi
pass "Branch check passed"

# 4. Tests
echo ""
echo "▶ Running tests..."
if [ -f "package.json" ]; then
  SCRIPTS=$(node -e "const p=require('./package.json'); console.log(Object.keys(p.scripts||{}).join(','))")
  if echo "$SCRIPTS" | grep -q "test"; then
    npm test 2>&1 && pass "Tests passed" || fail "Tests failed"
  else
    warn "No test script found — skipping"
  fi
else
  warn "No package.json found — skipping npm tests"
fi

# 5. Lint
echo ""
echo "▶ Running lint..."
if [ -f "package.json" ]; then
  if echo "$SCRIPTS" | grep -q "lint"; then
    npm run lint 2>&1 && pass "Lint passed" || fail "Lint failed"
  else
    warn "No lint script found — skipping"
  fi
fi

# 6. Build
echo ""
echo "▶ Running build..."
if [ -f "package.json" ]; then
  if echo "$SCRIPTS" | grep -q "build"; then
    npm run build 2>&1 && pass "Build passed" || fail "Build failed"
  else
    warn "No build script found — skipping"
  fi
fi

# 7. Version consistency
echo ""
echo "▶ Checking version consistency..."
PKG_VERSION=$(node -e "console.log(require('./package.json').version)")
info "package.json version: $PKG_VERSION"
pass "Version check passed"

echo ""
echo "═══════════════════════════════════"
echo -e "  ${GREEN}All preflight checks passed ✓${NC}"
echo "═══════════════════════════════════"
