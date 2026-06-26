---
name: compound
version: "1.0.0"
description: "Calculate compound interest and investment growth using financial formulas. Use when you need to plan savings, compare rates, or project wealth."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [finance, compound-interest, calculator, investment, savings, planning]
---

# Compound — Compound Interest Calculator

Compound is a command-line compound interest calculator that helps you plan investments, compare interest rates, build amortization schedules, and project financial growth over time.

All calculation history is stored in `~/.compound/data.jsonl` as JSONL records for future reference and comparison.

## Prerequisites

- Python 3.8+ with standard library
- `bash` shell

## Commands

### `calculate`
Calculate compound interest for a given principal, rate, and time period.

**Environment Variables:**
- `PRINCIPAL` (required) — Initial investment amount
- `RATE` (required) — Annual interest rate as percentage (e.g., 5.5)
- `YEARS` (required) — Number of years
- `FREQUENCY` — Compounding frequency: `daily`, `monthly`, `quarterly`, `annually` (default: monthly)
- `CONTRIBUTION` — Regular contribution amount (default: 0)
- `CONTRIB_FREQ` — Contribution frequency: `monthly`, `quarterly`, `annually` (default: monthly)

**Example:**
```bash
PRINCIPAL=10000 RATE=7.5 YEARS=20 FREQUENCY=monthly bash scripts/script.sh calculate
```

### `compare`
Compare multiple interest rate or compounding frequency scenarios side by side.

**Environment Variables:**
- `PRINCIPAL` (required) — Initial investment amount
- `RATES` (required) — Comma-separated list of rates to compare (e.g., "3,5,7,10")
- `YEARS` (required) — Number of years
- `FREQUENCY` — Compounding frequency (default: monthly)

### `schedule`
Generate a detailed payment/growth schedule showing balances at each period.

**Environment Variables:**
- `PRINCIPAL` (required) — Initial investment amount
- `RATE` (required) — Annual interest rate as percentage
- `YEARS` (required) — Number of years
- `FREQUENCY` — Compounding frequency (default: monthly)
- `CONTRIBUTION` — Regular contribution amount (default: 0)

### `table`
Display a year-by-year summary table of investment growth.

**Environment Variables:**
- `PRINCIPAL` (required) — Initial investment amount
- `RATE` (required) — Annual interest rate
- `YEARS` (required) — Number of years
- `CONTRIBUTION` — Regular contribution (default: 0)

### `rate`
Calculate the required interest rate to reach a financial goal.

**Environment Variables:**
- `PRINCIPAL` (required) — Starting amount
- `TARGET` (required) — Target amount
- `YEARS` (required) — Time period in years
- `FREQUENCY` — Compounding frequency (default: monthly)

### `goal`
Calculate how long it takes to reach a savings goal.

**Environment Variables:**
- `PRINCIPAL` (required) — Starting amount
- `TARGET` (required) — Goal amount
- `RATE` (required) — Annual interest rate
- `CONTRIBUTION` — Regular contribution (default: 0)

### `chart`
Generate an ASCII chart of investment growth over time.

**Environment Variables:**
- `PRINCIPAL` (required) — Initial amount
- `RATE` (required) — Annual interest rate
- `YEARS` (required) — Number of years
- `WIDTH` — Chart width in characters (default: 60)
- `HEIGHT` — Chart height in lines (default: 20)

### `export`
Export calculation history to a file.

**Environment Variables:**
- `OUTPUT` — Output file path (default: stdout)
- `FORMAT` — Export format: `json`, `csv`, `jsonl` (default: json)
- `CALC_ID` — Specific calculation ID to export (default: all)

### `config`
View or update default configuration settings.

**Environment Variables:**
- `KEY` — Configuration key to set
- `VALUE` — Configuration value

### `history`
View past calculations with their results.

**Environment Variables:**
- `LIMIT` — Maximum entries to display (default: 20)
- `SORT` — Sort by: `date`, `principal`, `rate`, `total` (default: date)

### `help`
Display usage information and available commands.

### `version`
Display the current version of the compound tool.

## Data Storage

All calculations are stored in `~/.compound/data.jsonl`. Each line is a JSON object with fields:
- `id` — Unique calculation identifier
- `timestamp` — ISO 8601 creation time
- `type` — Calculation type (calculate, compare, goal, etc.)
- `params` — Input parameters
- `result` — Calculation results (final amount, interest earned, etc.)

## Configuration

Config stored in `~/.compound/config.json`:
- `default_frequency` — Default compounding frequency (default: monthly)
- `currency_symbol` — Currency symbol for display (default: $)
- `decimal_places` — Number of decimal places (default: 2)

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
