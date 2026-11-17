---
name: financial-categorizer
description: "Process bank transaction CSV exports (Nordea, ICA), auto-categorize transactions using configurable rules, manage transaction links, and generate analytical database views."
metadata:
  openclaw:
    requires:
      bins:
        - python3
---


# financial-categorizer

Process bank transaction CSV exports, auto-categorize transactions using configurable rules, manage transaction links, and generate analytical SQLite database views.

## Quick Start

Run the CLI tool from your terminal pointing to your database path:

```bash
# 1. Add your main checking account
python cli.py --db ../data/finance.db add-account "Nordea Checking" --type tracked --ownership 1.0

# 2. Add hierarchical categories
python cli.py --db ../data/finance.db add-category "Food"
python cli.py --db ../data/finance.db add-category "Groceries" --parent 1

# 3. Add auto-categorization rules
python cli.py --db ../data/finance.db add-rule 2 "ICA MAXI" --type contains
python cli.py --db ../data/finance.db add-rule 1 "^Hyra" --type regex

# 4. Import transactions from a bank CSV file
python cli.py --db ../data/finance.db import transactions.csv --account "Nordea Checking"

# 5. Run auto-categorization over uncategorized transactions
python cli.py --db ../data/finance.db categorize

# 6. View monthly summary statistics
python cli.py --db ../data/finance.db stats-summary
```

## Data Storage Pattern

**User data lives OUTSIDE the skill directory.** Recommended structure:

```
workspace-finance/
├── skills/financial-categorizer/   # Portable skill (shareable)
│   ├── SKILL.md
│   ├── cli.py
│   ├── setup.py
│   └── financial_categorizer/
└── data/                           # Your private data
    ├── finance.db
    └── exports/
        ├── Nordea_Checking.csv
        └── ICA_Shared.csv
```

The skill provides logic. Your data stays private and portable.

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
- `cleanup-pending [--yes] [--dry-run] [--force-id <id>...]`
- `remove-transfer-rule <id> [--yes]`
- `auto-link [--yes] [--dry-run]`


## CLI Reference

