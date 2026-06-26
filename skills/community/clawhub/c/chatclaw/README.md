# ChatClaw Skill for OpenClaw

Connect your OpenClaw bot to the ChatClaw cloud dashboard for real-time remote chat, token tracking, and task management — from any browser or mobile device, with no port forwarding required.

## Quick Start

### 1. Get your API key

Sign in at [app.chatclaw.sumeralabs.com](https://app.chatclaw.sumeralabs.com), go to **Settings → API Keys**, and click **Generate API Key**. Your key starts with `ck_`.

### 2. Install the skill

**Option A — Via OpenClaw UI (recommended)**

1. Open the Control UI at `http://localhost:18789`
2. Go to **Skills → Marketplace** and search for **ChatClaw**
3. Click **Install**, paste your API key, click **Enable**

**Option B — Via CLI**

```bash
openclaw skill install chatclaw
openclaw skill enable chatclaw --config '{"api_key": "ck_your_key_here"}'
```

### 3. Verify

```bash
openclaw skill logs chatclaw
```

You should see:
```
Connected to cloud relay ✓
Gateway authenticated ✓
Both connections established — relaying messages ✓
```

Open [app.chatclaw.sumeralabs.com](https://app.chatclaw.sumeralabs.com) — your bot status will show **Online**.

## Standalone testing

```bash
# Uses production relay by default
python main.py ck_your_key_here

# Custom relay (e.g. local dev server)
python main.py ck_your_key_here ws://localhost:8000
```

## Configuration

| Key | Required | Default | Description |
|---|---|---|---|
| `api_key` | Yes | — | ChatClaw API key from app.chatclaw.sumeralabs.com |
| `cloud_url` | No | `wss://api.sumeralabs.com` | Relay URL — leave default unless self-hosting |

### Environment variables

Set `OPENCLAW_DATA_DIR` to override the OpenClaw data path (useful for non-standard installs).
The skill auto-detects `/data/.openclaw` (Docker/VPS) and `~/.openclaw` (standard install).

## Architecture

```
Dashboard (browser / mobile)
      ↕  wss://api.sumeralabs.com
ChatClaw Cloud Relay
      ↕  wss://api.sumeralabs.com/ws/agent/{api_key}
ChatClaw Skill  ← this package
      ↕  ws://localhost:18789     (Ed25519 auth handshake)
      ↕  http://localhost:18789/v1/chat/completions  (SSE streaming)
OpenClaw Gateway → Agent (LLM)
```

The skill maintains two outbound connections. No inbound ports are opened.

## Troubleshooting

| Problem | Solution |
|---|---|
| `Cloud connection failed` | Check API key is correct at app.chatclaw.sumeralabs.com |
| `OpenClaw identity files not found` | Run `openclaw wizard` or set `OPENCLAW_DATA_DIR` |
| `Gateway HTTP 403` | Restart skill — it auto-enables the required HTTP endpoint |
| Token count shows 0 | Normal on first message; counts appear after the first completion |

## License

[MIT-0](https://opensource.org/licenses/MIT-0) (No Attribution Required)
