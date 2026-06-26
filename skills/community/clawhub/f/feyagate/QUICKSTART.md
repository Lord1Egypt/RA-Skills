# FeyaGate Skill — Quick Start Guide

```
  _____                 ____       _
 |  ___|__ _   _  __ _ / ___| __ _| |_ ___
 | |_ / _ \ | | |/ _` | |  _ / _` | __/ _ \
 |  _|  __/ |_| | (_| | |_| | (_| | ||  __/
 |_|  \___|\__, |\__,_|\____|\__,_|\__\___|
           |___/
```

> **For AI Assistants (OpenClaw, Claude Code, Hermes, Codex, Windsurf, Copilot, 小智AI, Cursor):**
> Follow Steps 1-4 sequentially. Report progress at each step. Do NOT skip steps.
> Steps marked with **[AUTO]** can be executed without asking the user.
> Steps marked with **[ASK]** require user input before proceeding.

## Prerequisites

- Python 3.9+
- Internet access (for downloading MCP server binary ~30MB)

## One-Line Install [AUTO]

**macOS / Linux** — installs the Python package and MCP server binary in one step:

```bash
curl -fsSL https://raw.githubusercontent.com/toddpan/feyagate-skill/main/scripts/install.sh | bash
```

**Windows (PowerShell):**

```powershell
iwr -useb https://raw.githubusercontent.com/toddpan/feyagate-skill/main/scripts/install.ps1 | iex
```

After one-line install, skip to **Step 3** (install agent skill). If you prefer manual steps, continue below.

> **For developers:** Clone the repo and use `pip install -e .` instead of the one-line script — see Step 1 Option B.

## Step 1: Install [AUTO]

**Option A — from PyPI (standard online install):**

```bash
pip install feyagate-skill
```

**Option B — from source (developers / contributors):**

```bash
git clone https://github.com/toddpan/feyagate-skill.git
cd feyagate-skill
pip install -e ".[dev]"     # includes pytest and other dev dependencies
```

Verify:

```bash
feyagate --version
```

## Step 2: Setup & Start [AUTO]

Download and install the MCP server binary (may take 1-2 minutes):

```bash
feyagate setup
```

Default directory: `~/.feyagate`. Customize with `feyagate setup --dir ~/my-feyagate`.

Start the service:

```bash
feyagate start
```

Verify:

```bash
feyagate status
```

Service URL: `http://localhost:38080/mcp/http`. Custom port: `feyagate start --port 9090`.

## Step 3: Install as AI Agent Skill [ASK]

> **IMPORTANT:** This step installs the FeyaGate skill (SKILL.md + sub-skills) for the AI agent you are currently running in.
> Ask the user: "Which AI agent should I install for?" or detect from the environment.

```bash
feyagate install-claude     # Claude Code
feyagate install-cursor     # Cursor
feyagate install-openclaw   # OpenClaw
feyagate install-hermes     # Hermes Agent
feyagate install-windsurf   # Windsurf
feyagate install-copilot    # GitHub Copilot (VS Code)
feyagate install-codex      # OpenAI Codex CLI
```

After install, **restart the AI agent** to load the skill.

## Step 4: Authorize Smart Home Platform [ASK]

> Ask the user which platform(s) they want to authorize.

### Xiaomi / Mi Home (OAuth)

```bash
feyagate auth --status    # Check current status
feyagate auth             # Interactive OAuth authorization
```

The interactive flow will output a URL → user opens in browser → logs in → pastes the callback URL back.

### Tuya (QR Code Scan)

Requires Tuya Smart or Smart Life app. User Code location: **Me → Settings → Account & Security → User Code**.

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"auth/tuya_qr","arguments":{"user_code":"USER_CODE"}}}' \
  | python3 -m json.tool
```

Scan the returned `qr_url` with the Tuya app, then check status with `auth/tuya_qr_status`.

### Midea (Password Login)

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"auth/midea_login","arguments":{"account":"PHONE_OR_EMAIL","password":"PASSWORD"}}}' \
  | python3 -m json.tool
```

### eWeLink (Password Login)

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"auth/ewelink_login","arguments":{"email":"EMAIL","password":"PASSWORD","country_code":"+86"}}}' \
  | python3 -m json.tool
```

### Verify Authorization

```bash
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"auth/platforms","arguments":{}}}' \
  | python3 -m json.tool
