---
name: competitor-monitor
description: Monitor competitors' websites, social media, pricing, and product changes automatically. Use when the user wants to track competitor activity, detect website changes, monitor pricing updates, track new features or blog posts, get alerts on competitor moves, or conduct ongoing competitive intelligence. Supports scheduled checks with configurable alert channels.
---

# Competitor Monitor

Autonomous competitive intelligence for your agent.

## Quick Start

Add a competitor to track:
```bash
python3 scripts/monitor.py add --name "Acme Corp" --url https://acme.com --track pricing,blog,changelog
```

Run a check:
```bash
python3 scripts/monitor.py check --all
```

## Commands

### Add Competitor
```bash
python3 scripts/monitor.py add \
  --name "Competitor" \
  --url https://competitor.com \
  --track pricing,blog,changelog,features,social \
  --social-twitter @competitor \
  --check-interval 6h
```

### Check All Competitors
```bash
python3 scripts/monitor.py check --all
python3 scripts/monitor.py check --name "Acme Corp"
```

### View Change History
```bash
python3 scripts/monitor.py history --name "Acme Corp" --days 30
```

### Generate Report
```bash
python3 scripts/monitor.py report --format markdown --period week
```

## What Gets Tracked

| Signal | How | Alert When |
|--------|-----|------------|
| Pricing changes | Page diff on pricing URL | Any text change detected |
| Blog/changelog | RSS feed or page diff | New entries |
| Feature launches | Changelog + social monitoring | New announcements |
| Social activity | X/Twitter mentions and posts | Significant posts |
| SEO changes | Title/meta/H1 diffs | Structure changes |
| Tech stack | Built-with detection | Stack changes |

## Configuration

Stored at `~/.openclaw/competitor-monitor.json`:
```json
{
  "competitors": [
    {
      "name": "Acme Corp",
      "url": "https://acme.com",
      "pricingUrl": "https://acme.com/pricing",
      "blogUrl": "https://acme.com/blog",
      "twitter": "@acme",
      "trackingTypes": ["pricing", "blog", "changelog", "social"],
      "checkInterval": "6h"
    }
  ],
  "alertChannel": "telegram",
  "diffThreshold": 0.05
}
```

## Scheduling

Set up as a heartbeat task or cron:
```
# Check competitors every 6 hours
python3 scripts/monitor.py check --all --quiet --alert-changes
```

## Alert Format

When changes detected:
```
COMPETITOR ALERT: Acme Corp
Change type: Pricing
Detected: 2026-03-06 14:30 EST
Summary: Enterprise plan price increased from $99/mo to $129/mo
Diff: [link to stored diff]
```

## Advanced: Competitive Intelligence Reports

See `references/ci-templates.md` for weekly/monthly report templates that synthesize all tracked changes into actionable intelligence briefs.
