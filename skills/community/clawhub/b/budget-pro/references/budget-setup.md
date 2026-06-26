# Budget Setup

## Purpose
Establish monthly budget limits for spending categories and income tracking.

## When to Use
- "Set my food budget to $500"
- "Create a budget for me"
- "What's a good budget for housing?"
- "Update my entertainment budget"

## Budget Categories

### Standard Categories
| Category | Typical % of Income | Description |
|----------|---------------------|-------------|
| Housing | 25-35% | Rent, mortgage, insurance, property tax |
| Food | 10-15% | Groceries, dining out, coffee/snacks |
| Transport | 10-15% | Gas, car payment, insurance, maintenance, transit |
| Utilities | 5-10% | Electric, gas, water, internet, phone |
| Entertainment | 5-10% | Movies, events, hobbies, subscriptions |
| Health | 5-10% | Insurance, medical, dental, gym, therapy |
| Shopping | 5-10% | Clothing, household items, personal care |
| Savings | 10-20% | Emergency fund, investments, retirement |
| Debt | 5-15% | Credit cards, loans, student debt |
| Gifts/Charity | 2-5% | Presents, donations, tipping |

### Custom Categories
Users can create custom categories:
- Pet expenses
- Childcare
- Education
- Travel
- Business expenses

## Data Structure

```json
{
  "budgets": [
    {
      "id": "uuid",
      "category": "food",
      "limit": 500,
      "period": "monthly",
      "currency": "USD",
      "created_at": "2024-03-01T00:00:00",
      "updated_at": "2024-03-01T00:00:00",
      "alert_thresholds": {
        "warning": 0.7,
        "critical": 0.9,
        "overage": 1.0
      }
    }
  ],
  "income": {
    "sources": [
      {
        "name": "Salary",
        "amount": 5000,
        "frequency": "monthly",
        "after_tax": true
      }
    ],
    "total_monthly": 5000
  }
}
```

## Script Usage

```bash
# Set category budget
python scripts/set_budget.py \
  --category food \
  --limit 500 \
  --period monthly

# Set income
python scripts/set_budget.py \
  --type income \
  --amount 5000 \
  --frequency monthly \
  --source "salary"

# View all budgets
python scripts/budget_status.py --show-limits

# Update budget
python scripts/set_budget.py \
  --category entertainment \
  --limit 200 \
  --update
```

## Output Format

```
BUDGET SETUP SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Monthly Income: $5,000.00
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CATEGORY BUDGETS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fixed Expenses (Needs):
• Housing      $1,500.00  (30%)  ████████████████
• Utilities      $250.00   (5%)  ██
• Transport      $500.00  (10%)  █████
• Health         $300.00   (6%)  ███

Variable Expenses:
• Food           $500.00  (10%)  █████
• Shopping       $250.00   (5%)  ██
• Entertainment  $200.00   (4%)  ██

Financial Goals:
• Savings        $750.00  (15%)  ███████
• Debt           $250.00   (5%)  ██

GIFTS/CHARITY    $100.00   (2%)  █

TOTAL BUDGETED: $5,000.00
BALANCE: $0.00 ✅

BUDGET HEALTH: 100% allocated

⚠️  Note: Aim for 50/30/20 rule:
    • 50% Needs (Housing, Utilities, Transport, Health, Food)
    • 30% Wants (Shopping, Entertainment)
    • 20% Savings/Debt

Your current: 61% / 19% / 20%
    Consider reducing entertainment or shopping slightly
    to increase emergency fund contribution.
```

## Budget Guidelines

### 50/30/20 Rule
A simple budgeting framework:
- **50% Needs**: Housing, utilities, groceries, transport, minimum debt payments
- **30% Wants**: Dining out, entertainment, shopping, hobbies
- **20% Savings/Debt**: Emergency fund, retirement, extra debt payments

### Income-Based Recommendations

**Monthly Income: $3,000**
```
Housing:    $750-900   (25-30%)
Food:       $300-450   (10-15%)
Transport:  $300-450   (10-15%)
Utilities:  $150-300   (5-10%)
Savings:    $300-600   (10-20%)
```

**Monthly Income: $5,000**
```
Housing:    $1,250-1,750 (25-35%)
Food:       $500-750    (10-15%)
Transport:  $500-750    (10-15%)
Utilities:  $250-500    (5-10%)
Savings:    $500-1,000  (10-20%)
```

**Monthly Income: $8,000**
```
Housing:    $2,000-2,800 (25-35%)
Food:       $800-1,200  (10-15%)
Transport:  $800-1,200  (10-15%)
Savings:    $1,200-2,400 (15-30%)
```

## Setting Realistic Budgets

### Factors to Consider
1. **Fixed costs** that can't change (rent, loan payments)
2. **Variable necessities** (groceries, gas)
3. **Historical spending** (review last 3 months)
4. **Financial goals** (saving rate, debt payoff)
5. **Lifestyle preferences** (dining out frequency)

### Common Mistakes
- Underestimating food/dining costs
- Forgetting irregular expenses (annual insurance, gifts)
- Setting savings too high (unrealistic to maintain)
- Not accounting for seasonal variations

### First-Time Budget Setup
```bash
# Step 1: Set income
python scripts/set_budget.py --type income --amount [YOUR_INCOME]

# Step 2: Set fixed expenses
python scripts/set_budget.py --category housing --limit [RENT/MORTGAGE]
python scripts/set_budget.py --category utilities --limit [AVERAGE]
python scripts/set_budget.py --category transport --limit [CAR/GAS/TRANSIT]

# Step 3: Set variable necessities
python scripts/set_budget.py --category food --limit [BASED_ON_HISTORY]

# Step 4: Set financial goals
python scripts/set_budget.py --category savings --limit [TARGET_AMOUNT]

# Step 5: Fill remaining with wants
python scripts/set_budget.py --category entertainment --limit [REMAINING]
```

## Adjusting Budgets

### When to Adjust
- Income changes (raise, job loss)
- Major life changes (move, new baby)
- Consistently over/under in categories
- New financial goals

### How to Adjust
```bash
# Increase food budget, decrease entertainment
python scripts/set_budget.py --category food --limit 600 --update
python scripts/set_budget.py --category entertainment --limit 150 --update

# Or reallocate
python scripts/reallocate_budget.py \
  --from entertainment \
  --to food \
  --amount 100
```

## Alert Thresholds

Default thresholds (customizable per category):
- **70%** - Gentle heads up
- **90%** - Clear warning
- **100%** - Overage alert

```bash
# Set custom thresholds
python scripts/set_budget.py \
  --category food \
  --limit 500 \
  --warning-threshold 0.6 \
  --critical-threshold 0.85
```
