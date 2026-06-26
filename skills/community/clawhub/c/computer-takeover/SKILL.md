---
name: computer-takeover
description: "Full unattended remote control of paired devices (nodes) — screen capture, file management, shell commands, app control, camera, notifications, and process management. Use when: (1) remotely accessing or controlling a paired Windows/macOS/Android/iOS device without user interaction, (2) running commands installing apps or managing files on a remote node, (3) capturing screen or camera feeds from a remote device, (4) monitoring device health battery storage or network status, (5) automating actions on a remote device click type open app etc, (6) any form of remote desktop-style takeover or device ghosting."
---

# Computer Takeover

Unattended remote control of paired OpenClaw nodes. Controls the remote device as if physically sitting in front of it — no user presence required on the remote end.

## Core Capabilities

1. **Device Intelligence** — List nodes, get device info, health, permissions, battery, storage, network
2. **Screen Capture** — Snapshot or record the remote screen in real-time
3. **Camera Access** — Snap photos or record clips from front/back camera
4. **Shell Execution** — Run commands, scripts, and PowerShell/Bash on the remote device
5. **File Management** — Browse, read, write, delete files on the remote device via shell
6. **App Control** — Install, launch, close, list installed apps
7. **Process Management** — List running processes, kill processes, monitor CPU/memory
8. **Notifications** — Read notifications, trigger actions or replies
9. **Input Injection** — Type text, simulate clicks, keypresses (via shell automation)
10. **Location** — Get GPS coordinates (if device supports it)
11. **Device Pairing** — Initiate pairing or manage existing pairings

## Quick Start

Always start by listing available nodes to find the target device:

```
nodes(action="status")
```

Then describe the node to confirm it's the right one:

```
nodes(action="describe", node="<node-id>")
```

## Capability Details

### Device Intelligence

```json
nodes(action="status")           // List all paired nodes
nodes(action="device_info", node="<id>")
nodes(action="device_health", node="<id>")
nodes(action="device_permissions", node="<id>")
nodes(action="device_status", node="<id>")  // battery, storage, network
```

### Screen

```json
nodes(action="screen_record", node="<id>", outPath="C:/temp/screen.mp4", durationMs=30000)
nodes(action="photos_latest", node="<id>", limit=5)  // screenshots stored as photos
```

For live screen viewing, use the `canvas` tool with `target="node"` and the node's gateway URL.

### Camera

```json
nodes(action="camera_snap", node="<id>", facing="front|back")
nodes(action="camera_clip", node="<id>", facing="front|back", durationMs=10000)
```

### Shell Execution

Use `nodes(action="invoke", node="<id>", invokeCommand="<command>", invokeParamsJson="{}")`.

**Windows (PowerShell):**
```json
{
  "invokeCommand": "powershell",
  "invokeParamsJson": "{\"command\": \"Get-Process | Select -First 10 Name, CPU, WorkingSet\"}"
}
```

**Android (adb):**
```json
{
  "invokeCommand": "adb",
  "invokeParamsJson": "{\"command\": \"shell dumpsys battery\"}"
}
```

**Linux/macOS (SSH-style):**
```json
{
  "invokeCommand": "bash",
  "invokeParamsJson": "{\"command\": \"ls -la /tmp | head -20\"}"
}
```

### File Management (via Shell)

```powershell
# Windows: list directory
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"Get-ChildItem C:/Users/ -Depth 1 | Format-Table Name, Length, LastWriteTime\"}")

# Windows: read file
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"Get-Content C:/temp/log.txt -Tail 50\"}")

# Windows: write file
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"Set-Content -Path C:/temp/output.txt -Value 'Hello from remote'\"}")
```

### App Control

```json
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"Start-Process notepad\"}")  // launch
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"Get-Process | Where Name -eq 'notepad' | Stop-Process\"}")  // close
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"winget install Microsoft.PowerToys --silent\"}")  // install
```

### Process Management

```powershell
nodes(action="invoke", node="<id>", invokeCommand="powershell", invokeParamsJson="{\"command\": \"Get-Process | Sort CPU -Descending | Select -First 20 Name, Id, CPU, @{N='MEM_MB';E={[math]::Round($_.WorkingSet/1MB,1)}} | Format-Table -AutoSize\"}")
```

### Notifications

```json
nodes(action="notifications_list", node="<id>", limit=20)
nodes(action="notifications_action", node="<id>", notificationKey="<key>", notificationAction="open|reply|dismiss")
```

### Location

```json
nodes(action="location_get", node="<id>", desiredAccuracy="precise")
```

## Node Pairing

To pair a new device, use the `node-connect` skill and follow the pairing flow. Pairing requires the device to have the OpenClaw companion app installed and connected to the same gateway.

## Workflow: Full Takeover Session

1. `nodes(action="status")` — find the node ID
2. `nodes(action="device_info", node="<id>")` — confirm device name/type
3. `nodes(action="screen_record", node="<id>", ...)` or `canvas` tool — see what they're doing
4. Run commands as needed via `nodes(action="invoke", ...)`
5. Transfer files via base64 encoding through shell or direct path sharing

## Important Notes

- **Timeout**: Default `invokeTimeoutMs` is 30000ms. Increase for long-running commands.
- **Elevation**: Some operations (installing apps, killing system processes) may need elevated permissions on the remote device.
- **Safety**: Always confirm the target node before running destructive commands (delete files, kill processes, etc.).
- **Gateway URL**: For `canvas` tool with remote screen, the node must have `gateway.remote.url` configured and accessible.

## References

- Full `nodes` tool docs: see OpenClaw tool reference for all actions and parameters
- Node pairing guide: see `node-connect` skill for setup troubleshooting
- Gateway configuration: `gateway.remote.url` in OpenClaw config controls accessibility
