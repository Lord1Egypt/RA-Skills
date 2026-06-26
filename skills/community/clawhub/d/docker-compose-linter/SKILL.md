---
name: docker-compose-linter
description: Lint docker-compose.yml files for security, best practices, and port conflicts.
version: 1.0.0
---

# docker-compose-linter

A pure Python 3 (stdlib only) linter for docker-compose.yml files.

## Commands

```
python3 scripts/docker-compose-linter.py <command> [options] FILE
```

| Command    | Description                                      |
|------------|--------------------------------------------------|
| `lint`     | Lint a docker-compose.yml for issues             |
| `services` | List all services with their images/builds       |
| `ports`    | List all port mappings, detect conflicts         |
| `audit`    | Full audit (lint + services + ports summary)     |

## Options

| Option                        | Description                                      |
|-------------------------------|--------------------------------------------------|
| `--format text\|json\|markdown` | Output format (default: text)                  |
| `--strict`                    | Exit 1 on any issue (not just errors)            |
| `--ignore RULE`               | Ignore a specific rule (repeatable)              |
| `--min-severity error\|warning\|info` | Minimum severity to report (default: info) |

## Lint Rules

| Rule                  | Severity | Description                                              |
|-----------------------|----------|----------------------------------------------------------|
| `no-version`          | info     | Missing or outdated `version:` key                       |
| `no-healthcheck`      | warning  | Service without healthcheck defined                      |
| `no-restart-policy`   | warning  | Service without restart policy                           |
| `privileged-mode`     | error    | Service running in privileged mode                       |
| `port-conflict`       | error    | Multiple services mapping to same host port              |
| `host-network`        | warning  | Using network_mode: host (security risk)                 |
| `latest-tag`          | warning  | Image using :latest tag or no tag                        |
| `no-resource-limits`  | info     | No memory/CPU limits (deploy.resources)                  |
| `hardcoded-env`       | warning  | Secrets/passwords directly in environment variables      |
| `root-user`           | warning  | No user: specified (runs as root by default)             |
| `missing-depends-on`  | info     | Service uses links but no depends_on                     |
| `bind-mount-relative` | info     | Relative bind mount paths                                |
| `no-logging`          | info     | No logging configuration                                 |
| `duplicate-service`   | error    | Duplicate service names                                  |

## Examples

```bash
# Lint with default text output
python3 scripts/docker-compose-linter.py lint docker-compose.yml

# Only show errors and warnings
python3 scripts/docker-compose-linter.py --min-severity warning lint docker-compose.yml

# JSON output for CI pipelines
python3 scripts/docker-compose-linter.py --format json lint docker-compose.yml

# Full audit in markdown
python3 scripts/docker-compose-linter.py --format markdown audit docker-compose.yml

# Ignore specific rules
python3 scripts/docker-compose-linter.py --ignore root-user --ignore no-logging lint docker-compose.yml

# Strict mode: exit 1 on any issue
python3 scripts/docker-compose-linter.py --strict lint docker-compose.yml
```

## Requirements

- Python 3.7+
- No external dependencies (pure stdlib)
