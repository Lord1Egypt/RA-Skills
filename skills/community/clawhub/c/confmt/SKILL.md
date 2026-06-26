---
name: confmt
description: Format, convert, flatten, and diff configuration files. Supports JSON, TOML (Python 3.11+), and .env formats. Use when asked to pretty-print a config, flatten nested JSON to dot-notation, convert JSON to env vars, diff two config files to find changes, or sort config keys. Handles JSON↔flat↔env conversion. Zero dependencies.
---

# confmt 📝

Config file formatter, converter, and differ.

## Commands

```bash
# Pretty-print JSON config
python3 scripts/confmt.py format config.json --sort

# Flatten nested config to dot-notation
cat config.json | python3 scripts/confmt.py format -o flat

# Convert JSON to .env format
python3 scripts/confmt.py format config.json -o env

# Compact/minify
python3 scripts/confmt.py format config.json --compact

# Diff two config files
python3 scripts/confmt.py diff prod.json staging.json
```

## Formats
- **JSON** — read/write, pretty or compact
- **TOML** — read (Python 3.11+)
- **.env** — read/write
- **flat** — dot-notation output (key.subkey = value)

## Diff Output
- `+` added keys
- `-` removed keys
- `~` changed values
