---
name: feishu-setup
description: >
  Complete Feishu (飞书) integration setup guide for OpenClaw. Use when setting up a new OpenClaw
  instance with Feishu capabilities, configuring the openclaw-lark plugin, or troubleshooting
  Feishu connectivity. Covers: Feishu Open Platform app creation, OAuth scopes, event subscriptions,
  OpenClaw config generation, plugin installation, tool enablement, and permission verification.
  Triggers: "setup feishu", "configure feishu", "飞书配置", "飞书部署", "飞书接入",
  "feishu integration", "lark setup", "openclaw-lark".
---

# Feishu Setup Guide for OpenClaw

End-to-end guide to configure OpenClaw with full Feishu capabilities: IM, Calendar, Docs, Bitable, Contacts, Search, and OAuth.

## Architecture Overview

```
Feishu Cloud ←→ Feishu Bot (Webhook/Event) ←→ openclaw-lark plugin ←→ OpenClaw Gateway
```

- **openclaw-lark** (`@larksuite/openclaw-lark`): Official Feishu channel plugin. Provides all feishu_* tools, skills, and OAuth flow.
- **openclaw-extension-miaoda** (`@lark-apaas/openclaw-extension-miaoda`): Optional. Miaoda platform integration.
- **openclaw-extension-miaoda-coding** (`@lark-apaas/openclaw-extension-miaoda-coding`): Optional. Miaoda vibe-coding extension.

## Setup Checklist

### Phase 1: Create Feishu App (Open Platform)

1. Go to [Feishu Open Platform](https://open.feishu.cn/app) → Create App
2. Fill in App Name, Description, Icon
3. Note down credentials: **App ID** (`cli_xxx`) and **App Secret**
4. Under "Security Settings", configure **Encrypt Key** and **Verification Token** (or let platform auto-generate)

### Phase 2: Configure App Capabilities

Read [references/feishu-app-config.md](references/feishu-app-config.md) for detailed step-by-step instructions covering:

- Permissions & Scopes (OAuth)
- Event Subscriptions
- Bot capabilities
- Card interaction

### Phase 3: Install openclaw-lark Plugin

```bash
# In OpenClaw project directory
npx openclaw plugin install @larksuite/openclaw-lark

# Optional Miaoda extensions
npx openclaw plugin install @lark-apaas/openclaw-extension-miaoda
npx openclaw plugin install @lark-apaas/openclaw-extension-miaoda-coding
```

### Phase 4: Configure OpenClaw

Read [references/openclaw-config-reference.md](references/openclaw-config-reference.md) for the complete config template with all feishu-related sections.

Key config sections:
- `channels.feishu` — Channel credentials and policies
- `plugins.entries.openclaw-lark` — Plugin enablement
- `tools.alsoAllow` — Enable feishu tools
- `tools.deny` — Disable unwanted tools
- `skills.entries.feishu-task` — Task skill toggle

Quick start config patch:

```bash
openclaw config set channels.feishu.enabled true
openclaw config set channels.feishu.appId '<YOUR_APP_ID>'
openclaw config set channels.feishu.appSecret '<YOUR_APP_SECRET>'
openclaw config set channels.feishu.domain 'feishu'
openclaw config set channels.feishu.requireMention true
openclaw config set channels.feishu.dmPolicy 'allowlist'
openclaw config set channels.feishu.allowFrom '<OWNER_OPEN_ID>'
openclaw config set plugins.entries.openclaw-lark.enabled true
```

### Phase 5: Configure Webhook / Event Subscription

- **Event subscription URL**: `https://<YOUR_HOST>/feishu/webhook` (or as documented by openclaw-lark)
- Subscribe to events listed in [references/feishu-app-config.md](references/feishu-app-config.md)

### Phase 6: Restart and Verify

```bash
openclaw gateway restart
# Or in non-systemd env:
sh scripts/restart.sh
```

Verify:
1. Bot appears in Feishu contacts
2. Send a DM to bot — it should respond
3. Check `openclaw status` for channel health

## Tool Matrix

See [references/tool-matrix.md](references/tool-matrix.md) for the complete mapping of feishu_* tools to capabilities, with enable/disable configuration.

## Permission Scopes Reference

See [references/permissions-reference.md](references/permissions-reference.md) for all OAuth scopes needed per feature area.

## Troubleshooting

- **Bot not responding**: Check webhook URL, event subscription, and `openclaw status`
- **OAuth failures**: User needs to complete authorization flow; check scopes in Feishu Open Platform
- **Tool not found**: Verify tool is in `tools.alsoAllow` and not in `tools.deny`
- **Permission denied on API call**: Check Feishu app has the required scope enabled AND user has authorized

For deep diagnostics, read the feishu-troubleshooting skill if available.
