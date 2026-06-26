---
name: doctorclaw-expense-tracker
description: "Expense tracker — log expenses, categorize by type, track against budget, flag overspending. Monthly cron or on-demand."
version: 1.0.0
tags: [expenses, finance, budget, tracking, automation]
metadata:
  clawdbot:
    emoji: "🧾"
source:
  author: DoctorClaw
  url: https://www.doctorclaw.ceo
---

# Expense Tracker

Know where your money goes. This skill logs your business expenses, categorizes them automatically, tracks spending against your budget, and flags when you're overspending in any category — so tax time is easy and budget surprises are rare.

Run it monthly for a full report, or log expenses on the fly throughout the month.

## What You Get

- Expenses logged and categorized by type (software, marketing, travel, meals, etc.)
- Budget tracking with real-time remaining balance per category
- Overspending alerts when you approach or exceed budget limits
- Monthly expense report with totals, trends, and top categories
- Tax-ready categorization for easy handoff to your accountant
- Receipt/note attachment for each expense entry

## Setup

### Required
- **Expense log** — A CSV file, Google Sheet, or any structured list your agent can read and write to. Columns: date, description, amount, category, notes.

### Optional (but recommended)
- **Budget file** — Monthly budget with limits per category (if not set, the agent will track without limits)
- **Bank/card integration** — connect to Plaid, bank CSV exports, or credit card statements for auto-import
- **Receipt storage** — folder for receipt photos/PDFs referenced by expense entries
- **Delivery channel** — Telegram/Discord for budget alerts and monthly reports

### Configuration

Tell your agent:

1. **Expense log location** — file path or Google Sheet URL
2. **Budget limits** — monthly budget per category (e.g., Software: $200, Marketing: $500)
3. **Categories** — your expense categories (defaults: Software/SaaS, Marketing, Travel, Meals, Office, Professional Services, Education, Miscellaneous)
4. **Alert threshold** — when to warn about overspending (default: 80% of category budget)
5. **Report schedule** — when to generate monthly report (default: 1st of each month)
6. **Currency** — your currency (default: USD)
7. **Tax categories** — map your categories to tax deduction types if needed

## How It Works

### Step 1: Log Expenses
When user says "log an expense" or provides expense info:
- Parse: amount, description, date (default: today), category (auto-detect or ask)
- Auto-categorize based on description keywords:
  - "Slack", "Notion", "AWS", "subscription" → Software/SaaS
  - "Facebook ads", "Google ads", "sponsorship" → Marketing
  - "flight", "hotel", "Uber", "gas" → Travel
  - "lunch", "dinner", "coffee", "restaurant" → Meals
  - "office supplies", "desk", "monitor" → Office
  - "lawyer", "accountant", "consultant" → Professional Services
  - "course", "book", "conference" → Education
- Append to expense log with timestamp
- Show running total for the category this month

### Step 2: Track Against Budget
For each category with a budget limit:
- Calculate: spent this month, remaining budget, percentage used
- If approaching threshold (80%): send a warning
- If exceeded: send an alert with amount over budget

### Step 3: Generate Monthly Report

```
🧾 Expense Report — [Month Year]

💵 MONTHLY SUMMARY
Total spent: $[X] | Budget: $[X] | Remaining: $[X]
[X]% of total budget used

📊 BY CATEGORY
| Category           | Spent    | Budget   | Remaining | Status |
|---|---|---|---|---|
| Software/SaaS      | $420     | $500     | $80       | 🟡 84% |
| Marketing          | $1,200   | $1,500   | $300      | 🟡 80% |
| Travel             | $350     | $400     | $50       | 🟡 88% |
| Meals              | $180     | $300     | $120      | 🟢 60% |
| Office             | $0       | $200     | $200      | 🟢 0%  |
| Professional Svcs  | $500     | $500     | $0        | 🔴 100%|
| Education          | $49      | $200     | $151      | 🟢 25% |
| Miscellaneous      | $75      | $100     | $25       | 🟡 75% |

⚠️ ALERTS
• Professional Services at 100% — $500 of $500 used
• Travel at 88% — only $50 remaining
• Software approaching limit — $80 remaining

📋 TOP EXPENSES THIS MONTH
1. Marketing consultant — $500 (Professional Svcs)
2. Facebook Ads — $600 (Marketing)
3. Google Ads — $400 (Marketing)
4. Flight to NYC — $280 (Travel)
5. Annual Notion plan — $120 (Software)

📈 TRENDS
• Spending is [up/down] [X]% vs last month
• Largest increase: [category] (+$[X])
• Under budget in [X] of [X] categories
```

### Step 4: Deliver & Archive
- Send monthly report via configured channel
- Save to `memory/expenses/YYYY-MM.md` for historical reference
- Export expense data in CSV format for accountant if requested

## Examples

**User:** "Log $49 for Notion annual plan"

**Agent:**
> Logged: $49.00 — Notion annual plan
> Category: Software/SaaS (auto-detected)
> Software budget: $420 of $500 used (84%) — $80 remaining

**User:** "How am I doing on my budget this month?"

**Agent runs the report and responds with the full monthly summary.**

**User:** "Export my expenses for tax prep"

**Agent:** Exports a CSV with all expenses categorized by tax deduction type, ready for the accountant.

---

**User:** "Set up monthly expense reports on the 1st"

**Agent:** Configures cron for the 1st of each month at 9:00 AM, confirms:
> "Monthly expense report scheduled for the 1st of each month. I'll summarize your spending, flag any overages, and send it to your Telegram."

## Customization Ideas

- **Receipt OCR** — scan receipt photos and auto-extract amount, vendor, date
- **Recurring expense tracking** — auto-log subscriptions and recurring charges
- **Multi-currency support** — convert expenses in different currencies
- **Profit & loss** — combine with invoice tracker for a simple P&L statement
- **Quarterly tax estimates** — calculate estimated quarterly tax payments based on expenses
- **Team expense approval** — if you have employees, review and approve their expense submissions

## Want More?

This skill handles expense logging and budget tracking. But if you want:

- **Custom integrations** — connect to QuickBooks, Wave, Plaid, or your bank for automatic transaction import
- **Advanced automations** — auto-categorize from bank feeds, generate P&L statements, calculate tax estimates
- **Full system setup** — identity, memory, security, and 5 custom automations built specifically for your workflow

**DoctorClaw** sets up complete OpenClaw systems for businesses:

- **Guided Setup ($495)** — 2-hour live walkthrough. Everything configured, integrated, and running by the end of the call.
- **Done-For-You ($1,995)** — 7-day custom build. 5 automations, 3 integrations, full security, 30-day support. You do nothing except answer a short intake form.

→ [doctorclaw.ceo](https://www.doctorclaw.ceo)
