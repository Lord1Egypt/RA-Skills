#!/usr/bin/env bash
# audit-script-decision.sh
# ============================================================
# Audit script for build-protocol-decision quality gates.
# Verifies: live data freshness, stop-loss presence, position
# sizing, fake precision, daily P/L tracking, methodology transparency.
#
# Usage:
#   chmod +x audit-script-decision.sh
#   ./audit-script-decision.sh [path/to/decision-doc.md]
#
# Exit codes:
#   0 = all checks passed
#   1 = one or more FAIL (blocks delivery)
#   2 = one or more WARN (review recommended)
#
# Part of build-protocol-decision skill · 2026-04-30
# ============================================================

set -euo pipefail

# ── Config ────────────────────────────────────────────────────
TARGET_FILE="${1:-}"
STOOQ_BASE="https://stooq.com/q/l/?s=SYMBOL.us&f=sd2t2ohlcv&h&e=csv"
COINGECKO_BASE="https://api.coingecko.com/api/v3/simple/price"

PASS=0
WARN=0
FAIL=0

# ── Colors ────────────────────────────────────────────────────
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RESET='\033[0m'

pass()  { echo -e "${GREEN}[PASS]${RESET} $*"; ((PASS++)) || true; }
warn()  { echo -e "${YELLOW}[WARN]${RESET} $*"; ((WARN++)) || true; }
fail()  { echo -e "${RED}[FAIL]${RESET} $*"; ((FAIL++)) || true; }
info()  { echo -e "       $*"; }

# ── Guard: file required ──────────────────────────────────────
if [[ -z "$TARGET_FILE" ]]; then
  echo "Usage: $0 <path/to/decision-document.md>"
  echo ""
  echo "Checks performed:"
  echo "  1. Live data fetch (stocks / crypto)"
  echo "  2. Stop-loss presence in document"
  echo "  3. Position sizing calculation present"
  echo "  4. Fake precision detection (+X.XX% without methodology)"
  echo "  5. Daily P/L log present and timestamped"
  echo "  6. Methodology transparency (named method required)"
  echo "  7. Document freshness (date-stamp within 7 days)"
  echo "  8. Known risks documented (🔴 required)"
  exit 0
fi

if [[ ! -f "$TARGET_FILE" ]]; then
  echo "Error: file not found: $TARGET_FILE"
  exit 1
fi

echo ""
echo "============================================================"
echo " build-protocol-decision · Audit Script"
echo " Target: $TARGET_FILE"
echo " Time:   $(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "============================================================"
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 1 — Stop-loss presence
# ════════════════════════════════════════════════════════════════
echo "── Check 1: Stop-loss defined ──────────────────────────────"

if grep -qiE '止损|stop-loss|stop loss|stoploss|stop_loss|exit price|exit condition' "$TARGET_FILE"; then
  pass "Stop-loss / exit condition found in document"
else
  fail "No stop-loss or exit condition found"
  info "Every decision document must define a stop-loss or exit threshold."
  info "Add a line like: 'Stop-loss: \$XX.XX' or '止损: XX%'"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 2 — Methodology named
# ════════════════════════════════════════════════════════════════
echo "── Check 2: Methodology transparency ──────────────────────"

METHOD_FOUND=0
for method in "PE " "P/E" "DCF" "MA50" "MA200" "moving average" "decision matrix" "weighted" "TCO" "total cost"; do
  if grep -qi "$method" "$TARGET_FILE"; then
    METHOD_FOUND=1
    pass "Methodology keyword found: '$method'"
    break
  fi
done

if [[ $METHOD_FOUND -eq 0 ]]; then
  fail "No named methodology found (PE / DCF / MA / decision matrix / TCO)"
  info "Every recommendation must show its method, not just its conclusion."
  info "Add methodology section with at least one named analytical approach."
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 3 — Fake precision detection
# ════════════════════════════════════════════════════════════════
echo "── Check 3: Fake precision (Sycophancy of Precision) ───────"

# Detect patterns like +12.85% or -3.47% that have no "(est." nearby
PRECISION_LINES=$(grep -nE '[+-][0-9]+\.[0-9]{2,}%' "$TARGET_FILE" || true)

if [[ -z "$PRECISION_LINES" ]]; then
  pass "No suspicious high-precision percentage figures found"
else
  echo "$PRECISION_LINES" | while IFS= read -r line; do
    LINENUM=$(echo "$line" | cut -d: -f1)
    CONTENT=$(echo "$line" | cut -d: -f2-)
    # Check if same line or nearby line has "(est" label
    CONTEXT=$(sed -n "$((LINENUM > 2 ? LINENUM-2 : 1)),$((LINENUM+2))p" "$TARGET_FILE")
    if echo "$CONTEXT" | grep -qi '(est\|含估算\|estimated\|approx'; then
      pass "Line $LINENUM: precise % found but labeled as estimate — OK"
    else
      warn "Line $LINENUM: precise % figure without '(est.)' label: $CONTENT"
    fi
  done
  info "Precise numbers from estimates must be labeled: '+12.8% (est.)' or '含估算'"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 4 — Known risks documented (🔴 required)
# ════════════════════════════════════════════════════════════════
echo "── Check 4: Anti-sycophancy — risks documented ─────────────"

