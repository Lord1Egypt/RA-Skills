# Overage Recovery

## Purpose
Help users recover from budget overages through reallocation and spending adjustments.

## When to Use
- "I went over on entertainment"
- "Help me fix my budget"
- "How do I recover from overspending?"
- "Reallocate budget from food to dining"

## Recovery Strategies

### Strategy 1: Reallocation
Move unused budget from one category to another.

```bash
# Move $50 from transport to food
python scripts/reallocate_budget.py \
  --from transport \
  --to food \
  --amount 50
```

**When to use:** One category is underspent, another is over.

### Strategy 2: Future Adjustment
Reduce next month's budget in over-spent category.

```bash
# Reduce next month's entertainment budget
python scripts/set_budget.py \
  --category entertainment \
  --limit 150 \
  --period monthly \
  --update
```

**When to use:** Consistent over-spending in a category.

### Strategy 3: Spending Cutback
Reduce spending for remainder of month.

```
Current pace: $25/day
Required pace: $10/day for remaining 10 days
Action needed: Reduce daily spending by $15
```

**When to use:** Temporary overage, can adjust spending habits.

### Strategy 4: Accept and Learn
Acknowledge overage and use as learning.

```
Entertainment over by $45 this month
Cause: Concert tickets (one-time)
Learning: Plan better for seasonal events
Next month: No action needed
```

**When to use:** One-time expenses, genuine need.

## Overage Analysis Output

```
BUDGET OVERAGE ANALYSIS
Category: Entertainment
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CURRENT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Budget: $200.00
Spent:  $245.00
Overage: $45.00 (123% of budget)

CAUSE ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Top expenses this month:
1. $120 - Concert tickets (one-time event)
2. $65  - Dinner with friends (twice)
3. $35  - Movie night + snacks
4. $25  - Streaming subscriptions

Root cause: Concert tickets ($120) put category over budget
           Without this: $125 spent vs $200 budget = on track

RECOVERY OPTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Option A: Reallocate from underspent categories
─────────────────────────────────────────────────
Available to reallocate:
• Transport: $50 remaining ($150/$200) → Can move $30-40
• Utilities: $80 remaining ($170/$250) → Can move $40-50
• Health: $70 remaining ($30/$100) → Can move $20-30

Suggested: Move $45 from Utilities to Entertainment
Result: Entertainment balanced, Utilities still healthy at 88%

Execute? [Y/n]

Option B: Cut spending for rest of month
─────────────────────────────────────────────────
Days remaining: 12
Current pace needed: $0/day (already over)

If you spend $0 on entertainment for rest of month:
• Overage stays at $45
• Next month starts fresh

Realistic adjustment:
• Limit to $5/day for 12 days = $60 total
• Would increase overage to $85
• Not recommended

Option C: Accept and adjust next month
─────────────────────────────────────────────────
This is a one-time expense (concert season)
Accept $45 overage this month

Adjust next month:
• Set Entertainment budget to $250 for concert season
• Reduce Shopping by $30 to compensate
• Or accept higher spending during this period

Recommended if: This is truly one-time

Option D: Emergency fund buffer
─────────────────────────────────────────────────
Use savings buffer to cover overage:
• Transfer $45 from Savings to cover
• Reduces savings rate from 20% to 19%
• Emergency fund still intact

Recommended if: Savings rate > 15%

RECOMMENDATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Suggested: Option A - Reallocate $45 from Utilities

Why:
• Utilities consistently underspent
• Entertainment overage is genuine (concert)
• No behavior change needed
• Budget stays balanced overall

Alternative: Option C if you prefer to track true spending

What would you like to do? [A/B/C/D/Custom]
```

## Reallocation Script

```bash
# Check available funds for reallocation
python scripts/reallocate_budget.py --check-available

# Reallocate between categories
python scripts/reallocate_budget.py \
  --from utilities \
  --to entertainment \
  --amount 45 \
  --confirm

# Preview reallocation
python scripts/reallocate_budget.py \
  --from transport \
  --to food \
  --amount 50 \
  --preview
```

## Data Structure

```json
{
  "reallocations": [
    {
      "id": "uuid",
      "from_category": "utilities",
      "to_category": "entertainment",
      "amount": 45.00,
      "date": "2024-03-15",
      "reason": "Cover concert ticket overage",
      "original_budgets": {
        "utilities": 250,
        "entertainment": 200
      },
      "new_budgets": {
        "utilities": 295,
        "entertainment": 155
      }
    }
  ]
}
```

## Prevention Strategies

### Identify Patterns
```
ANALYSIS: Entertainment overages last 3 months
January: +$20 (birthday dinner)
February: +$15 (concert)
March: +$45 (concert season)

Pattern: Social events and concerts
Suggestion: Increase entertainment budget to $250 permanently
          Reduce shopping from $250 to $225
          Net change: +$0, better alignment with reality
```

### Seasonal Adjustments
```
Concert season: March-May (higher entertainment)
Holiday season: Nov-Dec (higher gifts, travel)
Back to school: Aug-Sep (higher shopping)

Adjust budgets seasonally:
python scripts/set_budget.py --category entertainment --limit 250 --months "Mar,Apr,May"
```

### Sinking Funds
```
For predictable irregular expenses:
• Annual insurance: $1200 → Save $100/month
• Holiday gifts: $600 → Save $50/month
• Car maintenance: $800 → Save $67/month

Create categories:
python scripts/set_budget.py --category "insurance-sinking" --limit 100
```

## Recovery Timeline

### Short-term (This Month)
- Reallocate if possible
- Cut discretionary spending
- Use emergency buffer if needed

### Medium-term (Next 2-3 Months)
- Adjust budget limits based on reality
- Build sinking funds
- Identify spending triggers

### Long-term (Ongoing)
- Review budget monthly
- Adjust for life changes
- Increase savings rate gradually

## Psychological Approach

### Avoid Shame
```
❌ "You failed your budget"
✅ "Let's adjust your budget to match reality"

❌ "You overspent again"
✅ "This category needs more room - let's fix it"

❌ "You need more discipline"
✅ "Your budget needs to match your values"
```

### Focus on Solutions
Every overage is data, not failure:
- What caused it?
- Was it necessary or discretionary?
- Is it one-time or ongoing?
- How do we adjust?

### Celebrate Recovery
```
🎉 Recovery complete!
You went over by $45, but:
• Found $50 available in Utilities
• Reallocated to cover the gap
• Overall budget still balanced
• Learned: Entertainment needs $250/month

Next month will be better! 💪
```
