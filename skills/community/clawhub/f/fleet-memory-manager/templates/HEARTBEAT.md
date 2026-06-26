# HEARTBEAT.md — Heartbeat Configuration

<!--
=============================================================================
HEARTBEAT CONFIGURATION
=============================================================================

Heartbeats are periodic polls from OpenClaw — typically every 15-30 minutes.
When you receive one, you have a choice: do something useful, or reply HEARTBEAT_OK.

This file defines WHAT to do when a heartbeat arrives. Think of it as a
checklist that the agent runs through and decides which items need attention.

WHY USE HEARTBEATS FOR MEMORY:
  The nightly consolidation cron handles deep MEMORY.md updates.
  Heartbeats handle the smaller, more frequent checks:
  - Is a project going stale?
  - Are there active blockers nobody's addressed?
  - Is memory getting too long?

  Together: cron = nightly deep review, heartbeat = daytime health checks.

HOW TO CUSTOMIZE:
  1. Replace the example projects with your actual active projects
  2. Adjust thresholds (48h stale, 500 line limit) to your preference
  3. Remove sections you don't need
  4. Add sections for things you want to monitor

HEARTBEAT TIMING:
  Don't do expensive checks every heartbeat. Use heartbeat-state.json to
  track when you last checked each thing, and skip checks done recently.

  Rule of thumb:
  - Light checks (new messages, quick status): every heartbeat OK
  - Medium checks (project status, email): every 2-4 hours
  - Heavy checks (memory health, consolidation review): daily/weekly
=============================================================================
-->

## Active Project Monitoring

<!--
Check these projects at most every 4 hours. Track last check in heartbeat-state.json.

For each project:
  - If status is BLOCKED → surface the blocker to the human
  - If last updated > 48 hours and status is IN_PROGRESS → flag as stale
  - If status is COMPLETE but not archived → prompt to archive
-->

### Projects to Monitor

<!-- [CUSTOMIZE] Replace with your actual active projects -->

- **[Project Alpha]** — [One-line description]
  - Check: `memory/<today>.md` → Active Projects section
  - Stale threshold: 48h
  - Channel to notify: [Discord channel name or ID]

- **[Project Beta]** — [One-line description]  
  - Check: [Where to check status — file path, API, etc.]
  - Stale threshold: 72h
  - Channel to notify: [Channel]

<!-- Add more projects as needed -->

### Project Status Logic

When checking projects, apply this logic:

```
IF project.status == BLOCKED AND last_surfaced > 2h ago:
  → Notify human: "⚠️ [Project] is blocked: [blocker description]"
  → Update heartbeat-state.json with notification timestamp

IF project.lastUpdated > staleThreshold AND project.status == IN_PROGRESS:
  → Notify human: "📊 [Project] hasn't been updated in X hours — still active?"
  → Only once per stale period (don't spam)

IF project.status == COMPLETE AND NOT archived:
  → Remind once: "[Project] is marked complete — archive the daily notes?"
```

---

## Memory Health Check

<!--
Run this check weekly (Sundays are good, low-activity day).
Track last run in heartbeat-state.json under "memoryHealth".
-->

### Weekly Memory Health (run if >7 days since last check)

1. **Check MEMORY.md size:**
   ```
   IF line_count(MEMORY.md) > 500:
     → Notify human: "📚 MEMORY.md is getting long ([N] lines). Consider pruning stale sections."
   ```

2. **Check daily notes folder:**
   ```
   IF any files in memory/ are older than 30 days AND not in archive/:
     → Notify human: "🗂️ [N] daily note files older than 30 days. Archive to memory/archive/?"
   ```

3. **Check consolidation recency:**
   ```
   IF last_consolidation > 7 days ago:
     → Notify human: "🔄 Last memory consolidation was [N] days ago. Run cron manually?"
   ```

4. **Report health summary:**
   ```
   "Memory health: [N] daily files, MEMORY.md [N] lines, last consolidated [date]"
   ```

---

## Routine Checks

<!--
Light checks that are cheap to run. Do these in batches — one heartbeat,
multiple checks. Only surface results that actually need attention.
-->

### Email Check (every 2-4 hours during active hours)
- Check for urgent unread messages
- Surface only: flagged mail, known-important senders, anything marked urgent
- Skip: newsletters, automated notifications, anything that can wait

### Calendar Check (twice daily — morning + afternoon)
- Upcoming events in next 24h
- Surface only: events in <2h that haven't been acknowledged
- Skip: events already discussed, recurring meetings already on radar

### Weather (once daily if location-relevant)
- Surface only: significant weather that might affect plans
- Skip: ordinary weather with no impact

---

## When to Reach Out vs. Stay Silent

### Reach Out When:
- Active project has been BLOCKED for >2h
- Important email arrived from known-important sender
- Calendar event coming up in <2h
- Memory health check found issues
- It's been >8h since any agent activity and human is likely online

### Stay Silent (HEARTBEAT_OK) When:
- Late night or early morning (23:00–08:00)
- All projects are IN_PROGRESS with no blockers
- Nothing new since last check
- You just checked <30 minutes ago
- The human is clearly in a session and focused

---

## Heartbeat State File

Track check timestamps in `memory/heartbeat-state.json`:

```json
{
  "lastChecks": {
    "email": 1703275200,
    "calendar": 1703260800,
    "weather": null,
    "projects": 1703272000,
    "memoryHealth": 1703100000
  },
  "installDate": "2024-01-01T00:00:00Z",
  "lastConsolidation": null,
  "notifications": {
    "projectAlpha_stale": null,
    "memoryOverLimit": null
  }
}
```

Update this file after each check. It's cheap and prevents duplicate notifications.

---

## Examples From Production: Bot Fleet Heartbeat

In our 7-bot fleet, Harrison (orchestrator) runs these checks during heartbeats:

**Every heartbeat:**
- Scan Discord for unread @mentions
- Check if any bot's last message was >4h ago (may be stuck)

**Every 4 hours:**
- Check active trading bot status (is it running? any errors?)
- Check YouTube pipeline queue (any videos stuck in processing?)

**Daily (morning):**
- Memory health report
- Active project roundup with status summary
- Any pending PRs or GitHub notifications?

**Weekly (Sunday):**
- Full MEMORY.md audit — prune stale content
- Archive daily notes >30 days old
- Review USER.md for any patterns to add

This batching approach means Harrison surfaces ~3-5 useful notifications per day
instead of spamming every 15 minutes.

---

*Managed by memory-manager skill | Customize for your active projects*