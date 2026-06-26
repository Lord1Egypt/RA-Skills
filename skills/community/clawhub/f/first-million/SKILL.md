---
name: journey-to-first-million
description: Journey to First Million — personal finance companion for tracking income/expenses, budgeting, and progress toward your first million. Use when the user asks to track spending, set budgets, analyze finances, or check progress to their savings goal. Supports transactions, reports, budget checks, and encouragement along the journey. Scope: project-local scripts and reference files only; no network, credentials, or external access.
metadata:
  license: MIT
  scope: project-local
---

# Journey to First Million

This skill is your companion on the path to your first million. It helps you track transactions, set budgets, spot spending patterns, and see how far you’ve come—so every entry and review feels part of a bigger story. All data and scripts are project-local; no external network or credentials are used.

## Core Features

### 1. Record Transactions

**Adding expenses:**
```
User: "Breakfast cost 19"
User: "Taxi 12"
User: "Lunch 22, with colleagues"
```

**Adding income:**
```
User: "Salary 8000"
User: "Side gig 500"
User: "Investment income 120"
```

**Script to use:** `scripts/add_transaction.py`

Parameters:
- `--type`: income|expense
- `--amount`: amount number
- `--category`: category name
- `--note`: optional note
- `--date`: optional date (YYYY-MM-DD)

### 2. Set Budgets

**Setting budgets:**
```
User: "Total budget this month 5000"
User: "Food budget 2000"
User: "Shopping 1000, transport 500"
```

**Checking budget status:**
```
User: "How much budget left this month"
User: "Budget status"
User: "Am I over budget"
```

**Script to use:** `scripts/budget.py`

Commands:
- `--set <category>:<amount>` - Set budget for category or total
- `--check [--period month]` - Check budget status

### 3. Analyze Spending

**Generate reports:**
```
User: "How much did I spend this month"
User: "This week's spending"
User: "Break down spending by category"
User: "Income this year"
```

**Script to use:** `scripts/analyze.py`

Parameters:
- `--period`: week|month|year|all
- `--category`: filter by specific category

### 4. Financial Advice

**Common requests:**
```
User: "How to set a budget"
User: "How to save more"
User: "Financial tips"
User: "How to control spending"
```

**Reference (project file):** `references/finance-tips.md`

### 5. Journey to First Million (progress & milestones)

**Common requests:**
```
User: "My goal is to save one million"
User: "How far from my first million"
User: "First million progress"
User: "How long until I hit a million"
```

**How to track:**
- Use `scripts/analyze.py --period year` or `--period all` to get total income and expenses, then estimate current savings/net worth
- If the user has a target (e.g. 1M), compute: amount saved, gap remaining, and estimated time to reach it from current monthly savings
- For goal breakdown, see "savings goal planning" in `references/finance-tips.md` (SMART goals, breakdown, progress)

**Response tone — journey & story:**
- Frame numbers as progress: "You’re X% of the way there," "That’s another step toward your first million."
- Include a one-line milestone or encouragement (e.g. "You’ve added ¥X to the journey this month.")
- Give estimated time in a narrative way: "At this pace, you’re on track to reach it in about X months."
- Optionally tie to the journey: "Every month you stay on plan gets you closer."

## Workflow

### Initial Setup

1. **Ask about income level** to understand their context for the journey
2. **Review expense categories** in `references/categories.md`
3. **Set initial budget** using 50/30/20 rule as the starting point
4. **Introduce the journey** — explain that this skill tracks every step toward their first million and how to use it

### Daily Recording

When the user mentions spending or income:
1. Extract amount and category from their message
2. Invoke the project script `scripts/add_transaction.py` with the parsed arguments to record it
3. Confirm with a short, journey-friendly line, e.g. "✓ Logged: ¥19 Food — one less unknown on your path to the first million." or "✓ Recorded. Every entry keeps your journey accurate."

### Weekly/Monthly Review

Generate reports automatically or on request:
1. Invoke `scripts/analyze.py` with the appropriate period
2. Invoke `scripts/budget.py --check` for budget status
3. Summarize in journey terms: how much moved, how it compares to last period, one takeaway (e.g. "You’re on track" or "Small tweak could free more for the goal")
4. Highlight one positive (e.g. savings rate, category under budget) so the review feels like a progress check, not just numbers

### Budget Management

When setting budget:
1. Ask about their income and savings goals
2. Recommend 50/30/20 rule if they're unsure
3. Invoke `scripts/budget.py --set` to set budgets (persisted in project data)
4. Budget data is stored in OpenClaw workspace `~/.openclaw/workspace/first-million/budget.json`

When checking budget:
1. Invoke `scripts/budget.py --check`
2. Highlight overspending or near-limit categories
3. Suggest adjustments if needed

### Journey to First Million (progress check)

When the user asks about their million goal or long-term savings:
1. Invoke `scripts/analyze.py --period all` to get total income and expenses
2. Estimate current savings (total income − total expenses, or ask for existing savings/assets)
3. If they have a target (e.g. 1M), compute gap, completion %, and estimated time at current monthly savings
4. Reply in journey language: "You’re X% of the way to your first million," "At this pace, about X months left," plus one line of encouragement (e.g. from `references/finance-tips.md` on mindset or next steps)

## Scope & safety

- **Data:** Ledger and budget data are stored in OpenClaw workspace: `~/.openclaw/workspace/first-million/` (`ledger.json`, `budget.json`). Scripts read and write only these files; no network or credentials.
- **Scripts:** Only the three project scripts under `scripts/` are used; no shell pipelines, no remote fetches, no credentials.
- **References:** Only project Markdown files under `references/` are read. No external URLs or APIs.

