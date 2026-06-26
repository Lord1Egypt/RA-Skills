---
name: clawpulse
description: Configure and maintain ClawPulse integration for OpenClaw, including token-protected status bridge, Tailscale-safe access, iOS endpoint/token defaults, and troubleshooting for ATS/auth/sync issues. Use when setting up a new machine, rotating tokens, fixing ClawPulse connectivity, or enabling assistant name + token usage + thought metadata in status responses.
---

# ClawPulse

## Overview
Set up a secure status bridge from OpenClaw to ClawPulse and keep it working with minimal manual steps.

## Dependencies
- Required: `openclaw`, `python3`
- Optional (remote access only): `tailscale`

## Quick Workflow
1. One-command bootstrap (recommended): `bash scripts/bootstrap_clawpulse.sh --apply`.
2. This runs bridge + monitor setup, then prints QR/token for app import.
3. Default bind is remote-ready (`0.0.0.0`) for mobile devices on Tailscale/LAN.
4. If sync fails, use the troubleshooting checklist.

## Step 1 — Bootstrap the bridge
Run:

```bash
# Dry-run: generate token/server file and print settings (no background process)
bash scripts/setup_clawpulse_bridge.sh

# Start service (remote-ready default + QR)
bash scripts/setup_clawpulse_bridge.sh --apply

# Optional local-only mode (hardened)
BIND_HOST=127.0.0.1 bash scripts/setup_clawpulse_bridge.sh --apply
```

Expected outputs:
- endpoint (local or Tailscale format)
- bearer token
- bind host/port and log path

## Step 2 — Validate response contract
The bridge response should include at least:

```json
{
  "online": true,
  "assistantName": "OpenClaw",
  "workStatus": "工作中",
  "tokenUsage": {"prompt": 1, "completion": 2, "total": 3},
  "thought": "..."
}
```

## Step 3 — Wire the app
Use in ClawPulse:
- URL: `http://<tailscale-or-lan-ip>:8787/health`
- Token: Bearer token from setup script
- Polling default: 5s (more responsive)

## Monitor mode (recommended)
Use monitor as the public endpoint, keep bridge as internal source.

```bash
# Start/restart monitor (reads bridge and applies anti-flap state machine)
bash scripts/setup_clawpulse_monitor.sh --apply
```

Then configure app with monitor endpoint/token (from script output or QR), not bridge token.

## Troubleshooting
- HTTP blocked on iOS: ensure app Info.plist has ATS exception for development, or use HTTPS.
- 401 auth error: token mismatch; regenerate and reapply.
- 403 forbidden: source IP is not local/Tailscale; confirm the device is connected to Tailscale.
- Timeout: check bridge process and network reachability.
- Wrong display name: update `workspace/IDENTITY.md` Name field.

## Token rotation
Re-run setup script with `ROTATE_TOKEN=1`:

```bash
ROTATE_TOKEN=1 bash scripts/setup_clawpulse_bridge.sh
```

Update token in ClawPulse immediately.
