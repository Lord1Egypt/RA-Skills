#!/usr/bin/env bash
# =============================================================================
# FILE:    upwork-auto-apply/scripts/pre-apply-check.sh
# VERSION: 1.0.3
#
# PURPOSE:
#   Filter a single Upwork job listing against the freelancer's blacklist rules
#   before any proposal is drafted. Outputs QUALIFIED or DISQUALIFIED with reasons.
#
# SYSTEM REQUIREMENTS:
#   - bash (version 3.2 or later) — pre-installed on macOS and Linux
#   - awk  — pre-installed on macOS and Linux, used for decimal comparison
#   - grep — pre-installed on macOS and Linux, used for duplicate ID detection
#   No other tools, no internet connection, no external APIs required.
#
# FILES READ:
#   upwork-auto-apply/.upwork/APPLICATION_LOG.md
#   (checks whether the Job ID has already been applied to)
#
# FILES WRITTEN:
#   None. This script is read-only. It only prints output to the terminal.
#
# HOW TO RUN:
#   Run this script from the upwork-auto-apply/ root folder:
#
#   bash scripts/pre-apply-check.sh \
#     --job-id "JOB123" \
#     --budget 1500 \
#     --job-type "fixed" \
#     --client-rating 4.7 \
#     --payment-verified true \
#     --client-spend 25000 \
#     --title "Build React Dashboard" \
#     --days-posted 3
#
# EXIT CODES:
#   0 = QUALIFIED   — proceed to proposal drafting
#   1 = DISQUALIFIED — skip this job
# =============================================================================

# =============================================================================
# CONFIGURATION
# Keep these values in sync with your assets/FREELANCER_PROFILE.md settings.
# =============================================================================

MIN_FIXED_BUDGET=500       # Minimum fixed-price budget in USD
MIN_HOURLY_RATE=25         # Minimum hourly rate in USD per hour
MIN_CLIENT_RATING="4.0"    # Minimum client rating out of 5.0 (decimal, use awk)
MIN_CLIENT_SPEND=0         # Minimum total client spend on Upwork in USD
REQUIRE_PAYMENT_VERIFIED=true
MAX_DAYS_POSTED=7          # Reject jobs older than this many days

# Blacklisted keywords — jobs with any of these in the title are rejected.
# Keep this list in sync with blacklist_keywords in FREELANCER_PROFILE.md.
BLACKLIST_KEYWORDS=(
  "logo design"
  "data entry"
  "virtual assistant"
  "quick and easy"
  "spec work"
  "test task"
  "tight budget"
  "cheapest"
  "unpaid"
  "equity only"
  "revenue share only"
)

# Path to the application log file.
# This must be run from the upwork-auto-apply/ root folder for this path to work.
LOG_FILE=".upwork/APPLICATION_LOG.md"

# =============================================================================
# COLORS
# =============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# =============================================================================
# ARGUMENT PARSING
# =============================================================================
JOB_ID=""
BUDGET=0
JOB_TYPE="fixed"
CLIENT_RATING="0"
PAYMENT_VERIFIED="false"
CLIENT_SPEND=0
JOB_TITLE=""
DAYS_POSTED=0

while [[ $# -gt 0 ]]; do
  case $1 in
    --job-id)            JOB_ID="$2";           shift 2 ;;
    --budget)            BUDGET="$2";            shift 2 ;;
    --job-type)          JOB_TYPE="$2";          shift 2 ;;
    --client-rating)     CLIENT_RATING="$2";     shift 2 ;;
    --payment-verified)  PAYMENT_VERIFIED="$2";  shift 2 ;;
    --client-spend)      CLIENT_SPEND="$2";      shift 2 ;;
    --title)             JOB_TITLE="$2";         shift 2 ;;
    --days-posted)       DAYS_POSTED="$2";       shift 2 ;;
    *)
      echo "Unknown argument: $1"
      echo "Usage: bash scripts/pre-apply-check.sh --job-id X --budget X --job-type fixed|hourly --client-rating X --payment-verified true|false --client-spend X --title \"Job Title\" --days-posted X"
      exit 1
      ;;
  esac
done

