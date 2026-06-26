---
name: em-intel
description: >
  Engineering Manager Intelligence: track team performance, engineer contributions, and project health across GitLab/GitHub + Jira/GitHub Issues.
  Use when asked for morning briefs, EOD reviews, team reports, quiet engineer alerts, epic health checks, or weekly newsletters.
  Maps engineer contributions to Jira tickets via feature branch analysis. Supports Slack, Telegram, and email delivery.
  Trigger on: /morning-brief, /eod-review, /team-report, "who worked on X", "which tickets are stalled", "send newsletter", "team performance".
license: MIT
metadata:
  author: larry.l.fang@gmail.com
  version: "2.1.1"
  tags: engineering-manager,gitlab,github,jira,team-performance,morning-brief,eod-review,newsletter,dora
---

# em-intel — Engineering Manager Intelligence

Track team performance, engineer contributions, and project health across GitLab/GitHub + Jira/GitHub Issues.

## Agent Instructions (read this first)

When this skill is triggered:

**1. Check if configured:**
```bash
test -f <skill_dir>/.env && echo "configured" || echo "not_configured"
```

**If not configured**, say:
> "em-intel needs a one-time setup. Run this and I'll guide you through it (takes ~2 min):"
> `python3 <skill_dir>/em_intel.py setup`
>
> Or to preview without any credentials first:
> `python3 <skill_dir>/em_intel.py morning-brief --dry-run`

The `setup` command handles everything: asks questions, opens token pages in the browser, writes `.env`, installs deps, and runs `doctor` automatically.

**If configured**, run the requested command directly:
```bash
cd <skill_dir> && python3 em_intel.py <command> [--dry-run]
```

**On error**, run `doctor` and surface the failing checks:
```bash
python3 <skill_dir>/em_intel.py doctor
```

---

## Quick Start (manual)

```bash
# 1. Copy and fill in your API keys
cp .env.example .env
# See SETUP.md for token URLs and required scopes

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Validate configuration
python3 em_intel.py doctor

# 4. Preview with mock data (no credentials needed)
python3 em_intel.py morning-brief --dry-run

# 5. Run for real
python3 em_intel.py morning-brief
```

## Commands

| Command | Description |
|---------|-------------|
| `doctor` | Check env vars and test API connections |
| `morning-brief [--dry-run]` | Merged yesterday, open PRs >3d, quiet engineers, stalled epics |
| `eod-review [--dry-run]` | Today's merges/opens, contributor list, cycle time trend |
| `team-report [--days N] [--dry-run]` | Full team performance report |
| `contributions [--engineer NAME] [--days N] [--dry-run]` | Branch→ticket contribution map |
| `quiet-engineers [--dry-run]` | Engineers with no MR activity |
| `epic-health [--dry-run]` | Stalled and unassigned epics |
| `newsletter [--week]` | Weekly digest via configured delivery channel |

### --dry-run

Pass `--dry-run` to any supported command to use realistic synthetic mock data instead of hitting real APIs. Useful for previewing output format before configuring credentials.

## Configuration

Set `EM_CODE_PROVIDER` to `gitlab` or `github`, and `EM_TICKET_PROVIDER` to `jira` or `github_issues`.

Delivery channels: `telegram`, `slack`, `email`, or `print` (stdout fallback).

See `.env.example` for all configuration options.

## Architecture

```
em_intel.py          ← CLI entrypoint (argparse)
adapters/            ← Code platform + ticket system adapters
  base.py            ← Abstract base classes & data models
  gitlab_adapter.py  ← GitLab REST API
  github_adapter.py  ← GitHub REST API
  jira_adapter.py    ← Jira REST API
  github_issues_adapter.py ← GitHub Issues as ticket system
  mock_adapter.py    ← Synthetic data for --dry-run mode
core/                ← Business logic
  branch_mapper.py   ← Map branches → tickets → engineers
  team_pulse.py      ← Quiet engineers, MR trends, cycle times
  jira_health.py     ← Stale epics, unassigned tickets, PR age
  newsletter.py      ← Weekly digest generation
  delivery.py        ← Telegram / Slack / Email / Print routing
commands/            ← Command implementations
  morning_brief.py   ← Morning briefing
  eod_review.py      ← End-of-day review
  team_report.py     ← Full team report
  newsletter.py      ← Newsletter generation & delivery
```
