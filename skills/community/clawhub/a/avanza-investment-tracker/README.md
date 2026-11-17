# Investment Tracker

## Description

This project aims to create a tool for tracking stocks and investments on investment platforms. The original idea for this project was when I was about to buy a SteamDeck. Then I thought better of it and started to wonder how much the money would grow over time if I invested it instead. I realized that it would require me to keep track of the assets that I purchase a particular month, even if I sell them and buy new ones later on. Or if I get dividends and reinvest them.

With this project, I am able to parse data from my investment platform, keep latest asset values up to date and calculate relevant statistics.

This project is a work in progress and will be updated as I go along.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage) — includes [Network access and privacy](#network-access-and-privacy)
- [CLI Reference](#cli-reference)
- [Virtual Portfolios](#virtual-portfolios)
- [Special Cases](#special-cases)
- [Contributing](#contributing)
- [License](#license)

## Features

- Parse and store data from an investment platform.
- Keep track of where money invested each month is moved and grown over time.
- **Per-account statistics**: Calculate gains/losses for each account separately, then merge for combined views
- Calculate statistics for months and years:
    - Deposit
    - Withdrawal
    - Current Value
    - Total Gain/Loss
    - Realized Gain/Loss
    - Unrealized Gain/Loss
    - APY (Annual Percentage Yield)
- Two viewing modes:
    - **Period-specific**: Track performance of investments made in each month/year
    - **Accumulated**: See total portfolio value over time with assets carried forward
- **Account filtering**: View statistics for any combination of accounts with full accumulated history support
- **System status**: Check database statistics, price freshness, and transaction date range
- **Virtual portfolios**: Track sub-portfolios (e.g. strategy sleeves) separately with allocation, transfers, and virtual-vs-parent performance comparison
- **Risk metrics**: Optional risk/beta calculations against a benchmark (fetches policy rates and benchmark prices from Riksbanken/Yahoo Finance)
- **Reporting**: Investment report command with a virtual-portfolio section and benchmark comparison
- **Safety rails**: Destructive commands (`reset --hard`, `delete-tx`, `account delete`) require confirmation and write an automatic timestamped `.bak` backup first

## Installation

1. Clone the repository.
2. Install the dependencies with `pip install -r requirements.txt`.

## Quick Start

```bash
# 1. Import your transaction data
python cli.py import data/your_transactions.csv

# 2. Get statistics with automatic price updates
python cli.py stats --update-prices auto --period year --deposits all

# 3. Check system status anytime
python cli.py status

# 4. (Optional) Set default accounts for filtering
python cli.py settings default-accounts "account1,savings_account"

# 5. (Optional) Set account nicknames for readability
python cli.py account nickname 1234567 "Savings"

# 6. View account summaries
python cli.py accounts --update-prices auto
```

## Usage

### Network access and privacy

By default this tool is not fully offline. Be aware of outbound requests:

- **Avanza public API** — live price/FX lookups send the asset names and currency pairs from your portfolio (this is how `--update-prices auto` works). Use `--update-prices never` to keep it fully offline (cached prices only).
- **Riksbanken API and Yahoo Finance** — only contacted for risk metrics (`--risk`, `--beta`) to fetch policy rates and benchmark prices; this sends the benchmark ticker and date range, not your holdings.

### Command Line Interface (CLI)

A unified CLI is available via `cli.py`. It provides subcommands for all major operations:

#### Modern Workflow (Recommended)

```bash
# Import CSV data and process transactions in one atomic operation
python cli.py import data/transactions.csv

# Show statistics with smart updates (auto-updates prices if stale)
python cli.py stats --update-prices auto --period year --deposits all

# Check system status (transactions, prices, metadata)
python cli.py status

# Reset database state (mark all transactions as unprocessed)
python cli.py reset

# Hard reset (delete all transactions, stats, and prices while keeping configuration)
# WARNING: irreversible — permanently deletes all financial history in the database. Back it up first.
python cli.py reset --hard
```

> **Irreversible operations.** `reset --hard`, `delete-tx`, `account allocate --undo`, and
> `account delete` permanently remove data and rebuild derived tables. There is no undo.
> Back up the database before running them, and prefer `--dry-run` where available
> (e.g. `delete-tx --dry-run`) to preview the blast radius. Avoid broad selectors like
> `delete-tx --since` unless you are certain what they will remove.
>
> Since the audit-hardening update, `reset --hard`, `delete-tx`, and `account delete`
> additionally: (1) ask for confirmation — interactively via a y/N prompt, and in
> non-interactive shells (agents, cron, scripts) only run when `--yes` is passed —
> and (2) automatically copy the database to a timestamped
> `<db>.pre-<command>.<YYYYMMDD-HHMMSS>.bak` file before making any changes.
> Backup files are never cleaned up automatically — delete them yourself once you are
> satisfied the operation went well (and consider adding `*.bak` to your `.gitignore` if
> the database lives in a git repo).

All commands accept optional `--database` and `--special-cases` arguments to override default paths:

```bash
python cli.py --database path/to/db.db --special-cases path/to/special.json import data.csv
```

#### Smart Update Features

The new `stats` command includes intelligent caching and update logic:

- **Price freshness**: Prices are considered "fresh" if updated within 1 day
- **Price interpolation**: Historical valuations automatically interpolate missing asset prices linearly between nearest known dates (e.g. from transaction purchases or API price updates).
  - Use `--no-interpolation` to disable this behavior and fall back to the closest prior price.
- **Auto-update**: `--update-prices auto` updates only if prices are stale
- **Force update**: `--update-prices always` forces price refresh
- **Skip update**: `--update-prices never` uses cached prices
- **Stats caching**: Statistics are recalculated only when needed (new transactions or price updates)
- **Default period**: You can set a default stats cohort period.
  ```bash
  # Set default stats period
  python cli.py settings default-stats-period year

  # Use the default stats period
  python cli.py stats
  ```


#### Account Nicknames

Assign human-readable names to account numbers for easier identification:

```bash
# Set a nickname for an account
python cli.py account nickname 1234567 "Savings"

# List all nicknames
python cli.py account nickname --list

# Remove a nickname
python cli.py account nickname --remove 1234567
```

Nicknames are stored in the database and displayed in the `accounts` command output alongside account numbers.

#### Account Filtering

The CLI supports filtering statistics by account with the `--account` flag. Statistics are calculated per-account for accuracy, then merged when viewing multiple accounts:

```bash
# Show stats for all accounts (default)
python cli.py stats --account all

# Show stats using default accounts set via settings
python cli.py stats --account default

# Show stats for specific accounts (comma-separated)
python cli.py stats --account "account1,savings_account"

# Accumulated statistics now work with any account combination
python cli.py stats --account "account1" --accumulated
```

Set default accounts for filtering:
```bash
# Set default accounts
python cli.py settings default-accounts "account1,savings_account"

# Reset to include all accounts
python cli.py settings default-accounts all
```

View account summaries with cash and asset values:
```bash
# Show all accounts
python cli.py accounts --update-prices auto

# Filter accounts (same syntax as stats command)
python cli.py accounts --account default

# View portfolio snapshot for specific accounts
python cli.py portfolio --account "account1,savings_account"

# Compare portfolio values for a specific account over a period
python cli.py portfolio --account "account1" --start-date 2026-06-29 --end-date 2026-07-06
```

Output format for `accounts` command:
```
Account                Cash (SEK) Assets (SEK)  Total (SEK)
--------------------------------------------------------
account1                        0       100000       100000
savings_account             50000            0        50000
--------------------------------------------------------
TOTAL                       50000       100000       150000
```

Output format for `portfolio` command (single account):
```
Account account1 (Account Nickname)
Deposits: 100,000 SEK
Withdrawals: 0 SEK
Net invested: 100,000 SEK
Current value: 105,000 SEK
Total gain: +5,000 SEK (+5.0%)
APY: 10.2% (MWRR)

  Holdings:
    Fund Name              Market Value    Allocation
    Asset A                 80,000 SEK         76.2%
    Asset B                 25,000 SEK         23.8%
  Total                    105,000 SEK        100.0%
```

With `--format json`, the single-account output includes a `holdings` list:
```json
{
  "account": "account1",
  "display_name": "Account Nickname",
  "deposits": 100000.0,
  "withdrawals": 0.0,
  "net_invested": 100000.0,
  "current_value": 105000.0,
  "total_gain": 5000.0,
  "total_gain_percent": 5.0,
  "apy": 10.2,
  "apy_mode": "mwrr",
  "holdings": [
    {
      "asset": "Asset A",
      "amount": 80.0,
      "price": 1000.0,
      "market_value": 80000.0,
      "allocation_percent": 76.19
    },
    {
      "asset": "Asset B",
      "amount": 25.0,
      "price": 1000.0,
      "market_value": 25000.0,
      "allocation_percent": 23.81
    }
  ]
}
```


### Understanding Statistics Output

The statistics output has two modes that serve different purposes:

#### 1. Regular Statistics (Default)
```bash
python cli.py stats --period month
```
- **Shows**: Activity for each specific month/year
- **"Value" column**: Current value of deposits made **during that specific period**
- **If zero deposits in a period**: Value = 0 (by definition)
- **If everything withdrawn**: Value = 0 (deposits fully withdrawn)
- **Use case**: Track performance of investments made in each period

#### 2. Accumulated Statistics
```bash
python cli.py stats --period month --accumulated
```
- **Shows**: Cumulative portfolio value over time
- **"Value" column**: Total portfolio value at period end (all assets held)
- **Carries forward**: Assets from earlier periods continue to appear
- **Use case**: See total portfolio growth over time

#### 3. APY Calculation Modes

You can specify the method used to calculate APY using the `--apy-mode` argument (supported by `stats` and `portfolio` commands):
- `--apy-mode mwrr` (default): Money-Weighted Rate of Return. This is implemented using the **Modified Dietz** method. It accounts for the timing and size of all cash flows (deposits and withdrawals) in the period.
- `--apy-mode twrr`: Time-Weighted Rate of Return. This measures pure investment performance independent of cash flow timing.

#### Example
**January 2024:**
- Deposit: 10,000 SEK
- Buy Asset A: 10,000 SEK
- Current price of Asset A: 12,000 SEK

**February 2024:**
- No deposits/withdrawals
- Asset A still held (worth 12,000 SEK)

**Regular stats show:**
- January: Value = 12,000 SEK (value of January deposit)
- February: Value = 0 (no February deposits)

**Accumulated stats show:**
- January: Value = 12,000 SEK
- February: Value = 12,000 SEK (asset carried forward)

### CSV Format Support

The parser automatically detects whether your CSV file uses Avanza's old or new export format (the new format includes a `Transaktionsvaluta` column). The following transaction types are recognized:

- Insättning (deposit)
- Uttag (withdrawal)
- Köp (purchase)
- Sälj (sale)
- Utdelning (dividend)
- Räntor / Ränta / Inlåningsränta (interest)
- Utländsk källskatt / Prelskatt / Preliminärskatt (taxes)
- Byte / Övrigt (listing changes)
- Tillgångsinsättning (asset deposit)

Empty numeric fields (like `Antal`, `Kurs`) are treated as zero.

**Asset name normalization:** Instrument names are trimmed of leading/trailing whitespace on import — Avanza exports occasionally include stray trailing spaces that would otherwise break exact-name lookups (e.g. `account allocate`). Any pre-existing names are normalized automatically the next time the database is opened.

**Unsettled trades (pending nota):** When you export on the same day as a non-SEK securities trade, Avanza includes preliminary rows whose brokerage (`Courtage`) and FX rate (`Valutakurs`) are not yet finalized. The importer detects these (non-SEK buy/sell with empty `Courtage` and `Valutakurs`) and defers them — it logs a warning per skipped row and leaves them out of the database. Re-export after the trade settles and re-import. Pass `import --allow-unsettled` to override and ingest them anyway.

**Price fetching note:** The `stats` command (with `--update-prices auto` or `--update-prices always`) fetches current asset prices from Avanza's public search API (`www.avanza.se/_api/search/filtered-search`). This API is intended for web frontend use and may have rate limits or terms of service restrictions. Use at your own risk and consider using official APIs if available. Always review the website's terms of service before using their data.

### Using the CLI (Recommended)

The unified CLI provides all functionality in a streamlined interface:

1. Add transaction data in CSV format to the `data` folder.
    - You might need to create a "special_cases.json" file in order to match and replace certain values in the data. See file specification in the documentation for the SpecialCases class.
2. Import and process transactions: `python cli.py import data/your_transactions.csv`
3. View statistics with automatic price updates: `python cli.py stats --update-prices auto`
4. (Optional) Set default accounts for filtering: `python cli.py settings default-accounts "account1,savings_account"`
5. (Optional) Set account nicknames: `python cli.py account nickname 1234567 "Savings"`
6. View account summaries: `python cli.py accounts --update-prices auto`
7. View portfolio snapshot or compare change over a period (equivalent to `stats --positions --summary`):
    - Snapshot: `python cli.py portfolio [--as-of YYYY-MM-DD]`
    - Period comparison: `python cli.py portfolio --start YYYY-MM-DD [--end YYYY-MM-DD]`
8. Check system status: `python cli.py status`

Note: All valuation commands (`stats`, `accounts`, `portfolio`) accept a `--format json` flag to return data in machine-readable JSON format instead of a plain-text table/block.

**Advanced usage with account filtering:**
```bash
# Show stats for specific accounts
python cli.py stats --account "account1" --update-prices auto

# Show accumulated stats for any account combination
python cli.py stats --account "account1" --accumulated --update-prices auto
python cli.py stats --account "account1,savings_account" --accumulated --update-prices auto

# Compare different account combinations
python cli.py accounts --account "account1"
python cli.py accounts --account "savings_account"
python cli.py accounts --account all

# Show portfolio snapshot as of a previous date
python cli.py portfolio --as-of 2026-07-06

# Compare portfolio values between two dates
python cli.py portfolio --start 2026-06-29 --end 2026-07-06

# Show portfolio snapshot with Money-Weighted Rate of Return (MWRR) APY
python cli.py portfolio --account "account1"

# Show portfolio snapshot using Time-Weighted Rate of Return (TWRR) APY
python cli.py portfolio --account "account1" --apy-mode twrr

```

## CLI Reference

| Command | Description |
| :--- | :--- |
| `python scripts/cli.py import FILE [--allocate-virtual] [--allow-unsettled]` | Import transaction entries from Avanza CSV (auto-allocate buys to virtuals; defers unsettled/pending-nota trades — see CSV Format Support) |
| `python scripts/cli.py stats [OPTIONS]` | Calculate and display cohort performance statistics (TWRR, deposits) |
| `python scripts/cli.py accounts [OPTIONS]` | Display summary of all accounts with asset values and cash |
| `python scripts/cli.py portfolio [OPTIONS]` | Show portfolio holdings, market value, allocation %, and APY (alias to `stats --positions --summary`) |
| `python scripts/cli.py status` | Display system status (transaction counts, price dates, date range) |
| `python scripts/cli.py settings SUBCOMMAND` | Configure defaults and account nicknames |
| `python scripts/cli.py reset [--hard] [--yes]` | Reset database state (`--hard` deletes data; default only marks unprocessed). `--hard` prompts for confirmation (or requires `--yes` non-interactively) and writes an automatic timestamped `.bak` backup first |
| `python scripts/cli.py delete-tx [OPTIONS]` | Delete individual transaction(s) by `--tx-id`, `--date`+`--asset`, or `--since`, then rebuild derived tables (see below). Prompts for confirmation unless `--dry-run` or `--yes` is used; writes an automatic timestamped `.bak` backup first |
| `python scripts/cli.py account SUBCOMMAND` | Manage accounts — virtual sub-portfolios (create/allocate/transfer/list/close/delete) and nicknames (see below) |
| `python scripts/cli.py report [OPTIONS]` | Investment report with a virtual-portfolio section and a virtual-vs-parent-vs-benchmark comparison |

### Deleting transactions

> **Irreversible.** `delete-tx` permanently removes the matched transactions and rebuilds
> derived tables — there is no undo. Back up the database first and use `--dry-run` to
> preview, especially with broad selectors like `--since`.

`delete-tx` removes specific real transactions and rebuilds the derived `assets` / cohort tables, so there is no need to `reset` the whole database after a bad import (e.g. a duplicate, or a row that slipped in before an unsettled trade was deferred). Targeting is mutually exclusive:

- `delete-tx --tx-id ROWID` — most precise (use `status`/`export` to find the rowid).
- `delete-tx --date YYYY-MM-DD --asset "Name" [--account ACCOUNT]` — the common surgical case.
- `delete-tx --since YYYY-MM-DD [--account ACCOUNT]` — remove everything from a date onward (e.g. undo today's import).

`--cascade` widens a `--date`+`--asset` match across the account family (parent + its virtuals) so a trade and its allocated split are removed together; `--dry-run` previews the deletion; `--yes` skips the confirmation prompt (required when running non-interactively, e.g. from an agent or script — the command refuses with exit code 1 otherwise). A timestamped `<db>.pre-delete-tx.<YYYYMMDD-HHMMSS>.bak` backup is written before any rows are deleted. When an allocated buy on a virtual is deleted, its orphaned funding `Intern överföring` transfer is removed automatically (mirroring `account allocate --undo`). After every deletion all transactions are reprocessed, so the `assets`/cohort tables always reflect the remaining transactions — never a half-deleted state.

### Global Options
- `--database PATH` (default: `data/asset_data.db`)
- `--special-cases PATH` (default: `data/special_cases.json`)

### Calculation & Output Options
- `--account ACCOUNTS`: Limit to specific accounts (e.g. `12345,67890`, `default`, or `all`). Omitting the flag (default) shows **physical accounts only** (excludes virtual portfolios); pass `all` to include virtual portfolios in aggregates.
- `--update-prices {auto,always,never}` (stats only): Controls when to fetch latest stock/fund prices from Avanza API
- `--update-all` (stats only): Update prices for all assets in the database, held or not
- `--as-of DATE`: View snapshot/stats as of a historical date (`YYYY-MM-DD`)
- `--cohorts-start DATE --cohorts-end DATE`: Filter which deposit cohorts are displayed
- `--cohort DATE`: Shorthand to filter by a single cohort month (`YYYY-MM`) or year (`YYYY`) (e.g. `--cohort 2024` groups yearly, `--cohort 2024-12` groups monthly)
- `--from DATE --to DATE`: Set the performance valuation window (double snapshot)
- `--positions`, `-p` (stats only): Show positions holdings breakdown under each cohort (or summary)
- `--summary`, `-s` (stats only): Consolidate cohort statistics into a single overview block
- `--apy-mode {mwrr,twrr}`: APY calculation method (`mwrr` uses Modified Dietz; `twrr` uses Time-Weighted)
- `--format {table,json}`: Output formatting (default: `table`)
- `--quiet`, `-q`: Suppress price data staleness warnings
- `--no-interpolation`: Disable linear interpolation for sparse historical price data (falls back to nearest prior price, which may trigger staleness warnings)
- `--risk`: Calculate and display portfolio-level risk metrics (Annualized Standard Deviation, Sharpe Ratio, Sortino Ratio, Maximum Drawdown with peak/trough calendar months)
- `--beta [TICKER]`: Include the portfolio Beta calculation vs the specified benchmark (e.g. `^OMXSPI`, `ACWI`). Defaults to `^OMXSPI` if the flag is passed without a ticker value. Specifying `--beta` automatically enables risk metrics.

### Guidelines: When to use what date boundaries
1. **To see how cohorts from a certain period look today:**
   Use `--cohorts-start YYYY-MM` / `--cohorts-end YYYY-MM`
   *Example:* `python scripts/cli.py stats --cohorts-start 2024-01`
2. **To see all cohorts' performance over a specific valuation window:**
   Use `--from YYYY-MM` / `--to YYYY-MM` (or `--as-of YYYY-MM`)
   *Example:* `python scripts/cli.py stats --from 2024-01 --to 2024-12`
3. **To see only a single cohort month or year:**
   Use `--cohort YYYY-MM` or `--cohort YYYY`
   *Example:* `python scripts/cli.py stats --cohort 2024-12` (sets date range to `2024-12` and default grouping to monthly)
   *Example:* `python scripts/cli.py stats --cohort 2024` (sets date range to `2024-01` to `2024-12` and default grouping to yearly)

> [!NOTE]
> In double-snapshot mode (`--from` / `--to`), the cohort-level output displays **`Start Value`** instead of **`Deposited`** for any cohorts created before the start date. Additionally, the **`Withdrawal`** line displays withdrawals made *specifically within the selected date range*, while withdrawals made prior to the start date are already accounted for in `Start Value`.

### Settings Subcommands
- `default-accounts ACCOUNTS`: Set default accounts (comma-separated list of IDs, or `all`)
- `default-stats-period {month,year}`: Set default period for performance reports

## Virtual Portfolios

Virtual portfolios let you track sub-strategies (e.g. "YOLO bets", "long-term holds") *within* a single physical Avanza account. A virtual portfolio is just another account in the database (`is_virtual = 1`, linked to a parent). Because shares are **reassigned** (not copied) to the virtual account, every share and every SEK lives on exactly one account at a time — aggregates do not double count.

All account management — sub-portfolios **and** nicknames — lives under the `account` command.

### Commands

```bash
# Create a virtual sub-portfolio under a physical parent (optionally fund it)
python cli.py account create --name "YOLO" --parent 1234567 [--starting-cash 5000 --starting-cash-date 2026-07-19]

# Allocate an imported transaction (full, or partial via --shares)
python cli.py account allocate --tx-date 2026-07-19 --tx-asset "Some Meme Stock" --to "YOLO" [--shares 50]

# Move cash between accounts
python cli.py account transfer-cash --amount 10000 --from 1234567 --to "YOLO" --date 2026-07-19

# Move an asset position between accounts
python cli.py account transfer --asset "Tesla" --shares 50 --from "YOLO" --to 1234567 --date 2026-09-01

# List virtual sub-portfolios with current value and APY
python cli.py account list [--apy-mode twrr] [--format json]

# Close a sub-portfolio: move all holdings + residual cash back to its parent
python cli.py account close --name "YOLO" --date 2026-09-01

# Account nicknames (moved here from `settings account-nickname`)
python cli.py account nickname 1234567 "Main"
python cli.py account nickname --list
python cli.py account nickname --remove 1234567
```

### How it works

- **`allocate`** moves a transaction (or splits it) onto the virtual account. Moving a buy transfers only the **shortfall** — if the virtual already has capital (e.g. from a prior sell), that cash is used and no transfer is needed. Partial splits proportionally divide `total` and `courtage`.
- **`allocate --to <parent>`** (undo) moves a transaction back from a virtual to the parent and **deletes** the funding transfer pair that was created during the original allocation. No compensating transactions are created. Requires `--from <virtual>`. Partial undo (`--shares`) is not supported.
- **`transfer`** (asset move) is represented internally as a sell on the source → cash transfer → rebuy on the destination (all tagged as synthetic). This composes the existing transaction handlers and is correct on every statistics path. The **source realizes its gain** up to the transfer and the **destination gets a fresh cost basis** at the transfer price — an honest "this position left / entered the strategy" bookkeeping.
- **`close`** moves every holding (via the same decomposition) plus any residual cash back to the parent, then reprocesses. The virtual account row is **preserved** (kept `is_virtual = 1`) so its historical cohort/performance data remains queryable; it simply ends up empty.
- **`delete`** is a clean teardown: reverts all real transactions back to the parent, removes every synthetic transaction tied to the virtual (including partner legs on other accounts), and deletes the account row. Unlike `close`, it leaves no trace — use it to correct a mistake rather than wind down a strategy. **Irreversible:** the virtual's historical performance data is lost on delete; use `close` instead if you want to preserve queryable history. Requires confirmation (y/N prompt, or `--yes` for non-interactive use) and writes an automatic timestamped `.bak` backup of the database before any changes.
- After every `account` mutation the cohort tables are rebuilt automatically (same reprocessing as an import).

### Viewing virtual portfolios

- `accounts` shows a hierarchical tree: each physical account lists its combined value (self + its virtual children), with the children indented and marked `[V]`. The `TOTAL` row sums physical rows only (children are a breakdown, so nothing is double counted).
- `stats` / `portfolio` default to **physical accounts only**. Pass `--account all` to include virtual portfolios, or `--account "YOLO"` to view a single virtual portfolio.

### SQL views (for dashboards / reports)

The SQLite database exposes virtual-portfolio-aware views that Grafana panels, weekly reports, or ad-hoc queries can consume directly. All views are recreated on every connect, so they always reflect the current schema.

| View | One row per | Key columns |
| :--- | :--- | :--- |
| `v_account_current_valuations` | account | `account`, `is_virtual`, `parent_account`, `display_name`, `cash`, `assets`, `total` |
| `v_account_asset_holdings` | (account, asset) | `account`, `is_virtual`, `parent_account`, `asset_name`, `held_amount` |
| `v_virtual_portfolio_rollup` | **physical** account | `parent_account`, `own_total`, `virtual_total`, `combined_total`, `virtual_count` (+ own/virtual/combined cash & assets) |
| `v_external_capital_flows` | capital-flow transaction | `date`, `account`, `transaction_type`, `origin`, `flow_amount` |

`is_virtual`/`parent_account` let you group or filter (e.g. physical-only with `WHERE is_virtual = 0`, or hierarchy with `GROUP BY parent_account`). The rollup view gives the "main account including its virtuals" total with no double counting — `combined_total = own_total + virtual_total`. The flows view's `origin` (`'avanza'` vs `'virtual'`) lets you exclude internal virtual transfers when computing real money in/out.

```sql
-- Physical accounts with their virtual sub-portfolios rolled in:
SELECT parent_display_name, own_total, virtual_total, combined_total
FROM v_virtual_portfolio_rollup;

-- Current holdings grouped by parent family:
SELECT COALESCE(parent_account, account) AS family, asset_name, SUM(held_amount)
FROM v_account_asset_holdings GROUP BY family, asset_name;
```

### Reporting

```bash
# Full report: overview + accounts hierarchy + virtual section + comparison
python cli.py report --update-prices auto

# Add a benchmark to the performance comparison (annualized over portfolio lifetime)
python cli.py report --benchmark ^OMXSPI

# Machine-readable
python cli.py report --format json
```

The `report` command shows the total portfolio value (physical own + virtual),
per-account and per-virtual APY, each virtual's share of its parent's combined
value, and a comparison table of physical / virtual / benchmark returns. It
reuses the stats engine for APY and Yahoo Finance (when `--benchmark` is given)
for the benchmark period return.

### Limitations

- **Sells and dividends are auto-routed.** When an imported sell or dividend arrives on an account that does not hold the asset (because the shares were allocated to a virtual), `import` automatically redistributes it to the account(s) that hold the shares, so reprocessing never aborts and income is attributed correctly:
  - **Sells**: drain the sell's own account first, then the largest related virtual holder; full reassignment when the own account holds none, proportional split when it holds some but not enough. Multi-holder cases route to the largest with a warning.
  - **Dividends**: split proportionally across every holder so each account is credited for the shares it actually holds.
  - This runs only when virtual portfolios exist (no-op otherwise).
- **Buys can be auto-allocated with `import --allocate-virtual`.** When a buy on a parent account cannot be funded (because cash is stranded in a virtual from a prior sell), the flag applies heuristics to assign it to the right virtual:
  1. A virtual that **both holds the asset and can fund the buy** → allocate there (largest holder if multiple, with a warning).
  2. A **new asset** (nobody holds it) and exactly one virtual can fund → allocate there.
  3. Everything else → left on the parent with a warning for manual allocation.
  - "Can fund" means the virtual's capital plus the parent's remaining capital covers the buy cost. The shortfall is transferred from the parent.
  - If a heuristic allocation is wrong, undo it with `account allocate --to <parent> --from <virtual>`.
- Funding a virtual requires the source account to hold enough capital at the transfer date.

## Special Cases

Corporate actions (splits, spin-offs, zero-priced deposits) can be overridden by copying the template and defining rules:
```bash
cp assets/special_cases_template.json ../data/avanza/special_cases.json
```

## Contributing

Thank you for your interest in contributing to this project! As a single-person hobby project, contributions are not expected but always welcome. If you have any ideas, bug fixes, or improvements, feel free to submit a pull request.

To contribute to this project, please follow these guidelines:

1. Fork the repository and create a new branch for your contribution.
2. Make your changes and ensure that the code is clean and well-documented.
3. Test your changes thoroughly to ensure they do not introduce any regressions.
4. Submit a pull request, explaining the purpose and details of your contribution.

Please note that as a hobby project, there may be limited resources available for reviewing and merging pull requests. Your patience is appreciated.

Thank you for your support and happy coding!

## License

Please make sure that you are allowed to access information from the price source that you are using. The author of this project is not responsible for any legal issues that may arise from the use of this project. The url used in the example script is only for demonstration purposes and should not be used without permission.

The code in this project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

Please note that this project uses other libraries. The licenses for these libraries are as follows:

- Libraries in `requirements.txt`:
  - requests: Apache License 2.0


Please respect the licenses for these libraries when using this project.