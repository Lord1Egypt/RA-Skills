# Daily Greeting Skill

> [!TIP]
> Give your OpenClaw agents a personality! They automatically send personalized daily greetings to users every morning.

<!-- Language Navigation -->
[English](README.md) | [中文](docs/README_zh.md)

---

## What It Does

Your agents wake up with you! Every morning (or on your schedule), each agent sends a personalized greeting to their bound channels with:

- 🤖 **Agent personality** - Each greeting matches the agent's persona
- 🌐 **User's language** - Greetings in the user's preferred language
- 📊 **Relevant info** - Status updates, progress, reminders based on agent role

## Features

| | |
|--------|---------|
| ⚡ **Auto-trigger** | Works on startup (BOOT.md) or schedule (OpenClaw cron) |
| 🛡️ **No duplicates** | State persistence prevents repeated greetings |
| 🌐 **Any channel** | Discord, Feishu, Telegram, and more |
| 🎨 **Persona-driven** | Each agent has its own greeting style |
| 🧹 **Clean removal** | Uninstalls cleanly without leftovers |

## Quick Start

### One-Line Install

Send OpenClaw this command:

```
Please execute the daily-greeting installation guide:
https://raw.githubusercontent.com/shz2050/daily-greeting/main/guide.md
```

OpenClaw handles everything automatically.

### Manual Installation

```bash
# Clone this repository
git clone https://github.com/shz2050/daily-greeting.git

# Copy to OpenClaw skills directory
cp -r daily-greeting ~/.openclaw/skills/daily-greeting

# Make script executable
chmod +x ~/.openclaw/skills/daily-greeting/scripts/greeting.sh
```

## Auto-trigger Setup

Both BOOT.md (startup) and OpenClaw cron (schedule) are enabled by default. State check prevents duplicate greetings.

**BOOT.md (triggers on Gateway startup):**

```bash
# Find workspace
ls ~/.openclaw/workspace/

# Create/edit BOOT.md
nano ~/.openclaw/workspace/BOOT.md
```

Add this content:

````markdown
# BOOT.md

<!-- daily-greeting:start -->
Please execute daily greeting:
```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run
```

After execution, reply ONLY: `NO_REPLY`.
<!-- daily-greeting:end -->
````

**OpenClaw Cron (triggers on schedule):**

```bash
openclaw cron add \
  --name "daily-greeting" \
  --cron "0 9 * * 1-5" \
  --session isolated \
  --message "bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run" \
  --wake now
```

Default: 9am on weekdays (Mon-Fri)

To view/modify:
```bash
openclaw cron list
```

**Record install info:**

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh install ~/.openclaw/workspace/BOOT.md
```

## Commands

```bash
# Run greeting manually
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run

# Check status
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh status

# Reset (allow re-execution)
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh reset

# Uninstall
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall
```

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "enabled": true,
  "workingDaysOnly": true,
  "delayMs": 3000,
  "excludeAgents": ["main"],
  "triggerMessage": "Please send a daily greeting to your bound channel. Requirements: 1) Compose the greeting in the user's preferred language (infer from channel history and user context); 2) Include relevant status information based on your agent role and ongoing tasks with the user (e.g., if you're a todo agent, summarize progress and today's priorities; if you're a diary agent, mention ongoing projects); 3) Use message tool to send to your bound channel; 4) End conversation after sending"
}
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable the skill |
| `workingDaysOnly` | boolean | `true` | Only trigger on weekdays (Mon-Fri) |
| `delayMs` | number | `3000` | Delay before execution (milliseconds) |
| `excludeAgents` | array | `["main"]` | Agents to exclude from greeting |
| `triggerMessage` | string | (see above) | Message sent to each agent |

## How It Works

```
Gateway starts / Cron triggers
    ↓
greeting.sh runs
    ↓
Reads config → checks working day → checks if already run today
    ↓
For each bound agent:
    - Agent sends personalized greeting to their channel
    ↓
State saved to data/state.json
```

## Uninstall

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall
```

This removes:
1. BOOT.md entry (only the marked section)
2. OpenClaw cron job
3. Skill directory

## Requirements

- OpenClaw Gateway
- Bash 4.0+
- jq (for JSON parsing)

## License

MIT License - See LICENSE file for details.

## Support

For issues and questions, please open a GitHub issue.

---

## Star History

[![Star History](https://api.star-history.com/svg?repos=shz2050/daily-greeting&type=Timeline&theme=dark)](https://star-history.com/#shz2050/daily-greeting&type=Timeline)
