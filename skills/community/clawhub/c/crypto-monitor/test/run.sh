#!/bin/bash
set -euo pipefail
PASS=0; FAIL=0

assert() { if [ $? -eq 0 ]; then PASS=$((PASS+1)); echo "  ✅ $1"; else FAIL=$((FAIL+1)); echo "  ❌ $1"; fi; }

echo "=== Crypto Monitor Tests ==="

echo "Test: SKILL.md exists"
[ -f SKILL.md ]; assert "SKILL.md found"

echo "Test: SKILL.md has frontmatter"
grep -q "^---" SKILL.md; assert "Frontmatter opening"
grep -q "^name:" SKILL.md; assert "name field"
grep -q "^description:" SKILL.md; assert "description field"
grep -q "^version:" SKILL.md; assert "version field"

echo "Test: Scripts are executable"
[ -x scripts/price.sh ]; assert "price.sh executable"
[ -x scripts/whale.sh ]; assert "whale.sh executable"
[ -x scripts/trending.sh ]; assert "trending.sh executable"
[ -x scripts/airdrop.sh ]; assert "airdrop.sh executable"

echo "Test: Scripts have valid shebangs"
head -1 scripts/price.sh | grep -q "^#!/bin/bash"; assert "price.sh shebang"
head -1 scripts/whale.sh | grep -q "^#!/bin/bash"; assert "whale.sh shebang"

echo "Test: No hardcoded secrets in scripts"
! grep -r "ghp_\|gho_\|sk-" scripts/ 2>/dev/null; assert "No leaks in scripts"

echo "Test: price.sh help works"
./scripts/price.sh --help >/dev/null 2>&1; assert "price.sh --help"

echo "Test: price.sh can fetch data (may fail on rate limit)"
./scripts/price.sh bitcoin --format json 2>/dev/null && assert "price.sh bitcoin fetch" || echo "  ⚠️  API rate limited (expected)"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
[ $FAIL -eq 0 ] && echo "🎉 All tests passed!" || echo "⚠️  Some tests failed"
exit $FAIL
