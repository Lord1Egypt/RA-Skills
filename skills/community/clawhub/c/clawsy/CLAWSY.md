# CLAWSY.md — Clawsy Mac Companion Integration Guide

Clawsy is the macOS companion app for OpenClaw. It gives your agent direct access to the user's Mac — screenshots, camera, clipboard, files, and more.

**Repo:** [iret77/clawsy](https://github.com/iret77/clawsy) (GitHub, public)

---

## Capabilities

| Capability | When to Use |
|---|---|
| **Screenshot** | When the user asks what's on screen, debug UI issues, visual feedback |
| **Camera** | When user wants to show something, environment context |
| **Clipboard Read** | When user says "check what I copied" or wants to share text |
| **Clipboard Write** | Push code/text directly to their clipboard — very useful! |
| **Quick Send** | Text sent directly to the agent (user types, you receive) |
| **Files** | Read/write files in the configured shared folder |
| **FinderSync** | Right-click folders → "Clawsy >" submenu → rules/telemetry/actions |

**Rule:** If Clawsy is connected and it improves UX — use it. Don't ask for permission first.

---

## Commands (nodes tool)

Clawsy registers as a `node`. Use the `nodes` tool:

```python
nodes(action="invoke", invokeCommand="screen.capture")
nodes(action="invoke", invokeCommand="clipboard.read")
nodes(action="invoke", invokeCommand="clipboard.write", invokeParamsJson='{"text":"..."}')
nodes(action="invoke", invokeCommand="camera.snap", invokeParamsJson='{"facing":"front"}')
nodes(action="invoke", invokeCommand="camera.list")
nodes(action="invoke", invokeCommand="file.list", invokeParamsJson='{"path": "."}')
nodes(action="invoke", invokeCommand="file.get", invokeParamsJson='{"name":"report.pdf"}')
nodes(action="invoke", invokeCommand="file.set", invokeParamsJson='{"name":"notes.txt", "content":"<base64>"}')
nodes(action="invoke", invokeCommand="location.get")
```

Available commands: `screen.capture`, `clipboard.read`, `clipboard.write`, `camera.list`, `camera.snap`, `file.list`, `file.get`, `file.set`, `file.get.chunk`, `file.set.chunk`, `file.move`, `file.copy`, `file.rename`, `file.stat`, `file.exists`, `file.batch`, `file.delete`, `file.rmdir`, `file.mkdir`, `location.get`

---

## clawsy-service Session

Screenshots, camera photos, and other automatic Clawsy events land in the dedicated `clawsy-service` session — **not in the main chat**. This keeps the main chat clean.

### Why?
Without a separate channel, every screenshot would interrupt the main chat. With `clawsy-service`, all push events collect there and the agent can retrieve them on demand.

### How to Retrieve
```python
sessions_history(sessionKey="clawsy-service", limit=5)
```

### How It Works (Technical)
The app sends screenshots via `node.event` with `event: "agent.deeplink"` and `sessionKey: "clawsy-service"` in payloadJSON. The Gateway routes it to this session instead of the active chat.

---

## clawsy-context.json

The `clawsy-monitor` service (see `server/monitor.mjs`) watches the `clawsy-service` session JSONL and extracts events into a structured JSON file in your workspace:

```json
{
  "clipboard": { "text": "...", "ts": 1234567890, "receivedAt": "..." },
  "screenshots": [{ "filePath": "clawsy-cache/screenshot-123.jpg", "ts": ..., "receivedAt": "..." }],
  "shares": [{ "text": "...", "ts": ..., "receivedAt": "..." }],
  "quickSend": [{ "text": "...", "ts": ..., "receivedAt": "..." }],
  "updatedAt": "..."
}
```

Each bucket is a ring buffer (max 20 items, 24h TTL). Screenshots are saved as files in the `clawsy-cache/` directory.

---

## Envelope Format

Incoming messages from Clawsy are wrapped in `clawsy_envelope`:

```json
{
  "clawsy_envelope": {
    "type": "quick_send",
    "content": "The actual message",
    "version": "0.9.12",
    "localTime": "2026-02-27T01:09:22.609Z",
    "tz": "Europe/Berlin",
    "telemetry": {
      "deviceName": "<device-name>",
      "deviceModel": "Mac",
      "batteryLevel": 0.51,
      "isCharging": false,
      "thermalState": 0,
      "activeApp": "Clawsy",
      "appSwitchRate": 0.22,
      "moodScore": 70,
      "isUnusualHour": false
    }
  }
}
```

### Telemetry Hints
- `thermalState > 1` → Mac is running hot, avoid heavy tasks
- `batteryLevel < 0.2` → mention battery if relevant
- `moodScore < 40` → user is stressed/busy, keep it short
- `isUnusualHour: true` → unusual time, be considerate

---

## Mission Control Protocol

Clawsy displays agent status in its Mission Control view via WebSocket events.

> **Mandatory for every agent:** Send `agent.info` at session start AND every heartbeat (TTL: 45 min). Send `agent.status` during active work and close with `progress: 1.0`.

### agent.info — Show Model in Popover Header

```python
sessions_send(sessionKey="clawsy-service", timeoutSeconds=3, message=json.dumps({
    "kind": "agent.info",
    "payload": {
        "agentName": "<YOUR_AGENT_NAME>",
        "model": "<CURRENT_MODEL>",
        "updatedAt": "<ISO-UTC>"
    }
}))
```

### agent.status — Show Tasks in Mission Control

```python
sessions_send(sessionKey="clawsy-service", timeoutSeconds=3, message=json.dumps({
    "kind": "agent.status",
    "payload": {
        "agentName": "<YOUR_AGENT_NAME>",
        "title": "Building feature X",
        "progress": 0.6,
        "statusText": "Compiling sources…"
    }
}))
```

### Behavior
- Clawsy receives events live over the existing WS connection
- `progress >= 1.0` → task disappears after 10 seconds
- On disconnect → all tasks are automatically cleared
- No file I/O, no FileWatcher, no stale data issues
- Timeout on `sessions_send` is normal and expected — the event is delivered if Clawsy is connected

### 🤖 Mandatory Snippet for Every Subagent You Spawn

When you delegate work to a subagent, paste this block into **every** task prompt. Replace `<label>` with the actual subagent label/name.

```
## Mission Control Updates (MANDATORY)

Report progress after each significant step using sessions_send:

Step 1 — immediately after starting:
sessions_send(sessionKey="agent:main:clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.status","payload":{"agentName":"<label>","title":"<task title>","progress":0.05,"statusText":"Starting…"}}')

Step 2 — at roughly 50% progress:
sessions_send(sessionKey="agent:main:clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.status","payload":{"agentName":"<label>","title":"<task title>","progress":0.5,"statusText":"<what you are doing>"}}')

Final step — after commit/done:
sessions_send(sessionKey="agent:main:clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.status","payload":{"agentName":"<label>","title":"<task title>","progress":1.0,"statusText":"Done"}}')

Use the FULL session key: agent:main:clawsy-service (not just "clawsy-service").
Timeout is expected and normal — the event still delivers.
```

---

## Finding the Connected Node

```python
nodes(action="status")
# → List of all connected nodes; pick the one with platform="macos" and connected=true
# → Note the nodeId for all subsequent calls
```

Find the shared folder path:
```python
nodes(action="invoke", node="<nodeId>", invokeCommand="file.list",
      invokeParamsJson='{"path": "."}')
# Clawsy configures the shared folder in app settings (default: ~/Documents/Clawsy)
```

---

## After Install — Pairing Link

After running `install.sh`, the pairing link is saved to a file in your workspace. Check for it and forward it to your human:

```bash
cat ~/.openclaw/workspace/clawsy-pairing-link.txt 2>/dev/null
```

If the file exists, send the link to your human — they click it on their Mac to connect Clawsy:

> Here is your Clawsy pairing link — click it on your Mac:
> `clawsy://pair?code=<CODE>`
>
> 1. Click the link → macOS asks "Open with Clawsy?" → Yes
> 2. Clawsy connects automatically
> 3. The auto-approve watcher approves the pairing — no further action needed!

After successful pairing, delete the file:

```bash
rm -f ~/.openclaw/workspace/clawsy-pairing-link.txt
```
