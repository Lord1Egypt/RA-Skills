---
name: financial-wealth-management
version: 1.0.0
description: Wealth management and financial advisory tools: client reviews, financial planning, portfolio analysis, and client reporting
source: anthropics/financial-services
---

# wealth-management

Wealth management and financial advisory tools: client reviews, financial planning, portfolio analysis, and client reporting

## 来源
来自 Anthropic 官方 financial-services 仓库的 wealth-management 插件。
原始仓库: https://github.com/anthropics/financial-services

## 可用命令 (Commands)

### client-report

---
description: Generate a client performance report
argument-hint: "[client name] [period, e.g. Q4 2025]"
---

Load the `client-report` skill to generate a professional client-facing performance report.

If a client and period are provided, use them. Otherwise ask for client details and reporting period.


---

### client-review

---
description: Prep for a client review meeting
argument-hint: "[client name]"
---

Load the `client-review` skill and prepare a client meeting package with performance, allocation, and talking points.

If a client name is provided, use it. Otherwise ask who the meeting is with.


---

### financial-plan

---
description: Build or update a financial plan
argument-hint: "[client name]"
---

Load the `financial-plan` skill to create or update a comprehensive financial plan covering retirement, education, estate, and cash flow projections.

If a client name is provided, use it. Otherwise ask for client details.


---

### rebalance

---
description: Analyze drift and generate rebalancing trades
argument-hint: "[client name or account]"
---

Load the `portfolio-rebalance` skill to analyze allocation drift and recommend tax-aware rebalancing trades.

If a client or account is provided, use it. Otherwise ask for the portfolio to analyze.


---

### tlh

---
description: Identify tax-loss harvesting opportunities
argument-hint: "[client name or account]"
---

Load the `tax-loss-harvesting` skill to scan taxable accounts for harvestable losses, suggest replacement securities, and manage wash sale windows.

If a client or account is provided, use it. Otherwise ask for the portfolio to scan.


---

## 底层技能 (Skills)

### client-review

---
name: client-review
description: Prepare for client review meetings with portfolio performance summary, allocation analysis, talking points, and action items. Pulls together account data into a concise meeting-ready format. Use before quarterly reviews, annual checkups, or ad-hoc client meetings. Triggers on "client review", "meeting prep for [client]", "quarterly review", "prep for [client name]", or "client meeting".
---

# Client Review Prep

## Workflow

### Step 1: Client Context

Gather or look up:
- **Client name** and household members
- **Account types**: Taxable, IRA, Roth, 401(k), trust, etc.
- **Total AUM** across accounts
- **Investment Policy Statement (IPS)**: Target allocation, risk tolerance, constraints
- **Life stage**: Accumulation, pre-retirement, retirement, legacy
- **Last meeting date** and any outstanding action items

### Step 2: Portfolio Performance

For each account and the household aggregate:

| Metric | QTD | YTD | 1-Year | 3-Year | Since Inception |
|--------|-----|-----|--------|--------|----------------|
| Portfolio return | | | | | |
| Benchmark return | | | | | |
| Alpha | | | | | |

**Performance Attribution:**
- Which asset classes / positions drove returns?
- Top 3 contributors and top 3 detractors
- Any outsized single-position impact?

### Step 3: Allocation Review

Current vs. target allocation:

| Asset Class | Target | Current | Drift | Action |
|------------|--------|---------|-------|--------|
| US Large Cap | | | | |
| US Mid/Small | | | | |
| International Developed | | | | |
| Emerging Markets | | | | |
| Fixed Income | | | | |
| Alternatives | | | | |
| Cash | | | | |

Flag any drift exceeding the IPS rebalancing threshold (typically 3-5%).

### Step 4: Talking Points

Generate a meeting agenda:

1. **Market overview** (2-3 min): Brief macro context and outlook
2. **Portfolio performance** (5 min): How did we do? Why?
3. **Allocation review** (5 min): Any rebalancing needed?
4. **Planning updates** (5-10 min):
 

---

### financial-plan

---
name: financial-plan
description: Build or update a comprehensive financial plan covering retirement projections, education funding, estate planning, and cash flow analysis. Use for new client onboarding, annual plan reviews, or scenario modeling. Triggers on "financial plan", "retirement plan", "can I retire", "education funding", "estate plan", "cash flow analysis", or "plan update".
---

# Financial Plan

## Workflow

### Step 1: Client Profile

Gather or confirm:
- **Demographics**: Age, spouse age, dependents, life expectancy assumptions
- **Employment**: Current income, expected raises, retirement age target
- **Accounts**: All investment accounts with balances and asset allocation
- **Income sources**: Salary, bonuses, rental income, Social Security estimates, pensions
- **Expenses**: Current annual spending, expected changes (mortgage payoff, kids' independence)
- **Liabilities**: Mortgage, student loans, other debt
- **Insurance**: Life, disability, LTC, health
- **Estate**: Wills, trusts, beneficiary designations, gifting strategy

### Step 2: Cash Flow Analysis

Build annual cash flow projections:

| Year | Age | Gross Income | Taxes | Living Expenses | Savings | Net Cash Flow |
|------|-----|-------------|-------|-----------------|---------|--------------|
| | | | | | | |

Key inputs:
- Inflation rate assumption (typically 2.5-3%)
- Tax rate (marginal and effective)
- Savings rate and where savings are directed (pre-tax, Roth, taxable)

### Step 3: Retirement Projections

**Accumulation Phase:**
- Current portfolio value
- Annual contributions (401k, IRA, taxable)
- Expected return by asset class
- Monte Carlo simulation: probability of success at various spending levels

**Distribution Phase:**
- Required annual spending in retirement (today's dollars → inflation-adjusted)
- Social Security start age and benefit
- Pension income (if any)
- Portfolio withdrawal rate and sequence
- Required Minimum Distributions (RMDs)

**Key Output:**
- Projected por

---
