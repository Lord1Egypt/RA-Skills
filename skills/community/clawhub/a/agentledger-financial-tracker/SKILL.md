---
name: financial-tracker
version: "1.0.0"
description: AI-powered financial tracking for solopreneurs — log income and expenses, monitor revenue toward monthly goals, generate P&L snapshots, flag cash flow risks, and build a running financial picture with zero spreadsheets.
tags: [finance, revenue-tracking, income, expenses, p-and-l, cash-flow, solopreneur, business-ops, goal-tracking, financial-dashboard]
platforms: [openclaw, cursor, windsurf, generic]
category: business
author: The Agent Ledger
license: CC-BY-NC-4.0
url: https://github.com/theagentledger/agent-skills
---

# Financial Tracker — by The Agent Ledger

> **Just deliver this skill to your agent.** One paste, and your agent becomes your personal CFO — no spreadsheets, no accounting software to learn. Your agent reads the instructions and handles the rest.

Track every dollar in and out of your solo business. Monthly P&L snapshots, revenue goal progress, cash flow flags, and tax estimate tracking — all maintained in plain text files your agent understands.

**Version:** 1.0.0
**License:** CC-BY-NC-4.0
**More:** [theagentledger.com](https://www.theagentledger.com)

---

## What This Skill Does

Configures your agent to act as a lightweight CFO for your solo business:

1. **Income Logging** — Record revenue entries with source, amount, date, and category
2. **Expense Logging** — Track business expenses with vendor, amount, purpose, and tax status
3. **Monthly P&L** — Generate profit-and-loss summaries on demand or on a schedule
4. **Revenue Goal Tracking** — Monitor progress toward monthly and annual income targets
5. **Cash Flow Flags** — Surface warning signs (slow months, rising costs, income concentration risk)
6. **Tax Estimate Tracking** — Rough quarterly self-employment tax estimates based on net income
7. **Year-to-Date Snapshot** — Running YTD revenue, expenses, and net income at any time

---

## Quick Start

Tell your agent:

> "Read the Financial Tracker skill. Set up my finance files and log this income: [source], $[amount], [date], [category]."

Your agent will create the file structure and start tracking immediately.

---

## Setup (5 Steps)

### Step 1 — Create Finance Directory

Your agent creates a `/finance/` folder in your workspace (or wherever you prefer):

```
finance/
  README.md           ← how to use these files
  income-log.md       ← all income entries
  expense-log.md      ← all expense entries
  monthly-summary.md  ← running monthly P&L (appended each month)
  finance-state.json  ← targets, YTD totals, running balances
  tax-estimates.md    ← quarterly tax tracking
```

Tell your agent: "Create the finance directory structure using the Financial Tracker skill."

### Step 2 — Set Your Targets

Your agent will ask for:

- **Monthly revenue target** — your income goal per month (e.g., $5,000)
- **Annual revenue target** — your yearly income goal (e.g., $60,000)
- **Expense budget** — monthly spend ceiling (e.g., $500)
- **Tax rate estimate** — rough self-employment rate (e.g., 30% — adjust based on your situation)

These go into `finance-state.json` and are used for all progress calculations.

> ⚠️ **Tax Disclaimer:** This skill provides rough estimates only. It is not tax advice. Consult a qualified tax professional for your actual tax obligations.

### Step 3 — Log Your First Income Entry

Tell your agent:

> "Log income: [source name], $[amount], [date], [category]"

Example: "Log income: Gumroad digital sales, $320, March 6, digital-products"

Your agent appends to `income-log.md` in this format:

```
| 2026-03-06 | Gumroad digital sales | $320.00 | digital-products | — |
```

### Step 4 — Log Expenses

Tell your agent:

> "Log expense: [vendor], $[amount], [date], [purpose], [tax-deductible: yes/no]"

Example: "Log expense: Canva Pro, $15, March 1, design tools, yes"

### Step 5 — Get Your First Snapshot

Tell your agent: "Give me a financial snapshot for this month."

Your agent generates a P&L summary, shows goal progress, and flags any concerns.

---

## File Formats

### income-log.md

```markdown
# Income Log

| Date | Source | Amount | Category | Notes |
|------|--------|--------|----------|-------|
| 2026-03-06 | Gumroad — premium guide | $49.00 | digital-products | — |
| 2026-03-05 | Freelance consulting | $500.00 | services | Project X |
| 2026-03-01 | Etsy digital downloads | $38.50 | digital-products | — |
```

**Income Categories (customize these):**
- `digital-products` — guides, templates, downloads
- `services` — consulting, freelance, coaching
- `subscriptions` — recurring SaaS or membership revenue
- `affiliate` — referral income
- `ads` — ad revenue (newsletter, blog)
- `other` — miscellaneous

### expense-log.md

```markdown
# Expense Log

| Date | Vendor | Amount | Purpose | Tax-Deductible | Notes |
|------|--------|--------|---------|----------------|-------|
| 2026-03-01 | Canva Pro | $15.00 | Design tools | Yes | Annual ÷ 12 |
| 2026-03-02 | Gumroad fees | $4.90 | Platform fees (10%) | Yes | On $49 sale |
| 2026-03-03 | ChatGPT Plus | $20.00 | AI tools | Yes | — |
```

**Expense Categories:**
- `platform-fees` — Gumroad, Etsy, Shopify, marketplace cuts
- `tools` — software subscriptions (AI, design, email, etc.)
- `ads` — paid advertising
- `contractors` — freelancers or outsourced work
- `education` — courses, books, memberships
- `misc` — anything that doesn't fit above

### finance-state.json

```json
{
  "targets": {
    "monthly_revenue": 5000,
    "annual_revenue": 60000,
    "monthly_expense_ceiling": 500,
    "tax_rate_estimate": 0.30
  },
  "ytd": {
    "year": 2026,
    "income": 0,
    "expenses": 0,
    "net": 0,
    "last_updated": ""
  },
  "current_month": {
    "month": "",
    "income": 0,
    "expenses": 0,
    "net": 0
  }
}
```

---

## Usage Patterns

### Log Income
> "Log income: [source], $[amount], [date], [category]"

> "Add revenue: Consulting call with client, $300, today, services"

### Log Expense
> "Log expense: [vendor], $[amount], [date], [purpose], tax-deductible"

> "Record expense: Mailchimp, $13, March 1, email marketing, yes"

### Monthly Snapshot
> "Financial snapshot for [month]" or "How did March go financially?"

Agent generates:
```
## March 2026 P&L

Income:       $1,247.00
Expenses:     $  182.50
Net Income:   $1,064.50

Revenue Goal Progress: $1,247 / $5,000 (24.9%) ← behind pace
Expense vs Budget:     $182.50 / $500 (36.5%) ✅ on track
Tax Reserve:           ~$319 set aside (30% of $1,064 net)

⚠️ Flag: Revenue concentration — 73% from one source (services)
```

### YTD Summary
> "Year-to-date financial summary" or "How's 2026 going financially?"

### Revenue Goal Check
> "Am I on track to hit my revenue goal this month?"

### Tax Estimate
> "What should I be setting aside for quarterly taxes?"

Agent calculates rough self-employment tax based on YTD net income and your configured rate.

### Expense Review
> "What did I spend money on this month?" or "What are my recurring expenses?"

### Income Breakdown
> "Break down my income sources for this quarter"

---

## Monthly P&L Format

Your agent appends a monthly summary to `monthly-summary.md` at the end of each month (or on demand):

```markdown
## March 2026

**Income**
| Source | Amount |
|--------|--------|
| Digital products | $587.00 |
| Services | $660.00 |
| **Total Income** | **$1,247.00** |

**Expenses**
| Category | Amount |
|----------|--------|
| Tools/software | $68.00 |
| Platform fees | $78.50 |
| Education | $36.00 |
| **Total Expenses** | **$182.50** |

**Net Income:** $1,064.50
**vs. Monthly Target ($5,000):** 21.3% — below target
**Tax Reserve (30%):** ~$319

**Flags:**
- ⚠️ Revenue below target by $3,752
- ✅ Expenses within budget
- ⚠️ Income concentration: 53% from services (single-source risk)

---
```

---

## Cash Flow Flags

Your agent automatically raises these warnings during any snapshot:

| Flag | Trigger | Why It Matters |
|------|---------|----------------|
| ⚠️ Revenue Below Pace | < 50% of monthly target by mid-month | You may fall short — act now |
| ⚠️ Income Concentration | 1 source > 60% of income | Client/product loss = big problem |
| ⚠️ Expense Spike | Month expenses > 120% of prior month | Something changed — review it |
| ⚠️ No Income Logged | 7+ days with zero entries | Activity may have stalled |
| 🔴 Negative Month | Net income < $0 | Expenses exceeded revenue |
| ✅ Goal Hit | Revenue ≥ monthly target | Celebrate, then plan the next |

---

## Tax Estimate Tracking

Your agent maintains a rough quarterly tax ledger in `tax-estimates.md`:

```markdown
# Tax Estimates

> ⚠️ Rough estimates only — not tax advice. Consult a professional.

## 2026

| Quarter | Net Income | Estimated Tax (30%) | Due Date | Status |
|---------|------------|---------------------|----------|--------|
| Q1 (Jan–Mar) | $0 | $0 | April 15 | — |
| Q2 (Apr–Jun) | — | — | June 15 | — |
| Q3 (Jul–Sep) | — | — | Sept 15 | — |
| Q4 (Oct–Dec) | — | — | Jan 15 | — |
```

Tell your agent: "Update my Q1 tax estimate" and it recalculates based on logged net income.

---

## AGENTS.md Standing Instructions

Add this to your `AGENTS.md` so your agent always knows its financial role:

```markdown
## Financial Tracking

I maintain a `finance/` directory with income and expense logs. When I mention revenue, sales, or spending:
- Log income entries to `finance/income-log.md`
- Log expense entries to `finance/expense-log.md`
- Update `finance/finance-state.json` YTD totals after each entry
- Never auto-send financial summaries externally
- Flag if monthly revenue is below 50% of target by mid-month
- Remind me at month-end to close the books and generate a P&L summary
```

---

## Customization

### Adjust Income Categories
In `income-log.md`, replace or add category labels to match your business model. No code changes needed — just use your own labels consistently.

### Multiple Revenue Streams
If you have separate businesses or products, add a `stream` column:

```markdown
| Date | Source | Amount | Category | Stream | Notes |
|------|--------|--------|----------|--------|-------|
| 2026-03-05 | Gumroad | $49 | digital | guide-sales | — |
| 2026-03-05 | Etsy | $12 | digital | cards | — |
```

Tell your agent: "Break down income by stream this month."

### Currency
All entries default to USD. To use a different currency, tell your agent:
> "Use [EUR/GBP/CAD/etc.] for all financial tracking."

It will note the currency in file headers.

### Monthly Recurring Expenses
For recurring subscriptions, tell your agent:
> "Add a recurring expense: [vendor], $[amount], [day of month], [purpose], [tax-deductible]"

Your agent will remind you to log it each month and flag if it goes missing.

### Income Alerts
Set a target and ask your agent to alert you via heartbeat when you hit milestones:

```markdown
## HEARTBEAT.md (finance section)
- Check finance/income-log.md — has monthly income crossed $1,000? $3,000? $5,000? 
  If a new milestone crossed, surface it in the briefing.
```

---

## Integration With Other Agent Ledger Skills

| Skill | How It Connects |
|-------|----------------|
| **Solopreneur Assistant** | Financial snapshot feeds into weekly business review |
| **Goal Tracker** | Revenue goals tracked as KRs; financial-tracker provides actual numbers |
| **Project Tracker** | Link projects to expected revenue; log actual vs projected |
| **Content Calendar** | Track revenue from content-driven products (newsletters, guides) |
| **Decision Log** | Log financial decisions (price changes, tool cuts, new investments) |
| **CRM** | Connect client deals in the pipeline to income logged when closed |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Agent logs income but doesn't update YTD | Ask: "Update finance-state.json YTD totals based on income-log.md" |
| Numbers don't match expectations | Ask: "Recount income-log.md for [month] — show me each entry" |
| Agent generates wrong month | Specify explicitly: "March 2026 P&L" |
| Tax estimate seems wrong | Check your `tax_rate_estimate` in finance-state.json; adjust if needed |
| Agent forgot the finance directory | Re-deliver this skill and say "Set up the finance directory" |

---

## Privacy Note

All financial data is stored locally in your workspace. This skill does not transmit data externally. Do not store account numbers, full credit card numbers, or banking credentials in any finance file — use only the amounts and vendors needed for business tracking.

---

*Financial Tracker v1.0.0 — by [The Agent Ledger](https://www.theagentledger.com)*
*Free to use under [CC-BY-NC-4.0](https://creativecommons.org/licenses/by-nc/4.0/). Subscribe at theagentledger.com for premium guides and advanced blueprints.*

> ⚠️ **Disclaimer:** This skill is for organizational tracking purposes only. Nothing in this skill constitutes financial, tax, legal, or investment advice. Always consult qualified professionals for your specific situation.
