# Expense Tracking

## Purpose
Log daily expenses and automatically track against category budgets.

## When to Use
- "I spent $45 on groceries"
- "Log $20 for lunch"
- "Add expense: $100 gas"
- "What did I spend this week?"

## Data Structure

```json
{
  "expenses": [
    {
      "id": "uuid",
      "amount": 45.67,
      "category": "food",
      "description": "Whole Foods groceries",
      "date": "2024-03-01",
      "timestamp": "2024-03-01T14:30:00",
      "payment_method": "credit_card",
      "tags": ["groceries", "organic"],
      "merchant": "Whole Foods",
      "notes": "Weekly shopping"
    }
  ]
}
```

## Script Usage

```bash
# Log simple expense
python scripts/log_expense.py \
  --amount 45.67 \
  --category food \
  --description "Groceries"

# Log detailed expense
python scripts/log_expense.py \
  --amount 85.00 \
  --category entertainment \
  --description "Concert tickets" \
  --date "2024-03-01" \
  --merchant "Ticketmaster" \
  --tags "events,music"

# List recent expenses
python scripts/list_expenses.py --days 7

# View expenses by category
python scripts/list_expenses.py --category food --month current

# Delete/correct expense
python scripts/delete_expense.py --expense-id "uuid"
```

## Output Format

```
EXPENSE LOGGED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Amount: $45.67
Category: Food
Description: Whole Foods groceries
Date: March 1, 2024

BUDGET IMPACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Food Budget: $500.00/month
Previously Spent: $320.45
This Expense: $45.67
Total Spent: $366.12
Remaining: $133.88

Status: ✅ ON TRACK (73% used)

Days remaining in month: 15
Daily budget remaining: $8.93/day

RECENT FOOD EXPENSES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Today      $45.67  Whole Foods
Yesterday  $12.50  Lunch with coworkers
Feb 28     $89.23  Grocery run
Feb 27     $28.00  Dinner out
Feb 26     $15.00  Coffee and pastry

TOP EXPENSES THIS MONTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. $120.00  Costco (Feb 15)
2. $95.50   Restaurant (Feb 14)
3. $89.23   Grocery run (Feb 28)
```

## Quick Entry Methods

### Natural Language Parsing
```
User: "Spent $50 on gas yesterday"
→ Parse: amount=$50, category=transport, date=yesterday

User: "Lunch $15"
→ Parse: amount=$15, category=food, description=lunch

User: "$200 Whole Foods groceries"
→ Parse: amount=$200, category=food, merchant=Whole Foods
```

### Category Mapping
Common terms automatically mapped to categories:
- **Food**: groceries, restaurant, lunch, dinner, coffee, takeout
- **Transport**: gas, uber, lyft, parking, toll, bus, subway
- **Entertainment**: movie, concert, netflix, spotify, game
- **Shopping**: amazon, target, clothing, shoes, electronics

## Expense Categories

### Primary Categories
Expenses must be assigned to one of the budget categories:
- Housing, Food, Transport, Utilities
- Entertainment, Health, Shopping
- Savings, Debt, Gifts/Charity

### Optional Tags
Additional tags for filtering/analysis:
- **Essential vs Discretionary**
- **Recurring vs One-time**
- **Individual vs Shared**
- **Work vs Personal**

## Common Patterns

### Recurring Expenses
```bash
# Mark as recurring
python scripts/log_expense.py \
  --amount 1200 \
  --category housing \
  --description "Rent" \
  --recurring monthly

# Will auto-log on 1st of each month
```

### Split Expenses
```bash
# Split across categories
python scripts/log_expense.py \
  --amount 150 \
  --description "Target shopping" \
  --split "food:50,shopping:100"
```

### Bulk Import
```bash
# Import from CSV
python scripts/log_expense.py \
  --import-file "expenses.csv" \
  --format csv
```

## Expense Review

### Daily Review
```bash
python scripts/list_expenses.py --today
```
Shows:
- All expenses logged today
- Running daily total
- Budget impact

### Weekly Review
```bash
python scripts/list_expenses.py --week
```
Shows:
- Weekly spending by category
- Comparison to budget
- Top 5 expenses
- Unusual spending alerts

### Monthly Review
```bash
python scripts/list_expenses.py --month
```
Shows:
- All expenses for month
- Category breakdown
- Merchant analysis
- Trends vs previous months

## Correcting Mistakes

### Edit Expense
```bash
python scripts/edit_expense.py \
  --expense-id "uuid" \
  --amount 50.00 \
  --category transport
```

### Delete Expense
```bash
python scripts/delete_expense.py --expense-id "uuid"
```

### Bulk Delete
```bash
python scripts/delete_expense.py \
  --category entertainment \
  --date "2024-03-01"
```

## Spending Insights

### Automatic Analysis
- **Spending velocity**: Are you on pace to hit budget?
- **Unusual expenses**: Significant deviations from average
- **Forgotten categories**: Categories with no recent expenses
- **Merchant patterns**: Where you spend most frequently

### Example Insight
```
💡 INSIGHT: Your food spending is 20% higher on weekends
   Consider meal prepping to reduce dining out costs.

💡 INSIGHT: You've logged 5 coffee purchases this week
   Total: $35. Weekly coffee budget: $20
   Suggestion: Make coffee at home 2-3 days/week
```
