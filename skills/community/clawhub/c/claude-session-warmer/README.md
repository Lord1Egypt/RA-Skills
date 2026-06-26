<p align="center">
  <img src="assets/hero.png" alt="claude-session-warmer" width="100%">
</p>

<p align="center">
  <a href="references/tos.md">Why it's allowed</a> ·
  <a href="https://decisionvex.github.io/claude-session-warmer/">Website</a> ·
  <a href="#setup--1-2-3">Setup</a> ·
  <a href="LICENSE">MIT</a>
</p>

**Align your Claude Pro/Max usage window to your working hours.** Built for people who
run **OpenClaw + Claude Code on a VPS** and want their daily 5-hour windows to start when
*they* start — not whenever the first prompt happens to land.

## The idea

Claude meters usage in a rolling **5-hour window anchored to your first message**. First
prompt at 09:40 → window 09:40–14:40, and the day's resets are stuck on that clock. Fire
a tiny **primer** at 05:00 instead → the window opens 05:00–10:00, a fresh window is
already waiting when you start work, and resets line up with your hours.

<p align="center">
  <img src="assets/window-alignment.png" alt="Window alignment: without vs with the warmer" width="92%">
</p>

## See it run

<p align="center">
  <img src="assets/demo.gif" alt="claude-session-warmer demo: check, schedule, warm" width="80%">
</p>

`claude-session-warmer` fires that primer through the **official `claude` CLI** on your
**always-on box** (the VPS where you already run OpenClaw), on a schedule. A laptop won't
do — it's asleep when you're away; you need a machine that's always on.

It **does not bypass any limit.** You can't exceed the 5-hour or weekly cap, and it
doesn't try — it only changes *when* the window opens. See
[`references/tos.md`](references/tos.md): this is the official-CLI automation exemption,
and it is *not* the token-spoofing thing Anthropic enforces against. Read it before
sharing.

## Prerequisite

The VPS already has the **official Claude Code CLI installed and logged in** to your
Pro/Max subscription (the same setup you develop with). If `claude -p "hi"` answers on
that box, you're ready. Log in **on the box itself** via the official flow — don't copy
tokens from another machine.

## Setup — 1, 2, 3

```bash
# 1. Tell it your timezone + start time
cp config.example.json config.json
#    edit: "timezone" (e.g. "Africa/Johannesburg"), "anchor" (e.g. "05:00"), "enabled": true

# 2. Check the box can warm the window, and preview the plan
node bin/session-warmer.mjs check       # verifies claude is installed + logged in here
node bin/session-warmer.mjs schedule    # e.g. 05:00  10:05  15:10  20:15

# 3. Schedule it
node bin/session-warmer.mjs install     # prints a ready-to-paste cron block
crontab -e                              # paste it, save — done
```

## Commands

| Command | What it does |
|---|---|
| `check` | Verify the `claude` CLI is installed **and logged in** on this box (run first) |
| `schedule` | Print today's primer times (no side effects) |
| `warm` | Fire one primer now (respects `enabled` + `dry_run`) — this is what cron runs |
| `install [--cron-only]` | Print cron / scheduled-task lines (`--cron-only` is pipeable) |
| `status` | Show config + the next primer time |

## Configuration

| Field | Meaning | Default |
|---|---|---|
| `enabled` | Must be `true` to actually send (opt-in) | `false` |
| `dry_run` | Log what would be sent without sending | `false` |
| `timezone` | IANA tz for all clock math — **set this** | `UTC` |
| `anchor` | First primer of the day (HH:MM) | `05:00` |
| `day_end` | Stop priming after this local time | `22:00` |
| `window_minutes` | Claude window length | `300` |
| `buffer_minutes` | Fire this long after a window closes | `5` |
| `prompt` | The trivial primer text | `ping — session warm-up…` |
| `claude_bin` / `claude_args` | The official CLI invocation | `claude` / `["-p"]` |

## Requirements

- Node 18+ on the VPS.
- The official **Claude Code CLI** (`claude`) installed and logged in on that VPS.
- A scheduler — cron (built in) or an OpenClaw/Cowork scheduled task. `install` prints both.

## What it is not

No token extraction, no client spoofing, no Agent-SDK-with-OAuth, no third-party harness,
no shared accounts, no copying auth between machines. Just a scheduled call to the real
`claude` binary already logged in on your box.

## License

MIT — see [LICENSE](LICENSE).
