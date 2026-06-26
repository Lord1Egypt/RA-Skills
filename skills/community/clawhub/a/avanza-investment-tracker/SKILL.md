---
name: avanza-investment-tracker
description: "Process Avanza CSV exports, calculate TWRR/Modified Dietz returns, and track portfolio performance. Use when importing stock transactions, calculating investment returns, or managing portfolio data."
---

# Avanza Investment Tracker

Parse transaction CSVs and compute portfolio performance metrics.

## Quick Start

Run from skill root with data paths pointing to your workspace:

```bash
# Import transactions (data lives outside skill)
python scripts/cli.py import ../data/avanza/transactions.csv

# Calculate stats with auto price update
python scripts/cli.py stats --update-prices auto --database ../data/avanza/asset_data.db

# Or use defaults (assumes you cd into a data directory first)
cd ../data/avanza
python ../../skills/avanza-investment-tracker/scripts/cli.py import transactions.csv
```

## Data Storage Pattern

**User data lives OUTSIDE the skill directory.** Recommended structure:

```
workspace-finance/
├── skills/avanza-investment-tracker/   # Portable skill (shareable)
│   ├── SKILL.md
│   ├── scripts/
│   └── assets/
└── data/avanza/                        # Your private data
    ├── transactions.csv
    ├── special_cases.json
    └── asset_data.db
```

The skill provides logic. Your data stays private and portable.

## CLI Reference

| Command | Description |
|---------|-------------|
| `python scripts/cli.py import FILE` | Import transactions from CSV |
| `python scripts/cli.py stats` | Show performance stats |
| `python scripts/cli.py stats --update-prices auto` | Update prices, then show stats |
| `python scripts/cli.py accounts` | Show account summaries |
| `python scripts/cli.py status` | Check system status |
| `python scripts/cli.py reset --confirm` | Clear database (DESTRUCTIVE) |

All commands accept:
- `--database PATH` (default: `data/asset_data.db`)
- `--special-cases PATH` (default: `data/special_cases.json`)

## Skill Contents

```
avanza-investment-tracker/
├── SKILL.md              # This file
├── requirements.txt      # pip dependencies
├── assets/               # Templates (copy to your data dir)
│   └── special_cases_template.json
├── scripts/              # Python code
│   ├── cli.py           # Main CLI entry
│   ├── data_parser.py
│   ├── database_handler.py
│   └── calculate_stats.py
└── references/           # Detailed guides (loaded as needed)
    ├── workflows.md
    └── troubleshooting.md
```

## Dependencies

- `requests` - For fetching stock prices
- Standard library: `sqlite3`, `csv`, `json`, `datetime`, `argparse`

Install: `pip install -r requirements.txt`

## Special Cases

Corporate actions (splits, spin-offs) may need manual rules:

1. Copy template: `cp assets/special_cases_template.json ../data/avanza/special_cases.json`
2. Edit with your rules
3. Import with `--special-cases ../data/avanza/special_cases.json`

## See Also

- **Detailed workflows**: See [references/workflows.md](references/workflows.md)
- **Troubleshooting**: See [references/troubleshooting.md](references/troubleshooting.md)

## Account Filtering

By default, stats show all accounts. Use `settings default-accounts` to set your preferred accounts:

```bash
# Set default accounts (your main portfolio)
python scripts/cli.py --database ../data/avanza/asset_data.db settings default-accounts "1234567,Savings Account,9876543"

# View stats for default accounts only
python scripts/cli.py --database ../data/avanza/asset_data.db stats --account default

# Or specify accounts directly
python scripts/cli.py stats --account "1234567,Savings Account"

# View all accounts
python scripts/cli.py stats --account all
```
