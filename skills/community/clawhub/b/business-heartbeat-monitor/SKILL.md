---
name: business-heartbeat-monitor
description: HEARTBEAT.md framework for continuous business monitoring — sites, services, inbox, payments, processes, and revenue.
---

# Business Heartbeat Monitor

Your agent runs heartbeats on a schedule. Each cycle is an opportunity to check on everything that matters and fix what's broken — before anyone notices.

This skill provides a complete HEARTBEAT.md framework for business operations monitoring.

## Core HEARTBEAT.md Template

```markdown
## Production Site Health (every heartbeat)
1. Check all production URLs for 200 status with expected content:
   - yoursite.com — expect 200 + contains "Your Brand"
   - app.yoursite.com — expect 200
   - api.yoursite.com/health — expect 200 + {"status":"ok"}
2. If any fail:
   - Attempt restart (via deployment redeploy, service restart, etc.)
   - If auto-recovery works: log to daily notes, move on
   - If auto-recovery fails: alert immediately on primary channel
3. Log all results to daily notes

## Service & Infrastructure Health (every heartbeat)
1. Check critical background services are running
   - Database connections responding
   - Queue workers processing
   - Cron jobs firing on schedule
2. If a service is down:
   - Attempt restart
   - If restart fails: alert with error details
3. If a process has been stalled for 2+ consecutive heartbeats:
   - Kill and restart automatically
   - Log the stall duration and any error output

## Support SLA Check (every heartbeat)
1. Scan inbox for unanswered customer messages
2. Flag any message older than your SLA threshold (e.g., 4 hours)
3. For routine questions (order status, how-to, account access):
   - Draft a response
   - Send if within Tier 1 autonomy, otherwise flag for review
4. For complex issues:
   - Summarize the problem
   - Flag for human review with recommended action

## Payment & Revenue Check (every heartbeat, summarize nightly)
1. Check for failed payments or declined charges
2. Flag any for retry or customer follow-up
3. Track daily revenue running total
4. Note any anomalies (unusual spikes, drops, large transactions)

## Background Process Health (every heartbeat)
1. Check for any listed active processes (tmux sessions, workers, agents)
2. For each: verify it's still running
3. If dead: restart automatically, log what happened
4. If stalled (same output for 2+ checks): kill and restart
5. If completed successfully: report completion, clean up
```

## Nightly Deep Dive Template

Run once per day (e.g., 3 AM):

```markdown
## Nightly Deep Dive (~3 AM)

### Revenue Review
1. Pull yesterday's complete revenue data
2. Break down by product/service
3. Compare to trailing 7-day and 30-day averages
4. Note what sold, what didn't, any patterns

### Day Review
1. What got done from today's plan?
2. What didn't get done and why?
3. What blocked progress?

### Tomorrow's Plan
1. Propose 3-5 concrete priorities ranked by expected impact
2. Each item should connect to a clear business goal
3. Include execution tasks and growth experiments
4. Write to tomorrow's daily notes file

### Health Summary
1. Uptime: percentage across all monitored services
2. Incidents: any outages or degradations, with resolution
3. Support: messages handled, average response time
4. Revenue: daily total, trend direction
```

## Integration with Autonomy Ladder

The monitoring system works best when paired with clear autonomy tiers:

| Monitor Finding | Autonomy Tier | Action |
|----------------|---------------|--------|
| Site returning 500 | Tier 1 | Fix + log |
| Background process crashed | Tier 1 | Restart + log |
| Support email >4 hours | Tier 1/2 | Draft response, send if routine |
| Payment failed | Tier 2 | Retry + report |
| Revenue anomaly | Tier 2 | Investigate + report |
| Service architecture issue | Tier 3 | Diagnose + propose fix |
| Customer escalation | Tier 3 | Summarize + flag |

## Daily Notes Format

Each heartbeat should append to the day's notes:

```markdown
## Heartbeat — 3:15 PM

### Health
- ✅ All sites returning 200
- ✅ All services healthy
- ⚠️ Worker queue backed up (47 pending, normally <10)
  - Cause: spike in API requests from new integration
  - Action: scaled workers from 2 → 4, queue clearing

### Support
- 2 new messages since last check
- Replied to order status inquiry (Tier 1, auto-sent)
- Flagged billing dispute for review (Tier 3)

### Revenue
- Running total: $342 (vs $289 yesterday at this time)
```

## Setup Checklist

1. Copy the HEARTBEAT.md template above
2. Replace example URLs with your actual production endpoints
3. Set your SLA threshold (4 hours is a good default)
4. Configure alerting channel (Telegram, Discord, Slack, etc.)
5. Define which background processes to monitor
6. Set your nightly deep dive time (2-4 AM recommended)
7. Pair with the Autonomy Ladder for escalation rules

## Tips

- **Start with site health only.** Get that working reliably before adding inbox triage and revenue tracking. Each layer of monitoring adds complexity.
- **Don't alert on everything.** The goal is signal, not noise. If your agent sends 15 "all clear" messages a day, you'll start ignoring them — and miss the one that matters.
- **Log everything, alert selectively.** Every heartbeat result goes in daily notes. Only failures and anomalies get sent to your channel.
- **Review weekly.** Check the daily notes for patterns. If the same service keeps restarting, that's not a monitoring success — it's an infrastructure problem to fix.
