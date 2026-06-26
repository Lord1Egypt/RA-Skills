# Agent Status Monitor

Monitor the status and activity of local AI development agents (Claude Code, OpenCode, OpenClaw, Cursor, etc.).

English | [简体中文](README.zh-CN.md)

![agent-status-monitor](https://socialify.git.ci/willin/agent-status-monitor/image?description=1&forks=1&name=1&owner=1&pattern=Circuit+Board&stargazers=1&theme=Auto)

## 🚀 Quick Start

### Installation

#### Option 1: Install via ClawHub

```bash
clawhub install agent-status-monitor
```

#### Option 2: Install via npx

```bash
npx skills add willin/agent-status-monitor
```

#### Option 3: Clone from GitHub

```bash
# Clone the repository
git clone https://github.com/willin/agent-status-monitor.git
cd agent-status-monitor

# Copy to OpenClaw workspace
cp -r . ~/.openclaw/workspace/skills/agent-status-monitor/

# Make scripts executable
chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh
```

### Usage

**Method 1: Run the main script**
```bash
~/.openclaw/workspace/skills/agent-status-monitor/scripts/check-agents.sh
```

**Method 2: Trigger in OpenClaw**

> ⚠️ **Note**: Avoid using "check agent status" alone, as it may trigger OpenClaw's built-in session status instead.

```
agents_monitor
Check Claude Code status
Is OpenCode running?
Monitor development tools
agent monitoring
```

**Method 3: Run individual agent checks**
```bash
./scripts/check-claude-code.sh
./scripts/check-openclaw.sh
./scripts/check-opencode.sh
./scripts/check-cursor.sh
```

## 📊 Output Example

```
========================================
   Agent Status Monitor
========================================

--- 进程状态 ---
--- Claude Code 状态 ---
● Claude Code: 🔥 Working (updated within 2 min) · 13 sessions

--- OpenClaw 状态 ---
● OpenClaw: 🔥 Working (updated within 2 min) · 3 sessions

--- OpenCode 状态 ---
● OpenCode: 💤 Idle (not used) · 1 session

--- Cursor IDE 状态 ---
○ Cursor IDE: Not running

========================================
```

## 📋 Status Indicators

| Status | Icon | Meaning |
|--------|------|---------|
| Working | 🔥 | Session files updated within 2 minutes |
| Waiting | ⏳ | Updated within 10 minutes (may be thinking/waiting for API) |
| Idle | 💤 | No updates for 10+ minutes, or unused |
| Not Running | ○ | Process not found |

## 🔧 Supported Agents

| Agent | Process Detection | Session Detection | Session Directory |
|-------|------------------|-------------------|-------------------|
| Claude Code | ✅ | ✅ | `~/.claude/projects/` |
| OpenClaw | ✅ | ✅ | `~/.openclaw/agents/` |
| OpenCode | ✅ | ✅ | `~/.local/state/opencode/` |
| Cursor IDE | ✅ | ❌ | N/A |

## 📁 Project Structure

```
agent-status-monitor/
├── README.md                       # This file (English)
├── README.zh-CN.md                 # Chinese README
├── LICENSE                         # MIT License
├── SKILL.md                        # OpenClaw skill definition
├── scripts/
│   ├── check-agents.sh             # Main script (calls all checks)
│   ├── check-claude-code.sh        # Claude Code detector
│   ├── check-openclaw.sh           # OpenClaw detector
│   ├── check-opencode.sh           # OpenCode detector
│   └── check-cursor.sh             # Cursor IDE detector
└── references/
    └── agent-commands.md           # Reference commands for each agent
```

## 🛠️ Customization

### Add a New Agent Detector

Create a new script in `scripts/`:

```bash
#!/bin/bash
# check-your-agent.sh
SESSIONS_DIR="$HOME/.your-agent/sessions"
# ... implement detection logic
```

Then update `check-agents.sh` to call it.

### Adjust Time Thresholds

Modify the time checks in individual scripts:
- `mmin -2` - Working threshold (default: 2 minutes)
- `mmin -10` - Waiting threshold (default: 10 minutes)

## ⚠️ Notes

1. **Local Only** - Only detects locally running agents, not cloud services
2. **Read-Only** - Does not modify or control any agents
3. **Filesystem Dependent** - Based on session file modification times
4. **False Positive Prevention** - Excludes macOS system processes (e.g., CursorUIViewService)
5. **Trigger Words** - Use specific triggers like `agents_monitor` or "Check Claude Code status" to avoid confusion with OpenClaw's built-in session status

## ❓ FAQ

**Q: Why does "check agent status" show OpenClaw session info instead?**

A: OpenClaw has a built-in session status feature. To use this skill, use specific triggers:
- ✅ `agents_monitor`
- ✅ "Check Claude Code status"
- ✅ "Is OpenCode running?"
- ❌ "Check agent status" (triggers built-in feature)

## 🐛 Troubleshooting

**Issue: Shows "Not Running" but agent is actually running**
```bash
# Manually check processes
ps aux | grep -i "<agent-name>" | grep -v grep

# Check if session directory exists
ls -la ~/.claude/projects/  # Claude Code example
```

**Issue: Script not executable**
```bash
chmod +x ~/.openclaw/workspace/skills/agent-status-monitor/scripts/*.sh
```

## 📝 Changelog

- **v1.0** - Initial release
  - Support for Claude Code, OpenCode, OpenClaw, Cursor IDE
  - Activity detection based on session file modification times
  - Modular script design for easy extension

## 🤝 Contributing

Issues and Pull Requests are welcome!

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.