| Command | Description |
|---------|-------------|
| `import <files>` | Import bank CSV transactions |
| `accounts` | List all registered bank accounts |
| `add-account <name>` | Create a new bank account |
| `update-account <id>` | Update account ownership ratio, type, name, etc. |
| `delete-account <id> [--yes]` | Delete a bank account (requires confirmation or `-y`) |
| `categories` | List all categories in tree view |
| `add-category <name> [--associated-account <name_or_id>]` | Create a new category, optionally associated with an external account |
| `update-category <id> [--associated-account <name_or_id>]` | Update category parents or fields (use `none` to clear association) |
| `delete-category <id> [--yes]` | Delete a category (requires confirmation or `-y`) |
| `rules [txn_id]` | List all match rules, or show the matching rule for a specific transaction |
| `add-rule <cat_id> <pattern>` | Add a categorization rule (regex, contains, exact) |
| `remove-rule <id> [--yes]` | Remove an auto-categorization rule (requires confirmation or `-y`) |
| `preview <pattern>` | Preview which transactions match a pattern before adding a rule |
| `categorize [--all]` | Run auto-categorization rules |
| `uncategorized [--group] [--non-zero] [--net | --unsplit]` | List all uncategorized transactions (supports `--net` or `--unsplit`) |
| `transactions [--category <name>] [--uncategorized] [--non-zero] [--account <name>] [--limit <n>] [--net | --unsplit]` | Search, list, and filter transactions (supports `--net` or `--unsplit`) |
| `manual-match <txn_id> <cat_id>` | Manually assign a category override to a transaction |
| `manual-unmatch <txn_id>` | Remove a manual categorization override |
| `stats-summary [--month <YYYY-MM>] [--period-type <type>] [--unsplit | --gross]` | Monthly summary of income, expenses, and net (supports `--unsplit` or `--gross`) |
| `stats-category <name> [--month <YYYY-MM>] [--from <date>] [--to <date>] [--period-type <type>] [--unsplit | --gross]` | Category total with subcategory rollups (supports `--unsplit` or `--gross`) |
| `stats-trend <name> [--from <date>] [--to <date>] [--period-type <type>] [--unsplit | --gross]` | Monthly trend for a category (supports `--unsplit` or `--gross`) |
| `stats-top [--month <YYYY-MM>] [--limit <n>] [--period-type <type>] [--unsplit | --gross]` | Top spending categories sorted by total expenses (supports `--unsplit` or `--gross`) |
| `stats-transfers [--month <YYYY-MM>] [--period-type <type>] [--unsplit | --gross]` | Net capital transfers to external accounts (supports `--unsplit` or `--gross`) |
| `stats-compare [--month <YYYY-MM>] [--period-type <type>] [--unsplit | --gross]` | Month-over-month comparison (supports `--unsplit` or `--gross`) |
| `stats-cashflow [--month <YYYY-MM>] [--period-type <type>] [--unsplit | --gross]` | Monthly cash flow summary (Operating, Transfers, Net; supports `--unsplit` or `--gross`) |
| `link <from_id> [to_id] --type [--to-account <name_or_id>] [--ratio <val> \| --ratio-to <val> \| --amount <val>] [--dry-run]` | Link transactions (specify `--to-account` for external transfers, or ratio/amount options to customize values; `--dry-run` to preview) |
| `unlink <id> [--yes]` | Remove a link (requires confirmation or `-y`) |
| `links` | List all transaction links |
| `auto-link [--dry-run] [--yes]` | Auto-detect and link internal transfers using transfer rules (requires confirmation or `-y` when not running dry-run) |
| `recalculate` | Manually recalculate adjusted amounts for all transactions |
| `db-cleanup [--dry-run] [--yes]` | Purge orphaned transaction links and rules (Integrity Cleanup) (requires confirmation or `-y` when not running dry-run) |
| `cleanup-pending [--dry-run] [--yes] [--force-id <id>...]` | Delete ghost pending reservations whose settled counterpart already exists (individual, split-authorization, or inexact amount matches — e.g. merchants that authorize a buffer and settle a different final amount; inexact matches fire only when unambiguous). Unresolved pendings are kept, listed with nearby same-merchant candidates, flagged as probable cancellations when old with no counterpart, and can be deleted explicitly via `--force-id` (requires confirmation or `-y` when not running dry-run) |
| `remove-transfer-rule <id> [--yes]` | Remove a transfer detection rule (requires confirmation or `-y`) |
| `salary-config` | Show current salary period configuration |
| `set-salary-mode <mode>` | Set the salary period mode (`calendar`, `fixed`, `salary`) |
| `set-salary-day <day>` | Set the fixed boundary day of the month (1-28) |
| `set-salary-category <name>` | Set the category name used to scan for salary paydays |
| `recurring [--status <active|cancelled|all>]` | List recurring payments configurations |
| `add-recurring <name> <pattern> [options] [--dry-run]` | Manually create a recurring payment config and link transactions |
| `update-recurring <id> [options] [--dry-run]` | Update recurring config fields and re-run transaction linking |
| `remove-recurring <id> [--hard] [--date <YYYY-MM-DD>] [--yes]` | Cancel (soft-close with end date) or hard-delete a recurring payment configuration (requires confirmation; use `--yes`/`-y` to bypass, mandatory in non-interactive mode) |
| `discover-recurring [--dry-run] [--yes]` | Auto-discover recurring transaction patterns and auto-close dead configurations (saving, re-linking, and auto-closing require confirmation; use `--yes`/`-y` to bypass, mandatory in non-interactive mode — run `--dry-run` first to preview) |
| `stats-recurring [query] [--month <YYYY-MM>] [--period-type <type>]` | Display subscription stats dashboard or detail reports for matching subscriptions |
| `estimate-period [--days <int>] [--level <0|1|2>]` | Project spending and estimate total outflow remaining in current period (rollup levels: 0=none, 1=top, 2=detailed) |
| `set-estimate-level <0|1|2>` | Set default category rollup level configuration for spending estimation |





## Configuring Salary Periods

By default, the salary period boundary is fixed to the 25th of the month. You can customize this grouping behavior using the salary configuration commands.

### Available Modes:
1. **`calendar`**: Group transactions by calendar months (1st to the last day).
2. **`fixed`**: Group transactions by a static day of the month (e.g., the 25th). Transactions on or after this day are grouped into the next month's period.
3. **`salary`**: Group transactions by automatically detecting the primary salary deposit date in each month (the transaction under the salary category with the largest positive amount).

### CLI Configuration Commands:
```bash
# View current configuration
python cli.py salary-config

# Change mode to salary (automatic payday detection)
python cli.py set-salary-mode salary

# Set the category name used to search for paydays (default is "Salary")
python cli.py set-salary-category "Salary"

# Change mode to a fixed day of the month (e.g. 27th)
python cli.py set-salary-mode fixed
python cli.py set-salary-day 27
```