```

## Setup Complete

After completing Steps 1-4, the user can control smart home devices through their AI agent.
The AI agent will automatically use the MCP tools (e.g. `device/list`, `device/specs`, `xiaomi/set_property`).

---

## Service Management

```bash
feyagate status      # Check service status
feyagate log         # View server logs
feyagate log -n 50   # View last 50 lines of logs
feyagate stop        # Stop service
feyagate restart     # Restart service
feyagate update      # Update MCP server to latest version
```

## Usage Examples

> These examples show how to use the MCP tools via curl.
> When using through an AI agent, the agent calls these tools automatically — no curl needed.

### List & Search Devices

```bash
# All devices
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"device/list","arguments":{"filter":[]}}}' \
  | python3 -m json.tool

# Search by keyword
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"device/list","arguments":{"filter":["living room","light"]}}}' \
  | python3 -m json.tool

# Filter by platform
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"device/list","arguments":{"filter":[],"platform":"xiaomi"}}}' \
  | python3 -m json.tool
```

### Control Xiaomi / MIOT Device

**Control flow:** `device/list` → `device/specs` (get siid/piid/aiid) → `xiaomi/set_property` or `xiaomi/execute_action`

> **Parameter naming:** Cross-platform tool `device/specs` uses `deviceId` (camelCase); platform-specific tools use `device_id` (snake_case).

```bash
# Query device spec
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"device/specs","arguments":{"deviceId":"YOUR_DID"}}}' \
  | python3 -m json.tool

# Read property
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xiaomi/get_properties","arguments":{"device_id":"YOUR_DID","siid":2,"piids":[1]}}}' \
  | python3 -m json.tool

# Set property (turn on light)
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"xiaomi/set_property","arguments":{"device_id":"YOUR_DID","siid":2,"piid":1,"value":true}}}' \
  | python3 -m json.tool

# Execute action
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"xiaomi/execute_action","arguments":{"device_id":"YOUR_DID","siid":2,"aiid":1}}}' \
  | python3 -m json.tool
```

### Scenes

```bash
# List scenes
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"scene/list","arguments":{"platform":"xiaomi"}}}' \
  | python3 -m json.tool

# Trigger scene
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"scene/trigger","arguments":{"platform":"xiaomi","sceneId":"SCENE_ID"}}}' \
  | python3 -m json.tool
```

### Xiao AI Speaker

```bash
# TTS broadcast
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"xiaoai/tts","arguments":{"device_id":"SPEAKER_DID","text":"Hello, welcome home"}}}' \
  | python3 -m json.tool

# Play music
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xiaoai/play_music","arguments":{"device_id":"SPEAKER_DID","text":"Play some pop music"}}}' \
  | python3 -m json.tool

# Voice control (silent mode)
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"xiaoai/control","arguments":{"device_id":"SPEAKER_DID","command":"turn on the living room light","silence":true}}}' \
  | python3 -m json.tool
```

### Camera

```bash
# CLI
feyagate snapshot --list
feyagate snapshot --camera-id CAMERA_DID --connect --count 3

# API: connect → wait → snapshot → disconnect
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"xiaomi/camera_connect","arguments":{"camera_id":"CAMERA_DID"}}}'
# Wait 3-5 seconds for P2P connection
curl -s -X POST http://localhost:38080/mcp/http \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"xiaomi/camera_snapshot","arguments":{"camera_id":"CAMERA_DID","count":1}}}' \
  | python3 -m json.tool
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `command not found: feyagate` | `pip install feyagate-skill` or `pip install -e .` from repo root |
| `FeyaGate not installed` | `feyagate setup` |
| `connection refused` | `feyagate start` |
| `authorized: false` | `feyagate auth` |
| `cannot open shared object file` | `feyagate update` or re-run `feyagate setup` |
| `Tool not found` | Check tool name with `tools/list` |
| `key 'device_id' not found` | `device/specs` uses `deviceId`; platform tools use `device_id` |
| `camera_connect` fails | Check camera native libraries in `lib/` |
| No frame data | Wait 3-5 seconds, check `xiaomi/camera_status` |

For full API reference, see [SKILL.md](SKILL.md), [FeyaGate_MCP_API.md](FeyaGate_MCP_API.md), and [FeyaGate_HTTP_API.md](FeyaGate_HTTP_API.md).
