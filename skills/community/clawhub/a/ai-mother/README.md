# AI Mother 👩👧👦

**Monitor and manage AI coding agents (Claude Code, Codex, OpenCode) running on your machine.**

AI Mother automatically detects stuck, idle, or errored AI agents and can auto-heal common issues or notify you when manual intervention is needed.

## Features

- 🔍 **Auto-discovery** - Finds all running AI agents (Claude Code, Codex, OpenCode)
- 🩺 **Health monitoring** - Detects stopped, idle, rate-limited, permission-waiting, or errored states
- 🔧 **Auto-healing** - Safely resumes stopped processes, sends Enter/Continue, requests status
- 💬 **Flexible permission handling** - Detects any permission prompt format, notifies owner with exact options, accepts any response (1, y, allow once, etc.)
- ⏱️ **Dynamic patrol frequency** - Auto-switches to 5-min patrol for active conversations, 30-min baseline otherwise
- 🔔 **Task completion notifications** - Notifies you when an AI finishes its task
- 🧹 **Duplicate detection** - Warns when multiple AIs work on the same directory
- 📊 **Analytics** - Track performance, runtime, and patterns over time
- 🎛️ **Dashboard** - Real-time TUI monitoring
- 🔒 **Race condition protection** - File locking prevents concurrent patrol corruption
- 📱 **Smart notifications** - DMs you on Feishu only when attention needed (0 tokens)

## Prerequisites

- **Python 3.7+** with pip
- **OpenClaw** with Feishu channel configured
- **AI agents** (Claude Code, Codex, OpenCode)
- **tmux** (As client warpper, so openclaw can send message to it, you could run tmux new session "claude --continue")

## Installation

```bash
# Install from ClawHub
clawhub install ai-mother

# Or clone manually
git clone <repo-url> ~/.openclaw/skills/ai-mother
cd ~/.openclaw/skills/ai-mother

# Install Python dependencies
pip3 install -r requirements.txt

# Run setup wizard
./scripts/setup.sh
```

## Quick Start

### 1. First-Time Setup

```bash
~/.openclaw/skills/ai-mother/scripts/setup.sh
```

This will:
- Prompt for your Feishu open_id
- Test notification delivery
- Create config.json
- Configure scheduled patrol (every 30 minutes)

**How to get your Feishu open_id:**
1. Send any message to your OpenClaw bot on Feishu
2. Run: `openclaw logs --tail 20 | grep 'ou_'`
3. Look for: `received message from ou_xxxxx`
4. Copy the `ou_xxxxx` string

### 2. Manual Patrol (Check All AIs)

```bash
~/.openclaw/skills/ai-mother/scripts/patrol.sh
```

### 3. Auto-Heal Issues

```bash
# Check and fix all agents
~/.openclaw/skills/ai-mother/scripts/health-check.sh

# Fix specific agent
~/.openclaw/skills/ai-mother/scripts/auto-heal.sh <PID>

# Dry-run (preview actions)
~/.openclaw/skills/ai-mother/scripts/auto-heal.sh <PID> --dry-run
```

### 4. Responding to Permission Confirmations

When an AI needs permission, AI Mother sends you a Feishu notification showing the **exact prompt** from the AI. Reply with whatever input the prompt requires:

```
# OpenCode "Allow once / Allow always / Reject" prompt:
AI Mother: 1 756882

# Claude Code numbered prompt:
AI Mother: 2 756882

# Generic y/n prompt:
AI Mother: y 756882

# Any custom text:
AI Mother: allow once 756882
```

The response is sent **exactly as typed** — no guessing, no format conversion.

**Manual handling:**
```bash
tmux attach -t 0
# Type the appropriate response directly
```

### 5. View Dashboard

```bash
~/.openclaw/skills/ai-mother/scripts/dashboard.sh
```

### 6. Analytics

```bash
# All agents
~/.openclaw/skills/ai-mother/scripts/analytics.py

# Specific agent
~/.openclaw/skills/ai-mother/scripts/analytics.py <PID>
```

