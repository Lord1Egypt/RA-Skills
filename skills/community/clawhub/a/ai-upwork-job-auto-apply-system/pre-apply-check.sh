#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# pre-apply-check.sh — HunterAI Pre-Flight Qualification Filter
# ═══════════════════════════════════════════════════════════════════════════
# PURPOSE:
#   Runs a structured qualification check on a single Upwork job listing.
#   Returns EXIT 0 if job PASSES (safe to bid) or EXIT 1 if job FAILS.
#   Outputs a human-readable report with the reason for each decision.
#
# USAGE (called by agent or manually):
#   ./scripts/pre-apply-check.sh \
#     --job-id "UPW-20240901-0042" \
#     --payment-verified "true" \
#     --client-rating "4.7" \
#     --client-reviews "12" \
#     --budget-type "fixed" \
#     --budget-amount "1500" \
#     --proposals "8" \
#     --title "Build a React dashboard with Node.js API" \
#     --description "Looking for a React developer to build..."
#
# EXIT CODES:
#   0 = PASS — Job clears all filters, proceed to scoring
#   1 = FAIL — Job rejected, log reason, skip proposal generation
#   2 = DUPLICATE — Job ID already exists in APPLICATION_LOG.md
# ═══════════════════════════════════════════════════════════════════════════

set -euo pipefail

# ─── ANSI Colors ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ─── Default Config (overridden by FREELANCER_PROFILE.md values) ──────────
MIN_CLIENT_RATING=4.0
MIN_CLIENT_REVIEWS=1
MIN_BUDGET_FIXED=300
MIN_BUDGET_HOURLY=35
MAX_PROPOSALS=50
PAYMENT_REQUIRED=true
LOG_FILE=".upwork/APPLICATION_LOG.md"
PROFILE_FILE="assets/FREELANCER_PROFILE.md"

# ─── Blacklisted Keywords (loaded from FREELANCER_PROFILE.md) ─────────────
BLACKLISTED_KEYWORDS=(
  "data entry"
  "copy paste"
  "logo design"
  "wordpress theme install"
  "per hour is negotiable"
  "small budget"
  "quick and easy"
  "will pay after"
  "test task first"
  "unpaid trial"
  "spec work"
)

# ─── Parse Arguments ──────────────────────────────────────────────────────
JOB_ID=""
PAYMENT_VERIFIED=""
CLIENT_RATING=""
CLIENT_REVIEWS=""
BUDGET_TYPE=""
BUDGET_AMOUNT=""
PROPOSALS=""
JOB_TITLE=""
JOB_DESCRIPTION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --job-id)            JOB_ID="$2"; shift 2 ;;
    --payment-verified)  PAYMENT_VERIFIED="$2"; shift 2 ;;
    --client-rating)     CLIENT_RATING="$2"; shift 2 ;;
    --client-reviews)    CLIENT_REVIEWS="$2"; shift 2 ;;
    --budget-type)       BUDGET_TYPE="$2"; shift 2 ;;
    --budget-amount)     BUDGET_AMOUNT="$2"; shift 2 ;;
    --proposals)         PROPOSALS="$2"; shift 2 ;;
    --title)             JOB_TITLE="$2"; shift 2 ;;
    --description)       JOB_DESCRIPTION="$2"; shift 2 ;;
    *) echo "Unknown argument: $1"; exit 1 ;;
  esac
done

# ─── Header ───────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${BOLD}${CYAN}   🏹 HunterAI Pre-Flight Check — ${JOB_ID}${RESET}"
echo -e "${BOLD}${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "   Title: ${YELLOW}${JOB_TITLE}${RESET}"
echo ""

PASS=true
FAIL_REASONS=()
WARNINGS=()

# ─── CHECK 1: Duplicate Detection ─────────────────────────────────────────
echo -e "  ${BOLD}[1/6] Duplicate Check${RESET}"
if [[ -f "$LOG_FILE" ]] && grep -q "$JOB_ID" "$LOG_FILE" 2>/dev/null; then
  echo -e "       ${RED}✗ DUPLICATE — Job ID already in APPLICATION_LOG.md${RESET}"
  echo ""
  echo -e "${RED}  ⛔ RESULT: SKIPPED (Duplicate)${RESET}"
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo ""
  exit 2
else
  echo -e "       ${GREEN}✓ New job — not in log${RESET}"
fi

# ─── CHECK 2: Payment Verification ────────────────────────────────────────
echo -e "  ${BOLD}[2/6] Payment Verification${RESET}"
if [[ "$PAYMENT_REQUIRED" == "true" && "$PAYMENT_VERIFIED" != "true" ]]; then
  echo -e "       ${RED}✗ FAIL — Payment not verified${RESET}"
  FAIL_REASONS+=("Payment unverified")
  PASS=false
else
  echo -e "       ${GREEN}✓ Payment verified${RESET}"
fi

# ─── CHECK 3: Client Rating ────────────────────────────────────────────────
echo -e "  ${BOLD}[3/6] Client Rating${RESET}"
# Use awk for float comparison (bash can't do floats natively)
RATING_CHECK=$(awk -v rating="$CLIENT_RATING" -v min="$MIN_CLIENT_RATING" \
  'BEGIN { print (rating >= min) ? "pass" : "fail" }')

