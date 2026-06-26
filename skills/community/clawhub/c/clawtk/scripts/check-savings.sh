#!/usr/bin/env bash
# ClawTK Savings Report
# Parses spend log and Engine gain data to show actual cost savings.

set -euo pipefail

OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw}"
STATE_FILE="$OPENCLAW_DIR/clawtk-state.json"
SPEND_LOG="$OPENCLAW_DIR/clawtk-spend.jsonl"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

if [ ! -f "$STATE_FILE" ]; then
    echo "ClawTK is not set up yet. Run /clawtk setup first."
    exit 1
fi

tier=$(jq -r '.tier' "$STATE_FILE")
install_date=$(jq -r '.installDate' "$STATE_FILE")

echo -e "${BOLD}ClawTK Savings Report${NC}"
echo -e "${CYAN}════════════════════════════════════════${NC}"
echo ""

# ── Spend Log Analysis ───────────────────────────────────────────────────────

if [ -f "$SPEND_LOG" ]; then
    now=$(date +%s)
    day_ago=$((now - 86400))
    week_ago=$((now - 604800))

    # Parse spend log with jq
    total_entries=$(wc -l < "$SPEND_LOG" | tr -d ' ')

    daily_spend=$(jq -s --argjson cutoff "$day_ago" '
        [.[] | select((.timestamp | fromdateiso8601) > $cutoff) | .estimatedCost] | add // 0
    ' "$SPEND_LOG")

    weekly_spend=$(jq -s --argjson cutoff "$week_ago" '
        [.[] | select((.timestamp | fromdateiso8601) > $cutoff) | .estimatedCost] | add // 0
    ' "$SPEND_LOG")

    total_spend=$(jq -s '[.[].estimatedCost] | add // 0' "$SPEND_LOG")

    daily_tokens=$(jq -s --argjson cutoff "$day_ago" '
        [.[] | select((.timestamp | fromdateiso8601) > $cutoff) | .tokens] | add // 0
    ' "$SPEND_LOG")

    weekly_tokens=$(jq -s --argjson cutoff "$week_ago" '
        [.[] | select((.timestamp | fromdateiso8601) > $cutoff) | .tokens] | add // 0
    ' "$SPEND_LOG")

    # Blocked calls (retry loops caught)
    loops_blocked=$(jq -s '[.[] | select(.toolName == "__blocked_retry_loop")] | length' "$SPEND_LOG" 2>/dev/null || echo "0")

    echo "Spend Tracking (since $install_date)"
    echo -e "${CYAN}────────────────────────────────────────${NC}"
    printf "  %-24s %s\n" "Today:" "\$$(printf '%.2f' "$daily_spend") ($((daily_tokens / 1000))K tokens)"
    printf "  %-24s %s\n" "This week:" "\$$(printf '%.2f' "$weekly_spend") ($((weekly_tokens / 1000))K tokens)"
    printf "  %-24s %s\n" "All time:" "\$$(printf '%.2f' "$total_spend")"
    printf "  %-24s %s\n" "Tool calls tracked:" "$total_entries"
    printf "  %-24s %s\n" "Retry loops caught:" "$loops_blocked"
    echo ""
else
    echo "  No spend data yet. Data will appear after your next session."
    echo ""
fi

# ── Config Savings Estimate ──────────────────────────────────────────────────

echo "Estimated Savings from Config Optimizations"
echo -e "${CYAN}────────────────────────────────────────${NC}"
echo ""
echo "  Based on typical OpenClaw usage ($150/month baseline):"
echo ""
printf "  %-30s ${GREEN}%s${NC}\n" "Heartbeat isolation:" "~\$45-65/mo saved"
printf "  %-30s ${GREEN}%s${NC}\n" "Heartbeat interval (55m):" "~\$10-15/mo saved"
printf "  %-30s ${GREEN}%s${NC}\n" "Cheap heartbeat model:" "~\$15-25/mo saved"
printf "  %-30s ${GREEN}%s${NC}\n" "Context cap (100K):" "~\$5-15/mo saved"
printf "  %-30s ${GREEN}%s${NC}\n" "Image downscaling:" "~\$3-5/mo saved"
echo ""
echo -e "  ${BOLD}Estimated total: \$78-125/mo saved (52-83%)${NC}"
echo ""

# ── Engine Savings ──────────────────────────────────────────────────────────────

if command -v rtk &>/dev/null; then
    echo "ClawTK Engine Compression"
    echo -e "${CYAN}────────────────────────────────────────${NC}"
    rtk gain 2>/dev/null || echo "  Run some commands first to see Engine savings."
    echo ""
else
    if [ "$tier" = "free" ]; then
        echo -e "${YELLOW}ClawTK Engine Compression (Pro only)${NC}"
        echo -e "${CYAN}────────────────────────────────────────${NC}"
        echo "  ClawTK Engine compresses CLI output by 60-90% before it reaches the LLM."
        echo "  This is the single biggest cost saver for heavy users."
        echo ""
        echo "  Upgrade: https://clawtk.co/pro (\$49 one-time)"
        echo ""
    fi
fi

# ── Spend Caps Status ────────────────────────────────────────────────────────

daily_cap=$(jq -r '.spendCaps.daily' "$STATE_FILE")
weekly_cap=$(jq -r '.spendCaps.weekly' "$STATE_FILE")
override=$(jq -r '.overrideUntil // "none"' "$STATE_FILE")

echo "Spend Caps"
echo -e "${CYAN}────────────────────────────────────────${NC}"
printf "  %-20s \$%s/day\n" "Daily cap:" "$daily_cap"
printf "  %-20s \$%s/week\n" "Weekly cap:" "$weekly_cap"
printf "  %-20s %s\n" "Override:" "$override"
echo ""
echo -e "${CYAN}════════════════════════════════════════${NC}"
