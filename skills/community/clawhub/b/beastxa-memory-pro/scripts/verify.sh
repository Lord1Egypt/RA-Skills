#!/usr/bin/env bash
#
# BeastXA Memory Pro — Installation Verifier
#
set -euo pipefail

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "🔍 BeastXA Memory Pro — Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

PASS=0
FAIL=0
WARN=0

check() {
    local label="$1"
    local condition="$2"
    if eval "$condition" > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅${NC} $label"
        ((PASS++))
    else
        echo -e "   ${RED}❌${NC} $label"
        ((FAIL++))
    fi
}

warn() {
    local label="$1"
    local condition="$2"
    if eval "$condition" > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅${NC} $label"
        ((PASS++))
    else
        echo -e "   ${YELLOW}⚠️${NC}  $label (optional)"
        ((WARN++))
    fi
}

echo "Prerequisites:"
check "Python 3 installed" "command -v python3"
check "OpenClaw installed" "command -v openclaw"
check "OpenClaw config exists" "test -f ~/.openclaw/openclaw.json"
echo ""

echo "Memory structure:"
check "memory/ directory exists" "test -d memory"
check "memory/topics/ directory exists" "test -d memory/topics"
check "memory/session-notes.md exists" "test -f memory/session-notes.md"
warn "MEMORY.md exists" "test -f MEMORY.md"
warn "memory/MEMORY-INDEX.md exists" "test -f memory/MEMORY-INDEX.md"
warn "Topic files exist" "ls memory/topics/*.md 2>/dev/null | head -1"
echo ""

echo "Configuration:"
check "memoryFlush enabled" "python3 -c \"
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    c = json.load(f)
assert c.get('agents',{}).get('defaults',{}).get('compaction',{}).get('memoryFlush',{}).get('enabled') == True
\""
check "Compaction instructions set" "python3 -c \"
import json
with open('$HOME/.openclaw/openclaw.json') as f:
    c = json.load(f)
assert 'instructions' in c.get('agents',{}).get('defaults',{}).get('compaction',{})
\""
echo ""

echo "Cron jobs:"
warn "Daily cleanup cron" "openclaw cron list 2>/dev/null | grep -q 'Memory Pro.*Daily'"
warn "Weekly deep clean cron" "openclaw cron list 2>/dev/null | grep -q 'Memory Pro.*Weekly'"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo -e "Results: ${GREEN}${PASS} passed${NC}, ${RED}${FAIL} failed${NC}, ${YELLOW}${WARN} warnings${NC}"

if [ "$FAIL" -eq 0 ]; then
    echo -e "${GREEN}🎉 All checks passed!${NC}"
else
    echo -e "${RED}⚠️  Some checks failed. Run install.sh to fix.${NC}"
fi
echo ""
