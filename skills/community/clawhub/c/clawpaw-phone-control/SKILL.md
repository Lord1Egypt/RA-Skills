---
name: clawpaw-setup
description: Guide users through ClawPaw Android setup — installing the APK, granting permissions, connecting SSH tunnel, and verifying the full LLM-to-phone control chain. Use when a user wants to set up ClawPaw, install the app, connect a new phone, or troubleshoot connection issues.
tools: Bash
disable-model-invocation: true
---

# ClawPaw Setup Guide

Walk the user through the complete setup step by step. Check each step before proceeding to the next. Use the scripts in the `scripts/` directory to automate checks.

## Step 1 — Check Prerequisites

Run the adb check script:

```bash
bash .claude/skills/clawpaw-setup/scripts/check-adb.sh
```

If `STATUS:NO_ADB`: guide user to install adb, then re-run.
If `STATUS:NO_DEVICE`: guide user to connect USB and enable USB Debugging.
If `STATUS:DEVICE_FOUND`: proceed to Step 2.

## Step 2 — Install APK

Ask the user if the ClawPaw app is already installed on the phone.

If not installed, build and install via adb:
```bash
# Build from source (requires Android Studio or Gradle)
cd android && ./gradlew assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Or guide the user to install manually from Android Studio (Run button).

After install, ask the user to:
1. Open the ClawPaw app
2. Tap **Connect**
3. Wait for **Backend connection** and **SSH tunnel** to show green dots

## Step 3 — Grant Permissions (USB connected)

Run the permissions script:

```bash
bash .claude/skills/clawpaw-setup/scripts/grant-permissions.sh
```

This grants 3 permissions:
- **WRITE_SETTINGS** — brightness control
- **WRITE_SECURE_SETTINGS** — auto-enable accessibility service
- **adb tcpip 5555** — enable wireless ADB over SSH tunnel

Then ask the user to check the phone for any permission dialogs and tap **Allow**.

## Step 4 — Verify SSH Tunnel

Ask the user to open the ClawPaw app and confirm both rows show a green dot:
- **Backend connection** (WebSocket)
- **SSH tunnel** (SSH reverse tunnel)

If SSH tunnel shows Disconnected or Error:
- Tap the **Retry** button next to the SSH tunnel status
- If still failing, restart the app

## Step 5 — Connect ADB (first time or after Pod restart)

Get the user's UID and Secret from the ClawPaw app main screen, then run:

```bash
bash .claude/skills/clawpaw-setup/scripts/reconnect-adb.sh <uid> <secret>
```

If output shows `failed to authenticate`:
- Tell user to look at the phone screen for an **"Allow USB debugging?"** dialog
- Tap **Always allow from this computer**, then **OK**
- Run the script again

If output shows `already connected` or `connected to`: proceed.

## Step 6 — End-to-End Verification

Run these curl commands with the user's credentials to confirm the full chain works:

```bash
# 1. Press home button
curl -sk -X POST https://www.clawpaw.me/api/adb/press_key \
  -H "Content-Type: application/json" \
  -H "x-clawpaw-secret: <SECRET>" \
  -d '{"uid":"<UID>","key":"home"}'
# Expected: {"success":true,"data":""}

# 2. Take screenshot
curl -sk -X POST https://www.clawpaw.me/api/adb/screenshot \
  -H "Content-Type: application/json" \
  -H "x-clawpaw-secret: <SECRET>" \
  -d '{"uid":"<UID>"}' | python3 -c "
import sys,json,base64
d=json.load(sys.stdin)
if d.get('success') and d.get('data',{}).get('data'):
    open('/tmp/phone_screen.png','wb').write(base64.b64decode(d['data']['data']))
    print('Screenshot saved to /tmp/phone_screen.png')
else:
    print('FAILED:', d)
"
```

Read `/tmp/phone_screen.png` and show it to the user to confirm.

## Step 7 — Configure MCP (optional)

To use ClawPaw tools directly in Claude Code (snapshot, tap, screenshot, etc.), add to `~/.claude.json`:

```json
"clawpaw": {
  "type": "stdio",
  "command": "node",
  "args": ["<path-to-repo>/mcp/dist/index.js"],
  "env": {
    "CLAWPAW_BACKEND_URL": "https://www.clawpaw.me",
    "CLAWPAW_UID": "<UID>",
    "CLAWPAW_SECRET": "<SECRET>"
  }
}
```

Then restart Claude Code.

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `device offline` | ADB TCP mode not set | Re-run Step 3 with USB connected |
| `INJECT_EVENTS permission denied` | USB debugging (Security settings) not enabled | Settings → Developer Options → USB debugging (Security settings) → ON |
| `WRITE_SETTINGS not granted` | Step 3 was skipped | Run `grant-permissions.sh` with USB connected |
| `SSH: Disconnected` | MIUI killed the service | Settings → Battery → ClawPaw → No restrictions; lock app in recents |
| `failed to authenticate` | New adb server, phone needs to approve | Check phone for Allow USB debugging dialog |
| Screenshot is black | Screen is off | Press power key first, or `adb shell input keyevent KEYCODE_WAKEUP` |