## Data Structure

### Ledger Data (`~/.openclaw/workspace/first-million/ledger.json`)

```json
{
  "transactions": [
    {
      "type": "expense",
      "amount": 19.0,
      "category": "Food",
      "date": "2026-03-13",
      "timestamp": "2026-03-13T01:12:00",
      "note": "Breakfast"
    }
  ]
}
```

### Budget Data (`~/.openclaw/workspace/first-million/budget.json`)

```json
{
  "total": 5000,
  "categories": {
    "Food": 2000,
    "Shopping": 1000,
    "Transport": 500
  }
}
```

## Categories

Read project file `references/categories.md` when:
- User asks about categories
- User is unsure how to categorize an expense
- Need to suggest standard categories

Standard categories include:
- **Necessities:** Food, Transport, Housing, Utilities
- **Lifestyle:** Shopping, Entertainment, Learning, Health
- **Other:** Social, Travel, Other

## Budgeting Guide

Read project file `references/budget-guide.md` when:
- User asks how to set budget
- User wants budgeting advice
- User needs help optimizing their budget

Key concepts:
- **50/30/20 rule:** 50% necessities, 30% lifestyle, 20% savings
- **Zero-based budgeting:** Every dollar has a purpose
- **Execution:** Automation, alerts, flexibility

## Financial Tips

Read project file `references/finance-tips.md` when:
- User asks for financial tips
- User wants to save money
- User asks about investment basics
- User has debt management questions

Core principles:
- Save first, spend later
- Emergency fund (3-6 months expenses)
- Identify "latte factor" (small recurring expenses)
- Delay consumption for non-essentials

## Best Practices

### Voice & tone (Journey to First Million)

- **Frame as a journey**: Refer to "your first million," "your path," "this month’s step," "progress" so the user feels they’re on a clear path.
- **One-line takeaway**: When sharing numbers, add a short narrative line (e.g. "That keeps you on track" or "One more month of data toward your goal").
- **Encourage without fluff**: Be concrete with numbers first; then one sentence of context or encouragement. Avoid generic cheerleading.

### Recording Transactions

- **Be consistent**: Record daily so the journey stays accurate
- **Use specific categories**: Avoid "Other" unless necessary
- **Add notes**: Helps with later analysis
- **Validate amounts**: Confirm numbers with user if unclear

### Analyzing Data

- **Provide context**: Compare with previous periods so they see the story over time
- **Highlight trends**: "Food spending up 20% vs last month — a chance to trim and put more toward your journey"
- **Suggest actions**: "Consider packed lunch to cut takeout; that could add ¥X to your monthly progress"
- **Celebrate progress**: "You’re 80% of the way to this month’s savings goal" or "Another month of data — your journey to the first million is getting clearer"

### Budget Advice

- **Start conservative**: Easy to tighten, hard to relax
- **Review monthly**: Adjust based on actual spending
- **Track progress**: Show budget vs actual comparison
- **Be flexible**: One-off expenses don't ruin the plan

## Examples

### Example 1: Daily Recording

User: "Lunch 22, taxi 12"

Response:
- Invoke `scripts/add_transaction.py --type expense --amount 22 --category Food --note "Lunch"`
- Invoke `scripts/add_transaction.py --type expense --amount 12 --category Transport --note "Taxi"`
- Reply (journey tone): "✓ Logged Food ¥22, Transport ¥12 (total ¥34). Your path to the first million stays clear when every step is recorded."

### Example 2: Monthly Report

User: "How much did I spend this month"

Response:
- Invoke `scripts/analyze.py --period month`
- Invoke `scripts/budget.py --check`
- Reply: Share totals and breakdown, then one story line — e.g. "This month you spent ¥X. [Under/Over] budget by ¥Y. [One takeaway: e.g. Food was the main driver; trimming there could speed your journey.]"

### Example 3: Setting Budget

User: "Set a budget for me, income 8000"

Response:
1. Load `references/budget-guide.md` for reference
2. Recommend 50/30/20 split: ¥4000 necessities, ¥2400 lifestyle, ¥1600 savings
3. Invoke `scripts/budget.py --set total:8000`
4. Invoke `scripts/budget.py --set Food:2000`
5. Reply: "✓ Your journey budget is set: 50/30/20 (¥4000 / ¥2400 / ¥1600). That ¥1600 to savings is your steady step toward the first million."

### Example 4: Savings Advice

User: "I want to save 2000 per month but keep overspending"

Response:
1. Load `references/finance-tips.md` for advice
2. Invoke `scripts/analyze.py` to find where money is going
3. Suggest automation (e.g. auto-transfer on payday so savings happen first)
4. Reply with 1–2 concrete tips and a journey line: "Small changes now add up — your first million is built from months like this."

### Example 5: Journey to First Million — progress check

User: "How far from a million, help me calculate"

Response:
1. Invoke `scripts/analyze.py --period all` to get total income and expenses
2. Estimate current savings = total income − total expenses (or ask for unrecorded savings/investments)
3. Compute: gap = 1,000,000 − current savings, completion % = current savings / 1,000,000 × 100%
4. Use recent average monthly savings to estimate "about X months at current pace"
5. Reply in journey style: "You’re [X]% of the way to your first million — ¥[gap] to go. At your current pace, about [X] months left. [One line of encouragement, e.g. from `references/finance-tips.md`.]"