# =============================================================================
# VALIDATE REQUIRED ARGUMENTS
# =============================================================================
if [[ -z "$JOB_ID" ]]; then
  echo "Error: --job-id is required."
  exit 1
fi
if [[ -z "$JOB_TITLE" ]]; then
  echo "Error: --title is required."
  exit 1
fi

# =============================================================================
# DECIMAL COMPARISON HELPER (uses awk — no python3 required)
# Returns 0 (true) if first argument is less than second argument.
# Example: decimal_lt "4.2" "4.5" → returns 0 (true, because 4.2 < 4.5)
# =============================================================================
decimal_lt() {
  awk -v a="$1" -v b="$2" 'BEGIN { exit !(a < b) }'
}

# =============================================================================
# TRACKING VARIABLES
# =============================================================================
DISQUALIFIED=false
REASONS=()
WARNINGS=()

disqualify() {
  DISQUALIFIED=true
  REASONS+=("$1")
}

warn() {
  WARNINGS+=("$1")
}

# =============================================================================
# PRINT HEADER
# =============================================================================
echo ""
echo -e "${BOLD}${BLUE}+----------------------------------------------------------+${RESET}"
echo -e "${BOLD}${BLUE}|   ProposalAI Pre-Flight Check  (upwork-auto-apply v1.0.3) |${RESET}"
echo -e "${BOLD}${BLUE}+----------------------------------------------------------+${RESET}"
echo ""
echo -e "  ${BOLD}Job ID:${RESET}       $JOB_ID"
echo -e "  ${BOLD}Title:${RESET}        $JOB_TITLE"
echo -e "  ${BOLD}Type:${RESET}         $JOB_TYPE"
echo -e "  ${BOLD}Budget:${RESET}       \$$BUDGET"
echo -e "  ${BOLD}Rating:${RESET}       $CLIENT_RATING / 5.0"
echo -e "  ${BOLD}Payment:${RESET}      Verified = $PAYMENT_VERIFIED"
echo -e "  ${BOLD}Spend:${RESET}        \$$CLIENT_SPEND total on Upwork"
echo -e "  ${BOLD}Posted:${RESET}       $DAYS_POSTED days ago"
echo ""
echo -e "  Running checks..."
echo ""

# =============================================================================
# CHECK 1: PAYMENT VERIFICATION
# =============================================================================
if [[ "$REQUIRE_PAYMENT_VERIFIED" == "true" && "$PAYMENT_VERIFIED" != "true" ]]; then
  disqualify "Payment method is not verified"
fi

# =============================================================================
# CHECK 2: BUDGET FLOOR
# Uses integer comparison (bash built-in, no external tools needed)
# =============================================================================
if [[ "$JOB_TYPE" == "fixed" ]]; then
  if (( BUDGET < MIN_FIXED_BUDGET )); then
    disqualify "Fixed budget \$$BUDGET is below your minimum of \$$MIN_FIXED_BUDGET"
  fi
elif [[ "$JOB_TYPE" == "hourly" ]]; then
  if (( BUDGET < MIN_HOURLY_RATE )); then
    disqualify "Hourly rate \$$BUDGET/hr is below your minimum of \$$MIN_HOURLY_RATE/hr"
  fi
fi

# =============================================================================
# CHECK 3: CLIENT RATING FLOOR
# Uses awk for decimal comparison — awk is pre-installed on macOS and Linux
# =============================================================================
if decimal_lt "$CLIENT_RATING" "$MIN_CLIENT_RATING"; then
  disqualify "Client rating $CLIENT_RATING is below your minimum of $MIN_CLIENT_RATING"
fi

# =============================================================================
# CHECK 4: CLIENT TOTAL SPEND FLOOR
# Uses integer comparison (bash built-in)
# =============================================================================
if (( CLIENT_SPEND < MIN_CLIENT_SPEND )); then
  disqualify "Client total spend \$$CLIENT_SPEND is below your minimum of \$$MIN_CLIENT_SPEND"
fi

# =============================================================================
# CHECK 5: JOB AGE
# Uses integer comparison (bash built-in)
# =============================================================================
if (( DAYS_POSTED > MAX_DAYS_POSTED )); then
  disqualify "Job is $DAYS_POSTED days old, exceeds your maximum of $MAX_DAYS_POSTED days"
