#!/usr/bin/env bash
# qa-check.sh — Automated QA gate checks for agent output
# Usage: qa-check.sh <gate-level> <file-or-content>
#   gate-level: 0 (internal), 1 (human-facing), 2 (external), 3 (code)
#
# Examples:
#   qa-check.sh 0 ./output.md          # Internal file check
#   qa-check.sh 3 ./src/app.js         # Code check
#   echo "message" | qa-check.sh 1 -   # Pipe content for human-facing check

set -euo pipefail

GATE="${1:-0}"
INPUT="${2:--}"
ERRORS=0
WARNINGS=0

# Color output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

fail() { echo -e "${RED}🔴 BLOCK: $1${NC}"; ((ERRORS++)); }
warn() { echo -e "${YELLOW}🟡 FIX: $1${NC}"; ((WARNINGS++)); }
pass() { echo -e "${GREEN}✅ $1${NC}"; }

# Read input
if [ "$INPUT" = "-" ]; then
  CONTENT=$(cat)
  FILEPATH="(stdin)"
else
  if [ ! -f "$INPUT" ]; then
    fail "File not found: $INPUT"
    exit 1
  fi
  CONTENT=$(cat "$INPUT")
  FILEPATH="$INPUT"
fi

echo "═══════════════════════════════════════"
echo "QA Gate $GATE Check: $FILEPATH"
echo "═══════════════════════════════════════"
echo ""

# ── Gate 0: Internal checks ──
echo "── Gate 0: Verify & Commit ──"

# Check for placeholders
if echo "$CONTENT" | grep -qiE '(TODO|PLACEHOLDER|TBD|Lorem ipsum)'; then
  fail "Placeholder text found"
  echo "$CONTENT" | grep -niE '(TODO|PLACEHOLDER|TBD|Lorem ipsum)' | head -5
else
  pass "No placeholder text"
fi

# Check file is non-empty
if [ -z "$CONTENT" ]; then
  fail "File is empty"
else
  pass "File is non-empty ($(echo "$CONTENT" | wc -c | tr -d ' ') bytes)"
fi

# Check for secrets
if echo "$CONTENT" | grep -qE '(sk-[a-zA-Z0-9]{20,}|api_key\s*[=:]\s*["\x27][A-Za-z0-9]{15,}|AKIA[A-Z0-9]{16}|ghp_[a-zA-Z0-9]{36})'; then
  fail "Possible secret/API key detected"
else
  pass "No secrets detected"
fi

# ── Gate 1: Human-facing checks (if gate >= 1) ──
if [ "$GATE" -ge 1 ]; then
  echo ""
  echo "── Gate 1: Human-Facing ──"

  # Character count for channel limits
  CHAR_COUNT=$(echo "$CONTENT" | wc -c | tr -d ' ')
  if [ "$CHAR_COUNT" -gt 4096 ]; then
    warn "Content is $CHAR_COUNT chars — exceeds Telegram limit (4096)"
  elif [ "$CHAR_COUNT" -gt 2000 ]; then
    warn "Content is $CHAR_COUNT chars — exceeds Discord limit (2000), OK for Telegram"
  else
    pass "Content length OK ($CHAR_COUNT chars)"
  fi

  # Check for long paragraphs (>3 lines without a break)
  LONG_PARA=$(echo "$CONTENT" | awk '
    BEGIN { count=0; long=0 }
    /^[[:space:]]*$/ { if (count > 3) long++; count=0; next }
    { count++ }
    END { if (count > 3) long++; print long }
  ')
  if [ "$LONG_PARA" -gt 0 ]; then
    warn "$LONG_PARA paragraph(s) exceed 3 lines — break them up"
  else
    pass "All paragraphs ≤ 3 lines"
  fi
fi

# ── Gate 2: External checks (if gate >= 2) ──
if [ "$GATE" -ge 2 ]; then
  echo ""
  echo "── Gate 2: External ──"

  # Check for internal context leaks
  if echo "$CONTENT" | grep -qiE '(memory/|MEMORY\.md|AGENTS\.md|SOUL\.md|OpenClaw|heartbeat|sub-agent|cron job|sessions_spawn)'; then
    fail "Possible internal context leak detected"
    echo "$CONTENT" | grep -niE '(memory/|MEMORY\.md|AGENTS\.md|SOUL\.md|OpenClaw|heartbeat|sub-agent|cron job|sessions_spawn)' | head -5
  else
    pass "No internal context leaks"
  fi

  # Check for private data patterns
  if echo "$CONTENT" | grep -qE '([0-9]{3}-[0-9]{2}-[0-9]{4}|[0-9]{4}[[:space:]][0-9]{4}[[:space:]][0-9]{4}[[:space:]][0-9]{4})'; then
    fail "Possible private data (SSN or card number pattern)"
  else
    pass "No private data patterns"
  fi
fi

# ── Gate 3: Code checks (if gate >= 3) ──
if [ "$GATE" -ge 3 ]; then
  echo ""
  echo "── Gate 3: Code & Technical ──"

  # Check for debug logging
  if echo "$CONTENT" | grep -qE '(console\.log|print\(.*debug|debugger;|pdb\.set_trace)'; then
    warn "Debug logging/breakpoints found"
    echo "$CONTENT" | grep -nE '(console\.log|print\(.*debug|debugger;|pdb\.set_trace)' | head -5
  else
    pass "No debug logging"
  fi

  # Check for hardcoded localhost/ports (potential config leak)
  if echo "$CONTENT" | grep -qE 'localhost:[0-9]{4,5}|127\.0\.0\.1:[0-9]{4,5}'; then
    warn "Hardcoded localhost/port found — should this be configurable?"
  else
    pass "No hardcoded localhost/ports"
  fi
fi

# ── Summary ──
echo ""
echo "═══════════════════════════════════════"
if [ "$ERRORS" -gt 0 ]; then
  echo -e "${RED}RESULT: BLOCKED — $ERRORS error(s), $WARNINGS warning(s)${NC}"
  exit 1
elif [ "$WARNINGS" -gt 0 ]; then
  echo -e "${YELLOW}RESULT: FIX NEEDED — $WARNINGS warning(s)${NC}"
  exit 0
else
  echo -e "${GREEN}RESULT: PASS — all checks clean${NC}"
  exit 0
fi
