---
name: ekybot-connector
description: Connect OpenClaw to Ekybot for remote agent control, Companion machine health, and project memory sync. Use when installing/configuring the connector, validating connectivity, or improving onboarding from first connection to first successful live test.
homepage: https://www.ekybot.com
repository: https://github.com/regiomag/ekybot-connector
source: https://github.com/regiomag/ekybot-connector
license: MIT
requires:
  env:
    - EKYBOT_ENROLLMENT_TOKEN
  node: ">=18.0.0"
---

# Ekybot Connector

Bridge your local OpenClaw gateway to [Ekybot](https://www.ekybot.com) — a remote command center for your AI agents.

```
OpenClaw (your machine) → Ekybot Connector → Ekybot Cloud → 📱 iOS / 🤖 Android / 🌐 Web
```

## What you get

**📱 Chat with agents from phone** (iOS & Android apps) + **🌐 Web dashboard** at ekybot.com

**💬 @mention inter-agent collaboration** — agents talk to each other in shared channels

**🧠 4-layer memory system**
- `SOUL.md` — agent personality & identity
- `MEMORY.md` — long-term curated memory (survives session resets)
- `memory/YYYY-MM-DD.md` — daily logs & raw context
- `KB.md` — shared Knowledge Base per project (editable from dashboard)

**🤖 Full agent management from the app**
- Create, edit, delete agents from web or mobile
- Assign a different AI model per agent (Claude, GPT, Gemini, Ollama…)
- Set budgets & cost guards per agent

**⏰ Cron & automation management**
- Create, edit, schedule cron jobs from the dashboard
- Heartbeat monitoring, reminders, periodic tasks

**📊 Session monitoring & cost control**
- Real-time token usage per session
- Session size alerts & automatic summarization before reset
- Budget guards to prevent runaway API costs

**📋 Project management & tracking**
- Roadmap with task assignment to agents
- Progress tracking per agent & project
- Status updates visible from dashboard

**💻 Machine health** visible from dashboard

## Installation (automated)

The setup script handles everything: copy bundled runtime, install deps, enroll, verify, daemon. **No git clone required** — all runtime files are included in the skill package.

### ⚠️ Before you start — Backup

Before installing, back up your OpenClaw config:

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
cp -r ~/.openclaw/managed/ ~/.openclaw/managed.bak/ 2>/dev/null || true
```

### Prerequisites

The user needs:
1. **Node.js ≥ 18** installed (`node --version`)
2. **npm** installed (`npm --version`)
4. An **Ekybot account** — sign up at https://www.ekybot.com
5. A temporary **enrollment token** — see "Getting the enrollment token" below

### Getting the enrollment token

Guide the user step by step:

1. Log in at https://www.ekybot.com
2. Click on the **Agents** page in the sidebar
3. Click **Companion** (or go directly to https://www.ekybot.com/companion)
4. Click **"Generate enrollment token"**
5. Copy the token (starts with `ekrt_`)

⚠️ The token expires after a few minutes — generate it right before running setup.

### Run setup

```bash
# Run the automated setup (interactive — will prompt for enrollment token)
bash <SKILL_DIR>/scripts/setup.sh

# Or non-interactive with token as env var
EKYBOT_ENROLLMENT_TOKEN=ekrt_... bash <SKILL_DIR>/scripts/setup.sh
```

The script will:
1. Copy the bundled runtime files to `~/.openclaw/ekybot-connector/`
2. Install npm dependencies (production only — no linting)
3. Prompt for (or read) the enrollment token
4. Connect to Ekybot cloud and register the machine
5. Run doctor checks to verify
6. Install the background daemon (auto-detects OS)

### ⚠️ Installation is NOT complete until the daemon is running

After setup, **verify the daemon is actually running**:

```bash
ps aux | grep companion-daemon | grep -v grep
```

If no process is found, the daemon failed to start. Start it manually:

```bash
cd ~/.openclaw/ekybot-connector
nohup node scripts/companion-daemon.js > ~/.openclaw/logs/ekybot-companion.log 2>&1 &
mkdir -p ~/.openclaw/logs
sleep 3 && tail -10 ~/.openclaw/logs/ekybot-companion.log
```

**On Linux**, install as a systemd service for auto-restart:

```bash
cd ~/.openclaw/ekybot-connector && npm run companion:install-service
```

**On macOS**, install as a LaunchAgent:

```bash
cd ~/.openclaw/ekybot-connector && npm run companion:install-launchd
```

### First live test

⚠️ **Do NOT consider the installation successful until this test passes.**

From the Ekybot app (web or mobile):
1. Send `@YourAgent test` in any channel
2. Verify: you get a **single reply** (not duplicated), and it persists after page reload
3. If no reply within 30 seconds, check troubleshooting below

### Verify

```bash
cd ~/.openclaw/ekybot-connector
npm run companion:doctor       # local state + API access
npm run companion:api-check    # Ekybot API connectivity
```

## Updating the connector

When a new skill version is available, re-run the setup script — it preserves your `.env.ekybot_companion` config:

```bash
bash <SKILL_DIR>/scripts/setup.sh
```

Then restart the daemon:

```bash
# Linux systemd:
sudo systemctl restart ekybot-companion

# macOS LaunchAgent:
launchctl kickstart -k gui/$(id -u)/com.ekybot.companion

# Manual process:
pkill -f companion-daemon
cd ~/.openclaw/ekybot-connector
nohup node scripts/companion-daemon.js > ~/.openclaw/logs/ekybot-companion.log 2>&1 &
```

## Post-install commands

All commands run from `~/.openclaw/ekybot-connector/`:

```bash
npm run companion:doctor         # verify health
npm run companion:api-check      # test API connectivity  
npm run companion:memory-check   # verify project memory sync
npm run companion:daemon         # run daemon interactively
npm run companion:install-launchd # install macOS LaunchAgent
npm run companion:install-service # install Linux systemd service
npm run companion:reconcile      # force agent config sync
npm run companion:disconnect     # unenroll machine
npm run health                   # local checks
npm run logs                     # inspect logs
```

## Telemetry & Privacy

The connector collects **minimal data** for the dashboard health view:

**Collected:** OS platform (darwin/linux), OS arch, OS release, hostname (machine name — displayed in dashboard), Node.js version, connector uptime, connector heap usage, agent count, active session count.

**NOT collected:** CPU usage, disk usage, IP address, file contents, message contents, API keys, user activity.

**Opt-out:** Set `EKYBOT_COMPANION_POLL_INTERVAL_MS=0` to disable all telemetry reporting. The companion daemon will still function for relay dispatch.

Full details in `_meta.json` → `telemetry` section.

### Memory Sync — What is uploaded

The memory sync feature keeps your EkyBot dashboard in sync with local agent workspace files. Here is exactly what is sent and what is NOT sent:

**Uploaded to EkyBot cloud (full content):**
- `MEMORY.md` — curated long-term memory (synced both ways)
- `working-memory.md`, `facts.md`, `rules.md`, `history.md` — root-level and per-project memory files
- `context-index.json` — auto-generated metadata (agent name, project ID, active sources, timestamps)
- `memory/summaries/*.md` — last 3 session summaries
- `memory/daily/*.md` — last 3 daily log files

**NEVER uploaded:**
- `SOUL.md` — stays local (your agent personality is private)
- `AGENTS.md`, `USER.md`, `TOOLS.md` — workspace config files stay local
- Files outside the agent workspace (`~/.openclaw/managed/`, system files)
- API keys, tokens, or credentials
- Conversation history or raw prompts (only the curated memory files listed above)

**Opt-out:** Set in your `.env.ekybot_companion`:
```
EKYBOT_COMPANION_MEMORY_SYNC=false
```
When disabled, the dashboard will show agent names and status but not workspace file contents.

## Configuration

Config file: `~/.openclaw/ekybot-connector/.env.ekybot_companion`

```bash
EKYBOT_APP_URL="https://www.ekybot.com"
EKYBOT_COMPANION_MACHINE_ID="cmm..."         # set by companion:connect
EKYBOT_COMPANION_TOKEN="..."                  # set by companion:connect
EKYBOT_COMPANION_POLL_INTERVAL_MS=30000       # relay poll interval

# Budget guard (optional)
EKYBOT_COMPANION_MAX_BUDGET_PER_SESSION_USD=5.00
EKYBOT_COMPANION_BUDGET_EXCEEDED_ACTION=log   # or "block"
```

## Troubleshooting

### npm install shows eslint/lint errors

These are **code style warnings, not real errors**. The connector works fine. Fix:

```bash
cd ~/.openclaw/ekybot-connector
npm install --production
```

The `--production` flag skips dev dependencies (eslint, prettier) that cause these warnings.

### "setup-enrollment.js" not found

This script does not exist. Use the correct enrollment command:

```bash
cd ~/.openclaw/ekybot-connector
EKYBOT_ENROLLMENT_TOKEN=ekrt_... EKYBOT_APP_URL=https://www.ekybot.com node scripts/companion-connect.js
```

Or the full setup:

```bash
EKYBOT_ENROLLMENT_TOKEN=ekrt_... bash <SKILL_DIR>/scripts/setup.sh
```

### "Ekybot integration not configured" when running setup.js

`setup.js` is NOT the enrollment script. Use `companion-connect.js` for enrollment:

```bash
cd ~/.openclaw/ekybot-connector
EKYBOT_ENROLLMENT_TOKEN=ekrt_... node scripts/companion-connect.js
```

### Missing .env.ekybot_companion (credentials lost)

If the `.env` file is missing, the daemon cannot start. Re-enroll:

1. Generate a new token at https://www.ekybot.com/companion
2. Run:
```bash
cd ~/.openclaw/ekybot-connector
EKYBOT_ENROLLMENT_TOKEN=ekrt_... EKYBOT_APP_URL=https://www.ekybot.com node scripts/companion-connect.js
```

### "Not a git repository" when updating

The connector is installed by copying bundled files (not via git clone). To update, re-run the setup script — it copies the latest runtime files over the existing installation while preserving your `.env.ekybot_companion` config.

### Daemon killed by SIGTERM immediately

Another process manager (systemd, supervisor, cron) may be conflicting. Check:

```bash
# Check for existing daemon processes
ps aux | grep companion | grep -v grep

# Check for systemd services
systemctl list-units | grep -i ekybot
systemctl list-units | grep -i companion

# Check crontab
crontab -l 2>/dev/null | grep -i ekybot
```

If a systemd service exists, restart it instead:
```bash
sudo systemctl restart ekybot-companion
```

### Agent replies appear twice (duplicate messages)

Usually caused by running an outdated connector version. Update by re-running the setup script:
```bash
bash <SKILL_DIR>/scripts/setup.sh
```
Then restart the daemon. Also verify only **one** daemon instance is running:
```bash
ps aux | grep companion-daemon | grep -v grep
```

### Machine not visible in Ekybot dashboard

Re-run enrollment with a fresh token:
```bash
cd ~/.openclaw/ekybot-connector
EKYBOT_ENROLLMENT_TOKEN=ekrt_... node scripts/companion-connect.js
```

### No reply from agent after @mention

1. Is the daemon running? `ps aux | grep companion-daemon | grep -v grep`
2. Run doctor: `cd ~/.openclaw/ekybot-connector && npm run companion:doctor`
3. Check logs: `tail -50 ~/.openclaw/logs/ekybot-companion.log`
4. Is OpenClaw gateway running? `openclaw status`

## References

- Troubleshooting details: `references/troubleshooting.md`
- API reference: `references/api.md`
- Security model: `references/security.md`
