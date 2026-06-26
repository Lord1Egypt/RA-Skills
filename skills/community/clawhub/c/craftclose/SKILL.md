---
name: craftclose
description: "AI-powered Minecraft server monitoring with crash detection, auto-restart, and smart alerts. Use when: monitoring Minecraft servers, diagnosing crashes, setting up auto-restart, configuring Telegram/Discord alerts, analyzing server performance, or managing Pterodactyl panel servers. NOT for: Bedrock-only servers, non-Minecraft game servers, or web application monitoring."
homepage: https://github.com/LaunchDay-Studio-Inc/craftclose
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "requires": { "bins": ["craftclose"], "nodePackages": ["craftclose"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "craftclose",
              "bins": ["craftclose"],
              "label": "Install CraftClose CLI (npm)",
            },
          ],
      },
  }
---

# CraftClose — AI Minecraft Server Monitor

AI-powered Minecraft server monitoring — crash detection, auto-restart, and smart alerts.

## When to Use

✅ **USE this skill when:**

- Monitoring a Minecraft server's health (TPS, players, uptime)
- Diagnosing crashes or performance issues
- Setting up auto-restart on crash detection
- Configuring Telegram bot or Discord webhook alerts
- Analyzing server logs with AI (Gemini)
- Managing servers via Pterodactyl panel
- Checking plugin conflicts or config issues

## When NOT to Use

❌ **DON'T use this skill when:**

- Bedrock-only servers (Java/Paper servers only)
- Non-Minecraft game servers
- Web application monitoring
- Network diagnostics unrelated to Minecraft

## Install

```bash
npm install -g craftclose
```

## Setup

```bash
# Copy example config
craftclose init

# Or manually create craftclose.yml
cp node_modules/craftclose/craftclose.example.yml ./craftclose.yml
```

## Config (`craftclose.yml`)

```yaml
servers:
  - name: my-server
    host: 127.0.0.1
    connections:
      ssh:
        port: 22
        username: minecraft
        key_path: ~/.ssh/id_rsa
      rcon:
        port: 25575
        password: changeme
      pterodactyl:
        panel_url: https://panel.example.com
        api_key: ptlc_xxxxx
        server_id: abc123

monitoring:
  interval: 60
  auto_restart: true
  max_restarts: 3
  restart_window: 300

alerts:
  telegram:
    bot_token: "123456:ABC..."
    chat_id: "-100123456"
  discord:
    webhook_url: "https://discord.com/api/webhooks/..."

ai:
  provider: gemini
  api_key: ${GEMINI_API_KEY}
```

## CLI Commands

```bash
# Test all connections
craftclose test

# Check server status
craftclose status

# Start continuous monitoring
craftclose monitor

# View crash/event history
craftclose history

# AI-powered crash analysis
craftclose analyze

# Config optimization suggestions
craftclose optimize

# Check plugin conflicts
craftclose conflicts

# Pterodactyl panel operations
craftclose panel status
craftclose panel restart
craftclose panel console "say Hello"
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Crash Detection** | 20+ built-in patterns (OOM, plugin errors, world corruption, etc.) |
| **Auto-Restart** | Configurable restart on crash with rate limiting |
| **AI Analysis** | BYOK Gemini for deep crash analysis and optimization |
| **3 Connections** | SSH, RCON, Pterodactyl — use any combo |
| **Alerts** | Telegram bot + Discord webhook notifications |
| **History** | TPS and player count stored in local SQLite |
| **Security** | 6-layer sandbox (path jail, RCON filter, input sanitizer, audit log, action allowlist, confirmation gate) |

## OpenClaw Integration

CraftClose is also an OpenClaw skill. When installed globally, OpenClaw can use it to monitor and manage Minecraft servers through natural language.

## Links

- [GitHub](https://github.com/LaunchDay-Studio-Inc/craftclose)
- [npm](https://www.npmjs.com/package/craftclose)
- [Discord](https://discord.gg/bJDGXc4DvW)
