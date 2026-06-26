---
name: generate
version: "1.0.0"
description: "Generate random test data including text, numbers, UUIDs, and structured formats. Use when creating mock datasets, sample records, or randomized test inputs."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# Generate — Universal Data Generator

A versatile CLI tool for generating random data of various types. Produce text, numbers, UUIDs, dates, names, emails, addresses, and structured formats like JSON and CSV for testing and development.

## Prerequisites

- Python 3.8+
- `bash` shell
- Write access to `~/.generate/`

## Data Storage

Generated data history is stored in JSONL format at `~/.generate/data.jsonl`. Each generation event is logged for reproducibility and batch export.

## Commands

Run commands via: `bash scripts/script.sh <command> [arguments...]`

### text

Generate random text strings: lorem ipsum, sentences, paragraphs, or custom patterns.

```bash
bash scripts/script.sh text --type lorem --words 50
bash scripts/script.sh text --type sentence --count 5
bash scripts/script.sh text --type paragraph --count 2
```

**Arguments:**
- `--type` — Text type: `lorem`, `sentence`, `paragraph`, `word` (optional, default: `lorem`)
- `--words` — Number of words for lorem (optional, default: 20)
- `--count` — Number of items to generate (optional, default: 1)

### number

Generate random numbers with configurable range and format.

```bash
bash scripts/script.sh number --min 1 --max 100
bash scripts/script.sh number --min 0.0 --max 1.0 --decimal 4
bash scripts/script.sh number --count 10 --min 1 --max 1000
```

**Arguments:**
- `--min` — Minimum value (optional, default: 0)
- `--max` — Maximum value (optional, default: 100)
- `--decimal` — Decimal places for float (optional, generates int if omitted)
- `--count` — How many numbers (optional, default: 1)

### uuid

Generate one or more UUIDs (v4).

```bash
bash scripts/script.sh uuid
bash scripts/script.sh uuid --count 5
bash scripts/script.sh uuid --format short
```

**Arguments:**
- `--count` — Number of UUIDs (optional, default: 1)
- `--format` — Format: `full`, `short` (8-char) (optional, default: `full`)

### date

Generate random dates within a range.

```bash
bash scripts/script.sh date --start 2020-01-01 --end 2025-12-31
bash scripts/script.sh date --count 10 --format iso
```

**Arguments:**
- `--start` — Start date YYYY-MM-DD (optional, default: 2020-01-01)
- `--end` — End date YYYY-MM-DD (optional, default: 2025-12-31)
- `--count` — Number of dates (optional, default: 1)
- `--format` — Date format: `iso`, `us`, `eu`, `unix` (optional, default: `iso`)

### name

Generate random person names.

```bash
bash scripts/script.sh name
bash scripts/script.sh name --count 10 --gender female
bash scripts/script.sh name --full
```

**Arguments:**
- `--count` — Number of names (optional, default: 1)
- `--gender` — Gender: `male`, `female`, `any` (optional, default: `any`)
- `--full` — Include last name (optional)

### email

Generate random email addresses.

```bash
bash scripts/script.sh email
bash scripts/script.sh email --count 5 --domain example.com
```

**Arguments:**
- `--count` — Number of emails (optional, default: 1)
- `--domain` — Email domain (optional, default: random)

### address

Generate random US-style addresses.

```bash
bash scripts/script.sh address
bash scripts/script.sh address --count 3
```

**Arguments:**
- `--count` — Number of addresses (optional, default: 1)

### json

Generate random JSON objects with a specified schema.

```bash
bash scripts/script.sh json --schema '{"name":"name","age":"int:18-65","email":"email"}'
bash scripts/script.sh json --schema '{"id":"uuid","score":"float:0-100"}' --count 5
```

**Arguments:**
- `--schema` — JSON schema definition (required)
- `--count` — Number of objects (optional, default: 1)

### csv

Generate random CSV data with headers.

```bash
bash scripts/script.sh csv --columns "name,email,age" --rows 20
bash scripts/script.sh csv --columns "id:uuid,name:name,score:float:0-100" --rows 50 --output data.csv
```

**Arguments:**
- `--columns` — Column definitions (required)
- `--rows` — Number of rows (optional, default: 10)
- `--output` — Output file (optional, default: stdout)

### password

Generate random passwords with configurable complexity.

```bash
bash scripts/script.sh password
bash scripts/script.sh password --length 24 --count 5
bash scripts/script.sh password --no-special --length 16
```

**Arguments:**
- `--length` — Password length (optional, default: 16)
- `--count` — Number of passwords (optional, default: 1)
- `--no-special` — Exclude special characters (optional)

### batch

Run multiple generation commands in batch from a config file.

```bash
bash scripts/script.sh batch --config batch.json
```

**Arguments:**
- `--config` — Batch configuration file (required)

### help

Display help information and list all available commands.

```bash
bash scripts/script.sh help
```

### version

Display the current tool version.

```bash
bash scripts/script.sh version
```

## Examples

```bash
# Generate 100 user records as CSV
bash scripts/script.sh csv --columns "id:uuid,name:name,email:email,age:int:18-65" --rows 100 --output users.csv

# Create JSON test data
bash scripts/script.sh json --schema '{"user":"name","score":"float:0-100"}' --count 20

# Quick password generation
bash scripts/script.sh password --length 20 --count 10
```

## Notes

- All generated data is logged in `~/.generate/data.jsonl` for reproducibility
- Use `--seed` (where supported) for deterministic output
- Schema types for JSON/CSV: `name`, `email`, `uuid`, `int:min-max`, `float:min-max`, `bool`, `date`, `string`
- Batch mode accepts a JSON config with an array of generation commands

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
