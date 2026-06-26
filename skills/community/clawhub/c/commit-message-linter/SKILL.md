---
name: commit-message-linter
description: Validate git commit messages against Conventional Commits spec and configurable rules. Use when linting commit messages, enforcing commit conventions, checking commit history quality, setting up commit-msg hooks, or validating messages in CI pipelines. Supports custom type/scope whitelists, length limits, pattern matching, and multiple output formats (text, JSON, markdown).
---

# Commit Message Linter

Validate commit messages against Conventional Commits and custom rules. Pure Python, no dependencies.

## Quick Start

```bash
# Lint last commit
python3 scripts/lint_commits.py

# Lint last 5 commits
python3 scripts/lint_commits.py --range HEAD~5..HEAD

# Lint a branch
python3 scripts/lint_commits.py --range main..feature-branch

# Lint a single message
python3 scripts/lint_commits.py --message "feat: add login"

# Read from stdin (git commit-msg hook)
python3 scripts/lint_commits.py --stdin < .git/COMMIT_MSG

# Read from file
python3 scripts/lint_commits.py --file .git/COMMIT_MSG
```

## Output Formats

```bash
python3 scripts/lint_commits.py --format text      # human-readable (default)
python3 scripts/lint_commits.py --format json       # CI/tooling
python3 scripts/lint_commits.py --format markdown   # reports
```

## Configuration

Generate default config:
```bash
python3 scripts/lint_commits.py init
```

Creates `.commitlintrc.json`. Also auto-discovers `.commitlintrc` or `commitlint.config.json`.

Key config options:
- `header_max_length` (72) — max header chars
- `require_conventional` (true) — enforce `<type>[scope]: <desc>` format
- `types` — allowed types (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert)
- `scopes` — allowed scopes (empty = any)
- `require_scope` (false) — mandate scope
- `require_body` (false) — mandate body
- `header_case` — description start case: lower/upper/sentence/any
- `no_trailing_period` (true) — reject trailing period on header
- `forbidden_patterns` — regex patterns that reject commits
- `required_patterns` — regex patterns that must match
- `--strict` flag treats warnings as errors

## Rules Reference

| Rule | Level | Description |
|------|-------|-------------|
| header-empty | error | Empty header |
| header-max-length | error | Header exceeds max length |
| header-min-length | warning | Header below min length |
| conventional-format | error | Not Conventional Commits format |
| type-enum | error | Type not in allowed list |
| scope-required | error | Missing required scope |
| scope-enum | error | Scope not in allowed list |
| description-empty | error | Empty description |
| description-case | warning | Wrong description case |
| header-no-period | warning | Trailing period |
| header-leading-whitespace | error | Leading whitespace |
| header-trailing-whitespace | warning | Trailing whitespace |
| body-separator | error | No blank line before body |
| body-required | warning | Missing required body |
| body-line-length | warning | Body line too long |
| body-max-lines | warning | Too many body lines |
| breaking-change-description | warning | Breaking ! without BREAKING CHANGE: in body |
| forbidden-pattern | error | Matches forbidden regex |
| required-pattern | warning | Doesn't match required regex |

## Exit Codes

- `0` — all commits pass (warnings OK unless `--strict`)
- `1` — errors found (or warnings with `--strict`)
- `2` — git/system error

## CI Integration (Git Hook)

As commit-msg hook (`.git/hooks/commit-msg`):
```bash
#!/bin/sh
python3 path/to/lint_commits.py --file "$1" --strict
```

Auto-ignored: merge commits, reverts, version tags, "Initial commit".
