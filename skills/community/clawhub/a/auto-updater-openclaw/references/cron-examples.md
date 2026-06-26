# OpenClaw Auto-Updater Cron Examples

## Daily skills-only update

Prefer a gentler per-skill update strategy when ClawHub rate limits are a concern.

```bash
openclaw cron add \
  --name "Daily Skills Auto-Update" \
  --cron "0 4 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --announce \
  --light-context \
  --message "Run the daily OpenClaw skills maintenance routine. Use native OpenClaw commands only. First identify tracked ClawHub-installed skills, then run openclaw skills update <slug> one by one, record updated/current/failed items, and if 429 Rate limit exceeded appears, explain it is a ClawHub remote rate limit and stop the rest of this run. Do not use legacy clawdbot or clawdhub commands."
```

## Daily core + skills update

```bash
openclaw cron add \
  --name "Daily OpenClaw Auto-Update" \
  --cron "0 4 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --announce \
  --light-context \
  --message "Run the daily OpenClaw maintenance routine using native OpenClaw commands only. Steps: (1) record the current OpenClaw version, (2) inspect whether OpenClaw core update commands are available and apply updates only through supported OpenClaw update flows, (3) update tracked skills gently, preferably with openclaw skills update <slug> one by one instead of blindly starting with --all, (4) if 429 Rate limit exceeded appears, say it is a ClawHub remote rate limit and stop the rest of this run, (5) report version before/after, updated skills, already-current skills, and failures. Do not use legacy clawdbot or clawdhub commands."
```

## Weekly safer schedule

```bash
openclaw cron add \
  --name "Weekly Skills Auto-Update" \
  --cron "0 30 3 * * 1" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --announce \
  --light-context \
  --message "Run the weekly OpenClaw skills maintenance routine with native OpenClaw commands only. Prefer updating tracked skills one by one with openclaw skills update <slug>. If 429 Rate limit exceeded appears, explain it is a ClawHub remote rate limit and stop the rest of this run. Provide a short summary at the end."
```

## Same-chat summary preference

If the user wants the summary to come back to the same conversation, prefer binding the job to the current session instead of relying only on generic announce delivery.
