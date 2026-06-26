---
name: gateway-notify
description: "Send automatic notifications when the OpenClaw gateway starts up. Supports Telegram, WhatsApp, Discord, Slack, Signal, iMessage, IRC, Google Chat, Line, WeChat, Feishu (Lark), and QQ Bot. Triggers on phrases like 'gateway restart notification', 'notify me when gateway starts', 'startup alert'. Run setup script to configure channel and recipient."
---

# Gateway Notify

Get notified instantly when your OpenClaw gateway starts up — via any supported messaging channel.

## Quick Start

Run the setup script with your preferred channel and recipient address:

```bash
bash scripts/setup.sh <channel> <address>
```

### Examples

```bash
# Telegram
bash scripts/setup.sh telegram @your_username

# WhatsApp
bash scripts/setup.sh whatsapp +1234567890

# Discord
bash scripts/setup.sh discord 1234567890

# Slack
bash scripts/setup.sh slack #general

# Signal
bash scripts/setup.sh signal +1234567890

# iMessage
bash scripts/setup.sh imessage user@icloud.com

# Google Chat
bash scripts/setup.sh googlechat spaces/xxx

# IRC
bash scripts/setup.sh irc #channel

# Line
bash scripts/setup.sh line user_id

# WeChat (requires openclaw-weixin plugin)
bash scripts/setup.sh openclaw-weixin openid@im.wechat

# Feishu / Lark (requires feishu plugin)
bash scripts/setup.sh feishu chat_id

# QQ Bot (requires qqbot plugin)
bash scripts/setup.sh qqbot chat_id
```

The script will:
1. Create the hook directory at `~/.openclaw/hooks/gateway-notify`
2. Generate `HOOK.md` and `handler.ts` with your channel config
3. Enable the hook
4. Print instructions to restart the gateway

After restart, you'll receive a notification like:

```
🚀 Gateway Started
⏰ 2026-04-03 15:52:00
🌐 127.0.0.1:18789
```

## Supported Channels

| Channel | Address Format |
|---------|---------------|
| telegram | `@username` or chat ID |
| whatsapp | `+countrycodenumber` |
| discord | Channel ID |
| slack | `#channel` or channel ID |
| signal | `+countrycodenumber` |
| imessage | Email or phone number |
| googlechat | Space ID |
| irc | `#channel` |
| line | User ID |
| openclaw-weixin | `openid@im.wechat` |
| feishu | Chat ID (e.g. `oc_xxx`) |
| qqbot | Numeric chat ID |

> **Note:** WeChat (`openclaw-weixin`), Feishu, and QQ Bot are bundled channel plugins. Make sure the channel is configured via `openclaw channels` before using this skill.

For channel-specific details and troubleshooting, see [references/CHANNELS.md](references/CHANNELS.md).

## How It Works

Uses OpenClaw's native hook system:
- Listens for `gateway:startup` events
- Sends a notification via `openclaw message send`
- Zero configuration beyond the initial setup

## Uninstall

```bash
openclaw hooks disable gateway-notify
rm -rf ~/.openclaw/hooks/gateway-notify
```
