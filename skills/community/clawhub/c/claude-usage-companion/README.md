<p align="center">
  <img src="assets/hero.png" alt="claude-usage-companion" width="100%">
</p>

<p align="center"><b>Monitor your Claude programmatic credit pool, and align your interactive window — on your always-on box.</b></p>

<p align="center">
  <a href="#install">Install</a> ·
  <a href="#setup--1-2-3">Setup</a> ·
  <a href="#why">Why</a> ·
  <a href="https://decisionvex.github.io/claude-usage-companion/">Website</a> ·
  <a href="LICENSE">MIT</a>
</p>

<p align="center">
  <a href="https://skills.sh/DecisionVex/claude-usage-companion"><img src="https://skills.sh/b/DecisionVex/claude-usage-companion" alt="skills.sh installs"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
</p>

<p align="center">
  <img src="assets/what-it-does.png" alt="Two jobs: monitor the credit pool, and remind you to align your window" width="94%">
</p>

<p align="center">
  <img src="assets/demo.gif" alt="Demo: check, report, remind" width="78%">
</p>

## Why

In **June 2026** Anthropic split Claude usage. Non-interactive usage — the **Claude Agent SDK,
`claude -p`, Claude Code GitHub Actions, and third-party agents** — moved onto a **separate
monthly credit pool** ($20 Pro / $100 Max 5x / $200 Max 20x, metered at API rates, **no
rollover**). Your interactive 5-hour window is now reserved for hands-on use of Claude Code,
Cowork, and claude.ai.

That creates two new chores on an always-on box, and this tool handles both:

1. **Watch the credit pool.** When it's exhausted, automated requests just stop. The companion
   reports month-to-date burn, projects month-end spend, and alerts you *before* you run dry.
2. **Align your interactive window.** It can't (and shouldn't) auto-open it — so it reminds
   *you* at your anchor time to send your first prompt, lining your 5-hour window up with your day.

It only **reports** and **reminds**. No automated priming, no scripted interactive input, no
credential tricks, no limit circumvention. Usage is read locally via
[`ccusage`](https://github.com/ryoppippi/ccusage) — no model calls, no window side effects.

> **Successor to [`claude-session-warmer`](https://github.com/DecisionVex/claude-session-warmer).**
> That skill primed the window with `claude -p`; the June 2026 change means `claude -p` no longer
> anchors the interactive window, so the warmer is retired in favour of this honest approach.

## Install

```bash
npx skills add DecisionVex/claude-usage-companion   # skills.sh
clawhub install claude-usage-companion              # OpenClaw / ClawHub
```

## Setup — 1, 2, 3

Run on the always-on box (Node 18+; `npm i -g ccusage` for the fast path).

```bash
# 1. Configure
cp config.example.json config.json
#    set "timezone", "plan" (pro|max5x|max20x), "anchor" (when you start work)

# 2. Check + see your burn
node bin/usage-companion.mjs check
node bin/usage-companion.mjs report

# 3. Schedule
node bin/usage-companion.mjs install   # prints a cron block
crontab -e                             # paste it, save
```

Sample `report`:

```
claude-usage-companion — programmatic credit pool (Africa/Johannesburg)
  month 2026-06 · day 17/30 · cap $200.00 (max20x)

  spent so far   █                               2%   $4.45
  projected EOM  █                               4%   $7.85

  avg/day $0.26 · 13 days left
  outlook: ✓ comfortably within budget
```

## Commands

| Command | What it does |
|---|---|
| `check` | Verify Node + `ccusage` and read your usage (run first) |
| `report` | Month-to-date spend, projected month-end, top models |
| `guard` | Alert only if over `warn_pct`/`critical_pct` — this is what cron runs |
| `remind` | Emit the anchor-time "start your session" nudge |
| `status` | Config + next scheduled actions |
| `install [--cron-only]` | Print the cron block (`--cron-only` pipes to `crontab -`) |

## Configuration

| Field | Meaning | Default |
|---|---|---|
| `timezone` | IANA tz for all clock math — **set this** | `UTC` |
| `plan` | `pro` / `max5x` / `max20x` → credit cap | `max5x` |
| `monthly_credit_usd` | Override the cap | `null` |
| `warn_pct` / `critical_pct` | Alert thresholds (% of cap) | `80` / `95` |
| `anchor` | Local time you start work | `08:00` |
| `reminder_enabled` | Send the anchor-time nudge | `true` |
| `alert_command` | Shell command receiving alerts on stdin (e.g. post to Slack); `null` = stdout + `companion.log` | `null` |
| `ccusage_cmd` | How to invoke ccusage | `["npx","-y","ccusage@latest"]` |

For your exact remaining balance, the authoritative source is the **"Usage credits"** line in
`/usage` inside Claude Code. `report`/`guard` approximate the pool from local ccusage cost — which
on an always-on automation box is essentially all programmatic.

## License

MIT — see [LICENSE](LICENSE). Not affiliated with Anthropic.
