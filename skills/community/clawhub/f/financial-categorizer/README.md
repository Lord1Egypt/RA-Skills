# financial-categorizer

Personal finance transaction categorization with a SQLite backend.

Imports bank CSV files, auto-categorizes transactions using configurable rules, and provides SQL views for dashboards and analysis.

## Features

- **Multi-account support** — tracked active accounts and external savings/investments with ownership ratios
- **Auto-categorization** — regex, exact, and contains match rules with priority ordering and manual overrides
- **Transaction linking** — mark transfers and reimbursements between transactions; adjusted amounts are pre-computed
- **SQL views** — ready-to-query views for monthly summaries, category breakdowns, and daily spending
- **CSV import** — auto-detects Nordea and ICA formats, handles pending transactions
- **CLI** — full command-line interface for all operations

## Install

```bash
pip install -e .
```

Requires Python 3.10+.

## Quick Start

```bash
# Import transactions from a CSV
financial-categorizer import transactions.csv --account "Nordea Checking"

# Add categorization rules
financial-categorizer add-rule 3 "ICA MAXI" --type contains
financial-categorizer add-rule 4 "^Hyra" --type regex

# Categorize uncategorized transactions
financial-categorizer categorize

# View stats
financial-categorizer stats-summary --month 2026-04
financial-categorizer stats-top --limit 10
financial-categorizer stats-category Food --month 2026-04

# Link a transfer between accounts
financial-categorizer link 1 2 --type internal_transfer

# Recalculate adjusted amounts
financial-categorizer recalculate
```

## Architecture

All data lives in a single SQLite database (`data/finance.db` by default).

### Core tables
- **accounts** — bank accounts with type and ownership ratio
- **transactions** — imported transactions with `adjusted_amount` (pre-computed)
- **categories** — hierarchical categories (parent/child)
- **match_rules** — patterns for auto-categorization
- **transaction_links** — connects transfers and reimbursements

### Views
- `v_effective_transactions` — all transactions with adjusted amounts
- `v_monthly_summary` — income, expenses, net per month
- `v_category_monthly` — category totals per month
- `v_daily_spending` — daily spending breakdown

### Adjusted amounts

`adjusted_amount` is a denormalized column on every transaction, pre-computed from:

1. `amount * account.ownership_ratio` (base)
2. Transaction link adjustments (transfers neutralize both sides, external transfers zero out)

Stats and views read this column directly — no JOINs at query time. Run `recalculate` to refresh after any manual changes.

## Security & Data Integrity

This tool modifies your local SQLite database. To prevent accidental data loss, please observe the following guidelines:

> [!WARNING]
> Always make a backup of your database before performing database cleanup, auto-linking, or destructive operations:
> ```bash
> # Simple file copy backup
> cp data/finance.db data/finance.db.bak
> 
> # Safe SQLite backup command
> sqlite3 data/finance.db ".backup data/finance.db.bak"
> ```

### Destructive Operations & Confirmation Prompts
Destructive commands require interactive confirmation `[y/N]` when run in a terminal (TTY). If you are running these commands in automated scripts or non-interactive shells, you must pass the `--yes` or `-y` flag to bypass the prompt; otherwise, the command will abort with an error.

The following commands require confirmation:
- `delete-account <id> [--yes]`
- `delete-category <id> [--yes] [--reassign <id>] [--force]`
- `remove-rule <id> [--yes]`
- `unlink <id> [--yes]`
- `db-cleanup [--yes] [--dry-run]`
- `remove-transfer-rule <id> [--yes]`
- `auto-link [--yes] [--dry-run]`

## CLI Reference

| Command | Description |
|---|---|
| `import <files>` | Import CSV transactions |
| `accounts` | List accounts |
| `add-account <name>` | Create an account |
| `update-account <id>` | Update account fields |
| `delete-account <id> [--yes]` | Delete an account (requires confirmation or `-y`) |
| `categories` | List categories (tree view) |
| `add-category <name> [--associated-account <name_or_id>]` | Create a category, optionally associated with an external account |
| `update-category <id> [--associated-account <name_or_id>]` | Update category fields (use `none` to clear association) |
| `delete-category <id> [--yes]` | Delete a category (requires confirmation or `-y`) |
| `rules [transaction_id]` | List match rules, or show the matching rule for a specific transaction |
| `add-rule <cat> <pattern>` | Add a categorization rule |
| `remove-rule <id> [--yes]` | Remove a rule (requires confirmation or `-y`) |
| `preview <pattern>` | Preview what a rule would match |
| `categorize [--all]` | Run auto-categorization |
| `uncategorized [--group] [--non-zero]` | Show uncategorized transactions |
| `transactions [--category <name>] [--uncategorized] [--non-zero] [--account <name>] [--limit <n>]` | Search and list transactions |
| `manual-match <txn> <cat>` | Manually assign a category |
| `manual-unmatch <txn>` | Remove a manual categorization override |
| `stats-summary [--period-type <type>]` | Monthly income/expenses/net |
| `stats-category <name> [--period-type <type>]` | Category total with subcategory rollup |
| `stats-trend <name> [--period-type <type>]` | Monthly breakdown for a category |
| `stats-top [--period-type <type>]` | Top spending categories |
| `stats-transfers [--month <YYYY-MM>] [--period-type <type>]` | Net capital transfers to external accounts |
| `stats-cashflow [--month <YYYY-MM>] [--period-type <type>]` | Monthly cash flow summary (Operating, Transfers, Net) |
| `link <from> [to] --type [--to-account <name_or_id>] [--ratio <val> \| --ratio-to <val> \| --amount <val>] [--dry-run]` | Link transactions (specify `--to-account` for external transfers, or ratio/amount options to customize values; `--dry-run` to preview) |
| `unlink <id> [--yes]` | Remove a link (requires confirmation or `-y`) |
| `links` | List transaction links |
| `auto-link [--dry-run] [--yes]` | Auto-detect and link internal transfers (requires confirmation or `-y` when not running dry-run) |
| `recalculate` | Refresh adjusted_amount |
| `db-cleanup [--dry-run] [--yes]` | Clean up orphaned database records (requires confirmation or `-y` when not running dry-run) |
| `remove-transfer-rule <id> [--yes]` | Remove a transfer detection rule (requires confirmation or `-y`) |
| `salary-config` | Show current salary period configuration |
| `set-salary-mode <mode>` | Set salary period mode (`calendar`, `fixed`, `salary`) |
| `set-salary-day <day>` | Set fixed boundary day of the month (1-28) |
| `set-salary-category <name>` | Set category name used to scan for salary paydays |

## Testing

```bash
pip install pytest
pytest tests/
```
