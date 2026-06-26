---
name: claude-session-warmer
description: >-
  Align your Claude Pro/Max usage window to your working hours. Claude's 5-hour
  usage window is anchored to your FIRST message of a session, so claude-session-warmer
  fires a tiny "primer" prompt through the official Claude Code CLI on your always-on
  box (the VPS where you already run OpenClaw + Claude Code) at chosen anchor times —
  e.g. 05:00, then each time a window closes — so a fresh window is already open when
  you start work and your resets line up with your day. Use this skill whenever the user
  mentions usage windows, the 5-hour limit, usage resets, "warming up" or "pre-starting"
  their Claude session/window, aligning Claude limits to working hours, getting maximum
  use out of a Pro/Max plan, or wants to set up or change a warm-up/primer schedule on a
  VPS. It only shifts WHEN the window opens — it never exceeds quota.
---

# claude-session-warmer

Make your Claude Pro/Max usage window start *when you want it to* — not whenever your
first prompt of the day happens to land.

## What it does (and explicitly does not do)

Claude meters usage in a **rolling 5-hour window anchored to your first message**. Start
at 09:40 and your window is 09:40–14:40; your afternoon reset is pinned there. Send one
trivial **primer** at 05:00 instead and the window opens 05:00–10:00 — a fresh window is
already waiting when you sit down, and every reset that day lines up with your working
hours.

claude-session-warmer sends that primer through the **official `claude` CLI**, on a
schedule, **on your always-on box** — the same VPS where you already run OpenClaw and an
authenticated Claude Code. (A laptop is the wrong host: it's asleep when you're not
working, so it can't fire the early primer. The whole point is a machine that's always
on.)

It does **not** bypass or beat any limit. You cannot exceed the 5-hour cap or the weekly
cap, and this skill does not try to — it only changes **when** the window opens. That
distinction is what keeps it inside Anthropic's terms; read `references/tos.md` before
publishing or sharing.

## Prerequisite (you almost certainly already have this)

The box must have the **official Claude Code CLI installed and logged in** to your
Pro/Max subscription — exactly the setup you already use to develop with OpenClaw on that
VPS. If `claude -p "hi"` answers on that box, you're ready. **Do not** copy auth tokens
from another machine — log in on the box itself via the official flow (that token-copying
is the one thing Anthropic enforces against; see `references/tos.md`).

## Setup — 1, 2, 3

Run these on the VPS, from the skill's folder.

**1. Tell it your timezone and start time.**
```bash
cp config.example.json config.json
# edit config.json: set "timezone" (e.g. "Africa/Johannesburg"), your "anchor"
# start time (e.g. "05:00"), then set "enabled": true
```

**2. Check the box can warm the window, and preview the plan.**
```bash
node bin/session-warmer.mjs check      # confirms claude is installed + logged in here
node bin/session-warmer.mjs schedule   # shows the primer times (e.g. 05:00 10:05 15:10 20:15)
```
If `check` fails, it tells you exactly what to fix (install the CLI, or run `claude` once
to log in).

**3. Schedule it.**
```bash
node bin/session-warmer.mjs install    # prints a ready-to-paste cron block
crontab -e                             # paste the block; save
```
Done — the VPS now warms your Claude window every day so your windows align to your hours.
(Prefer OpenClaw/Cowork scheduled tasks? `install` also prints that recipe — one task per
primer time running `node bin/session-warmer.mjs warm`.)

## Hard constraints (do not violate)

1. **Official CLI only.** The primer is sent via the real `claude -p` binary. Never
   extract or reuse OAuth tokens, never spoof the Claude Code client, never route the
   primer through the Agent SDK with subscription auth or any third-party harness.
2. **The user's own subscription, logged in on the box itself.** No token copying between
   machines, no shared accounts.
3. **One trivial prompt per primer.** The point is to *open* the window, not do work.
4. **Opt-in.** `enabled` ships `false`. Do not arm it without the user setting it true.
5. **Honest framing.** Describe it as window *alignment*, never as "bypassing limits."

## How the math works

`schedule` walks from `anchor` to `day_end` in steps of `window_minutes + buffer_minutes`.
Each step lands just after a window closes, so the primer at that time starts a brand-new
5-hour window. With the defaults (anchor 05:00, window 300m, buffer 5m): 05:00, 10:05,
15:10, 20:15. All clock math is timezone-aware via `Intl` — set your IANA `timezone` and
DST/travel are handled; no extra dependencies.

## Commands

- `check` — verify the CLI is installed + authenticated on this box (run this first).
- `schedule` — print today's primer times (no side effects).
- `warm` — fire one primer now (respects `enabled` + `dry_run`); this is what cron runs.
- `install [--cron-only]` — print cron / scheduled-task lines (`--cron-only` is pipeable).
- `status` — show config + the next primer time.

## Files

- `bin/session-warmer.mjs` — the engine (Node, no deps).
- `config.example.json` — copy to `config.json` and edit.
- `references/tos.md` — why the official-CLI path is permitted and what is not. **Read before publishing.**
- `README.md` — user-facing overview for the public repo.
