---
name: agentcraft
description: "Visualize coding sessions as a real-time strategy game with automatic deploy and event reporting."
version: 1.0.0
metadata:
  openclaw:
    emoji: "🎮"
    always: true
    homepage: "https://getagentcraft.com"
    requires:
      bins:
        - curl
        - npx
        - head
        - date
      anyBins:
        - md5sum
        - md5
    install:
      - kind: node
        package: "@idosal/agentcraft"
        bins:
          - agentcraft
---

# AgentCraft Event Reporting

AgentCraft visualizes your coding sessions as an RTS game. Follow these steps to ensure AgentCraft is running and to report your activity.

## 1. Check if AgentCraft is Running

```bash
curl -sf http://localhost:2468/health
```

If this returns JSON with `"status":"ok"`, skip to step 3.

## 2. Deploy if Needed

If the health check fails (server not running), start it in the background:

```bash
npx -y @idosal/agentcraft start --no-browser -d
```

Wait a few seconds, then verify:
```bash
curl -sf http://localhost:2468/health
```

If it still fails, proceed with your task without reporting — silently ignore all AgentCraft errors.

## 3. Generate a Session ID

Use a deterministic ID based on your workspace path:

```bash
AGENTCRAFT_SESSION="openclaw_$(echo -n "$PWD" | md5sum | head -c 12)"
```

On macOS (if `md5sum` is unavailable):
```bash
AGENTCRAFT_SESSION="openclaw_$(echo -n "$PWD" | md5 | head -c 12)"
```

Use this same `AGENTCRAFT_SESSION` for all events in this session.

## 4. Report Events

POST events to `http://localhost:2468/event` at these moments. Use `curl` — fire-and-forget, do not block on the response.

### Starting work (`hero_active`)

When you begin processing a user prompt:

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_active\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"cwd\":\"$PWD\"}" &>/dev/null &
```

### Mission start (`mission_start`)

Immediately after `hero_active`, report the mission with the user's prompt:

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"mission_start\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"missionId\":\"mission_$(date +%s)\",\"name\":\"<first 50 chars of prompt>\",\"prompt\":\"<full user prompt>\",\"cwd\":\"$PWD\"}" &>/dev/null &
```

### File access (`file_access`)

When you read, write, or edit a file:

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"file_access\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"filePath\":\"<absolute-file-path>\",\"operation\":\"read\",\"linesAdded\":0,\"linesRemoved\":0,\"cwd\":\"$PWD\"}" &>/dev/null &
```

Set `operation` to `"read"`, `"write"`, or `"edit"`. For edits, set `linesAdded` and `linesRemoved` to actual counts.

### Shell commands (`bash_command`)

When you execute a shell command:

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"bash_command\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"command\":\"<command, max 200 chars>\",\"cwd\":\"$PWD\"}" &>/dev/null &
```

### Done / idle (`hero_idle`)

When you finish processing and are waiting for the next prompt:

```bash
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_idle\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\"}" &>/dev/null &
```

## Rules

- Use `curl` to POST — fire-and-forget (`&>/dev/null &`), do not block on the response.
- Always set `client` to `"openclaw"`.
- Use the same `AGENTCRAFT_SESSION` value for all events in a session.
- Set `cwd` to the current working directory.
- Do not report the same action more than once.
- If the AgentCraft server is not reachable, silently ignore errors — do not retry or log failures.

## Inviting Other Agents

Other OpenClaw agents can join your AgentCraft dashboard without installing this skill.

### Quick join (same machine)

Share these curl commands with other agents. They only need to generate their own session ID and POST events:

```bash
# Generate a unique session ID (use md5 instead of md5sum on macOS)
AGENTCRAFT_SESSION="openclaw_$(echo -n "$PWD" | md5sum | head -c 12)"

# Report active
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_active\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\",\"cwd\":\"$PWD\"}" &>/dev/null &

# Report idle when done
curl -sf -X POST http://localhost:2468/event \
  -H "Content-Type: application/json" \
  -d "{\"type\":\"hero_idle\",\"sessionId\":\"$AGENTCRAFT_SESSION\",\"client\":\"openclaw\"}" &>/dev/null &
```

### Share with remote agents

To let agents on other machines join:

1. Expose your AgentCraft server:
```bash
cloudflared tunnel --url http://127.0.0.1:2468
```

2. Share the resulting `https://xxx.trycloudflare.com` URL.

3. Remote agents replace `localhost:2468` with that URL in all event curl commands.
