---
name: freelance-job-scraper
description: "Autonomous freelance job monitoring agent. Scans Hacker News Who is Hiring, YC jobs board, and remote job aggregators for high-value automation and AI gigs, scores them by relevance and payout, and flags actionable leads."
version: "1.0.0"
tags: ["freelance", "jobs", "automation", "scraping", "hacker-news", "yc", "remote"]
---

# Freelance Job Scraper

Scans multiple job boards and freelance platforms for AI/automation-related gigs. Scores each opportunity by relevance, payout, and competition level.

## What It Does

- Scrapes HN "Who is Hiring" monthly threads
- Monitors YC jobs board for automation/AI-related postings
- Checks remoteok.com, weworkremotely.com for relevant gigs
- Scores opportunities by payout, competition, and AI fit
- Generates a prioritized daily digest report

## Prerequisites

- `gh` CLI authenticated (for HN comments/jobs access)
- Python 3.6+ (standard library only)
- Browser or web fetch for job board scraping

## Quick Start

```bash
# Scan all sources and generate report
python3 scripts/scan_jobs.py

# Filter by keyword
python3 scripts/scan_jobs.py --keyword "automation"

# Output to file
python3 scripts/scan_jobs.py --output freelance_leads.md
```

## Scoring Criteria

| Score | Factor |
|-------|--------|
| High payout ($100+) | +3 pts |
| AI/automation relevant | +3 pts |
| Remote OK | +1 pt |
| Few competition (fewer replies) | +2 pts |
| YC company | +2 pts |

## Output Format

```markdown
## Freelance Lead Digest — 2026-03-27

### 🔥 Hot Leads (score >= 7)
1. **[Company] — Role/Task** | $AMOUNT | YC | 3 replies
   - Link: https://...
   - Why: AI/automation fit

### 🎯 Medium Leads (score 4-6)
...

### 💤 Low Priority
...
```

## Architecture

- `scripts/scan_jobs.py` — Main scraper (Python stdlib only)
- `references/hn_jobs_guide.md` — How to navigate HN jobs
- Uses `gh api` for HN content, web fetch for external boards
