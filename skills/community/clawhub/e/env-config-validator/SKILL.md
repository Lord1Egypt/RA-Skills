---
name: env-config-validator
description: Validate .env files against schemas, compare environments (dev vs prod), detect common mistakes (trailing spaces, placeholders, invalid ports, missing protocols, duplicate keys, unquoted spaces), auto-generate schemas, and type-check values. Supports text, JSON, and markdown output with CI-friendly exit codes. Use when asked to validate environment config, check .env files for errors, compare env files, diff environments, detect env misconfigurations, generate env schema, audit .env variables, check for missing env vars, or ensure env consistency across environments. Triggers on "validate env", "check .env", "compare environments", "env diff", "env schema", "env audit", "missing env vars", "environment config".
---

# Env Config Validator

Validate .env files, compare environments, detect common mistakes, and enforce schemas.

## Quick Start

```bash
# Validate with auto-detected common checks
python3 scripts/validate_env.py .env

# Validate against a schema
python3 scripts/validate_env.py .env --schema env-schema.json

# Compare dev vs prod
python3 scripts/validate_env.py --diff .env.development .env.production

# Generate schema from existing .env
python3 scripts/validate_env.py --generate-schema .env -o env-schema.json

# JSON output for CI
python3 scripts/validate_env.py .env --output json --severity error
```

## Common Checks (Auto-Detected)

The validator automatically detects these issues without a schema:

| Check | Severity | What it catches |
|-------|----------|-----------------|
| Trailing whitespace | warning | Invisible chars causing bugs |
| Unquoted spaces | warning | Values with spaces not wrapped in quotes |
| Placeholders | error | `change_me`, `TODO`, `xxx`, `your_*` values |
| Empty values | info | Defined but blank variables |
| Double-nested quotes | warning | `""value""` quoting errors |
| URL missing protocol | warning | URL vars without http(s):// |
| Port out of range | error | Port > 65535 or < 1 |
| Short secrets | warning | SECRET/PASSWORD/KEY < 8 chars |
| Inconsistent booleans | info | `yes`/`1` instead of `true`/`false` |
| Mixed case keys | info | `some_Var` instead of `SOME_VAR` |
| Inline comments | warning | `value # comment` (not all parsers support) |
| Duplicate keys | warning | Same variable defined twice |

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--schema` | — | JSON schema file for type/required validation |
| `--diff FILE FILE` | — | Compare two env files |
| `--generate-schema` | — | Auto-generate schema from .env file |
| `--output` | text | Output format: text, json, markdown |
| `-o` | stdout | Output file path |
| `--ignore` | — | Skip specific check IDs (repeatable) |
| `--severity` | info | Minimum severity: error, warning, info |

## Exit Codes

- `0` — No issues (or only info)
- `1` — Warnings found (or diff has differences)
- `2` — Errors found

## Workflow

### Pre-deploy Validation

1. Generate schema from working .env: `--generate-schema .env -o schema.json`
2. Add schema to repo, validate in CI: `validate_env.py .env --schema schema.json --severity error`
3. Diff staging vs prod: `--diff .env.staging .env.production`

### Audit Existing Project

1. Run `validate_env.py .env` to find common mistakes
2. Fix errors and warnings
3. Generate schema for future validation

## References

- **schema-format.md** — Full JSON schema specification, supported types, field reference