fi

# =============================================================================
# CHECK 6: KEYWORD BLACKLIST
# Converts title to lowercase, then checks each keyword using bash string match.
# No external tools needed for this check.
# =============================================================================
TITLE_LOWER=$(echo "$JOB_TITLE" | tr '[:upper:]' '[:lower:]')
for keyword in "${BLACKLIST_KEYWORDS[@]}"; do
  if [[ "$TITLE_LOWER" == *"$keyword"* ]]; then
    disqualify "Blacklisted keyword found in title: '$keyword'"
    break
  fi
done

# =============================================================================
# CHECK 7: DUPLICATE APPLICATION CHECK
# Uses grep to search the local log file — grep is pre-installed on macOS and Linux.
# This script reads: upwork-auto-apply/.upwork/APPLICATION_LOG.md
# Run from the upwork-auto-apply/ root folder for the relative path to resolve.
# =============================================================================
if [[ -f "$LOG_FILE" ]]; then
  if grep -q "JOB_ID:.*$JOB_ID" "$LOG_FILE" 2>/dev/null; then
    disqualify "Duplicate: Job ID $JOB_ID is already in .upwork/APPLICATION_LOG.md"
  fi
else
  warn "Log file not found at $LOG_FILE — duplicate check skipped."
  warn "Make sure you run this script from the upwork-auto-apply/ root folder."
fi

# =============================================================================
# SOFT WARNINGS (non-disqualifying)
# Uses awk for decimal comparison
# =============================================================================
if decimal_lt "$CLIENT_RATING" "4.5" && [[ "$DISQUALIFIED" == "false" ]]; then
  warn "Client rating $CLIENT_RATING passes the minimum but is below 4.5 — consider carefully"
fi

if (( CLIENT_SPEND == 0 )); then
  warn "Client has \$0 total spend on Upwork — no track record"
fi

if (( DAYS_POSTED >= 5 )); then
  warn "Job is $DAYS_POSTED days old — competition may have grown"
fi

# =============================================================================
# OUTPUT RESULTS
# =============================================================================

if [[ ${#WARNINGS[@]} -gt 0 ]]; then
  echo -e "  ${YELLOW}Warnings (not disqualifying):${RESET}"
  for w in "${WARNINGS[@]}"; do
    echo -e "     ${YELLOW}! $w${RESET}"
  done
  echo ""
fi

if [[ "$DISQUALIFIED" == "true" ]]; then

  echo -e "  ${RED}${BOLD}RESULT: DISQUALIFIED${RESET}"
  echo ""
  echo -e "  ${RED}Reasons:${RESET}"
  for reason in "${REASONS[@]}"; do
    echo -e "     ${RED}x $reason${RESET}"
  done
  echo ""
  echo -e "${BOLD}${RED}+----------------------------------------------------------+${RESET}"
  echo -e "${BOLD}${RED}|  SKIP THIS JOB — do not draft a proposal                 |${RESET}"
  echo -e "${BOLD}${RED}+----------------------------------------------------------+${RESET}"
  echo ""
  exit 1

else

  echo -e "  ${GREEN}${BOLD}RESULT: QUALIFIED${RESET}"
  echo ""
  echo -e "  ${GREEN}All checks passed:${RESET}"
  echo -e "     ${GREEN}+ Payment verified${RESET}"
  echo -e "     ${GREEN}+ Budget meets your floor (\$$BUDGET)${RESET}"
  echo -e "     ${GREEN}+ Client rating acceptable ($CLIENT_RATING / 5.0)${RESET}"
  echo -e "     ${GREEN}+ No blacklisted keywords in title${RESET}"
  echo -e "     ${GREEN}+ Not a duplicate application${RESET}"
  echo -e "     ${GREEN}+ Job is fresh ($DAYS_POSTED days old)${RESET}"
  echo ""
  echo -e "${BOLD}${GREEN}+----------------------------------------------------------+${RESET}"
  echo -e "${BOLD}${GREEN}|  PROCEED TO PROPOSAL DRAFTING                            |${RESET}"
  echo -e "${BOLD}${GREEN}+----------------------------------------------------------+${RESET}"
  echo ""
  exit 0

fi
