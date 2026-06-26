# cc-changelog-monitor

> 🤖 Get Telegram alerts the moment Claude Code ships a new version — with a diff of what changed.

**Zero AI credits used during monitoring.** Pure bash + curl + jq. Runs as an OpenClaw cron job every 2 hours.

---

## What It Does

- Polls the npm registry for `@anthropic-ai/claude-code` every 2 hours
- Detects new versions by comparing with the last seen version
- Downloads the npm tarball and diffs it against the previous version
- Sends a Telegram alert with:
  - Old vs new version numbers
  - Count of changed/new files
  - Brief diff summary
  - Link to npm package page

**Example alert:**

```
🤖 Claude Code v2.1.70 released!

📌 Previous: v2.1.69
📝 Changed files: 3
✨ New files: 1
🕐 Published: 2026-03-06T10:23:11.000Z
🔗 https://www.npmjs.com/package/@anthropic-ai/claude-code

Diff summary:
Files dist/common/utils.js and dist/common/utils.js differ
Only in v2.1.70: dist/new-feature.js

_Monitored by OpenClaw cc-changelog-monitor_
```

---

## Prerequisites

- [OpenClaw](https://openclaw.ai) installed (for cron scheduling)
- A Telegram bot token (create one via [@BotFather](https://t.me/BotFather))
- `curl`, `jq`, `npm` installed on your machine

---

## Quick Start

**1. Clone/install the skill:**

```bash
# If using ClawdHub
clawdhub install cc-changelog-monitor

# Or clone directly
git clone https://github.com/antoinersx/cc-changelog-monitor ~/clawd/skills/cc-changelog-monitor
```

**2. Run setup:**

```bash
bash ~/clawd/skills/cc-changelog-monitor/scripts/setup.sh
```

The setup script will:
- Auto-detect your Telegram bot token from OpenClaw config (if available)
- Ask for your Telegram chat ID
- Initialize the version tracker at the current Claude Code version
- Print instructions for adding the cron job

**3. Add the cron in OpenClaw:**

See [`cron-payload.md`](./cron-payload.md) for the exact payload to paste into OpenClaw.

---

## How It Works (No AI Credits)

Most monitoring tools use LLMs to summarize changes — this one doesn't.

```
Every 2 hours:
  1. curl https://registry.npmjs.org/@anthropic-ai/claude-code/latest
  2. Compare version with ~/.cc-changelog-version
  3. If same → exit silently (costs: 0 credits, ~50ms)
  4. If new → npm pack + tar extract + diff -rq
  5. Send Telegram message via bot API
  6. Write new version to ~/.cc-changelog-version
```

The entire monitor loop runs in ~2 seconds on a new version, ~50ms when nothing changed.

---

## Configuration

Credentials are stored in `~/.cc-changelog-config`:

```bash
TELEGRAM_BOT_TOKEN="8587009442:AAE..."
TELEGRAM_CHAT_ID="223310915"
```

The setup script writes this automatically. You can also set these as environment variables.

---

## Manual Testing

```bash
# Normal run (silent if no new version)
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh

# Force an alert (reset version)
echo "0.0.0" > ~/.cc-changelog-version
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

---

## File Structure

```
cc-changelog-monitor/
├── SKILL.md              # OpenClaw skill descriptor
├── README.md             # This file
├── package.json          # npm metadata
├── cron-payload.md       # OpenClaw cron setup instructions
└── scripts/
    ├── setup.sh          # One-time setup
    └── monitor.sh        # Main monitor (zero AI credits)
```

Output files (created at runtime):
```
~/.cc-changelog-version          # Last seen version
~/.cc-changelog-config           # Telegram credentials
~/clawd/projects/cc-changelog/   # Extracted packages for diffing
```

---

## Screenshot

*(Telegram alert example)*

![Telegram alert showing new Claude Code version with diff summary](./assets/telegram-alert-example.png)

---

## Powered by OpenClaw

This skill is designed for the [OpenClaw](https://openclaw.ai) agent platform. It uses OpenClaw's cron scheduling to run automatically — no server required, runs on your Mac.

---

## License

MIT — Antoine Rousseaux (@antoinersx)
