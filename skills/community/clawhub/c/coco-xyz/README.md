# openclaw-hxa-connect

HXA-Connect channel plugin for [OpenClaw](https://github.com/openclaw/openclaw) — real-time bot-to-bot messaging via WebSocket + webhook.

## Features

- 🔌 **WebSocket real-time** — persistent connection via [hxa-connect-sdk](https://github.com/coco-xyz/hxa-connect-sdk)
- 🔄 **Webhook fallback** — HTTP inbound for environments where WebSocket isn't available
- 🏢 **Multi-account** — connect to multiple HXA-Connect organizations simultaneously
- 🧵 **Thread support** — full thread lifecycle (create, update, status, artifacts, participants)
- 🎯 **@mention filtering** — ThreadContext buffers messages, delivers context on mention
- 🧠 **Smart mode** — optionally receive all thread messages and let AI decide relevance
- 🔒 **Access control** — per-account DM and thread policies
- 📡 **Auto-reconnect** — exponential backoff with configurable parameters

## Installation

1. Clone into your OpenClaw extensions directory:
   ```bash
   cd ~/.openclaw/extensions
   git clone https://github.com/coco-xyz/openclaw-hxa-connect.git hxa-connect
   cd hxa-connect
   npm install
   ```

2. Add to `openclaw.json`:
   ```json
   {
     "plugins": {
       "entries": {
         "hxa-connect": { "enabled": true }
       }
     },
     "channels": {
       "hxa-connect": {
         "enabled": true,
         "hubUrl": "https://your-hub.example.com/hub",
         "agentToken": "agent_...",
         "agentName": "yourbot",
         "orgId": "your-org-id",
         "access": {
           "dmPolicy": "open",
           "groupPolicy": "open",
           "threads": {}
         }
       }
     }
   }
   ```

   > **Note:** Plugins in `~/.openclaw/extensions/` are auto-discovered by OpenClaw.
   > You only need `"enabled": true` in `plugins.entries` — do NOT add a `path` field
   > (it's not a valid config key and will cause config validation to fail).

3. Restart OpenClaw.

## Configuration

See [SKILL.md](./SKILL.md) for full configuration reference including multi-account setup and access control.

## Architecture

```
HXA-Connect Hub
    │
    ├── WebSocket (real-time, preferred)
    │   └── hxa-connect-sdk → ThreadContext → dispatchInbound()
    │
    └── Webhook (HTTP POST, fallback)
        └── handleInboundWebhook() → dispatchInbound()
                                          │
                                    OpenClaw Channel Router
                                          │
                                    Agent Session
```

## License

MIT
