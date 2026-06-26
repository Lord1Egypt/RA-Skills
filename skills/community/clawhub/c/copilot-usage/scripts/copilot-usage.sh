#!/usr/bin/env bash
# copilot-usage.sh — GitHub Copilot premium request usage dashboard
# Usage: bash copilot-usage.sh [--month M] [--year Y] [--model NAME] [--json] [--set-plan PLAN]
#
# Plans: free | student | pro | pro+ | business | enterprise
# Config: ~/.config/copilot-usage/config.json

set -euo pipefail

CONFIG_DIR="$HOME/.config/copilot-usage"
CONFIG_FILE="$CONFIG_DIR/config.json"

MONTH=""
YEAR=""
MODEL_FILTER=""
JSON_MODE=false
SET_PLAN=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --month)    MONTH="$2"; shift 2 ;;
    --year)     YEAR="$2";  shift 2 ;;
    --model)    MODEL_FILTER="$2"; shift 2 ;;
    --json)     JSON_MODE=true; shift ;;
    --set-plan) SET_PLAN="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# --- Plan quotas (GitHub does not expose these via API) ---
declare -A PLAN_QUOTAS=(
  ["free"]=50
  ["student"]=300
  ["pro"]=300
  ["pro+"]=1500
  ["business"]=300
  ["enterprise"]=1000
)

# --- Handle --set-plan ---
if [[ -n "$SET_PLAN" ]]; then
  PLAN_KEY="${SET_PLAN,,}"  # lowercase
  if [[ -z "${PLAN_QUOTAS[$PLAN_KEY]+x}" ]]; then
    echo "❌ Unknown plan: $SET_PLAN"
    echo "   Valid plans: free, student, pro, pro+, business, enterprise"
    exit 1
  fi
  mkdir -p "$CONFIG_DIR"
  QUOTA="${PLAN_QUOTAS[$PLAN_KEY]}"
  cat > "$CONFIG_FILE" << EOF
{
  "plan": "$PLAN_KEY",
  "quota": $QUOTA,
  "set_at": "$(date -u +%Y-%m-%d)"
}
EOF
  echo "✅ Plan configured: $PLAN_KEY ($QUOTA premium requests/month)"
  echo "   Config saved to: $CONFIG_FILE"
  exit 0
fi

# --- Load config ---
QUOTA=0
PLAN_NAME="unknown"
if [[ -f "$CONFIG_FILE" ]]; then
  QUOTA=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('quota', 0))")
  PLAN_NAME=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('plan', 'unknown'))")
fi

# --- Auth check ---
GH_USER=$(gh api /user --jq '.login' 2>/dev/null || echo "")
if [[ -z "$GH_USER" ]]; then
  echo "❌ Not authenticated. Run: gh auth login"
  echo "   Required scopes: manage_billing:copilot, user"
  exit 1
fi

# --- Build API endpoint ---
QUERY="?"
[[ -n "$YEAR" ]]         && QUERY+="year=${YEAR}&"
[[ -n "$MONTH" ]]        && QUERY+="month=${MONTH}&"
[[ -n "$MODEL_FILTER" ]] && QUERY+="model=${MODEL_FILTER}&"
QUERY="${QUERY%&}"
[[ "$QUERY" == "?" ]] && QUERY=""
ENDPOINT="/users/${GH_USER}/settings/billing/premium_request/usage${QUERY}"

echo "🔍 Fetching Copilot usage..."
echo ""

TMP_FILE=$(mktemp /tmp/copilot-usage-XXXXXX.json)
trap 'rm -f $TMP_FILE' EXIT

gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "$ENDPOINT" > "$TMP_FILE" 2>&1 || {
    echo "❌ API call failed."
    echo "   Make sure gh is authenticated with: manage_billing:copilot, user"
    echo "   Run: gh auth refresh -s manage_billing:copilot"
    echo ""
    cat "$TMP_FILE"
    exit 1
  }

if $JSON_MODE; then
  cat "$TMP_FILE"
  exit 0
fi