RED_COUNT=$(grep -c '🔴' "$TARGET_FILE" || true)
if [[ "$RED_COUNT" -ge 1 ]]; then
  pass "Found $RED_COUNT 🔴 critical flag(s) in document"
else
  fail "No 🔴 critical risks found"
  info "Every decision document must acknowledge at least one major risk."
  info "Add a 'Known Risks' section with at least one 🔴 item."
  info "All-upside analysis is fake analysis."
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 5 — Position sizing present (for investment decisions)
# ════════════════════════════════════════════════════════════════
echo "── Check 5: Position sizing ────────────────────────────────"

if grep -qiE 'position size|仓位|shares?.*=|risk per trade|max.*position' "$TARGET_FILE"; then
  pass "Position sizing calculation or reference found"
else
  warn "No position sizing found — required for investment decisions"
  info "If this is not an investment decision, ignore this warning."
  info "For investments: document position size formula or result."
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 6 — Daily P/L tracking
# ════════════════════════════════════════════════════════════════
echo "── Check 6: P/L tracking ───────────────────────────────────"

if grep -qiE 'p/l|pnl|profit.*loss|每日.*盈亏|daily.*track' "$TARGET_FILE"; then
  pass "P/L tracking reference found in document"
else
  warn "No P/L tracking found"
  info "Post-decision: daily P/L log required for active positions."
  info "Template in references/investment-playbook-template.md §7"
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 7 — Document freshness (date-stamp)
# ════════════════════════════════════════════════════════════════
echo "── Check 7: Document date-stamp ────────────────────────────"

DATE_LINE=$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$TARGET_FILE" | head -1 || true)

if [[ -z "$DATE_LINE" ]]; then
  warn "No date-stamp (YYYY-MM-DD) found in document"
  info "Decision records must be date-stamped. Prices and analysis expire."
else
  DOC_EPOCH=$(date -d "$DATE_LINE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$DATE_LINE" +%s 2>/dev/null || echo "0")
  NOW_EPOCH=$(date +%s)
  AGE_DAYS=$(( (NOW_EPOCH - DOC_EPOCH) / 86400 ))

  if [[ $AGE_DAYS -le 1 ]]; then
    pass "Document dated $DATE_LINE — fresh (${AGE_DAYS}d old)"
  elif [[ $AGE_DAYS -le 7 ]]; then
    pass "Document dated $DATE_LINE — ${AGE_DAYS}d old (acceptable)"
  elif [[ $AGE_DAYS -le 30 ]]; then
    warn "Document dated $DATE_LINE — ${AGE_DAYS}d old. Verify prices are still current."
  else
    fail "Document dated $DATE_LINE — ${AGE_DAYS}d old. Prices are almost certainly stale."
    info "Re-fetch live prices before making decisions from this document."
  fi
fi
echo ""

# ════════════════════════════════════════════════════════════════
# CHECK 8 — Live data fetch (optional, interactive)
# ════════════════════════════════════════════════════════════════
echo "── Check 8: Live data fetch (optional) ─────────────────────"

# Extract ticker symbols mentioned in the document (simple heuristic: ALLCAPS 2-5 chars)
TICKERS=$(grep -oE '\b[A-Z]{2,5}\b' "$TARGET_FILE" | grep -vE '^(THE|AND|FOR|NOT|BUT|ARE|USD|GBP|EUR|ETF|IPO|DCF|EPS|TTM|SLA|TCO|API|RSI|URL|PDF)$' | sort -u | head -5 || true)

if [[ -z "$TICKERS" ]]; then
  info "No ticker symbols detected — skipping live price check"
  info "If this is an investment decision, add ticker symbols to document."
else
  info "Detected potential tickers: $TICKERS"
  info "To fetch live prices, run:"
  for ticker in $TICKERS; do
    info "  curl \"https://stooq.com/q/l/?s=${ticker}.us&f=sd2t2ohlcv&h&e=csv\""
  done
  info ""
  info "For crypto (example for BTC):"
  info "  curl \"${COINGECKO_BASE}?ids=bitcoin&vs_currencies=usd&include_24hr_change=true\""
  warn "Live price fetch not automated — run the above commands manually"
  info "Compare fetched prices against any prices in the document."
fi
echo ""

# ════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════
echo "============================================================"
echo " AUDIT SUMMARY"
echo "============================================================"
echo -e " ${GREEN}PASS: $PASS${RESET}  |  ${YELLOW}WARN: $WARN${RESET}  |  ${RED}FAIL: $FAIL${RESET}"
echo ""

if [[ $FAIL -gt 0 ]]; then
  echo -e "${RED}❌ AUDIT FAILED — $FAIL blocking issue(s) must be resolved before delivery.${RESET}"
  echo ""
  echo "Blocking issues:"
  echo "  - No stop-loss defined → every open position is undefined risk"
  echo "  - No methodology named → 'gut call' is not analysis"
  echo "  - No 🔴 risks documented → all-upside = sycophantic"
  echo "  - Document >30 days old → prices are stale fiction"
  exit 1
elif [[ $WARN -gt 0 ]]; then
  echo -e "${YELLOW}⚠️  AUDIT PASSED WITH WARNINGS — $WARN item(s) to review.${RESET}"
  echo "Warnings do not block delivery but should be addressed."
  exit 2
else
  echo -e "${GREEN}✅ AUDIT PASSED — all checks clean.${RESET}"
  exit 0
fi
