# HEARTBEAT.md — Cron Schedule

## Schedule

| Trigger | Frequency | Action |
| :--- | :--- | :--- |
| CEO Heartbeat | Hourly, 9-18 UTC, Mon-Fri | Fetch GitHub Issues, analyze, delegate |
| Pulse Signal | Daily, 08:30 UTC | Generate daily news synthesis |
| Performance Review | Weekly, Monday 09:00 UTC | Review published content metrics |
| Competitor Scan | Daily, 07:00 UTC | Scan competitor publications |

## Heartbeat Checklist

When the CEO Agent wakes up:

1. Run `gh issue list --repo YOUR_ORG/YOUR_REPO --state open --limit 10`
2. For each new issue: read body, assemble context, write analysis comment
3. Check pulse/signals/ for latest signals
4. Check ops/social/published_posts.json for recent metrics
5. Create and assign sub-agent tasks as needed
6. Update MEMORY.md with any strategic insights

## Cron Configuration (VPS)

```bash
# Edit crontab
crontab -e

# CEO heartbeat: every hour during business hours
0 9-18 * * 1-5 cd /path/to/emergence-agent-ceo && openclaw run --skill ceo-heartbeat

# Daily pulse: every morning at 08:30 UTC
30 8 * * * cd /path/to/emergence-agent-ceo && openclaw run --skill pulse-generate

# Weekly performance review: Monday 09:00 UTC
0 9 * * 1 cd /path/to/emergence-agent-ceo && openclaw run --skill performance-review
```
