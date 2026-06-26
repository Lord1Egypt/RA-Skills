# OpenClaw Dynamic Island

macOS Dynamic Island style widget for [OpenClaw](https://github.com/nicepkg/openclaw) — shows real-time multi-agent status on your desktop, with custom emolog icons.

![preview](https://img.shields.io/badge/macOS-13%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green)

## What it does

A translucent, frosted-glass pill floats at the top center of your screen, just like iPhone's Dynamic Island. It monitors OpenClaw agent session files and displays live status:

| State | Icon | Meaning |
|-------|------|---------|
| Sleeping / Idle | ![idle](emolog/idle.png) | Not connected / Ready |
| Alert | ![alert](emolog/alert.png) | Message received |
| Thinking | ![thinking](emolog/thinking.png) | Processing / tool call |
| Done | ![done](emolog/done.png) | Task completed (window shakes!) |
| Error | ![error](emolog/error.png) | Something went wrong |

> Icons powered by [emolog](https://apps.apple.com/app/emolog/id6443809191) — cute emoji for your Dynamic Island.

### Multi-Agent

- Shows all your agents with their current state
- Hover to expand: see agent list with the latest 2 messages per agent
- Highlight block follows your cursor across agents
- Click an agent name to open its Feishu chat directly
- Compact pill shows emoji + agent count when idle

### Sounds

- Glass sound on task completion
- Bass sound on error

## Requirements

- macOS 13+
- Python 3.9+
- Swift (comes with Xcode Command Line Tools)

```bash
# Install Xcode Command Line Tools (if not already)
xcode-select --install

# Install Python dependency
pip3 install websockets
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/zhixiangshon-cell/openclaw-dynamic-island.git
cd openclaw-dynamic-island

# 2. Configure
cp config.example.json config.json
# Edit config.json — set your agents directory and agent names

# 3. Run
./start.sh
```

The Dynamic Island will appear at the top center of your screen.

To stop:

```bash
./start.sh stop
```

## Configuration

Edit `config.json`:

```json
{
  "agents_dir": "~/.openclaw/agents",
  "http_port": 7788,
  "ws_port": 7789,
  "agent_names": {
    "my-agent-id": "My Bot",
    "another-agent": "Group Chat"
  },
  "agent_links": {
    "my-agent-id": "lark://applink.feishu.cn/client/chat/open?openId=xxx",
    "another-agent": "lark://applink.feishu.cn/client/chat/open?openChatId=xxx"
  }
}
```

| Field | Description | Default |
|-------|-------------|---------|
| `agents_dir` | Path to OpenClaw agents directory | `~/.openclaw/agents` |
| `http_port` | HTTP server port | `7788` |
| `ws_port` | WebSocket port | `7789` |
| `agent_names` | Map agent IDs to friendly display names | `{}` |
| `agent_links` | Map agent IDs to Feishu chat URLs (clickable) | `{}` |

## Auto-start on Login

```bash
# Install Launch Agent
sed "s|__INSTALL_DIR__|$(pwd)|g" com.openclaw.face.plist > ~/Library/LaunchAgents/com.openclaw.face.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.face.plist

# Uninstall
launchctl unload ~/Library/LaunchAgents/com.openclaw.face.plist
rm ~/Library/LaunchAgents/com.openclaw.face.plist
```

## Architecture

```
server.py       — Watches agent session JSONL files, pushes events via WebSocket
index.html      — Renders emolog icons + multi-agent UI (widget + expanded view)
widget.swift    — Native macOS pill window (NSPanel + frosted glass + WKWebView + hover detection)
start.sh        — Start/stop helper script
config.json     — Your local configuration (git-ignored)
emolog/         — Custom emolog icons (idle, alert, thinking, done, error)
```

## How it Works

1. `server.py` watches `~/.openclaw/agents/*/sessions/*.jsonl` for new lines
2. Parses each line to detect state changes (message received, thinking, done, error)
3. Broadcasts events to connected WebSocket clients
4. `widget.swift` creates a floating NSPanel with frosted glass effect
5. Loads `index.html?widget` in a transparent WKWebView inside the pill
6. The page connects via WebSocket and updates emolog icons/status in real-time
7. On task completion, JS tells Swift to physically shake the window + play sound
8. Hover over the pill to expand and see all agents with recent messages
9. Swift HoverView tracks mouse position and highlights the agent group under cursor

## License

MIT
