# Gateway Notify

Auto-notify when OpenClaw gateway restarts. Supports multiple messaging channels.

## Features

- 🚀 Automatic notification on gateway startup
- 📊 Shows model, time, and port info
- 🌐 Supports 5 channels: iMessage, WhatsApp, Telegram, Discord, Slack
- ⚡ One-command setup

## Quick Start

```bash
scripts/setup_gateway_notify.sh <channel> <address>
```

Examples:
```bash
scripts/setup_gateway_notify.sh imessage user@example.com
scripts/setup_gateway_notify.sh telegram @username
```

## Installation

### Method 1: From GitHub

```bash
git clone https://github.com/deemoartisan/gateway-notify.git
cd gateway-notify
scripts/setup_gateway_notify.sh imessage your@email.com
```

### Method 2: Download .skill file

Download `gateway-notify.skill` from releases and install:
```bash
openclaw skills install gateway-notify.skill
```

## Documentation

- [English Manual](SKILL.md)
- [中文手册](https://github.com/deemoartisan/gateway-notify/blob/main/gateway-notify使用手册.md)

## Supported Channels

| Channel | CLI Tool | Address Format |
|---------|----------|----------------|
| iMessage | `imsg` | Email or phone |
| WhatsApp | `wacli` | Phone with country code |
| Telegram | `openclaw message` | Username or Chat ID |
| Discord | `openclaw message` | Channel ID |
| Slack | `openclaw message` | Channel name or ID |

## License

MIT

## Author

哥们鼠 🦞
