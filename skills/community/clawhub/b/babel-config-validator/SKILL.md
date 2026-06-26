---
name: babel-config-validator
description: Validate Babel config files (babel.config.json, .babelrc, .babelrc.json, package.json#babel) for deprecated presets, plugin conflicts, ordering issues, and best practices. Use when validating Babel transpiler configs, auditing build setups, migrating Babel versions, or linting babel config files.
---

# Babel Config Validator

Validate `babel.config.json`, `.babelrc`, `.babelrc.json`, and `package.json#babel` for deprecated presets/plugins, conflicting transforms, ordering issues, and best practices. Supports text, JSON, and summary output formats with CI-friendly exit codes.

## Commands

```bash
# Full validation (all 24+ rules)
python3 scripts/babel_config_validator.py validate babel.config.json

# Quick syntax-only check (structure rules only)
python3 scripts/babel_config_validator.py check .babelrc

# Explain config in human-readable form
python3 scripts/babel_config_validator.py explain babel.config.json

# Suggest improvements
python3 scripts/babel_config_validator.py suggest package.json

# JSON output (CI-friendly)
python3 scripts/babel_config_validator.py validate .babelrc --format json

# Summary only (pass/fail + counts)
python3 scripts/babel_config_validator.py validate .babelrc --format summary

# Strict mode (warnings become errors)
python3 scripts/babel_config_validator.py validate .babelrc --strict
```

## Rules (24+)

| # | Category | Severity | Rule |
|---|----------|----------|------|
| S1 | Structure | Error | File not found or unreadable |
| S2 | Structure | Error | Empty config or no content |
| S3 | Structure | Warning | Both babel.config and .babelrc present (conflict) |
| S4 | Structure | Warning | Unknown top-level config keys |
| S5 | Structure | Error | Invalid JSON syntax |
| P1 | Presets | Error | Deprecated preset (es2015, es2016, es2017, latest, stage-*) |
| P2 | Presets | Warning | Preset ordering matters (@babel/preset-typescript before @babel/preset-env) |
| P3 | Presets | Warning | Duplicate presets |
| P4 | Presets | Error | Unknown/misspelled preset name |
| P5 | Presets | Warning | Missing @babel/preset-env (most configs need it) |
| L1 | Plugins | Error | Deprecated plugin (@babel/plugin-proposal-* → built-in) |
| L2 | Plugins | Warning | Duplicate plugins |
| L3 | Plugins | Warning | Plugin ordering conflict (decorators before class-properties) |
| L4 | Plugins | Warning | Conflicting plugins (transform-runtime + external-helpers) |
| L5 | Plugins | Warning | Plugin without @babel/ scope (may be community or typo) |
| M1 | Modules | Warning | modules: false in preset-env without bundler context |
| M2 | Modules | Warning | sourceType mismatch with modules setting |
| M3 | Modules | Warning | Conflicting module transforms |
| E1 | Env/Overrides | Warning | Empty env config section |
| E2 | Env/Overrides | Warning | Override without test pattern |
| E3 | Env/Overrides | Warning | Unknown env name (not development/production/test) |
| B1 | Best Practices | Warning | loose mode inconsistency across plugins |
| B2 | Best Practices | Warning | Missing targets/browserslist (unoptimized output) |
| B3 | Best Practices | Warning | useBuiltIns without corejs version |
| B4 | Best Practices | Warning | corejs version outdated (< 3) |

## Output Formats

- `text` (default): Human-readable with colors and severity icons
- `json`: Machine-parseable JSON array of findings
- `summary`: Pass/fail with error/warning counts

## Exit Codes

- `0`: No errors (warnings only or clean)
- `1`: One or more errors found
- `2`: File not found or invalid input

## Requirements

- Python 3.8+
- No external dependencies (pure stdlib)
