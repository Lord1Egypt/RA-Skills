---
name: feyagate
description: MCP smart home gateway for AI agents. Control Xiaomi, Tuya, Midea, eWeLink, cameras, and XiaoAI speakers via MCP protocol.
version: 1.2.31
emoji: "🏠"
homepage: https://www.feyagate.com
metadata:
  openclaw:
    requires:
      bins:
        - curl
      config:
        - ~/.feyagate/config/config.yaml
    envVars:
      - name: FEyagate_INSTALL_DIR
        required: false
        description: Override installation directory (default ~/.feyagate)
      - name: FEyagate_PORT
        required: false
        description: HTTP port for the MCP proxy server (default 38080)
sub_skills:
  - name: feyagate-xiaomi
    file: skills/xiaomi.md
    trigger: Xiaomi, Mi Home, MIOT, 小米, camera, P2P, XiaoAI, 小爱, TTS, speaker, 摄像头
  - name: feyagate-tuya
    file: skills/tuya.md
    trigger: Tuya, Smart Life, 涂鸦, DP code, QR auth
  - name: feyagate-midea
    file: skills/midea.md
    trigger: Midea, 美居, 美的, AC, air conditioner, 空调
  - name: feyagate-ewelink
    file: skills/ewelink.md
    trigger: eWeLink, Sonoff, iTEAD, switch, relay
  - name: feyagate-automation
    file: skills/automation.md
    trigger: schedule, timer, trigger, automation, room, memory, note, 定时, 自动化, 房间, 记忆
  - name: feyagate-extension
    file: skills/extension.md
    trigger: serial, RS485, UART, GPIO, Xiaozhi, 小智, license, config, stats, 统计
---

# FeyaGate Skill — MCP Smart Home Gateway

Control smart home devices (lights, cameras, AC, speakers) from any AI agent via MCP protocol. Supports **Xiaomi · Tuya · Midea · eWeLink · Serial · GPIO**.

## Prerequisites

- Python 3.9+
- macOS / Linux / Windows
- `curl` (for installation)

## Before Using Any Tool

Run this check **before** calling any FeyaGate MCP tool:

```bash
feyagate status
```

- **RUNNING** → proceed with tool calls
- **STOPPED** or command not found → run `feyagate start` first
- Not installed → `pip install feyagate-skill && feyagate setup && feyagate start`

## Quick Start

```bash
pip install feyagate-skill       # Install Python package
feyagate setup                   # Download MCP server binary (~30MB)
feyagate start                   # Start service on localhost:38080
feyagate install-claude          # Register with your AI agent
feyagate auth                    # Authorize smart home platform
```

Other agents: `install-cursor`, `install-openclaw`, `install-hermes`, `install-codex`, `install-windsurf`, `install-copilot`

Full guide: [QUICKSTART.md](QUICKSTART.md)

## Server Lifecycle

| Action | Command |
|--------|---------|
| Install binary | `feyagate setup [--dir PATH]` |
| Start | `feyagate start [--port PORT]` |
| Stop | `feyagate stop` |
| Restart | `feyagate restart [--port PORT]` |
| Status | `feyagate status` |
| Logs | `feyagate log [-n 50]` |
| Update | `feyagate update` |
| Auth | `feyagate auth [--status] [--code CODE]` |

## Cross-Platform Tools

These tools work across all platforms (system auto-detects device platform):

| Tool | Arguments | Returns |
|------|-----------|---------|
| `device/list` | `filter` (string[]), `platform` (opt) | Devices with `platform` field |
| `device/specs` | `deviceId` (string) | Platform-specific spec: properties, actions |
| `platform/status` | — | All platform connection/auth/sync status |
| `gateway/info` | — | Version, device count, ports |
| `scene/list` | `platform` (string) | Scene list |
| `scene/trigger` | `platform`, `sceneId` | Trigger result |

> **Parameter convention:** `device/specs` uses `deviceId` (camelCase); platform-specific tools (`xiaomi/*`, `tuya/*`) use `device_id` (snake_case).

## Sub-Skill Loading Strategy

The main skill provides cross-platform tools. Load sub-skills on demand based on the user's platform:

| Sub-Skill | File | When to Load |
|-----------|------|-------------|
| **feyagate-xiaomi** | [skills/xiaomi.md](skills/xiaomi.md) | Xiaomi/Mi Home devices, cameras, XiaoAI speakers |
| **feyagate-tuya** | [skills/tuya.md](skills/tuya.md) | Tuya/Smart Life devices |
| **feyagate-midea** | [skills/midea.md](skills/midea.md) | Midea/美的 appliances |
| **feyagate-ewelink** | [skills/ewelink.md](skills/ewelink.md) | eWeLink/Sonoff devices |
| **feyagate-automation** | [skills/automation.md](skills/automation.md) | Schedule, triggers, rooms, memory |
| **feyagate-extension** | [skills/extension.md](skills/extension.md) | Serial, GPIO, Xiaozhi AI, license |

**Workflow:** `device/list` → `device/specs` → identify platform → load corresponding sub-skill

## License

- **Free**: Xiaomi platform (device control, cameras, XiaoAI, MCP proxy)
- **Licensed**: All platforms (Xiaomi + Tuya + Midea + eWeLink)
  - `tuya/set_property`, `midea/set_property`, `ewelink/set_property` return `license_required` on free edition
  - `get_properties` and read tools work without license

## Configuration

`~/.feyagate/config/config.yaml`:

```yaml
server:
  http_port: 38080
  ws_port: 8765
  bind_address: "0.0.0.0"
auth:
  cloud_server: "cn"      # cn / de / sg / us / ru / i2
camera:
  frame_interval: 500
  jpeg_quality: 90
xiaozhi:
  endpoint: ""            # ws:// or wss:// (empty = disabled)
```

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `command not found: feyagate` | `pip install feyagate-skill` |
| `FeyaGate not installed` | `feyagate setup` |
| `connection refused` | `feyagate start` |
| `authorized: false` | `feyagate auth` or platform auth tool |
| `Tool not found` | Check `tools/list` output |
| `license_required` | Set license via `license/set` tool |

Full API docs: [FeyaGate_MCP_API.md](FeyaGate_MCP_API.md), [FeyaGate_HTTP_API.md](FeyaGate_HTTP_API.md)
