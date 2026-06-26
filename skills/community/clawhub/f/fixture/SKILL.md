---
name: fixture
version: "1.0.0"
description: "Generate and manage test data fixtures using CLI templates. Use when creating seed data, mock records, or reproducible test datasets."
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
---

# Fixture — Test Data Fixture Generator

A CLI tool for generating, managing, and exporting test data fixtures. Create reproducible datasets from templates with seeded randomness for consistent test environments.

## Prerequisites

- Python 3.8+
- `bash` shell
- Write access to `~/.fixture/`

## Data Storage

All fixtures are stored in JSONL format at `~/.fixture/data.jsonl`. Templates are stored at `~/.fixture/templates.json`.

## Commands

Run commands via: `bash scripts/script.sh <command> [arguments...]`

### create

Create a new fixture record with specified fields and values.

```bash
bash scripts/script.sh create --name "test_user" --type user --fields '{"name":"Alice","email":"alice@test.com","age":30}'
```

**Arguments:**
- `--name` — Fixture name/label (required)
- `--type` — Fixture type/category (required)
- `--fields` — JSON object of field values (required)

### load

Load fixtures from a JSON or JSONL file into the fixture store.

```bash
bash scripts/script.sh load --file fixtures.json
bash scripts/script.sh load --file data.jsonl --format jsonl
```

**Arguments:**
- `--file` — Input file path (required)
- `--format` — File format: `json`, `jsonl` (optional, default: auto-detect)

### dump

Dump all fixtures or filtered subset to stdout or a file.

```bash
bash scripts/script.sh dump
bash scripts/script.sh dump --type user --output users.json
```

**Arguments:**
- `--type` — Filter by fixture type (optional)
- `--output` — Output file path (optional, default: stdout)

### list

List all fixtures with summary information.

```bash
bash scripts/script.sh list
bash scripts/script.sh list --type user
```

**Arguments:**
- `--type` — Filter by fixture type (optional)

### seed

Generate multiple fixture records from a template with seeded random data.

```bash
bash scripts/script.sh seed --template user --count 10 --seed 42
```

**Arguments:**
- `--template` — Template name to use (required)
- `--count` — Number of records to generate (required)
- `--seed` — Random seed for reproducibility (optional)

### reset

Clear all fixtures or a specific type from the data store.

```bash
bash scripts/script.sh reset
bash scripts/script.sh reset --type user
```

**Arguments:**
- `--type` — Only reset fixtures of this type (optional)
- `--confirm` — Skip confirmation prompt (optional)

### template

Manage fixture templates: create, list, or show template definitions.

```bash
bash scripts/script.sh template --list
bash scripts/script.sh template --create user --schema '{"name":"string","email":"email","age":"int:18-65"}'
bash scripts/script.sh template --show user
```

**Arguments:**
- `--list` — List all templates (optional)
- `--create` — Create template with given name (optional)
- `--schema` — JSON schema for template creation (optional)
- `--show` — Show a specific template (optional)

### validate

Validate fixtures against their template schema.

```bash
bash scripts/script.sh validate
bash scripts/script.sh validate --type user
```

**Arguments:**
- `--type` — Validate only a specific type (optional)

### export

Export fixtures to various formats: JSON, JSONL, CSV, SQL.

```bash
bash scripts/script.sh export --output fixtures.csv --format csv
bash scripts/script.sh export --output seed.sql --format sql --table users
```

**Arguments:**
- `--output` — Output file path (required)
- `--format` — Export format: `json`, `jsonl`, `csv`, `sql` (required)
- `--table` — Table name for SQL export (optional)

### import

Import fixtures from external sources or standard formats.

```bash
bash scripts/script.sh import --file data.csv --type user
```

**Arguments:**
- `--file` — Input file path (required)
- `--type` — Assign fixture type (required)

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
# Create a template
bash scripts/script.sh template --create user --schema '{"name":"string","email":"email","age":"int:18-65"}'

# Seed 50 users
bash scripts/script.sh seed --template user --count 50 --seed 42

# List all fixtures
bash scripts/script.sh list

# Export to SQL
bash scripts/script.sh export --output seed.sql --format sql --table users

# Reset all data
bash scripts/script.sh reset --confirm
```

## Notes

- Templates define field types: `string`, `email`, `int:min-max`, `float:min-max`, `bool`, `uuid`, `date`
- Seeded generation guarantees identical output given the same seed
- Use `validate` to check fixtures match their template schema
- SQL export generates INSERT statements compatible with most databases

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
