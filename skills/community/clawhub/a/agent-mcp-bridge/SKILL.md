---
name: agent-mcp-bridge
description: Set up and use an MCP message broker for direct inter-agent communication between OpenClaw and other AI agents (e.g. hermes-agent, Claude Code, any MCP-capable agent). Use when you need two AI agents on the same machine to exchange messages without human relay — replacing Discord copy-paste or txt file workarounds. Triggers on phrases like "set up agent communication", "MCP broker", "inter-agent messaging", "connect two agents", "agent bridge", "Isaac Hermes communication", or any request to enable direct agent-to-agent messaging.
---

# Agent MCP Bridge

A lightweight FastMCP + SQLite message broker that lets two AI agents communicate directly via MCP tools. Both agents connect to the same server as MCP clients — symmetric, no platform-specific adapters.

## Architecture

```
Agent A (OpenClaw)          MCP Broker              Agent B (hermes-agent / any)
   send_message() ──────► FastAPI+SQLite ◄────────── poll_messages()
   poll_messages() ◄────── localhost:8765 ──────────► send_message()
```

## Quick Setup

### 1. Install and start the broker

```bash
cp -r <skill-dir>/scripts/server/ ~/.openclaw/agent-bridge-mcp/
cd ~/.openclaw/agent-bridge-mcp
./start.sh   # creates venv, installs deps, starts on port 8765
```

### 2. Register as a launchd service (macOS auto-start)

```bash
cp <skill-dir>/references/launchd-plist.md ~/Library/LaunchAgents/ai.openclaw.agent-bridge.plist
# Edit the plist to set correct paths, then:
launchctl load ~/Library/LaunchAgents/ai.openclaw.agent-bridge.plist
```

### 3. Add to OpenClaw config

Add to `~/.openclaw/openclaw.json`:
```json
{
  "mcp": {
    "servers": {
      "agent-bridge": {
        "url": "http://127.0.0.1:8765/mcp",
        "transport": "streamable-http"
      }
    }
  }
}
```

### 4. Connect the other agent

Give the other agent the MCP URL: `http://127.0.0.1:8765/mcp` (streamable-http transport). They connect with their native MCP client support.

## MCP Tools

| Tool | Parameters | Returns | Use when |
|---|---|---|---|
| `send_message` | `from_agent`, `to`, `subject`, `body`, `reply_to?` | `{message_id, timestamp}` | Sending a task or reply |
| `poll_messages` | `agent_id`, `limit?` | list of message dicts | Checking your inbox |
| `mark_read` | `message_id` | `{status}` | After processing a message |
| `list_agents` | — | list of agent ids | Discovering who's active |

## Message format

```json
{
  "id": "83223c09",
  "from_agent": "hermes",
  "to_agent": "isaac",
  "subject": "Research request",
  "body": "Please analyze...",
  "timestamp": "2026-03-31T16:58:31Z",
  "thread_id": "83223c09",
  "reply_to": null,
  "status": "pending"
}
```

## Fallback: Filesystem bridge

If the MCP server is unavailable, use the filesystem bridge (zero infrastructure):
- See `references/filesystem-bridge.md` for setup
- Inbox/outbox dirs: `~/.openclaw/shared/{agent}-inbox/`

## Heartbeat integration (OpenClaw)

Add to `HEARTBEAT.md` to auto-process incoming messages:
```
Check ~/.openclaw/shared/isaac-inbox/ for new .json files.
If any exist: read, process, reply via hermes-inbox/, move to processed/.
```

## Verification

Test the full loop:
```bash
# From Python
from agent_bridge import AgentBridge
bridge = AgentBridge("isaac")
bridge.send("hermes", "Handshake test", "Can you receive this?")
# Other agent polls and replies
msgs = bridge.receive()
```
