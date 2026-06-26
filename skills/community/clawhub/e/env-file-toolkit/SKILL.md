---
name: env-file-toolkit
description: Manage .env files with validate, diff, template generation, merge, and missing-key checks. Use when working with environment variable files, comparing .env.local vs .env.production, generating .env.example templates, validating .env syntax, merging env files, or checking for missing environment variables.
---

# Env File Toolkit

Swiss-army knife for `.env` file management. Validate syntax, diff environments, generate templates, merge files, and check for missing keys.

## Commands

### Validate

Check `.env` syntax, find duplicates, empty values, and formatting issues:

```bash
python3 scripts/env_toolkit.py validate .env
```

### Diff

Compare two `.env` files — shows keys only in one file and changed values:

```bash
python3 scripts/env_toolkit.py diff .env.local .env.production
```

### Template

Generate a `.env.example` with smart placeholders (strips secrets, infers types):

```bash
python3 scripts/env_toolkit.py template .env
python3 scripts/env_toolkit.py template .env -o .env.example
python3 scripts/env_toolkit.py template .env --keep-values  # keep actual values
```

### Merge

Merge multiple `.env` files (later files override earlier):

```bash
python3 scripts/env_toolkit.py merge .env.defaults .env.local -o .env.merged
```

### List Keys

List all variable names in a `.env` file:

```bash
python3 scripts/env_toolkit.py list-keys .env
python3 scripts/env_toolkit.py list-keys .env --with-values
```

### Check Missing

Verify a target `.env` has all keys from a template:

```bash
python3 scripts/env_toolkit.py check-missing .env.example .env
python3 scripts/env_toolkit.py check-missing .env.example .env --strict
```

## Dependencies

- Python 3.8+ (stdlib only, no pip packages needed)
