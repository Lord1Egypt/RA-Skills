# claw-use-mihomo

[![npm](https://img.shields.io/npm/v/mihomod)](https://www.npmjs.com/package/mihomod)

Network proxy manager and health watchdog for [mihomo](https://github.com/MetaCubeX/mihomo). OpenClaw skill + npm CLI.

## Features

- 📦 **Install** mihomo binary (auto-detect OS/arch)
- ⚙️ **Configure** from subscription URLs or protocol links (vmess/ss/trojan/vless)
- 🔍 **Monitor** proxy health with configurable endpoints
- 🔄 **Auto-switch** to best available node on failure
- 🛡️ **Safe config writes** — atomic write + YAML validation + backup
- 🖥️ **Cross-platform** Linux, macOS, Windows

## Quick Start

```bash
# Install mihomo
npx mihomod install

# Configure from subscription
npx mihomod config "https://your-subscription-url"

# Or add individual nodes
npx mihomod add "vmess://..."

# Start mihomo
npx mihomod start

# Check status
npx mihomod status

# Start health watchdog
npx mihomod watch
```

## Commands

| Command | Description |
|---------|-------------|
| `install` | Download and install mihomo binary |
| `config <url>` | Generate config from subscription URL |
| `add <url>` | Add a single proxy node |
| `start` | Start mihomo service |
| `stop` | Stop mihomo service |
| `status` | Show proxy status |
| `nodes` | List all proxy nodes |
| `switch [name]` | Switch to specific or best node |
| `watch` | Start health watchdog daemon |

## Configuration

Auto-created at `~/.config/mihomod/config.json`:

```json
{
  "mihomo": {
    "api": "http://127.0.0.1:9090",
    "secret": "",
    "configPath": "~/.config/mihomo/config.yaml"
  },
  "watchdog": {
    "endpoints": [
      {"url": "https://www.gstatic.com/generate_204", "expect": 204}
    ],
    "checkInterval": 30,
    "failThreshold": 2,
    "cooldown": 60,
    "maxDelay": 3000,
    "nodePriority": ["US", "SG", "JP", "HK"]
  },
  "selector": "🚀节点选择"
}
```

## Safety

- **Atomic config writes**: new config is written to a temp file, validated (YAML parse + structure check), then renamed into place. Old config is always backed up to `.bak`.
- **All network calls have timeouts**: API 5s, subscriptions 30s, binary downloads 120s.
- **Subscription size capped** at 10MB.
- **Graceful shutdown**: watchdog handles SIGTERM/SIGINT cleanly.

## Agent-Friendly

All commands output JSON by default (human-readable when stdout is a TTY). Designed for AI agent automation.

## As OpenClaw Skill

```bash
openclaw skills install claw-use/claw-use-mihomo
```

## License

MIT
