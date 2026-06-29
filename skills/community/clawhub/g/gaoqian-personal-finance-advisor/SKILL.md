---
name: Personal Finance Advisor
slug: personal-finance-advisor
description: AI-powered personal finance management skill. Provides budgeting, expense tracking, investment portfolio analysis, tax optimization strategies, retirement planning, debt management, and financial goal setting with personalized recommendations.
version: 1.0.0
author: ai-gaoqian
tags:
  - finance
  - budgeting
  - investment
  - tax-planning
  - wealth-management
metadata:
  openclaw:
    requires: "python>=3.10, openclaw>=0.9.0"
---

# Personal Finance Advisor

Comprehensive personal finance management for individuals and families. Covers budgeting, investing, tax planning, debt management, and long-term wealth building.

## Usage

```
finance: analyze my monthly spending from [CSV/Excel file]
finance: review my investment portfolio allocation
finance: calculate tax optimization for 2026
finance: create debt payoff plan for $50,000 at 6.8% APR
finance: project retirement savings with current contribution rate
```

## Execution Flow

1. **Expense Analysis** — Categorize transactions, identify spending patterns, detect subscription leaks, compare to 50/30/20 rule
2. **Budget Builder** — Generate personalized budget based on income, fixed expenses, savings goals; zero-based and envelope methods supported
3. **Portfolio Review** — Asset allocation analysis, fee impact calculation, risk assessment, rebalancing recommendations, tax-loss harvesting opportunities
4. **Tax Optimizer** — Deduction maximization, retirement account strategy (401k/IRA/Roth), capital gains planning, estimated tax calculation
5. **Debt Manager** — Avalanche vs. snowball comparison, refinancing analysis, payoff timeline projection
6. **Goal Planner** — Retirement, education, home purchase, emergency fund — all with Monte Carlo simulation for probability scoring

## Output Format

```markdown
# Personal Finance Report
**Period**: January - May 2026

## Monthly Cash Flow
- Income: $8,500/mo
- Expenses: $6,200/mo
- Savings Rate: 27.1% ✅

## Spending Breakdown
| Category | Amount | % of Income | Status |
|----------|--------|-------------|--------|
| Housing  | $2,200 | 25.9% | Within target |
| Food     | $980   | 11.5% | Within target |
| Transport| $450   | 5.3%  | Within target |
| Subscriptions | $320 | 3.8% | ⚠️ Review (detected 3 unused) |
| Entertainment | $620 | 7.3% | ⚠️ Over budget |

## Portfolio Summary
- Total Value: $145,000
- Allocation: 60% Stocks / 25% Bonds / 10% Cash / 5% Crypto
- YTD Return: +8.3%
- Fee Drag: 0.42% ($609/year)

## Recommendations
1. Cancel 3 unused subscriptions → Save $95/mo
2. Rebalance portfolio: Reduce crypto from 5% to 3%
3. Increase 401k contribution from 8% to 12% → Tax saving $1,200/year
4. Refinance auto loan: 6.8% → 4.2% rate available → Save $1,850 over remaining term

## Financial Health Score: 78/100
✅ Emergency Fund: 6 months (healthy)
⚠️ Debt-to-Income: 32% (elevated)
✅ Retirement Projection: On track for age 62
```

## Notes

- All financial data processed locally; no data sent to external services
- Investment recommendations are educational, not fiduciary advice
- Tax calculations based on 2026 tax code; verify with CPA for complex situations
- CSV/Excel import supports major bank export formats (Chase, Bank of America, Wells Fargo, etc.)
