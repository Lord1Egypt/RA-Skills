---
name: gateway-control-ui
description: Step-by-step guide to log into the OpenClaw Control UI, enter gateway token, approve device pairing, and verify connection
metadata:
  openclaw:
    emoji: 🔧
    requires:
      bins: ["openclaw", "cat"]
---

# Gateway Control UI Login & Pairing

Use when a user needs to access the OpenClaw Gateway Control UI, authenticate, pair a device, and confirm connectivity.

## Prerequisites
- OpenClaw gateway running (`openclaw status`)
- Control UI URL configured in `gateway.controlUi.allowedOrigins`
- Gateway token available in config (`/data/.openclaw/openclaw.json`)
- Device pairing approval (CLI)

## Steps

### 1. Open Control UI
- URL: use your configured OpenClaw service URL (from `gateway.controlUi.allowedOrigins`)
- HTTP Basic Auth:
  - Username: use your `SERVICE_USER_OPENCLAW` value
  - Password: use your `SERVICE_PASSWORD_OPENCLAW` value
- Optional embedded form:
  - `https://<user>:<pass>@<your-openclaw-domain>/`

### 2. Get Gateway Token
```bash
cat /data/.openclaw/openclaw.json | grep -A 2 '"token"'
```
Token is under:
```json
"gateway": { "auth": { "token": "YOUR_TOKEN_HERE" } }
```

### 3. Enter Token in UI
- On Overview page, click **Gateway Token** field
- Paste token
- Click **Connect**

### 4. Approve Pairing (CLI)
```bash
openclaw devices list
openclaw devices approve <requestId>
```

### 5. Verify Success
- In Control UI: status shows green “OK” and dashboard loads
- CLI:
  ```bash
  openclaw status --deep
  ```
  Check `Gateway` → `reachable` and channels show `OK`.

## Troubleshooting
- Page stays on form? WebSocket URL may need to be filled (usually left blank for remote)
- Pairing fails? Run `openclaw devices list` again to see pending requests
- Token invalid? Check `/data/.openclaw/openclaw.json` for correct value
