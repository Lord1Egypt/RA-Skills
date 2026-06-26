# Budget Planner

Plan and track budgets using your AI agent. Works for personal finance, project budgets, or department spending.

## What It Does
- Creates structured budgets with categories, allocations, and actuals
- Tracks spending against budget with variance analysis
- Flags overspending early with threshold alerts
- Generates monthly/quarterly budget reports
- Supports multiple budget types (personal, project, department)

## Usage

### Create a Budget
Tell your agent: "Create a monthly budget for [purpose] with a total of $[amount]"

The agent will ask about categories and allocations, then create a structured budget file.

### Budget File Format
Budgets are stored as markdown tables in your workspace:

```markdown
# Budget: [Name] — [Period]
Total: $X,XXX

| Category | Allocated | Spent | Remaining | Status |
|----------|-----------|-------|-----------|--------|
| Rent | $1,500 | $1,500 | $0 | ✅ On track |
| Food | $600 | $450 | $150 | ✅ Under |
| Transport | $200 | $280 | -$80 | 🔴 Over |
```

### Track Spending
Tell your agent: "Log $45 under Food" or "I spent $280 on transport this month"

### Get Reports
- "How's my budget looking?" — summary with variances
- "Where am I overspending?" — flags problem categories
- "Project my end-of-month spend" — extrapolates from current pace

### Alert Thresholds
Default alerts:
- ⚠️ **Warning** at 80% of category allocation
- 🔴 **Over budget** when exceeded
- 📊 **Weekly digest** if enabled

## Tips
- Start with broad categories, refine over time
- Review weekly — catching overspend early is the whole point
- Use "rollover" for categories where unspent funds carry forward
- Compare month-over-month to spot trends

## More Business Tools
Get industry-specific AI agent context packs at [AfrexAI](https://afrexai-cto.github.io/context-packs/) — pre-built configurations that make your agent a domain expert from day one.