if [[ "$RATING_CHECK" == "fail" ]]; then
  echo -e "       ${RED}✗ FAIL — Client rating ${CLIENT_RATING} < minimum ${MIN_CLIENT_RATING}${RESET}"
  FAIL_REASONS+=("Client rating too low (${CLIENT_RATING})")
  PASS=false
else
  echo -e "       ${GREEN}✓ Client rating ${CLIENT_RATING} ⭐ (≥ ${MIN_CLIENT_RATING})${RESET}"
fi

# ─── CHECK 4: Client Review Count ─────────────────────────────────────────
echo -e "  ${BOLD}[4/6] Client Review Count${RESET}"
if [[ "$CLIENT_REVIEWS" -lt "$MIN_CLIENT_REVIEWS" ]]; then
  echo -e "       ${YELLOW}⚠ WARNING — Client has only ${CLIENT_REVIEWS} review(s) (risky but not auto-reject)${RESET}"
  WARNINGS+=("Low review count (${CLIENT_REVIEWS})")
else
  echo -e "       ${GREEN}✓ ${CLIENT_REVIEWS} client reviews on record${RESET}"
fi

# ─── CHECK 5: Budget Threshold ────────────────────────────────────────────
echo -e "  ${BOLD}[5/6] Budget Check${RESET}"
if [[ "$BUDGET_TYPE" == "fixed" ]]; then
  BUDGET_CHECK=$(awk -v budget="$BUDGET_AMOUNT" -v min="$MIN_BUDGET_FIXED" \
    'BEGIN { print (budget >= min) ? "pass" : "fail" }')
  BUDGET_LABEL="fixed price"
  BUDGET_MIN="$MIN_BUDGET_FIXED"
else
  BUDGET_CHECK=$(awk -v budget="$BUDGET_AMOUNT" -v min="$MIN_BUDGET_HOURLY" \
    'BEGIN { print (budget >= min) ? "pass" : "fail" }')
  BUDGET_LABEL="hourly"
  BUDGET_MIN="$MIN_BUDGET_HOURLY"
fi

if [[ "$BUDGET_CHECK" == "fail" ]]; then
  echo -e "       ${RED}✗ FAIL — Budget \$${BUDGET_AMOUNT} (${BUDGET_LABEL}) below minimum \$${BUDGET_MIN}${RESET}"
  FAIL_REASONS+=("Budget too low (\$${BUDGET_AMOUNT})")
  PASS=false
else
  echo -e "       ${GREEN}✓ Budget \$${BUDGET_AMOUNT} (${BUDGET_LABEL}) clears threshold${RESET}"
fi

# ─── CHECK 6: Blacklisted Keywords ────────────────────────────────────────
echo -e "  ${BOLD}[6/6] Keyword Blacklist Scan${RESET}"
COMBINED_TEXT=$(echo "${JOB_TITLE} ${JOB_DESCRIPTION}" | tr '[:upper:]' '[:lower:]')
KEYWORD_HIT=false
HIT_KEYWORD=""

for keyword in "${BLACKLISTED_KEYWORDS[@]}"; do
  if echo "$COMBINED_TEXT" | grep -qi "$keyword" 2>/dev/null; then
    KEYWORD_HIT=true
    HIT_KEYWORD="$keyword"
    break
  fi
done

if [[ "$KEYWORD_HIT" == "true" ]]; then
  echo -e "       ${RED}✗ FAIL — Blacklisted keyword detected: '${HIT_KEYWORD}'${RESET}"
  FAIL_REASONS+=("Blacklisted keyword: '${HIT_KEYWORD}'")
  PASS=false
else
  echo -e "       ${GREEN}✓ No blacklisted keywords found${RESET}"
fi

# ─── Competition Warning (soft check — not a reject) ──────────────────────
if [[ "$PROPOSALS" -gt "$MAX_PROPOSALS" ]]; then
  WARNINGS+=("High competition: ${PROPOSALS} proposals already submitted")
fi

# ─── FINAL VERDICT ────────────────────────────────────────────────────────
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"

if [[ "$PASS" == "true" ]]; then
  echo -e "${GREEN}${BOLD}  ✅ RESULT: PASSED — Clear for proposal generation${RESET}"
  
  if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}  ⚠️  Warnings (noted, not blocking):${RESET}"
    for warning in "${WARNINGS[@]}"; do
      echo -e "${YELLOW}     • ${warning}${RESET}"
    done
  fi
  
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo ""
  exit 0
else
  echo -e "${RED}${BOLD}  ⛔ RESULT: REJECTED — Do not generate proposal${RESET}"
  echo ""
  echo -e "${RED}  Rejection reasons:${RESET}"
  for reason in "${FAIL_REASONS[@]}"; do
    echo -e "${RED}     • ${reason}${RESET}"
  done
  
  if [[ ${#WARNINGS[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}  Additional warnings:${RESET}"
    for warning in "${WARNINGS[@]}"; do
      echo -e "${YELLOW}     • ${warning}${RESET}"
    done
  fi
  
  echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
  echo ""
  exit 1
fi
