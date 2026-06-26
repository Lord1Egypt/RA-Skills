# Budget Alerts & Thresholds

## Purpose
Proactive notifications when spending approaches or exceeds budget limits.

## Alert Levels

### Level 1: Gentle Heads Up (70%)
**Triggered when:** Category reaches 70% of budget

**Message Format:**
```
📊 Budget Update: Food
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You've spent $350 of your $500 monthly food budget (70%).

Remaining: $150 for the next 12 days
That's about $12.50 per day.

You're doing well! Just a friendly heads up.
```

**Action:** None required, informational only

### Level 2: Warning (90%)
**Triggered when:** Category reaches 90% of budget

**Message Format:**
```
⚠️  Budget Warning: Entertainment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You've spent $180 of your $200 monthly budget (90%).

Remaining: $20 for the next 18 days
Daily budget remaining: $1.11/day

OPTIONS:
1. Pause entertainment spending for now
2. Reallocate $50 from Shopping (underspent)
3. Accept overage and reduce next month's budget

Reply with option number or ask for details.
```

**Action:** User decision needed

### Level 3: Overage (100%+)
**Triggered when:** Category exceeds 100% of budget

**Message Format:**
```
🚨 Budget Exceeded: Shopping
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

You've spent $275 of your $250 monthly budget (110%).

Overage: $25.00
Days remaining: 10

RECOVERY OPTIONS:

A) Cut $25 from another category:
   • Food has $50 remaining (reallocate $25)
   • Entertainment has $30 remaining (reallocate $25)

B) Reduce next month's Shopping budget to $225

C) Accept overage and adjust future budgets

What would you like to do?
```

**Action:** Immediate reallocation or adjustment needed

## Data Structure

```json
{
  "alerts": [
    {
      "id": "uuid",
      "category": "food",
      "level": "warning",
      "threshold": 0.9,
      "triggered_at": "2024-03-20T15:30:00",
      "amount_spent": 450.00,
      "budget_limit": 500.00,
      "acknowledged": false,
      "action_taken": null
    }
  ],
  "alert_settings": {
    "enabled": true,
    "delivery": "immediate",
    "digest_day": "sunday",
    "quiet_hours": {"start": "22:00", "end": "08:00"}
  }
}
```

## Script Usage

```bash
# Check and trigger alerts
python scripts/check_alerts.py

# Configure alert settings
python scripts/set_alert_preferences.py \
  --threshold warning 0.75 \
  --threshold critical 0.90 \
  --quiet-hours 22:00-08:00

# View alert history
python scripts/list_alerts.py --days 30

# Acknowledge alert
python scripts/acknowledge_alert.py --alert-id "uuid"
```

## Custom Thresholds

### Per-Category Settings
```bash
# Strict budget for entertainment
python scripts/set_budget.py \
  --category entertainment \
  --limit 200 \
  --warning-threshold 0.6 \
  --critical-threshold 0.8

# Lenient budget for food (necessity)
python scripts/set_budget.py \
  --category food \
  --limit 600 \
  --warning-threshold 0.8 \
  --critical-threshold 0.95
```

### Global Settings
```bash
# Change default thresholds
python scripts/set_alert_preferences.py \
  --default-warning 0.75 \
  --default-critical 0.90 \
  --default-overage 1.0
```

## Alert Delivery

### Immediate Alerts
Sent right when threshold is crossed during expense logging.

### Digest Mode
Alerts batched and sent at scheduled time (default: Sunday evening).

### Quiet Hours
No alerts sent during configured quiet hours (default: 10pm-8am).

## Smart Alerts

### Context-Aware
Consider time in month:
```
Day 5 of month: 50% budget used = ALERT (on pace to exceed)
Day 25 of month: 90% budget used = OK (normal pace)
```

### Spending Velocity
```
⚠️  At current pace, you'll exceed your Food budget by $120
    Pace: $20/day average
    Projected month-end: $620 (budget: $500)
    
    Suggestion: Reduce daily spending to $10 for remaining 12 days
```

### Anomaly Detection
```
💡 Unusual spending detected:
   $200 charge to Electronics (usually $0-50/month)
   Category: Shopping
   
   Is this expected? [Yes/No/Wrong Category]
```

## Alert Fatigue Prevention

### Rate Limiting
- Max 1 alert per category per day
- Similar expenses don't trigger repeated alerts
- Snooze option available

### Smart Grouping
```
📊 Multiple Budget Updates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Approaching limits:
• Food: 85% ($425/$500)
• Entertainment: 75% ($150/$200)

On track:
• Transport: 45% ($90/$200)
• Utilities: 30% ($75/$250)

Review your budgets? [Yes/No]
```

## Weekend/Monthly Summaries

### Weekly Digest (Sunday)
```
WEEKLY BUDGET DIGEST
Week of Feb 25 - Mar 3
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORIES ON TRACK ✅
• Transport: $45/$200 (23%)
• Utilities: $60/$250 (24%)
• Health: $0/$100 (0%)

CATEGORIES AT RISK ⚠️
• Food: $380/$500 (76%) - $120 remaining
• Entertainment: $170/$200 (85%) - $30 remaining

BUDGET EXCEEDED 🚨
• Shopping: $275/$250 (110%) - $25 over

TOP EXPENSES THIS WEEK
1. $120 - Grocery run (Whole Foods)
2. $85 - Concert tickets
3. $65 - Gas fill-up

PROJECTED MONTH-END
Based on current spending pace:
• Food: $580 (over by $80)
• Entertainment: $240 (over by $40)
• Shopping: $320 (over by $70)

💡 SUGGESTION: Reduce food spending by $7/day to stay on budget
```

### Monthly Summary (Last day of month)
```
MONTHLY BUDGET REVIEW
March 2024
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL SPENT: $4,200 of $5,000 budget
SAVINGS: $800 (16%)

CATEGORY PERFORMANCE
✅ Under budget: Transport (-$50), Utilities (-$30)
⚠️  Close to budget: Food (+$20 over)
🚨 Over budget: Entertainment (+$45), Shopping (+$75)

LESSONS LEARNED
• Entertainment: Concert season hit harder than expected
• Shopping: New laptop purchase one-time expense
• Food: Weekend dining out added up

NEXT MONTH ADJUSTMENTS
Consider increasing Entertainment to $250 for concert season
Shopping should normalize without large purchases
```
