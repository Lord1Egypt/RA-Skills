---
name: browserslist-validator
description: Validate .browserslistrc files and browserslist config in package.json for syntax errors, deprecated browsers, redundant queries, and best practices. Use when validating browserslist configuration, checking browser targeting, auditing frontend build configs, or linting .browserslistrc files.
---

# Browserslist Validator

Validate `.browserslistrc` files and `browserslist` entries in `package.json` for syntax errors, deprecated browsers, redundant queries, and best practices.

## Commands

```bash
# Full validation (all rules)
python3 scripts/browserslist_validator.py validate .browserslistrc

# Validate browserslist in package.json
python3 scripts/browserslist_validator.py validate package.json

# Quick syntax-only check
python3 scripts/browserslist_validator.py check .browserslistrc

# Estimate coverage
python3 scripts/browserslist_validator.py coverage .browserslistrc

# Explain each query in human-readable form
python3 scripts/browserslist_validator.py explain .browserslistrc

# JSON output
python3 scripts/browserslist_validator.py validate .browserslistrc --format json

# One-line PASS/WARN/FAIL summary
python3 scripts/browserslist_validator.py validate .browserslistrc --format summary

# Strict mode (warnings become errors)
python3 scripts/browserslist_validator.py validate .browserslistrc --strict

# Target environment
python3 scripts/browserslist_validator.py validate .browserslistrc --env production
```

## Rules (20)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Syntax | E | File not found or unreadable |
| S2 | Syntax | E | Empty config (no queries) |
| S3 | Syntax | E | Invalid query syntax / unknown browser name |
| S4 | Syntax | W | Duplicate queries |
| B1 | Browsers | W | Dead/deprecated browser (IE, Blackberry, etc.) |
| B2 | Browsers | W | Browser with <0.01% global usage |
| B3 | Browsers | E | Browser version does not exist (e.g. Chrome 999) |
| B4 | Browsers | E | Unknown browser name |
| Q1 | Queries | W | Redundant query (covered by broader query) |
| Q2 | Queries | W | Conflicting queries (e.g. `> 1%` and `< 0.5%`) |
| Q3 | Queries | E | `not dead` without any positive query |
| Q4 | Queries | W | Empty result after `not` negation |
| C1 | Coverage | W | Very low total coverage (<80%) |
| C2 | Coverage | W | Very high coverage (>99.5%, may include dead browsers) |
| C3 | Coverage | I | No mobile browser coverage hint |
| C4 | Coverage | I | No country-specific override detected |
| P1 | Best Practices | W | IE queries present (recommend dropping IE) |
| P2 | Best Practices | W | Unreasonably old versions (`last 20 versions`) |
| P3 | Best Practices | W | `all` query used (too broad) |
| P4 | Best Practices | W | Version pinning instead of range (`Chrome 90`) |

## Output Formats

- **text** (default): Human-readable with `[E]`/`[W]`/`[I]` severity prefix
- **json**: Machine-readable structured output
- **summary**: Single-line `PASS` / `WARN` / `FAIL`

## Exit Codes

- `0` — No errors
- `1` — Errors found (or warnings in `--strict` mode)
- `2` — File not found or parse error
