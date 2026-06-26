---
name: feishu-bot-setup
description: Automated setup and configuration of Feishu/Lark bots with OpenClaw. Use when creating multiple Feishu bots with independent workspaces, memories, and dedicated agents. Handles agent creation, Feishu channel configuration, credential management, and routing bindings. Supports customizable roles, responsibilities, and personalities. Supports both WebSocket and webhook connection modes.
---

# Feishu Bot Setup

Automated setup and configuration of Feishu/Lark bots with OpenClaw.

## Features

- **Flexible Role Definition** - Customize role, style, and responsibilities for each bot
- **Batch Configuration** - Set up multiple bots with one command
- **Independent Workspaces** - Each bot has isolated storage and memory
- **Auto-generated Configs** - Automatically creates SOUL.md, IDENTITY.md, AGENTS.md
- **WebSocket/Webhook** - Support both connection modes

## Overview

This skill automates the creation and configuration of multiple Feishu bots, each with:
- Independent agent workspace
- Dedicated memory and configuration files
- Feishu channel integration
- Proper routing and bindings

## Prerequisites

- OpenClaw installed and running
- Gateway configured and accessible
- Feishu app credentials (App ID, App Secret, Encrypt Key, Verification Token)

## Quick Start

### 1. Prepare Bot Configuration

Create a configuration file with bot details. All fields under `personality` are **customizable**:

```json
{
  "bots": [
    {
      "name": "general-assistant",
      "agentId": "feishu-bot-1",
      "appId": "cli_xxx",
      "appSecret": "xxx",
      "encryptKey": "xxx",
      "verificationToken": "xxx",
      "connectionMode": "websocket",
      "personality": {
        "role": "通用助手",
        "tagline": "你的第一接待入口",
        "style": "温和简洁、快速响应",
        "styleDescription": "态度友好，回答简洁明了，快速响应",
        "responsibilities": [
          "常识问答",
          "轻量办公",
          "需求分流",
          "日常兜底"
        ],
        "description": "我是你的全能基础助理，快速响应你的各种需求。",
        "motto": "有问必答，有求必应，做你最贴心的第一入口。",
        "emoji": "🙋"
      }
    }
  ]
}
```

#### Personality Fields (All Optional, Customizable)

| Field | Description | Example |
|-------|-------------|---------|
| `role` | Bot's role name | "数据分析助手" |
| `tagline` | Short tagline | "你的数据专家" |
| `style` | Working style | "严谨、高效" |
| `styleDescription` | Detailed style | "注重数据准确性，逻辑严密" |
| `responsibilities` | List of duties | ["数据分析", "报表生成"] |
| `description` | Self-introduction | "我是数据分析专家..." |
| `motto` | Signature motto | "让数据说话" |
| `emoji` | Bot emoji | "📊" |

**You can define ANY role you need** - customer service, sales, HR, finance, legal, etc.

### 2. Run Setup Script

```bash
python3 /root/.openclaw/workspace/skills/feishu-bot-setup/scripts/setup_bots.py /path/to/config.json
```

### 3. Restart Gateway

```bash
openclaw gateway restart
```

## Manual Setup Steps

If you need more control, follow these manual steps:

### Step 1: Create Agent

```bash
openclaw agents add <agent-id> --workspace /path/to/workspace --non-interactive
```

### Step 2: Configure Feishu Channel

Edit `~/.openclaw/openclaw.json` and add to `channels.feishu.accounts`:

```json
"<bot-name>": {
  "appId": "cli_xxx",
  "appSecret": "xxx",
  "encryptKey": "xxx",
  "verificationToken": "xxx",
  "domain": "feishu",
  "connectionMode": "websocket",
  "webhookPath": "/webhook/feishu/<bot-name>",
  "dmPolicy": "open",
  "groupPolicy": "open",
  "requireMention": false,
  "reactionNotifications": "off",
  "typingIndicator": true,
  "resolveSenderNames": true
}
```

### Step 3: Bind Agent to Feishu Account

```bash
openclaw agents bind --agent <agent-id> --bind feishu:<bot-name>
```

### Step 4: Create Agent Configuration Files

Create these files in the agent workspace:

- `SOUL.md` - Role definition and personality
- `IDENTITY.md` - Identity information
- `AGENTS.md` - Workspace documentation
- `TOOLS.md` - Tool usage notes (optional)
- `HEARTBEAT.md` - Scheduled tasks (optional)

### Step 5: Restart Gateway

```bash
openclaw gateway restart
```

## Role Examples

You can create bots for ANY purpose. Here are some examples:

### Customer Service Bot
```json
{
  "role": "客服专员",
  "tagline": "你的贴心客服",
  "style": "耐心细致、专业友好",
  "responsibilities": ["问题解答", "投诉处理", "订单查询", "售后服务"],
  "emoji": "🎧"
}
```

### Sales Assistant Bot
```json
{
  "role": "销售顾问",
  "tagline": "你的销售专家",
  "style": "热情主动、洞察需求",
  "responsibilities": ["产品咨询", "方案推荐", "报价生成", "客户跟进"],
  "emoji": "💼"
}
```

### HR Assistant Bot
```json
{
  "role": "HR助手",
  "tagline": "你的人力资源伙伴",
  "style": "专业严谨、保密可靠",
  "responsibilities": ["政策解答", "请假审批", "入职指引", "福利咨询"],
  "emoji": "👔"
}
```

### Legal Advisor Bot
```json
{
  "role": "法务顾问",
  "tagline": "你的法律助手",
  "style": "严谨审慎、依法依规",
  "responsibilities": ["合同审核", "法律咨询", "风险提示", "合规建议"],
  "emoji": "⚖️"
}
```

## Configuration Reference

### Connection Modes

- **websocket** (default): Long-lived connection, no public URL needed
- **webhook**: Requires public URL for Feishu to send events

### Policies

- `dmPolicy`: `open`, `allowlist`, `pairing`, `disabled`
- `groupPolicy`: `open`, `allowlist`, `disabled`
- `requireMention`: `true` or `false`

## Troubleshooting

### Bot Not Responding

1. Check gateway status: `openclaw gateway status`
2. Verify bindings: `openclaw agents bindings`
3. Check logs: `openclaw logs --follow`
4. Ensure Feishu app is published and events are subscribed

### Credential Issues

- Verify App ID and App Secret match Feishu Open Platform
- Check Encrypt Key and Verification Token are correct
- Ensure app has required permissions (robot, im:message)

## Resources

- `scripts/setup_bots.py` - Automated setup script
- `references/example-config.json` - Example configuration
- `references/agent-templates/` - Agent configuration templates
