---
name: fleet-pr-agent
description: "Multi-repo PR monitoring and triage agent. Scans GitHub repos for open PRs, prioritizes by staleness/review status/CI state, and generates a structured Markdown triage summary. Use when managing PRs across multiple repositories."
version: "1.1.0"
slug: fleet-pr-agent
tags: ["github", "pr", "monitoring", "triage", "multi-repo", "automation"]
---

# Fleet PR Agent

Multi-repository pull request monitoring, triage, and summary tool for engineering teams and AI agent fleets managing many repos at once.

## What It Does

- Scans one or more GitHub repos for open PRs using the `gh` CLI
- Prioritizes by: staleness, review status, CI pass/fail, label priority
- Generates a structured Markdown triage report (no external dependencies — pure Python stdlib + `gh`)
- Supports concurrent scanning of multiple repos in a single run

## Prerequisites

- `gh` CLI authenticated (`gh auth status`)
- Python 3.6+ (standard library only — no pip packages required)
- Repos accessible to your GitHub token

## Quick Start

```bash
# Scan a single repo
python3 scripts/triage.py owner/repo

# Scan multiple repos
python3 scripts/triage.py owner/repo1 owner/repo2 owner/repo3

# Generate triage report to file
python3 scripts/triage.py owner/repo --output report.md
```

## Usage as Claude Code Skill

When invoked as `/fleet-pr-agent`, provide repos:

```
/fleet-pr-agent owner/repo1 owner/repo2
```

The agent will:
1. Fetch all open PRs from each repo via `gh`
2. Score and rank them by urgency (stale > failing CI > needs review > draft)
3. Output a prioritized Markdown summary

## Triage Priority Rules

| Priority | Condition |
|----------|-----------|
| P0 - Critical | CI failing + older than 3 days |
| P1 - High | Approved but not merged, or review requested > 2 days ago |
| P2 - Medium | Open > 5 days, no review activity |
| P3 - Low | Draft PRs, recently opened |

## Output Format

```markdown
## PR Triage Report — 2026-03-27

### P0 — Critical (2)
- [#123 Fix auth middleware](url) — CI failing since Mar 24, 2 approvals
- [#456 DB migration](url) — CI failing since Mar 25, no reviews

### P1 — High (1)
- [#789 Add caching layer](url) — Approved Mar 25, ready to merge

### P2 — Medium (3)
...

### Summary
- Total open PRs: 15
- Needing attention: 6
- Repos scanned: 2
```

## Configuration

Set env vars to override defaults:

| Variable | Default | Description |
|----------|---------|-------------|
| `FLEET_PR_STALE_DAYS` | `5` | Days before a PR is considered stale |
| `FLEET_PR_CI_WEIGHT` | `3` | Weight multiplier for CI-failing PRs |
| `FLEET_PR_MAX_PRS` | `50` | Max PRs to fetch per repo |

## Architecture

- `scripts/triage.py` — Pure Python 3 triage engine (stdlib only)
- No external package dependencies
- Uses `gh pr list --json` for all data fetching
- Portable across Linux, macOS, Windows (Python + gh required)

## License

MIT
