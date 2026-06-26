---
name: dingtalk
description: DingTalk channel plugin for OpenClaw - send and receive messages via DingTalk (钉钉)
metadata:
  {
    "openclaw":
      {
        "requires": { "openclaw": ">=2026.2.0" },
      },
  }
---

# DingTalk Channel Plugin for OpenClaw

Connect OpenClaw to DingTalk (钉钉) for enterprise messaging.

## Features

- Send/receive messages via DingTalk API
- Support for both internal apps and webhook robots
- DM and group chat policies
- User allowlist support

## Configuration

### Method 1: Environment Variables

```bash
export DINGTALK_CLIENT_ID="your-app-key"
export DINGTALK_CLIENT_SECRET="your-app-secret"
```

### Method 2: Config File

```bash
openclaw config --section channels
# Select DingTalk and follow prompts
```

Or manually edit config:

```yaml
channels:
  dingtalk:
    enabled: true
    clientId: "ding6kntxc33nvloty5z"
    clientSecret: "your-secret"
    dmPolicy: "allowlist"  # or "open", "pairing"
    allowFrom:
      - "user001"
      - "user002"
    groupPolicy: "allowlist"  # or "open", "disabled"
    groupAllowFrom:
      - "chat001"
```

### Method 3: Webhook Robot (Group Chat)

For group robot webhooks:

```yaml
channels:
  dingtalk:
    enabled: true
    webhookUrl: "https://oapi.dingtalk.com/robot/send?access_token=xxxxx"
    webhookSecret: "SECxxxxx"  # optional, for signature verification
```

## Getting Credentials

1. Go to [DingTalk Open Platform](https://open.dingtalk.com)
2. Create a micro-app or internal robot
3. Copy the **App Key** and **App Secret**
4. For internal apps, ensure these permissions:
   - Contact management (读取通讯录)
   - Message notifications (发送工作通知)

## Usage

### Sending Messages

```typescript
await message({
  channel: "dingtalk",
  target: "user-id",
  text: "Hello from OpenClaw!"
});
```

### Receiving Messages

Configure DingTalk callback URL to point to your OpenClaw Gateway:

```
https://your-gateway/webhook/dingtalk
```

## API Reference

- [DingTalk Open Platform](https://open.dingtalk.com/document/isv/server-api-overview)
- [Robot Webhook API](https://open.dingtalk.com/document/isv/group-robot)

## Troubleshooting

**Error: "invalid timestamp"**
- Check your system time is synchronized

**Error: "app not authorized"**
- Ensure your app has the required permissions in DingTalk admin console

**Error: "ip not in whitelist"**
- Add your OpenClaw Gateway IP to DingTalk app IP whitelist

## Development

This plugin is in beta. Report issues at: https://github.com/openclaw/openclaw

## License

MIT