> [!WARNING]
> If you choose the **`fixed`** day mode, be aware that bank deposits and transactions can shift early or late due to weekends and holidays.
> - Ensure your fixed day is configured early or late enough so that fluctuations in actual payday do not cause two salary deposits to fall into the same period (which would result in one month showing double income and the next showing zero income).
> - Alternatively, use the **`salary`** mode, which automatically detects the actual deposit transaction dates and shifts the boundaries dynamically.

### Querying Statistics by Salary Period
All statistics and breakdown commands support the `--period-type` parameter:
* `calendar` — Force standard calendar month boundaries.
* `salary` — Force salary period boundaries (using the active `salary-config` settings).
* `default` — Dynamically resolve to your active `salary-config` mode:
  - If mode is `calendar`, defaults to calendar months.
  - If mode is `fixed` or `salary`, defaults to salary periods.

For example, to query your housing category spending using the active salary period:
```bash
python cli.py stats-category Housing --period-type salary --month 2026-06
```

If you do not specify a `--period-type` flag, it will automatically default to the setting configured via `set-salary-mode`.

## Tracking Recurring Payments & Subscriptions

This tool supports advanced, automated tracking and lifecycle management of recurring payments (e.g. Netflix, Spotify, broadband, utility bills) and income (e.g. Salary).

### Core Concepts

1. **Recurring Payments Table (`recurring_payments`)**
   Defines the rules, intervals, expected days, amount ranges, and lifespans for each recurring item.
2. **Subscription Lifecycle & Runs**
   Resumed subscriptions (after cancellation) are tracked as separate runs/rows in `recurring_payments`.
   * **Resumption**: If a transaction matches a pattern of a cancelled subscription (after its `end_date`), it automatically spawns a new run/configuration for the resumption.
   * **Auto-Closing**: Active configurations that are missing expected payments are automatically closed (`end_date` is set to the last matched payment date) when running `discover-recurring` or passing the `--close` flag to `import` / `categorize`.
   * **Confirmation Gates**: `remove-recurring` and `discover-recurring` (without `--dry-run`) prompt for confirmation before making changes, like the other destructive commands. Use `--yes`/`-y` to bypass (mandatory in non-interactive mode), and `discover-recurring --dry-run` to preview first.
3. **Flexible Date Intervals**
   Supports strict date/day checking with a configured tolerance window:
   * **Monthly**: Expected day of month (e.g. 25th, last day `-1`).
   * **Weekly**: Expected weekday.
   * **Yearly**: Expected month and day.
   * **Days**: Custom interval (e.g. every 90 days).
   * **Tolerance**: Tolerates shifts due to weekends/holidays (default 4 days).

### Common Workflows

#### 1. Auto-Discover Recurring Candidates
Scan transaction history to auto-identify recurring items (such as monthly subscriptions or utility bills) and automatically save them:
```bash
# Preview candidates without writing to the database
python cli.py discover-recurring --dry-run

# Run auto-discovery and save configurations (prompts for confirmation; --yes to bypass)
python cli.py discover-recurring --yes
```

#### 2. Manually Add/Update Configurations
```bash
# Add a monthly Netflix subscription
python cli.py add-recurring Netflix "netflix.com" --amount-min -149 --amount-max -189 --interval monthly --day-of-month 6 --category Media

# Dry-run update previewing matches
python cli.py update-recurring 1 --amount-max -219 --dry-run
```

#### 3. View Outflow Dashboard & Stats
```bash
# Active subscriptions monthly cost summary and expected next dates
python cli.py stats-recurring

# Detailed subscription history across active/cancelled runs and transaction lists
python cli.py stats-recurring "Disney Plus"
```

## Common Workflows


### Handling Shared-Expense Reimbursements

If you make a shared purchase (e.g., from the `Gemensamt` account, 50% ownership) and get reimbursed by an external person (e.g., via Swish to your `Personligt` account, 100% ownership) and subsequently transfer the payback to the shared account:

1. **Reimburse the shared expense**: Link the reimbursement transaction (the Swish inflow) directly to the original expense transaction (the shared purchase):
   ```bash
   python cli.py --db data/finance.db link <swish_transaction_id> <expense_transaction_id> --type reimbursement --ratio 1.0
   ```
   * *Effect*: The Swish transaction is fully neutralized to `0.00` adjusted amount, and the credit to the expense transaction is automatically scaled by the shared account's ownership ratio (e.g., 50%), reducing your net cost correctly.
   * *Note*: The credit is scaled by the target account's ownership ratio (e.g., 50%) because the benefit of the payback is shared between the joint account owners.

