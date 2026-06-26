---
name: daily-greeting
description: Give your OpenClaw agents personality! Automatically sends personalized daily greetings to all bound channels. Each agent greets users in their preferred language with relevant status updates. Supports BOOT.md and OpenClaw cron triggers.
---

# Daily Greeting Skill

## Features

- 🎯 **Dual trigger modes**: Supports both BOOT.md (on startup) and cron (scheduled)
- 📊 **State persistence**: Records execution status, prevents duplicate runs
- 🔌 **Multi-platform**: Supports Discord, Feishu, etc.
- ⏰ **Working days filter**: Only triggers on weekdays (configurable)
- 🔄 **Resettable**: Supports manual reset
- 🛡️ **Safe repetition prevention**: Both BOOT.md and cron can coexist - state check prevents duplicate greetings

## Installation

1. Clone or copy skill to `~/.openclaw/skills/daily-greeting/`
2. Ensure script is executable: `chmod +x scripts/greeting.sh`

## Usage

### Manual Execution

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run
```

### Auto-trigger

Choose one or both triggering methods based on your usage:

#### Method 1: BOOT.md (triggers on Gateway startup)

Add to workspace `BOOT.md`:

```markdown
# BOOT.md

<!-- daily-greeting:start -->
Please execute daily greeting:
```
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run
```

After execution, reply ONLY: `NO_REPLY`.
<!-- daily-greeting:end -->
```

#### Method 2: OpenClaw Cron (triggers on schedule)

```bash
openclaw cron add \
  --name "daily-greeting" \
  --cron "0 9 * * 1-5" \
  --session isolated \
  --message "bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh run" \
  --wake now
```

Default: 9am on weekdays (Mon-Fri)

Both methods work together safely - state check prevents duplicate greetings.

## Configuration

Configure in `config.json`:

```json
{
  "enabled": true,
  "workingDaysOnly": true,
  "delayMs": 3000,
  "excludeAgents": ["main"],
  "triggerMessage": "Please send a daily greeting to your bound channel. Requirements: 1) Compose the greeting in the user's preferred language (infer from channel history and user context); 2) Include relevant status information based on your agent role and ongoing tasks with the user (e.g., if you're a todo agent, summarize progress and today's priorities; if you're a diary agent, mention ongoing projects); 3) Use message tool to send to your bound channel; 4) End conversation after sending"
}
```

## Greeting Content

Each agent organizes their own greeting message based on their persona and sends it to their bound channel.

## Commands

| Command | Description |
|---------|-------------|
| `bash scripts/greeting.sh run` | Execute greeting manually |
| `bash scripts/greeting.sh status` | View execution status |
| `bash scripts/greeting.sh reset` | Reset state (allows re-trigger) |
| `bash scripts/greeting.sh install` | Record BOOT.md path (for uninstall) |
| `bash scripts/greeting.sh uninstall` | Remove skill and clean BOOT.md |

## State File

State is stored in `data/state.json`:

```json
{
  "lastRun": "2026-04-03T10:40:00Z",
  "agents": {
    "diary": "completed"
  }
}
```

## Uninstall

```bash
bash ~/.openclaw/skills/daily-greeting/scripts/greeting.sh uninstall
```

This will:
1. Read the recorded BOOT.md path from `data/install.json`
2. Remove **only** the marked daily-greeting section
3. Remove the OpenClaw cron job
4. Delete the skill directory

## Open Source License

MIT License - Welcome contributions!