# Bounty Hunter Agent

## Metadata
- **Name:** bounty-hunter-agent
- **Version:** 1.0.0
- **Author:** lanxevo3
- **Tags:** github, bounty, automation, monetization, algora, opire
- **License:** MIT

## Description

Autonomous GitHub bounty hunting agent. Scans for paid issues across GitHub, Algora, and Opire, evaluates viability based on competition level and payout amount, and helps you prioritize and submit PRs automatically.

## What It Does

1. **Scans** repositories for bounty-labeled issues (`bounty`, `💰`, `reward`, `paid`, `algora`, `opire`)
2. **Evaluates** competition level by checking existing PRs and comments on each issue
3. **Scores** opportunities by payout amount, competition density, issue age, and repo activity
4. **Prioritizes** a ranked list of actionable bounties sorted by expected value
5. **Tracks state** in a local JSON file so you never re-scan the same issues
6. **Spawns fix sessions** — integrates with OpenClaw to kick off autonomous coding sessions for top-ranked bounties

## Prerequisites

- **gh CLI** authenticated (`gh auth status` should succeed)
- **Python 3.8+** (stdlib only — no pip dependencies)
- Optional: OpenClaw runtime for automated fix session spawning

## Usage

### Quick Scan
```bash
python ~/.agents/skills/bounty-hunter-agent/scripts/bounty_scan.py
```

### With OpenClaw
When installed as a skill, invoke via:
```
/bounty-hunter-agent scan
```

The agent will:
- Search GitHub for bounty-labeled issues
- Check Algora and Opire for listed bounties
- Output a ranked JSON report to `~/.agents/skills/bounty-hunter-agent/state/bounties.json`
- Print a human-readable summary to stdout

### Configuration

Set environment variables to customize behavior:

| Variable | Default | Description |
|---|---|---|
| `BOUNTY_MIN_PAYOUT` | `25` | Minimum payout in USD to consider |
| `BOUNTY_MAX_COMPETITION` | `5` | Max competing PRs before skipping |
| `BOUNTY_SCAN_LIMIT` | `100` | Max issues to scan per query |
| `BOUNTY_STATE_DIR` | `~/.agents/skills/bounty-hunter-agent/state` | Where to store state |

### Output Format

The scan produces a ranked list:
```json
[
  {
    "rank": 1,
    "score": 87.5,
    "repo": "org/repo",
    "issue": 123,
    "title": "Add feature X",
    "payout_usd": 200,
    "competing_prs": 1,
    "url": "https://github.com/org/repo/issues/123",
    "labels": ["bounty", "💰 200"],
    "age_days": 3
  }
]
```

## How Scoring Works

```
score = payout_weight * (payout / max_payout)
      + competition_weight * (1 - competing_prs / max_competition)
      + freshness_weight * (1 - age_days / max_age)
```

Default weights: payout=50, competition=35, freshness=15

Lower competition + higher payout + newer issue = higher score.
