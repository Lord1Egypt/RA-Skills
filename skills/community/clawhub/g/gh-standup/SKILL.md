---
name: gh-standup
description: Generate a GitHub standup summary covering the period since the last standup. Use when the user asks for a standup, work summary, weekly update, or "what did I do since [day]". Accepts a repo (org/repo) or organization name, and one or more standup days (e.g. Friday, or Monday,Thursday). Pulls merged PRs and direct commits authored by the user since the last standup date, and formats a clean summary.
---

# gh-standup

Generate a standup summary from GitHub activity since the last standup day.

## Quick Start

```bash
# Single repo, weekly Friday standup
python3 scripts/standup.py --repo ORG/REPO --standup-days Friday

# Multiple standup days
python3 scripts/standup.py --repo ORG/REPO --standup-days Monday,Thursday

# Whole org, specific author
python3 scripts/standup.py --org MY_ORG --standup-days Friday --author username
```

## Parameters

| Flag | Required | Default | Description |
|------|----------|---------|-------------|
| `--repo` | one of | — | Single repo (`org/repo`) |
| `--org` | one of | — | Entire GitHub org (all repos) |
| `--standup-days` | no | `Friday` | Comma-separated weekdays |
| `--author` | no | `@me` | GitHub username or `@me` |

## Workflow

1. Run `scripts/standup.py` with the user's repo/org and standup days
2. The script calculates the most recent past standup day and uses it as `since`
3. Output: merged PRs + direct commits (PR commits de-duped) since that date
4. Post the output as the standup message

## Requirements

- `gh` CLI authenticated (`gh auth status`)
- Python 3.10+

## Notes

- `--org` fetches all repos in the org; can be slow for large orgs — prefer `--repo` when possible
- PRs are matched by merge date; commits by author date
- Commits that belong to a merged PR are excluded from "Direct Commits" to avoid duplication