2. **Link the account transfer**: Link the outflow from your main account to the inflow on your joint account as an internal transfer:
   ```bash
   python cli.py --db data/finance.db link <transfer_out_id> <transfer_in_id> --type internal_transfer
   ```
   * *Effect*: Both sides of the transfer are neutralized to `0.00`, ensuring no false income or outflows are recorded.
    * *Note*: This step is skipped if the transfer has already been auto-linked.

### Managing Pending Reimbursements (Unlinked Inflows)

#### Option A: Flat List Workflow (Keeping Them Uncategorized)
Use the `--non-zero` flag on the `uncategorized` command to show pending actions (positive inflows to link, negative expenses to categorize):
```bash
python cli.py uncategorized --non-zero
```

#### Option B: Dedicated Category Workflow (Filtering Positive Inflows Only)
To auto-route only positive inflows (like Swish reimbursements) to a category (e.g., ID `9`) while leaving negative outflows uncategorized, add a rule with a minimum amount filter:
```bash
python cli.py add-rule 9 "Swish" --type contains --amount-min 0.01
```

Query unlinked/pending reimbursements using:
```bash
python cli.py transactions --category Reimbursements --non-zero
```
*(Once linked, the adjusted amount drops to `0.00` and the transaction disappears from both lists).*

### How to Think About Reimbursements & Composite Transactions

When working with transaction links, it is crucial to distinguish between the **raw bank ledger amount** (actual cash flow) and the **effective category/budgetary amount** (represented by the `adjusted_amount` column).

#### The Core Principle
Reimbursements are not new income; they are a return of capital.
* If an expense is reimbursed, the net expense is zero.
* The incoming reimbursement money is not labor/investment income; it simply offsets the expense.

If you don't link them, your gross income and gross expenses will both be overstated by the reimbursement amount, distorting your reports.

#### Composite Transactions (e.g. Reimbursement Baked into Salary)
Often, a reimbursement is not a standalone transaction (like a Swish payment), but is packaged/baked into a larger composite transaction, such as a salary payment.
For example, if your employer pays you a single amount of `50,000 SEK`, which contains:
* `45,000 SEK` of actual labor income
* `5,000 SEK` of expense reimbursement for a credit card charge

To avoid distorting both income and expenses, you must split this composite transaction. In this system, you do this using **transaction links** with fractional ratios.

#### Link Ratio Calculation Modes
The `link` command provides three modes to simplify this:

1. **Source Ratio (`--ratio <float>`)** - *Default*
   Calculates the ratio relative to the source (`from_id`) transaction. Use when you want to allocate a direct fraction of the source.

2. **Destination Ratio (`--ratio-to <float>`)**
   Calculates the ratio relative to the destination (`to_id`) transaction.
   * For example, to fully reimburse/zero out the `First Card` expense of `-5,000 SEK` from your salary, use:
     ```bash
     python cli.py link <salary_txn_id> <expense_txn_id> --type reimbursement --ratio-to 1.0
     ```
   * This automatically calculates the exact ratio ($5000 / 50000 = 0.10$). It reduces the salary's `adjusted_amount` to `45,000 SEK` (reflecting your true labor income) and increases the credit card expense's `adjusted_amount` to `0.00 SEK` (reflecting your true net expense).

3. **Exact Cash (`--amount <float>`)**
   Specify the exact cash amount in SEK being reimbursed.
   * For example, to link exactly `5,000 SEK`:
     ```bash
     python cli.py link <salary_txn_id> <expense_txn_id> --type reimbursement --amount 5000
     ```


#### Dry-run Previews
Always run with the `--dry-run` flag first to preview the downstream `adjusted_amount` effects before committing changes to the database:
```bash
python cli.py link <from_id> <to_id> --type reimbursement --ratio-to 1.0 --dry-run
```

## Tracking External Accounts

You can track capital transfers from your tracked accounts to untracked external accounts (such as savings or stock brokerage accounts).

### Setup and Workflow:
1. **Create the External Account**:
   ```bash
   python cli.py add-account "Avanza Brokerage" --type external
   ```
2. **Associate a Category**:
   Create a category of type `transfer` associated with this external account:
   ```bash
   python cli.py add-category "Brokerage Transfer" --type transfer --associated-account "Avanza Brokerage"
   ```
