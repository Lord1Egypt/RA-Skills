# cashbook

> Local-first personal bookkeeping Skill for OpenClaw. Supports natural language & screenshot-based expense recording, budget tracking, and financial reports. All data stored locally in SQLite — zero cloud dependency.

## Features

✅ **Natural Language Recording** — "Spent $38 on coffee today" → auto-parse amount, category, account  
✅ **Screenshot Recording** — Upload Alipay/WeChat/POS receipt screenshots, auto-extract fields  
✅ **Account Management** — Debit cards, credit cards, e-wallets with automatic balance tracking  
✅ **Budget Tracking** — Set monthly limits per category or total, with overspend alerts  
✅ **Weekly & Monthly Reports** — Spending breakdown, category distribution, budget progress  
✅ **CSV Import** — Batch import Alipay/WeChat transaction history with auto-categorization  
✅ **Multi-language** — Chinese, English, and Japanese category aliases supported  
✅ **Local-first** — SQLite single-file storage, full data ownership, export anytime  

## Install

```bash
clawhub install cashbook
```

No manual setup needed — the database initializes automatically on first use.

## Quick Start

### Record an expense
```
You: Spent 68 on groceries at Walmart
Bot: ✅ Recorded: Expense ¥68.00 / Shopping / Default Wallet / 2026-03-16
```

### Set a budget
```
You: Set monthly food budget to 2000
Bot: ✅ Set 餐饮 monthly budget ¥2,000.00

You: How much food budget left this month?
Bot: Monthly food budget: ¥2,000.00
    Spent: ¥1,234.00 (61.7%)
    Remaining: ¥766.00
    Status: On track ✅
```

### Screenshot recording
Upload a payment screenshot → auto-extract amount/merchant/date → confirm → recorded

### Monthly report
```
You: Generate monthly report
Bot: 📊 March 2026 Report
    Total Expenses: ¥4,567.00    Total Income: ¥15,000.00
    
    Expense Breakdown:
      1. Food       ¥1,234.00  27.0%  █████░░░░
      2. Transport   ¥890.00   19.5%  ████░░░░░
      ...
```

## Supported Languages

| Language | Example | Category Mapping |
|----------|---------|-----------------|
| Chinese | "今天咖啡花了38" | 餐饮 (native) |
| English | "Spent 38 on coffee" | food → 餐饮 |
| Japanese | "食費 38円" | 食費 → 餐饮 |

## File Structure

```
cashbook/
├── SKILL.md                 # Skill instructions
├── references/              # Reference docs
│   ├── schema.md           # Data model
│   ├── account.md          # Account management guide
│   └── budget.md           # Budget management guide
└── scripts/                # Python scripts
    ├── db.py               # Database module (auto-init)
    ├── init.py             # Manual initialization
    ├── add_tx.py           # Record transaction
    ├── delete_tx.py        # Delete transaction
    ├── account.py          # Account CRUD
    ├── category.py         # Category management
    ├── budget.py           # Budget management
    ├── query.py            # Query transactions
    ├── report.py           # Weekly/monthly reports
    ├── import_csv.py       # CSV import (Alipay/WeChat)
    └── export.py           # Data export
```

## Tech Stack

- **Language**: Python 3 (standard library only, zero dependencies)
- **Storage**: SQLite (local single-file)
- **Data Path**: `~/.local/share/cashbook/cashbook.db`
- **Override**: Set `CASHBOOK_DB` environment variable

## Data Security

- ✅ 100% local storage, no cloud sync
- ✅ Only stores card nicknames and last 4 digits (no full card numbers or passwords)
- ✅ Export to CSV/JSON anytime
- ✅ Custom database path supported

## Preset Categories

**Expenses**: Food, Transport, Shopping, Entertainment, Medical, Housing, Education, Travel, Other  
**Income**: Salary, Bonus, Freelance, Other

Custom categories supported via `scripts/category.py add`.

## License

MIT
