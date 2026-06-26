---
name: clawsy
version: 1.0.3
description: >
  Clawsy is a native macOS companion app that gives your OpenClaw agent eyes and
  hands on the user's Mac — screenshots, clipboard, camera, files, location, and
  live Mission Control. Connects via WebSocket (SSH fallback available).
  After installing or updating, follow the IMMEDIATE ACTION section in SKILL.md
  to send the user their setup code.
metadata:
  openclaw:
    emoji: "\U0001F431"
    postInstall:
      - command: >-
          python3 -c "import json,pathlib;
          c=json.loads(pathlib.Path.home().joinpath('.openclaw/gateway.json').read_text());
          h=c.get('host','localhost');t=c.get('authToken','');
          print(f'CLAWSY-SETUP\nhost: {h}\ntoken: {t}')"
        label: "Read gateway config for Clawsy setup code"
    postInstallMessage: >
      Clawsy skill installed. Now send the user the setup instructions from SKILL.md
      (section "IMMEDIATE ACTION AFTER INSTALL") including the download link and the
      setup code printed above. Do NOT just say "installed".
---

# Clawsy Skill — Agent Reference

**Platform:** macOS 14+ (Sonoma / Sequoia), Apple Silicon + Intel
**Download:** <https://github.com/iret77/clawsy/releases/latest>

---

## IMMEDIATE ACTION AFTER INSTALL

After installing this skill, you **must** send the user their setup instructions.
Do not just reply "installed" or "done".

1. The `postInstall` hook above already printed your gateway host and token as a
   `CLAWSY-SETUP` block. If not, read them manually:
   ```bash
   cat ~/.openclaw/gateway.json | python3 -c "import json,sys;c=json.load(sys.stdin);print('host:', c.get('host','localhost'));print('token:', c.get('authToken',''))"
   ```
2. Send the user **everything in one message**:
   > **Clawsy Setup**
   >
   > 1. Download Clawsy (free, macOS 14+): https://github.com/iret77/clawsy/releases/latest
   > 2. Unzip, drag to /Applications, run `xattr -cr /Applications/Clawsy.app`, launch.
   > 3. Click "Add Host" and paste this setup code:
   >
   > ```
   > CLAWSY-SETUP
   > host: <actual hostname>
   > token: <actual token>
   > ```

Replace the placeholders with the real values. Do not send placeholders.

---

## Sub-Agent Propagation (MANDATORY)

When spawning sub-agents, you **must** include a Clawsy context block so they
can report progress and use Clawsy capabilities. Copy this verbatim into every
sub-agent system prompt:

```
## Clawsy — macOS Companion
A Clawsy node (platform="macos") is connected. You can:
- Take screenshots: nodes(action="invoke", invokeCommand="screen.capture")
- Read clipboard: nodes(action="invoke", invokeCommand="clipboard.read")
- Write clipboard: nodes(action="invoke", invokeCommand="clipboard.write", invokeParamsJson='{"text":"..."}')
- Read/write files in shared folder: file.get, file.set, file.list, etc.
- Get location: nodes(action="invoke", invokeCommand="location.get")

Report progress after each significant step:
sessions_send(sessionKey="clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.status","payload":{"agentName":"<YOUR_LABEL>","title":"<STEP>","progress":<0.0-1.0>,"statusText":"<DETAILS>"}}')
Start at 0.05 — finish at 1.0. Timeout errors on sessions_send are normal; do not retry.

For full command reference, read the clawsy skill: skill(name="clawsy")
```

This applies to **all** sub-agents — current and future. A sub-agent that does
not receive this block cannot report Mission Control status and will not know
about Clawsy capabilities.

---

## Quick Start — Is Clawsy Connected?

```python
nodes(action="status")
# Look for a node with platform="macos" and connected=true
```

- **Connected:** Use any command from the reference below.
- **Not connected / No node found:** **You must run the First-Time Setup now.** Check if the user already has Clawsy installed. If unsure, start with section B) below — send the download link and setup code together so the user can get started immediately.

---

## First-Time Setup

### A) User Already Has Clawsy Installed

The user clicks "Add Host" in Clawsy. The app copies a setup prompt to the
clipboard. The user sends it to you via any channel (Telegram, Slack, etc.).

