---
name: eslint-flat-config-validator
description: Validate ESLint v9+ flat config files (JSON-exported) for structural correctness, language options, rules configuration, plugin hygiene, file patterns, and best practices. Use when auditing ESLint projects, enforcing config standards in CI, or reviewing eslint.config.js changes.
---

# ESLint Flat Config Validator

Validate ESLint v9+ flat configuration files exported as JSON for structural correctness, language options, rules configuration, plugin setup, file/ignore patterns, and best practices. Uses pure Python 3 stdlib (`json`, `argparse`, `re`, `os`, `sys`) -- no external dependencies.

Since ESLint flat configs are JS/MJS/CJS (`eslint.config.js`), the validator works with JSON-exported snapshots. Export your config first:

```bash
node -e "import('./eslint.config.js').then(m => console.log(JSON.stringify(m.default)))" > eslint.config.json
```

Then validate the JSON output.

## Commands

### validate -- Comprehensive validation with all rules and summary

```bash
python3 scripts/eslint_flat_config_validator.py validate eslint.config.json
python3 scripts/eslint_flat_config_validator.py validate eslint.config.json --strict
python3 scripts/eslint_flat_config_validator.py validate eslint.config.json --format json
```

### lint -- Run all rules

```bash
python3 scripts/eslint_flat_config_validator.py lint eslint.config.json
python3 scripts/eslint_flat_config_validator.py lint eslint.config.json --format summary
```

### rules -- Check rules configuration

```bash
python3 scripts/eslint_flat_config_validator.py rules eslint.config.json
python3 scripts/eslint_flat_config_validator.py rules eslint.config.json --format json
```

### plugins -- Check plugin configuration

```bash
python3 scripts/eslint_flat_config_validator.py plugins eslint.config.json
python3 scripts/eslint_flat_config_validator.py plugins eslint.config.json --format json
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Treat warnings as errors -- exit code 1 (CI-friendly) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format summary` | Compact summary with counts |

## Validation Rules (25)

### Structure (5)

| Rule | Severity | Description |
|------|----------|-------------|
| S1 | error | File not found or unreadable |
| S2 | error | Empty config (empty array or no objects) |
| S3 | error | JSON syntax errors |
| S4 | error | Not an array (flat config must be an array of config objects) |
| S5 | warning | Unknown top-level keys in config objects (valid: files, ignores, languageOptions, linterOptions, plugins, processor, rules, settings, name) |

### Language Options (5)

| Rule | Severity | Description |
|------|----------|-------------|
| L1 | error | Invalid ecmaVersion (must be number >= 3 or "latest") |
| L2 | error | Invalid sourceType (must be "module", "script", or "commonjs") |
| L3 | warning | Invalid parser value (should be object with parse/parseForESTree, warn if string) |
| L4 | error | globals with invalid values (only "readonly"/"writable"/"off" or true/false/"readable") |
| L5 | info | Missing ecmaVersion (defaults to "latest" in ESLint v9) |

### Rules (5)

| Rule | Severity | Description |
|------|----------|-------------|
| R1 | error | Unknown severity (must be "off"/0, "warn"/1, "error"/2) |
| R2 | warning | Rules with deprecated names |
| R3 | warning | Conflicting rules (e.g., indent + @typescript-eslint/indent) |
| R4 | info | Empty rules object |
| R5 | error | Rule config not array or severity (must be severity or [severity, ...options]) |

### Plugins (3)

| Rule | Severity | Description |
|------|----------|-------------|
| P1 | info | Empty plugins object |
| P2 | error | Plugin value not object (plugin values should be plugin objects) |
| P3 | warning | Duplicate plugin key across config objects |

### Files/Ignores (4)

| Rule | Severity | Description |
|------|----------|-------------|
| F1 | info | Missing files pattern in non-global config (config without files/ignores applies globally) |
| F2 | error | Invalid glob patterns (empty string) |
| F3 | error | files as string instead of array |
| F4 | error | ignores as string instead of array |

### Best Practices (3)

| Rule | Severity | Description |
|------|----------|-------------|
| X1 | warning | No rules defined in any config object |
| X2 | warning | Many config objects (>20) suggest consolidation |
| X3 | info | Missing "name" property (recommended in v9 for debugging) |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings allowed unless `--strict`) |
| 1 | Errors found (or warnings in `--strict` mode) |
| 2 | File not found / parse error |

## CI Integration

```yaml
# GitHub Actions
- name: Validate ESLint flat config
  run: |
    node -e "import('./eslint.config.js').then(m => console.log(JSON.stringify(m.default)))" > /tmp/eslint.config.json
    python3 scripts/eslint_flat_config_validator.py validate /tmp/eslint.config.json --strict --format json
```

## Example Output

```
eslint.config validate — eslint.config.json
============================================
[ERROR  ] S5: Unknown top-level key in config object #2: 'env'
         'env' is not valid in flat config. Valid keys: files, ignores, languageOptions, linterOptions, plugins, processor, rules, settings, name
[ERROR  ] R1: Invalid rule severity for 'no-unused-vars': 'on'
         Severity must be 'off'/0, 'warn'/1, or 'error'/2.
[WARNING] R2: Deprecated rule 'no-buffer-constructor' in config object #1
         This rule was deprecated in ESLint v7. Remove it or replace with the recommended alternative.
[WARNING] X1: No rules defined in any config object
         At least one config object should define rules for ESLint to enforce anything.
[INFO   ] X3: Config object #3 missing 'name' property
         Adding a name helps identify config objects in ESLint's debug output and error messages.

Result: INVALID
Summary: 2 error(s), 2 warning(s), 1 info
```