3. **Add a Categorization Rule**:
   Add a match rule to auto-categorize transfers:
   ```bash
   python cli.py add-rule <category_id> "AVANZA" --type contains
   ```
4. **Auto-linking**:
   When transactions are categorized (via `categorize` or manual overrides), if they match a transfer category linked to an external account, an `external_transfer` link is created automatically.

### Manual Linking:
For one-off transfers, you can link a transaction directly to an external account:
```bash
python cli.py link <transaction_id> --type external_transfer --to-account "Avanza Brokerage"
```

### Querying Statistics:
Use the `stats-transfers` command to view net capital movements per external account:
```bash
python cli.py stats-transfers --month 2026-06
```

## Skill Contents

```
financial-categorizer/
├── SKILL.md                    # This file
├── requirements.txt            # pip dependencies
├── setup.py                    # setuptools configuration
├── cli.py                      # Main entrypoint
└── financial_categorizer/      # Package code
    ├── __init__.py
    ├── categorizer.py          # Auto-categorization & rule engine
    ├── db_handler.py           # Database CRUD & raw schema setup
    ├── importer.py             # CSV Parser (Nordea & ICA formats)
    ├── matching.py             # Shared matching helpers (diacritic folding, aggregate tolerance)
    └── stats.py                # SQL View registers and stats math
```

## SQLite Views

For analytical reporting (e.g. dashboards, Grafana), the following views are registered in the database:

1. **`v_effective_transactions`** — Joins transactions with accounts to factor in ownership ratios and transfer link adjustments. Includes `adjusted_amount`, `unsplit_amount`, and `raw_amount` columns.
2. **`v_monthly_summary`** — Calculates net income/expenses by month (includes unsplit and gross aggregations).
3. **`v_category_monthly`** — Calculates monthly spending by category (includes unsplit and gross aggregations).
4. **`v_daily_spending`** — Daily expense aggregation.
5. **`v_cumulative_spending_monthly`** — Running month-to-date daily cumulative spending.
6. **`v_daily_spending_moving_average`** — 30-day moving average of daily spending.
7. **`v_category_monthly_averages`** — Average monthly spending by category.
8. **`v_salary_period_summary`** — Expense/income summary grouped by salary periods (using the active salary config: fixed or salary).
9. **`v_breakout_categories`** — Groups monthly spending into high-level categories (Groceries, Loans, Housing, Leisure, Car, etc.).
10. **`v_uncategorized_groups`** — Groups uncategorized transactions by normalized Swish/Card payment descriptions to identify potential new rules.

---

## Querying Unmatched Reimbursements via CLI

Unmatched reimbursements (pending paybacks or refunds) are incoming transactions on tracked accounts that have not yet been neutralized by a transaction link. They can be queried and filtered using the CLI:

### Workflow:

1. **Query the transactions** depending on the categorization workflow in use:
   * **If using Uncategorized / Flat List (Option A)**:
     ```bash
     python cli.py uncategorized --non-zero
     ```
   * **If using a Dedicated Category (Option B)**:
     ```bash
     python cli.py transactions --category Reimbursements --non-zero --limit 100
     ```

2. **Identify candidates from the output**:
   * **Inflows**: Look for transactions with positive amounts (`amount > 0`).
   * **Regular Income Exclusions**: Filter out regular income sources (e.g., `"Lön"`, `"Salary"`, `"BARNBDR"`).
   * **Adjusted Amount**: Verify that the adjusted amount is non-zero (linked/neutralized transactions show `adjusted_amount = 0.00`).

### Example Filter Logic:
If the CLI output shows:
```
Transactions (4):
  [12] 2026-06-23   25000.00 SEK                      Personligt      [Uncategorized]     Lön
  [15] 2026-06-18    1250.00 SEK                      Personligt      [Uncategorized]     BARNBDR
  [18] 2026-06-16     500.00 SEK                      Personligt      [Uncategorized]     Swish inbetalning DOE, JOHN
  [21] 2026-05-20      50.00 SEK                      Personligt      [Uncategorized]     Swish inbetalning DOE, JOHN
```
* **Include**: `[18]` (+500.00) and `[21]` (+50.00) (positive Swish payments from an individual are reimbursement candidates).
* **Exclude**: `[12]` (Lön/Salary) and `[15]` (barnbidrag/regular benefit payment).


## Dependencies

- `pytest` - For testing suite
- Standard library modules: `sqlite3`, `csv`, `datetime`, `logging`, `re`, `argparse`, `os`

Install: `pip install -e .`
