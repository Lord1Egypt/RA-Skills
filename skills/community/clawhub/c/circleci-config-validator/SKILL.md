---
name: circleci-config-validator
description: Validate .circleci/config.yml files for syntax, structure, security, and best practices. Use when validating CircleCI pipeline configuration, auditing CI/CD workflows, linting .circleci/config.yml, or checking CircleCI config for common mistakes.
---

# circleci-config-validator

A pure Python 3 (stdlib + PyYAML) validator for `.circleci/config.yml` files covering 22 rules across 5 categories.

## Commands

```
python3 scripts/circleci_config_validator.py <command> [options] FILE
```

| Command    | Description                                            |
|------------|--------------------------------------------------------|
| `validate` | Full validation — all 22 rules                         |
| `check`    | Quick syntax + structure check only                    |
| `jobs`     | List all jobs with executor type and step count        |
| `graph`    | Show workflow dependency graph as text                 |

## Options

| Option                   | Description                                    |
|--------------------------|------------------------------------------------|
| `--format text\|json\|summary` | Output format (default: text)            |
| `--strict`               | Treat warnings as errors (exit 1)              |

## Rules

| ID | Category | Sev | Description |
|----|----------|-----|-------------|
| S001 | Structure | E | YAML syntax error |
| S002 | Structure | E | Missing `version` key |
| S003 | Structure | E | Invalid version (must be 2 or 2.1) |
| S004 | Structure | W | Missing `jobs` or `workflows` section |
| S005 | Structure | W | Unknown top-level keys |
| J001 | Jobs | E | Job missing execution environment |
| J002 | Jobs | E | Job missing `steps` |
| J003 | Jobs | W | Empty steps list |
| J004 | Jobs | W | Unknown step name |
| J005 | Jobs | E | `run` step missing `command` |
| W001 | Workflows | E | Workflow references undefined job |
| W002 | Workflows | E | Circular job dependency via `requires` |
| W003 | Workflows | E | `requires` references undefined job |
| W004 | Workflows | W | Empty workflow (no jobs) |
| SEC1 | Security | E | Hardcoded secret in environment variable |
| SEC2 | Security | W | `setup_remote_docker` without version pin |
| SEC3 | Security | W | Deprecated `deploy` step used |
| SEC4 | Security | I | `context` used without branch filters |
| B001 | Best Practices | I | Missing `resource_class` |
| B002 | Best Practices | I | No `working_directory` set |
| B003 | Best Practices | W | `save_cache` without matching `restore_cache` |
| B004 | Best Practices | W | Docker image using `latest` tag |

## Examples

```bash
# Full validation
python3 scripts/circleci_config_validator.py validate .circleci/config.yml

# Quick syntax check
python3 scripts/circleci_config_validator.py check .circleci/config.yml

# JSON output for CI
python3 scripts/circleci_config_validator.py --format json validate .circleci/config.yml

# One-line pass/fail
python3 scripts/circleci_config_validator.py --format summary validate .circleci/config.yml

# Strict mode (warnings = errors)
python3 scripts/circleci_config_validator.py --strict validate .circleci/config.yml

# List jobs
python3 scripts/circleci_config_validator.py jobs .circleci/config.yml

# Dependency graph
python3 scripts/circleci_config_validator.py graph .circleci/config.yml
```

## Exit Codes

- `0` — No errors (warnings may exist)
- `1` — Errors found (or warnings in `--strict` mode)
- `2` — File not found or YAML parse error

## Requirements

- Python 3.7+
- PyYAML (falls back to graceful error if unavailable)