**When you receive the prompt**, respond with the gateway connection details:

```
CLAWSY-SETUP
host: <gateway hostname or IP — no protocol, no port>
token: <gateway authentication token>
```

The user pastes your response into Clawsy. Done — host is created and connects.

> **How to find the values:**
> - `host`: The hostname or IP where the OpenClaw gateway runs.
> - `token`: The `authToken` from your gateway config. Run
>   `cat ~/.openclaw/gateway.json | python3 -c "import json,sys;print(json.load(sys.stdin).get('authToken',''))"` if unsure.

After pairing, a node with `platform="macos"` appears in `nodes(action="status")`.
Approve if prompted:
```bash
openclaw nodes approve <requestId>
```

### B) User Needs to Install Clawsy First (Most Common Path)

Look up your gateway host and token, then send **everything in one message** so
the user can get started right away:

> **Clawsy Setup**
>
> 1. Download Clawsy (free, macOS 14+): https://github.com/iret77/clawsy/releases/latest
> 2. Unzip, drag to /Applications, run `xattr -cr /Applications/Clawsy.app`, launch.
> 3. Click "Add Host" and paste this setup code:
>
> ```
> CLAWSY-SETUP
> host: <your gateway hostname or IP>
> token: <your gateway auth token>
> ```

Replace the placeholders with actual values before sending (see "How to find
the values" above). The user should not have to come back and ask for more info.

---

## setupState — Targeted Onboarding

When a Clawsy node connects, the `hello` payload includes `setupState`:

```json
{
  "setupState": {
    "sharedFolderConfigured": true,
    "sharedFolderPath": "~/Documents/Clawsy",
    "finderSyncEnabled": false,
    "accessibilityGranted": false,
    "screenRecordingGranted": true,
    "firstLaunch": false
  }
}
```

Read it from `clawsy-service` session history. If any permissions are missing,
tell the user **specifically** what to enable — don't send a generic list.

---

## Command Reference

### Screen & Camera

| Command | Approval | Description |
|---------|----------|-------------|
| `screen.capture` | User approval | Capture the full screen or selected area. Returns `{format, base64}` |
| `camera.snap` | User approval | Take a photo from the Mac camera. Params: `deviceId` (optional). Returns `{format, base64}` |
| `camera.list` | Auto | List available cameras. Returns `[{id, name}]` |

### Clipboard

| Command | Approval | Description |
|---------|----------|-------------|
| `clipboard.read` | User approval | Read current clipboard text |
| `clipboard.write` | Auto | Write text to clipboard. Params: `{text}` |

### Location

| Command | Approval | Description |
|---------|----------|-------------|
| `location.get` | Auto | Get device GPS location. Returns `{latitude, longitude, accuracy, locality, country, ...}`. 10s timeout. |

### File Operations

All file operations are **auto-approved** and sandboxed to the configured shared
folder (default `~/Documents/Clawsy`). Paths are relative to the shared folder root.

| Command | Params | Description |
|---------|--------|-------------|
| `file.list` | `subPath?`, `recursive?` | List files. `recursive: true` walks subdirectories (max depth 5) |
| `file.get` | `name` | Read file, returns base64 content |
| `file.set` | `name`, `content` (base64) | Write file |
| `file.stat` | `path` | File metadata: size, dates, type. Supports glob |
| `file.exists` | `path` | Returns `{exists, isDirectory}` |
| `file.mkdir` | `name` | Create directory (with intermediate parents) |
| `file.delete` | `name` | Delete file or directory |
| `file.rmdir` | `name` | Delete directory (alias for file.delete) |
| `file.move` | `source`, `destination` | Move/rename file. Supports glob in source |
| `file.copy` | `source`, `destination` | Copy file. Supports glob in source |
| `file.rename` | `path`, `newName` | Rename file (name only, same directory) |
| `file.checksum` | `path` | SHA256 hash of file |
| `file.batch` | `ops[]` | Execute multiple operations sequentially (see below) |
| `file.get.chunk` | `name`, `index`, `chunkSize?` | Read chunk of large file (default 350KB) |
| `file.set.chunk` | `name`, `chunk` (base64), `index`, `total` | Write chunk; assembles on final chunk |

### file.batch Operations

```python
nodes(action="invoke", invokeCommand="file.batch",
  invokeParamsJson='{"ops": [
    {"op": "mkdir", "name": "output"},
    {"op": "copy", "source": "template.txt", "destination": "output/report.txt"},
    {"op": "delete", "name": "temp.log"}
  ]}')
```

Supported `op` values: `copy`, `move`, `delete`, `mkdir`, `rename`.
Returns per-operation results with `ok` status for each.

### Large File Transfers (> 200 KB)

The gateway has a ~512 KB payload limit. For large files, use chunked transfer:

**Upload (agent to Mac):**
```python
# Split file into ~150KB base64 chunks
for i, chunk in enumerate(chunks):
    nodes(action="invoke", invokeCommand="file.set.chunk",
      invokeParamsJson=f'{{"name":"large.pdf","chunk":"{chunk}","index":{i},"total":{len(chunks)}}}')
```

**Download (Mac to agent):**
```python
stat = nodes(action="invoke", invokeCommand="file.stat",
  invokeParamsJson='{"path":"large.pdf"}')
# Calculate chunk count from stat.size, then:
for i in range(chunk_count):
    chunk = nodes(action="invoke", invokeCommand="file.get.chunk",
      invokeParamsJson=f'{{"name":"large.pdf","index":{i}}}')
```

---

## Invoking Commands

Use the `nodes` tool. Clawsy registers as a node with `platform="macos"`.

```python
# Screenshot
nodes(action="invoke", invokeCommand="screen.capture")

# Clipboard
nodes(action="invoke", invokeCommand="clipboard.read")
nodes(action="invoke", invokeCommand="clipboard.write",
  invokeParamsJson='{"text": "Hello from agent"}')

# Camera
nodes(action="invoke", invokeCommand="camera.snap")
nodes(action="invoke", invokeCommand="camera.list")

# Files
nodes(action="invoke", invokeCommand="file.list")
nodes(action="invoke", invokeCommand="file.list",
  invokeParamsJson='{"subPath": "docs/", "recursive": true}')
nodes(action="invoke", invokeCommand="file.get",
  invokeParamsJson='{"name": "report.pdf"}')
nodes(action="invoke", invokeCommand="file.set",
  invokeParamsJson='{"name": "output.txt", "content": "<base64>"}')

# Location
nodes(action="invoke", invokeCommand="location.get")
```

---

## Mission Control (MANDATORY)

When Clawsy is connected, you **must** send status events so the user sees what
you're doing. This is not optional.

### agent.info — Identity (send on session start + every heartbeat)

```python
sessions_send(sessionKey="clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.info","payload":{"agentName":"YourName","model":"claude-opus-4-6","updatedAt":"2026-03-29T12:00:00Z"}}')
```

TTL is 45 minutes. Resend every heartbeat to stay visible.

### agent.status — Task Progress (send during active work)

```python
sessions_send(sessionKey="clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.status","payload":{"agentName":"YourName","title":"Building feature X","progress":0.5,"statusText":"Compiling sources..."}}')
```

- `progress`: `0.0` to `1.0`. At `1.0`, task disappears after 10 seconds.
- **Timeout errors are normal.** The event is still delivered. Do not retry.

### HEARTBEAT.md Snippet

Add this to your HEARTBEAT.md:

```markdown
## Clawsy (every heartbeat)
If clawsy-service session exists:
sessions_send(sessionKey="clawsy-service", timeoutSeconds=3,
  message='{"kind":"agent.info","payload":{"agentName":"<NAME>","model":"<MODEL>","updatedAt":"<ISO-UTC>"}}')
If actively working, also send agent.status with current task + progress.
```

---

## Incoming Data — clawsy-service Session

Push data from Clawsy arrives in the `clawsy-service` session, not in the main
chat.

```python
sessions_history(sessionKey="clawsy-service", limit=10)
```

### Envelope Types

| Type | Contains | Triggered by |
|------|----------|--------------|
| `quick_send` | `content` (text) + `telemetry` | User presses `Cmd+Shift+K` |
| `screenshot` | Image data | screen.capture result / user-initiated |
| `clipboard` | Text content | clipboard.read result |
| `camera` | Image data | camera.snap result |
| `file_rule` | File path + rule info | .clawsy rule trigger |

### Quick Send Telemetry

```json
{
  "clawsy_envelope": {
    "type": "quick_send",
    "content": "User's message",
    "telemetry": {
      "deviceName": "MacBook Pro",
      "batteryLevel": 0.75,
      "isCharging": true,
      "thermalState": 0,
      "activeApp": "Safari",
      "moodScore": 70,
      "isUnusualHour": false
    }
  }
}
```

Hints: `thermalState > 1` = overheating, `batteryLevel < 0.2` = low battery,
`moodScore < 40` = user may be stressed, `isUnusualHour` = late/early work.

---

## Shared Folder & .clawsy Rules

### .clawsy Manifest Files

Folders within the shared directory can contain a `.clawsy` manifest for
automation rules. Users configure these via Finder right-click menu.

```json
{
  "version": 1,
  "folderName": "Projects",
  "rules": [
    {
      "trigger": "file_added",
      "filter": "*.pdf",
      "action": "send_to_agent",
      "prompt": "Summarize this document"
    }
  ]
}
```

- **Triggers:** `file_added`, `file_changed`, `manual`
- **Filters:** Glob patterns (`*.pdf`, `*.mov`, `*`)
- **Actions:** `send_to_agent`, `notify`

Rule events arrive in `clawsy-service` as `file_rule` envelopes.

---

## Error Handling

| Situation | Action |
|-----------|--------|
| `sessions_send` times out | Normal. Event is delivered. Do not retry. |
| No node with `platform="macos"` | Clawsy not connected. Skip Clawsy actions silently. |
| `invoke` returns `denied` | User denied the request. Respect it. Do not re-ask. |
| `invoke` returns `sandbox_violation` | Path escapes shared folder. Fix the path. |
| `invoke` returns `timeout` | Command took >30s. Retry once if appropriate. |
| Node disconnects mid-task | Mission Control clears automatically. No cleanup. |
| `AUTH_TOKEN_MISMATCH` | Clawsy auto-recovers. Wait for reconnection. |

---

## macOS Permissions

These are on the user's side. If a capability doesn't work, point them to the
specific setting — don't list everything.

| Permission | Required for | Where |
|------------|-------------|-------|
| Screen Recording | `screen.capture` | System Settings > Privacy > Screen Recording |
| Camera | `camera.snap` | System Settings > Privacy > Camera |
| Accessibility | Global hotkeys (`Cmd+Shift+K`) | System Settings > Privacy > Accessibility |
| Notifications | Desktop alerts | System Settings > Notifications > Clawsy |
| FinderSync Extension | Finder right-click menu | System Settings > Extensions > Finder |
| Share Extension | "Send to Agent" in Share menu | Automatic when app is in /Applications |

---

## Connection Architecture

```
Mac (Clawsy) ──── WSS ────> OpenClaw Gateway (port 18789)
                              SSH tunnel as fallback
```

- **Primary:** Direct WebSocket. Setup code contains gateway host + token.
- **SSH fallback:** User configures in Settings when direct WSS is unreachable.
- **Auth:** Server token > device token (Ed25519, persisted per host).
- **Multi-host:** Clawsy can connect to multiple gateways simultaneously. Each
  host has its own connection, shared folder, and color-coded label.

---

## When to Use What

| You want to... | Use |
|----------------|-----|
| See user's screen | `screen.capture` |
| Read what user copied | `clipboard.read` |
| Give user text to paste | `clipboard.write` |
| See what's in front of the user | `camera.snap` |
| Exchange files with user | `file.get` / `file.set` via shared folder |
| Transfer large files (>200KB) | `file.get.chunk` / `file.set.chunk` |
| Batch file operations | `file.batch` |
| Know where user is | `location.get` |
| Show user what you're working on | `agent.status` via Mission Control |
| Respond to user's quick message | Read `quick_send` from `clawsy-service` |
| React to file drops in shared folder | .clawsy rules (`file_added` trigger) |
