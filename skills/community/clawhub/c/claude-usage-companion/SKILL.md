---
name: claude-usage-companion
description: >-
  Monitor your Claude programmatic credit pool and align your interactive window — on your
  always-on box. Since June 2026 Anthropic meters non-interactive usage (Claude Agent SDK,
  `claude -p`, Claude Code GitHub Actions, third-party agents) from a SEPARATE monthly credit
  pool ($20 Pro / $100 Max 5x / $200 Max 20x, API rates, no rollover) instead of your 5-hour
  interactive window. claude-usage-companion (1) tracks that credit pool — month-to-date burn,
  projected month-end spend, and an alert before you run dry so automations don't stop
  unexpectedly; and (2) reminds you, the human, at your anchor time to send your first
  interactive prompt so your 5-hour window lines up with your working day. Use this skill when
  the user mentions Claude usage limits, the programmatic/Agent-SDK credit pool, running out of
  credits, monitoring claude -p or GitHub Actions spend, ccusage, usage reports, budgeting Claude
  automation on a VPS, or wants to align/start their interactive session window. It only reports
  and reminds — it never automates the model or circumvents any limit.
---

# claude-usage-companion

Keep your Claude usage on an always-on box healthy after the **June 2026 usage split** — when
programmatic usage (`claude -p`, Agent SDK, GitHub Actions, third-party agents) moved onto a
**separate monthly credit pool** instead of your interactive 5-hour window.

It does two clean, hands-off jobs:

1. **Monitor the credit pool** — month-to-date burn, projected month-end spend, and an alert
   when you're on track to exhaust it (the pool has **no rollover**; when it's gone, automated
   requests stop).
2. **Remind you to align your interactive window** — at your anchor time it nudges *you* (a
   human) to send your first prompt, so your 5-hour window tracks your working day.

> Replaces `claude-session-warmer`. That skill primed the interactive window with `claude -p`,
> which **no longer works**: as of ~June 15 2026 `claude -p` draws from the separate credit pool
> and does not anchor the 5-hour interactive window. This companion is the honest successor —
> it never automates the model and never circumvents a limit; it only **reports** and **reminds**.

## What it is NOT

No automated priming of the window, no scripted interactive input, no token/credential tricks,
no limit circumvention. Usage data is read locally with `ccusage` (a parse of `~/.claude` — no
model calls, no window side effects). Cost is USD at API rates, the same basis as the credit pool.

## Prerequisite

An always-on box (the VPS where you run OpenClaw / Claude Code) with **Node 18+** and
[`ccusage`](https://github.com/ryoppippi/ccusage). Fast path: `npm i -g ccusage`.

## Setup — 1, 2, 3

Run on the box, from the skill folder.

**1. Tell it your timezone, plan, and start time.**
```bash
cp config.example.json config.json
# edit: "timezone" (e.g. "Africa/Johannesburg"), "plan" (pro | max5x | max20x),
#       and "anchor" (the local time you start work, e.g. "08:00")
```

**2. Check the box and see your burn.**
```bash
node bin/usage-companion.mjs check     # verifies node + ccusage + reads your usage
node bin/usage-companion.mjs report    # month-to-date burn, projection, top models
```

**3. Schedule it.**
```bash
node bin/usage-companion.mjs install   # prints a ready-to-paste cron block
crontab -e                             # paste it, save
```
Now the box checks your credit pool a few times a day (alerting only when you cross a threshold)
and reminds you at your anchor time to start your interactive session.

## Commands

- `check` — verify Node + `ccusage` are available and config is valid (run first).
- `report` — month-to-date spend, projected month-end, top models (no side effects).
- `guard` — evaluate thresholds; alert only if over `warn_pct`/`critical_pct` (what cron runs).
- `remind` — emit the anchor-time "start your session" nudge (what cron runs).
- `status` — show config and next scheduled actions.
- `install [--cron-only]` — print the cron block (`--cron-only` is pipeable to `crontab -`).

## Configuration (`config.json`)

| Field | Meaning | Default |
|---|---|---|
| `timezone` | IANA tz for all clock math — **set this** | `UTC` |
| `plan` | `pro` / `max5x` / `max20x` → sets the credit cap ($20/$100/$200) | `max5x` |
| `monthly_credit_usd` | Override the cap if your number differs | `null` |
| `warn_pct` / `critical_pct` | Alert thresholds (% of cap, actual or projected) | `80` / `95` |
| `anchor` | Local time you start work (window reminder) | `08:00` |
| `reminder_enabled` | Send the anchor-time nudge | `true` |
| `alert_command` | Shell command to receive alerts on stdin (e.g. post to Slack). `null` = stdout + `companion.log` | `null` |
| `ccusage_cmd` | How to invoke ccusage | `["npx","-y","ccusage@latest"]` |

For your exact remaining balance, the authoritative source is the **"Usage credits"** line in
`/usage` inside Claude Code; `report`/`guard` approximate the pool from local ccusage cost, which
on an always-on automation box is essentially all programmatic.

## Files

- `bin/usage-companion.mjs` — the engine (Node; only external tool is `ccusage`).
- `config.example.json` — copy to `config.json` and edit.
- `README.md` — public overview.
