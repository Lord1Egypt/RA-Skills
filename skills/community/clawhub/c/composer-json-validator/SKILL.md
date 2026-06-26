---
name: composer-json-validator
description: Validate and lint PHP Composer composer.json files for structure, dependencies, autoload, and best practices. Use when asked to lint, validate, check, or audit composer.json files, verify PHP project configuration, or ensure Composer quality. Triggers on "lint composer", "validate composer.json", "check php deps", "composer best practices".
---

# Composer JSON Validator

Validate and lint PHP Composer `composer.json` files for structure, dependencies, autoload configuration, and best practices.

## Commands

### lint — Run all lint checks

```bash
python3 scripts/composer_json_validator.py lint composer.json
python3 scripts/composer_json_validator.py lint composer.json --strict
python3 scripts/composer_json_validator.py lint composer.json --format json
python3 scripts/composer_json_validator.py lint composer.json --format markdown
```

### dependencies — Inspect require/require-dev

```bash
python3 scripts/composer_json_validator.py dependencies composer.json
python3 scripts/composer_json_validator.py dependencies composer.json --format json
```

### scripts — Inspect scripts section

```bash
python3 scripts/composer_json_validator.py scripts composer.json
python3 scripts/composer_json_validator.py scripts composer.json --format markdown
```

### validate — Full validation (structure + lint + summary)

```bash
python3 scripts/composer_json_validator.py validate composer.json
python3 scripts/composer_json_validator.py validate composer.json --strict --format json
```

## Flags

| Flag | Description |
|------|-------------|
| `--strict` | Exit code 1 on warnings (CI-friendly) |
| `--format text` | Human-readable output (default) |
| `--format json` | Machine-readable JSON |
| `--format markdown` | Markdown report |

## Lint Rules (22 checks)

### Structure (5)
1. Valid JSON syntax
2. Required fields: `name`, `description`, `type`
3. Valid package name format (`vendor/package`)
4. Valid `type` value (`library`, `project`, `metapackage`, `composer-plugin`)
5. `license` field present and valid SPDX identifier

### Dependencies (6)
6. No duplicate packages across `require` and `require-dev`
7. Version constraints use valid operators (`^`, `~`, `>=`, etc.)
8. No dev-only packages in `require` (phpunit, mockery, etc.)
9. No wildcard `*` versions
10. PHP version constraint present in `require`
11. `ext-*` dependencies are explicit (not `*`)

### Autoload (4)
12. PSR-4 autoload defined
13. Namespace ends with `\\` (PSR-4 convention)
14. No duplicate namespaces across autoload entries
15. `autoload-dev` separate from `autoload`

### Best Practices (7)
16. `scripts` section present
17. No `post-install-cmd`/`post-update-cmd` executing arbitrary URLs
18. `config.sort-packages` enabled
19. `minimum-stability` explicit when not `stable`
20. `prefer-stable` set when `minimum-stability` is not `stable`
21. No hardcoded absolute paths in autoload
22. All repository URLs use HTTPS

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | No errors (warnings allowed unless `--strict`) |
| 1 | Errors found (or warnings in `--strict` mode) |
| 2 | Invalid arguments / file not found |

## Example Output

```
composer.json lint results
==========================
[ERROR]   name: Package name must match vendor/package format
[WARN]    dependencies: phpunit/phpunit found in require (should be in require-dev)
[WARN]    autoload: config.sort-packages not enabled
[INFO]    scripts: scripts section present

Summary: 1 error(s), 2 warning(s), 1 info
```
