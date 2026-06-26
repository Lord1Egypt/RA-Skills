#!/usr/bin/env bash
# copilot-alert.sh — Check Copilot usage against threshold and alert if exceeded
# Usage: bash copilot-alert.sh [--threshold 80]
# Exit 0 = ok (silent), Exit 2 = threshold exceeded or overage detected

set -euo pipefail

CONFIG_FILE="$HOME/.config/copilot-usage/config.json"
THRESHOLD=80

while [[ $# -gt 0 ]]; do
  case "$1" in
    --threshold) THRESHOLD="$2"; shift 2 ;;
    *) shift ;;
  esac
done

# Auth check
GH_USER=$(gh api /user --jq '.login' 2>/dev/null || echo "")
if [[ -z "$GH_USER" ]]; then
  echo "❌ gh not authenticated. Run: gh auth login"
  exit 1
fi

# Load quota from config
QUOTA=0
PLAN_NAME="unknown"
if [[ -f "$CONFIG_FILE" ]]; then
  QUOTA=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('quota', 0))")
  PLAN_NAME=$(python3 -c "import json; d=json.load(open('$CONFIG_FILE')); print(d.get('plan', 'unknown'))")
fi

if [[ "$QUOTA" -eq 0 ]]; then
  echo "⚠️  Copilot plan not configured."
  echo "   Run: bash copilot-usage.sh --set-plan <plan>"
  echo "   (GitHub API does not expose plan quota — must be set manually)"
  exit 1
fi

# Fetch usage
DATA=$(gh api \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "/users/${GH_USER}/settings/billing/premium_request/usage" 2>/dev/null)

if [[ -z "$DATA" ]]; then
  echo "❌ Failed to fetch usage data"
  exit 1
fi

python3 << PYEOF
import json, sys, datetime

data = json.loads(r"""$DATA""")
items = data.get("usageItems", [])
total_included = sum(i["discountQuantity"] for i in items)
total_overage  = sum(i["netQuantity"] for i in items)
total_cost     = sum(i["netAmount"] for i in items)
quota          = $QUOTA
plan           = "$PLAN_NAME"
threshold      = $THRESHOLD

pct       = (total_included / quota) * 100 if quota > 0 else 0
remaining = quota - total_included

today = datetime.date.today()
if today.month == 12:
    reset = datetime.date(today.year + 1, 1, 1)
else:
    reset = datetime.date(today.year, today.month + 1, 1)
days_left = (reset - today).days

if pct >= threshold or total_overage > 0:
    print(f"⚠️  Copilot quota alert [{plan.upper()}]")
    print(f"   Used      : {int(total_included)} / {quota} ({pct:.1f}%)")
    print(f"   Remaining : {int(remaining)} requests")
    print(f"   Reset in  : {days_left} days ({reset})")
    if total_overage > 0:
        print(f"   Overage   : {int(total_overage)} requests billed = \${total_cost:.2f}")
    sys.exit(2)
else:
    print(f"✅ Copilot quota OK [{plan.upper()}]: {int(total_included)}/{quota} ({pct:.1f}%) — {int(remaining)} remaining, resets in {days_left} days")
    sys.exit(0)
PYEOF