# --- Render dashboard ---
NEXT_RESET=$(date -u -d "$(date -u +%Y-%m-01) +1 month" +"%Y-%m-01" 2>/dev/null \
  || python3 -c "
from datetime import date
d = date.today()
if d.month == 12:
    print(date(d.year + 1, 1, 1))
else:
    print(date(d.year, d.month + 1, 1))
")

python3 - "$GH_USER" "$NEXT_RESET" "$QUOTA" "$PLAN_NAME" "$CONFIG_FILE" "$TMP_FILE" << 'PYEOF'
import json, sys, datetime, os

data      = json.load(open(sys.argv[6]))
gh_user   = sys.argv[1]
next_reset= sys.argv[2]
quota     = int(sys.argv[3])
plan_name = sys.argv[4]
cfg_file  = sys.argv[5]

items = data.get("usageItems", [])
tp    = data.get("timePeriod", {})
today = datetime.date.today()
days_left = (datetime.date.fromisoformat(next_reset) - today).days

# Model multiplier table (source: GitHub docs, April 2026)
MULTIPLIERS = {
    "gpt-5 mini":                    0,
    "gpt-4.1":                       0,
    "gpt-4o":                        0,
    "claude haiku 4.5":              0.33,
    "gemini 3 flash":                0.33,
    "claude sonnet 4":               1,
    "claude sonnet 4.5":             1,
    "claude sonnet 4.6":             1,
    "gemini 2.5 pro":                1,
    "gemini 3.1 pro":                1,
    "claude opus 4.5":               3,
    "claude opus 4.6":               3,
    "claude opus 4.6 (fast mode)":   30,
}

def get_multiplier(model_name):
    key = model_name.lower().strip()
    return MULTIPLIERS.get(key, 1)  # default 1x for unknown models

# Aggregates
total_gross    = sum(i["grossQuantity"] for i in items)
total_included = sum(i["discountQuantity"] for i in items)
total_overage  = sum(i["netQuantity"] for i in items)
total_cost     = sum(i["netAmount"] for i in items)

# Header
print("📊 GitHub Copilot — Premium Request Usage")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print(f"  Account   : {gh_user}")
print(f"  Period    : {tp.get('year')}-{str(tp.get('month')).zfill(2)}")
print(f"  Reset in  : {days_left} days ({next_reset})")

if quota > 0:
    plan_label = plan_name.upper()
    print(f"  Plan      : {plan_label}  ({quota} premium requests/month)")
else:
    print(f"  Plan      : ⚠️  Not configured — run: bash copilot-usage.sh --set-plan <plan>")
    print(f"              (GitHub API does not expose plan quota — must be set manually)")
    print(f"              Valid plans: free, student, pro, pro+, business, enterprise")

print()

if not items:
    print("  No usage data found for this period.")
    sys.exit(0)

# Quota bar
if quota > 0:
    remaining = quota - total_included
    pct = min(total_included / quota * 100, 100)
    bar_fill = int(pct / 100 * 30)
    bar = "█" * bar_fill + "░" * (30 - bar_fill)
    status = "⚠️ " if pct >= 80 or total_overage > 0 else "✅"
    print(f"  Quota used : {int(total_included):>5} / {quota}  {status}")
    print(f"  Remaining  : {int(remaining):>5}")
    print(f"  [{bar}] {pct:.1f}%")
else:
    print(f"  Requests used this month : {int(total_gross)}")

print()

# Overage
if total_overage > 0:
    print(f"  ⚠️  Overage : {int(total_overage)} requests billed at $0.04 each = ${total_cost:.2f}")
else:
    print(f"  ✅ No overage")

print()

# Per-model breakdown
print("  Breakdown by model:")
print(f"  {'Model':<32} {'Gross req':>9}  {'×':>4}  {'~Prompts':>9}  {'Note'}")
print(f"  {'─'*32}  {'─'*9}  {'─'*4}  {'─'*9}  {'─'*20}")

for item in sorted(items, key=lambda x: -x["grossQuantity"]):
    model   = item["model"]
    gross   = item["grossQuantity"]
    overage = item["netQuantity"]
    mult    = get_multiplier(model)

    if mult == 0:
        # Free/included model
        actual  = gross  # 1:1, no premium consumption
        note    = "included (free)"
    elif mult > 0:
        actual  = gross / mult
        note    = f"⚠️ +{int(overage)} overage" if overage > 0 else ""
    else:
        actual  = gross
        note    = ""

    mult_str   = f"{mult}×" if mult > 0 else "free"
    actual_str = f"~{actual:.0f}" if mult not in (0, 1) else f"{int(actual)}"

    print(f"  {model:<32} {int(gross):>9}  {mult_str:>4}  {actual_str:>9}  {note}")

print()
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  'Gross req' = premium requests charged (multiplier already applied)")
print("  '~Prompts'  = estimated actual interactions (gross ÷ multiplier)")
print("  Overage rate: $0.04/request | Multipliers: docs.github.com/copilot/billing/copilot-requests")
PYEOF

echo ""
echo "  Details: github.com/settings/billing/summary"
