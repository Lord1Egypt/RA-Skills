---
name: auto-updater
description: Automatically keep OpenClaw and installed workspace skills up to date using native OpenClaw commands. Use when the user wants automatic update checks, scheduled maintenance, daily skill updates, recurring OpenClaw update workflows, or a cron-based self-update routine for OpenClaw.
metadata: {"openclaw":{"emoji":"🔄","os":["win32","linux","darwin"]}}
---

# OpenClaw Auto-Updater

Use this skill to set up or run **native OpenClaw update routines**.

This skill is for **OpenClaw**, not legacy Clawdbot/ClawdHub setups. Prefer these commands:

- `openclaw update ...` for OpenClaw itself
- `openclaw skills update ...` for installed skills
- `openclaw cron ...` for scheduling

## What to do

When the user asks for automatic updates:

1. Check whether they want:
   - OpenClaw core updates
   - skill updates
   - both
2. Prefer **native OpenClaw commands** over legacy `clawdbot` / `clawdhub` commands.
3. If scheduling is requested, create a cron job with `openclaw cron add` or the cron tool. Prefer binding the job to the current session when the user wants the summary to come back to the same chat.
4. Make the cron message ask for:
   - current OpenClaw version before/after (if updated)
   - which skills were updated
   - any failures or skipped items
5. Keep summaries short and readable.

## Safe default behavior

Default recommendation:

- Update **skills** automatically
- Leave **OpenClaw core binary/app updates** as opt-in unless the user explicitly wants automatic core updates too

Reason: skill updates are lower risk than changing the OpenClaw runtime itself.

## Native command patterns

### Check OpenClaw status/version

```bash
openclaw --version
openclaw status
```

### Update installed skills

```bash
openclaw skills update <slug>
openclaw skills update --all
```

### Inspect skills first

```bash
openclaw skills list
openclaw skills check
```

### Check/update OpenClaw itself

```bash
openclaw update --help
```

Only automate core updates after the user explicitly asks.

## Cron template: skills-only auto-update

For lower rate-limit pressure, prefer updating skills one by one instead of always starting with `--all`. Recommended example:

```bash
openclaw cron add \
  --name "Daily Skills Auto-Update" \
  --cron "0 4 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --announce \
  --message "Run the daily OpenClaw skills maintenance routine. Use native OpenClaw commands only. Prefer a gentle strategy: first identify tracked ClawHub-installed skills, then run openclaw skills update <slug> one by one, record updated/current/failed items, and if 429 Rate limit exceeded appears, explain it is a ClawHub remote rate limit and stop the rest of this run. Do not use legacy clawdbot or clawdhub commands." \
  --light-context
```

## Cron template: core + skills update

Only use this if the user explicitly wants OpenClaw itself updated automatically.

```bash
openclaw cron add \
  --name "Daily OpenClaw Auto-Update" \
  --cron "0 4 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --announce \
  --message "Run the daily OpenClaw maintenance routine using native OpenClaw commands only. Steps: (1) record the current OpenClaw version, (2) inspect whether OpenClaw core update commands are available and apply updates only through supported OpenClaw update flows, (3) update tracked skills gently, preferably with openclaw skills update <slug> one by one instead of blindly starting with --all, (4) if 429 Rate limit exceeded appears, say it is a ClawHub remote rate limit and stop the rest of this run, (5) report version before/after, updated skills, already-current skills, and failures. Do not use legacy clawdbot or clawdhub commands." \
  --light-context
```

## Reporting format

Use a compact report like:

```text
🔄 OpenClaw Update Complete

OpenClaw: unchanged / updated <before → after>
Skills updated: <list>
Already current: <list or count>
Issues: <none or short list>
```

## Notes

- Prefer `openclaw cron` over ad-hoc shell schedulers when the user wants in-product automation.
- Prefer isolated cron jobs for maintenance tasks, but prefer current-session binding when the user expects the summary back in the same chat.
- When ClawHub rate limits are likely, prefer `openclaw skills update <slug>` one by one before resorting to `--all`.
- If a command requires user approval or elevated access, stop and ask.
- If the user only asked to install this skill, do not create the cron job automatically.
