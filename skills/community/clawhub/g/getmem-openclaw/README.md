# getmem.ai Memory Plugin for OpenClaw

Persistent memory for every user via [getmem.ai](https://getmem.ai). Automatically ingests conversations and injects relevant context before each agent reply.

## Install

```bash
openclaw plugins install clawhub:@getmem/openclaw-getmem
openclaw config set plugins.openclaw-getmem.apiKey gm_live_...
openclaw gateway restart
```

Get your API key at [platform.getmem.ai](https://platform.getmem.ai) — **$20 free credit on signup, $10/month added automatically**.

## How it works

On every inbound message:
1. **Fetch** — calls `GET /v1/memory/get` with the sender's user ID and message as query
2. **Inject** — appends retrieved memory context to the agent's prompt
3. **Ingest** — after the agent replies, calls `POST /v1/memory/ingest` with the full exchange (fire-and-forget)

Memory accumulates over time. The more you use it, the richer the context becomes.

## Config options

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `apiKey` | ✅ | — | Your getmem.ai API key (`gm_live_...`) |
| `baseUrl` | ❌ | `https://memory.getmem.ai` | API base URL |
| `enabled` | ❌ | `true` | Enable/disable memory |

## Verify it's working

After restart, check your gateway logs:

```
[getmem] Hooks registered: message:received ✓  message:sent ✓
[getmem] Memory active — getmem.ai
```

If you see `Memory active` but **not** the hooks line, the hooks failed to register. See troubleshooting below.

On the first message after install, you should see:
```
[getmem] message_received fired — session:... action:received
```

## Troubleshooting

### "hook registration missing name" in logs
This is an OpenClaw internal warning when a plugin registers a hook without a `name` option. This plugin includes the required `{ name: "..." }` option — if you see this error, you may be running an old version. Reinstall:
```bash
openclaw plugins uninstall openclaw-getmem
openclaw plugins install clawhub:@getmem/openclaw-getmem
```

### Hooks not firing (no "message_received fired" in logs)
Ensure the plugin loaded with both hooks confirmed in startup logs. If only "Memory active" appears without the hooks line, the gateway may have loaded a cached version. Try:
```bash
openclaw gateway restart
```

### Memory not accumulating
Check that `message:sent` hook is firing after replies. If ingest calls fail, you'll see:
```
[getmem] ingest failed: ...
```

### API key errors
Verify your key starts with `gm_live_` and is set correctly:
```bash
openclaw config get plugins.openclaw-getmem.apiKey
```

## Links

- [getmem.ai](https://getmem.ai) — landing page
- [platform.getmem.ai](https://platform.getmem.ai) — dashboard & API keys
- [API docs](https://getmem.ai/llms-full.txt) — full API reference
- [GitHub](https://github.com/getmem-ai) — source code
