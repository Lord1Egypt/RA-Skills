# Investment Tracker

## Description

This project aims to create a tool for tracking stocks and investments on investment platforms. The original idea for this project was when I was about to buy a SteamDeck. Then I thought better of it and started to wonder how much the money would grow over time if I invested it instead. I realized that it would require me to keep track of the assets that I purchase a particular month, even if I sell them and buy new ones later on. Or if I get dividends and reinvest them.

With this project, I am able to parse data from my investment platform, keep latest asset values up to date and calculate relevant statistics.

This project is a work in progress and will be updated as I go along.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
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
python cli.py settings account-nickname 1234567 "Savings"

# 6. View account summaries
python cli.py accounts --update-prices auto
```

## Usage

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
```

All commands accept optional `--database` and `--special-cases` arguments to override default paths:

```bash
python cli.py --database path/to/db.db --special-cases path/to/special.json import data.csv
```

#### Smart Update Features

The new `stats` command includes intelligent caching and update logic:

- **Price freshness**: Prices are considered "fresh" if updated within 1 day
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
python cli.py settings account-nickname 1234567 "Savings"

# List all nicknames
python cli.py settings account-nickname --list

# Remove a nickname
python cli.py settings account-nickname --remove 1234567
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

**Price fetching note:** The `stats` command (with `--update-prices auto` or `--update-prices always`) fetches current asset prices from Avanza's public search API (`www.avanza.se/_api/search/filtered-search`). This API is intended for web frontend use and may have rate limits or terms of service restrictions. Use at your own risk and consider using official APIs if available. Always review the website's terms of service before using their data.

### Using the CLI (Recommended)

The unified CLI provides all functionality in a streamlined interface:

1. Add transaction data in CSV format to the `data` folder.
    - You might need to create a "special_cases.json" file in order to match and replace certain values in the data. See file specification in the documentation for the SpecialCases class.
2. Import and process transactions: `python cli.py import data/your_transactions.csv`
3. View statistics with automatic price updates: `python cli.py stats --update-prices auto`
4. (Optional) Set default accounts for filtering: `python cli.py settings default-accounts "account1,savings_account"`
5. (Optional) Set account nicknames: `python cli.py settings account-nickname 1234567 "Savings"`
6. View account summaries: `python cli.py accounts --update-prices auto`
7. Check system status: `python cli.py status`

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