# OpenClaw Cron Setup — cc-changelog-monitor

This document explains how to add the Claude Code version monitor as an OpenClaw cron job.

## Option 1: Via OpenClaw Chat (Recommended)

Just tell OpenClaw:

> "Add a cron job called 'Claude Code Version Monitor' that runs every 2 hours and executes: `bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh`"

OpenClaw will set it up automatically.

---

## Option 2: Manual Cron Config

OpenClaw cron jobs are stored in `~/.openclaw/cron/`. You can add a job by asking OpenClaw to create one, or via the cron tool.

**Cron schedule:** `0 */2 * * *` (every 2 hours, on the hour)

**Command to run:**
```bash
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

**Settings:**
- **Name:** Claude Code Version Monitor
- **Schedule:** `0 */2 * * *`
- **Session target:** isolated (no persistent session needed)
- **Delivery:** none (Telegram alerts handled by the script itself)
- **Timeout:** 60 seconds

---

## Option 3: Native macOS cron (fallback, no OpenClaw required)

```bash
crontab -e
```

Add this line:
```
0 */2 * * * bash $HOME/clawd/skills/cc-changelog-monitor/scripts/monitor.sh >> $HOME/clawd/projects/cc-changelog/monitor.log 2>&1
```

---

## Verifying the Cron Works

After setup, check the log or wait for the next run:

```bash
# Check when the cron last ran (OpenClaw cron)
cat ~/clawd/projects/cc-changelog/monitor.log 2>/dev/null || echo "No log yet"

# Manual test
bash ~/clawd/skills/cc-changelog-monitor/scripts/monitor.sh
```

---

## What Happens During Each Run

| Scenario | Duration | Telegram | Credits |
|----------|----------|----------|---------|
| Same version | ~50ms | No alert | 0 |
| New version | ~2-10s | Alert sent | 0 |
| npm down | ~5s | No alert | 0 |

The script **never calls an LLM** — zero AI credits consumed per run.

---

## Disabling the Monitor

To pause monitoring without deleting the cron:

```bash
# Move version far ahead to prevent false alerts when re-enabling
echo "99.99.99" > ~/.cc-changelog-version
```

To fully disable: delete or disable the cron job in OpenClaw.
