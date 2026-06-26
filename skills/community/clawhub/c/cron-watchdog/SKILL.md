---
name: watchdog
description: Monitor all OpenClaw cron jobs for failures and auto-fix common errors (model-not-allowed, timeouts). Posts to Slack only when issues are found. Runs every 6 hours. Use when you need automated cron health monitoring and self-healing.
metadata:
  openclaw:
    emoji: "🐺"
    requires:
      tools:
        - cron
        - message
---

# Watchdog — Cron Health Monitor

Monitors all cron jobs for failures and auto-fixes them. Posts to Slack only when issues are found or unfixable errors exist.

## CRITICAL: Slack Routing

When sending messages to Slack, you MUST specify `channel: "slack"` in every message tool call:

```
message(action: "send", channel: "slack", target: "C0AHYTV5WP7", message: "...")
```

Without `channel: "slack"`, messages will fail silently.

## Schedule

Every 6 hours: 5, 11, 17, 23 CT

## Steps

1. `cron(action: "list")` — get all jobs and their current status
2. For each job, check: `lastStatus` error? `consecutiveErrors > 0`? What was `lastError`?
3. For **model not allowed** errors: use `cron(action: "update", jobId: "...", patch: { payload: { model: "anthropic/claude-sonnet-4-6" } })`, then force-run, log change
4. For **timeout errors**: use `cron(action: "update", jobId: "...", patch: { payload: { timeoutSeconds: <current + 60> } })` — NEVER edit cron JSON files directly
5. For **other errors**: analyze, attempt fix if possible, or flag as unresolved
6. Post to Slack `C0AHYTV5WP7` (#morning-briefs) **ONLY if issues were found/fixed or unfixable errors exist**
7. If everything is healthy: no Slack message (silent pass)

## CRITICAL: Never Edit cron/jobs.json Directly

Always use the `cron` tool with `action="update"` to modify job settings. Direct file edits break the cron system.

## Slack Alert Format

```
🐺 Watchdog Report — <timestamp>

✅ Fixed: <job-name> — <what was fixed>
❌ Unfixable: <job-name> — <error summary>
⚠️ Flagged: <job-name> — <issue description>
```

Only send if at least one issue exists.