## Automatic Monitoring

AI Mother uses **dynamic patrol frequency**:
- **30-minute baseline** - always running via cron
- **5-minute high-frequency** - auto-enabled when active conversations detected (≥3 messages in 30min)
- **Auto-downgrade** - returns to 30-min when conversations go quiet

Each patrol will:
- Scan all AI agents (excludes tmux wrappers)
- Auto-heal safe issues
- Detect permission confirmations (any format)
- Detect duplicate AIs on same directory
- Notify when tasks complete (once per completion, no spam)
- Notify you on Feishu only when manual intervention needed (0 tokens)

## What Gets Auto-Healed

✅ **Safe (no approval needed):**
- Resume stopped processes (with safety checks)
- Send Enter for "press enter to continue"
- Auto-confirm read-only operations
- Request status from idle AIs (>2h)
- Suggest model switch on rate limits

❌ **Always escalates to you:**
- Elevated permissions
- Destructive commands
- Code modifications
- External communications
- Financial operations

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `setup.sh` | First-time configuration wizard |
| `patrol.sh [--quiet]` | Scan all AI agents (file-locked, safe to call frequently) |
| `health-check.sh` | Quick health check + auto-heal |
| `auto-heal.sh <PID>` | Auto-fix common issues |
| `cleanup-duplicates.sh [--auto]` | Detect and clean up duplicate AIs on same directory |
| `manage-patrol-frequency.sh` | Adjust patrol cron frequency based on conversation activity |
| `handle-owner-response.sh <PID> <response>` | Send any response to AI (1, y, allow once, etc.) |
| `check-tmux-waiting.sh <PID>` | Detect waiting/permission states in tmux |
| `analytics.py [PID]` | Performance analytics |
| `get-ai-context.sh <PID>` | Deep context for one agent |
| `send-to-ai.sh <PID> <msg>` | Send message to AI |
| `smart-diagnose.sh <PID>` | Detect abnormal patterns |
| `dashboard.sh` | Real-time TUI dashboard |
| `notify-owner.sh <msg>` | Send Feishu DM (0 tokens) |
| `resume-ai.sh <PID>` | Resume stopped process |

## Troubleshooting

### "No owner open_id configured"
Run setup wizard: `./scripts/setup.sh`

### "Test message failed"
Check:
- Feishu channel enabled: `openclaw config`
- Bot has message permissions in Feishu admin panel
- open_id is correct (starts with `ou_`)

### Analytics shows no data
- Database integration requires patrol to run at least once
- Run: `./scripts/patrol.sh` to populate initial data
- Check: `sqlite3 ~/.openclaw/skills/ai-mother/ai-mother.db "SELECT COUNT(*) FROM history;"`

### Dashboard won't start
Install rich library: `pip3 install rich --user`

### Auto-heal not working
- Check if process is actually stuck: `ps -p <PID>`
- Run with dry-run first: `./scripts/auto-heal.sh <PID> --dry-run`
- Check logs for safety skip reasons

## Configuration

Edit `~/.openclaw/skills/ai-mother/config.json`:

```json
{
  "owner_feishu_open_id": "ou_your_actual_id_here"
}
```

**Security note**: Never commit `config.json` to git - it contains your personal Feishu ID.

## Uninstall

```bash
# Remove cron job
openclaw cron list  # Find ai-mother-patrol job ID
openclaw cron remove <job-id>

# Remove skill
rm -rf ~/.openclaw/skills/ai-mother

# Optional: Remove data
rm -f ~/.openclaw/skills/ai-mother/ai-mother.db
rm -f ~/.openclaw/skills/ai-mother/ai-state.txt
```

## Privacy & Security

- **DM-only notifications** - Never sends to group chats
- **Local storage** - All data stays on your machine
- **No external APIs** - Only uses OpenClaw's Feishu integration
- **Conservative auto-heal** - Skips anything potentially unsafe

## Contributing

Found a bug or have a feature request? Open an issue or PR on GitHub.

## License

MIT
