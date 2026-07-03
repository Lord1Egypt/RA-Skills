---
name: cron-scripts
description: Run bash scripts on a schedule without LLM involvement. Zero model cost, hot-reload, pure shell. A workaround until openclaw/openclaw#80793 lands.
---

# cron-scripts 🕐

**Run bash scripts on a schedule — no LLM, no agent turns, zero model cost.**

This is a practical workaround for the missing `payload.kind: "script"` in OpenClaw cron
([issue #80793](https://github.com/openclaw/openclaw/issues/80793),
[issue #18160](https://github.com/openclaw/openclaw/issues/18160)).
It uses a gateway startup hook to load a directory of shell scripts and schedule them with
the same `croner` library OpenClaw already bundles — no extra dependencies.

## When to use this (not LLM crons)

| Use script cron | Use LLM cron |
|----------------|--------------|
| Health checks, HTTP pings | Summarising logs |
| File/lock cleanup | Deciding what to report |
| Fixed Telegram/webhook notifications | Writing weekly digests |
| Git pulls, backups | Any task needing reasoning |
| Watching directories for changes | Classifying content |

If a task doesn't need a brain, it shouldn't spin up one.

## Installation

### 1. Install the gateway hook

Copy `hooks/cron-scripts-loader/handler.ts` from this skill into your OpenClaw hooks directory:

```bash
mkdir -p ~/.openclaw/hooks/cron-scripts-loader
cp <skill-dir>/hooks/cron-scripts-loader/handler.ts \
   ~/.openclaw/hooks/cron-scripts-loader/handler.ts
```

Then restart the gateway:

```bash
openclaw gateway restart
```

The hook registers itself on `gateway.startup` and begins watching
`~/.openclaw/cron-scripts/` immediately. No further config needed.

### 2. Create your scripts directory

```bash
mkdir -p ~/.openclaw/cron-scripts
```

The hook creates this automatically on first startup, but creating it now lets you
add scripts before restarting.

## Writing scripts

Every script needs a short frontmatter block in the first 20 lines:

```bash
#!/usr/bin/env bash
# name: my-job          # required — shown in gateway logs
# schedule: 0 8 * * *  # required — standard 5-field cron expression
# tz: Europe/Berlin     # optional — IANA timezone (default: UTC)
# timeout: 120          # optional — seconds before SIGTERM (default: 120)

# ... your script here
```

The cron expression is written in **wall-clock time** of the given `tz` — do **not**
convert to UTC yourself.

Then drop it in `~/.openclaw/cron-scripts/` and make it executable:

```bash
chmod +x ~/.openclaw/cron-scripts/my-job.sh
```

**No restart needed.** The hook watches the directory with `fs.watch` and hot-reloads
within ~300ms of any file change.

## Sending notifications from scripts

Scripts can post to any OpenClaw channel via the local announce API:

```bash
# Post to a Telegram user
curl -sf -X POST http://localhost:3000/api/announce \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello from script cron\", \"channel\": \"telegram\", \"to\": \"<YOUR_CHAT_ID>\"}"
```

Or call external services directly (Telegram Bot API, Slack webhooks, etc.).

## Disabling / deleting a job

- **Disable:** rename to `my-job.sh.disabled` — the watcher ignores non-`.sh` files
- **Delete:** remove the file — job stops within 300ms, no restart needed

## Logs

All script output is captured and forwarded to the gateway log under
`[cron-scripts-loader][<name>]`:

```
[cron-scripts-loader][my-job] Starting run
[cron-scripts-loader][my-job] some stdout line
[cron-scripts-loader][my-job] Finished ok (exit 0)
```

Non-zero exit codes are logged as errors but never crash other jobs.

## Example script

See `examples/health-check.sh` for a minimal HTTP health check that posts failures
to Telegram.

## Constraints

- Scripts run as the same user as the gateway process
- Pure bash — no access to the OpenClaw tool system
- If a previous run is still active when the next tick fires, the new run is **skipped**
  (croner `protect: true`) to prevent pile-ups
- Relies on `croner` from OpenClaw's own `node_modules` — tested against OpenClaw
  2026.x; if croner moves, update the require path in the hook

## Context

This skill was built as a workaround for:

- [#80793 — Support script target type in openclaw cron](https://github.com/openclaw/openclaw/issues/80793)
- [#18160 — Direct Exec Mode for Cron Jobs](https://github.com/openclaw/openclaw/issues/18160)

If those issues are resolved natively, this skill becomes unnecessary. Until then,
it's the cleanest way to keep your cron inventory unified in one place without
burning model tokens on tasks that are pure bash.
