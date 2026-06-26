---
name: expense-tracker
description: Track and analyze personal expenses from receipts, bank statements, or manual input. Use when the user wants to: scan receipts (photos/PDFs), categorize spending, track budgets, generate expense reports, analyze spending patterns, or log transactions. Triggers on "track expenses", "receipt scan", "spending report", "budget tracker", "expense log", "where did my money go".
---

# Expense Tracker

Track, categorize, and analyze personal/business expenses.

## Quick Start

Log a transaction:
```bash
python3 scripts/expense.py add --amount 45.99 --category food --desc "Grocery run" --date 2026-03-31
```

Scan a receipt image:
```bash
python3 scripts/expense.py scan receipt.jpg
```

View reports:
```bash
python3 scripts/expense.py report --period month    # this month
python3 scripts/expense.py report --period week     # this week
python3 scripts/expense.py report --category food   # food spending
python3 scripts/expense.py report --budget           # budget vs actual
```

## Commands

| Command | Description |
|---------|-------------|
| `add` | Add a manual transaction |
| `scan` | OCR a receipt image and extract items |
| `import` | Import CSV bank statement |
| `report` | Generate spending reports |
| `budget` | Set/view monthly budgets by category |
| `categories` | List or edit categories |
| `export` | Export data as CSV |

## Receipt Scanning

The `scan` command uses OCR to extract:
- Merchant name
- Date
- Line items with prices
- Total amount

Extracted items are auto-categorized using keyword matching (see references/categories.md for rules).

## Data Storage

All data stored in `~/.expense-tracker/`:
- `transactions.json` — all transactions
- `budgets.json` — monthly budget limits
- `categories.json` — custom categories and rules

## Report Formats

Reports show:
- Total spent per category (bar chart ASCII)
- Month-over-month comparison
- Budget utilization percentage
- Top merchants by spend
- Daily/weekly spending trend

## CSV Import

Import bank statements (auto-detects columns):
```bash
python3 scripts/expense.py import bank_export.csv --date-col Date --amount-col Amount --desc-col Description
```
