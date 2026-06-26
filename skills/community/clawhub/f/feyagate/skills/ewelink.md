---
name: ewelink
description: eWeLink platform tools. Account/password auth, read/write device properties for Sonoff and eWeLink devices.
version: 1.2.31
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# eWeLink Platform Tools

> **Parent skill:** [SKILL.md](../SKILL.md) — provides cross-platform tools (`device/list`, `device/specs`, `platform/status`) and MCP endpoint config.

## Authorization

### Account Login

eWeLink uses email/phone and password login.

**Login:**

```json
{
  "name": "auth/ewelink_login",
  "arguments": {
    "email": "YOUR_EMAIL_OR_PHONE",
    "password": "YOUR_PASSWORD",
    "country_code": "+86"
  }
}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `email` | Yes | eWeLink account email or phone number |
| `password` | Yes | eWeLink account password |
| `country_code` | No | Country code (e.g., `+86` for China, `+1` for US) |

Returns on success:
```json
{
  "success": true,
  "auth_status": {
    "authenticated": true,
    "region": "cn",
    "token_remaining_seconds": 2592000,
    "ws_connected": true,
    "ws_handshaked": true
  },
  "device_count": 1
}
```

Token is valid for 2592000 seconds (30 days). WebSocket connection is established automatically for real-time updates. Re-login when expired.

**Refresh device list after login:**

```json
{
  "name": "ewelink/refresh",
  "arguments": {}
}
```

### Other Auth Tools

| Tool | Description |
|------|-------------|
| `ewelink/refresh` | Refresh device list from cloud |
| `auth/ewelink_logout` | Clear eWeLink authorization |

### Check Authorization Status

```json
{
  "name": "auth/platforms",
  "arguments": {}
}
```

Look for the `ewelink` entry to verify `authenticated: true`.

## Device Control

| Tool | Arguments | Returns |
|------|-----------|---------|
| `ewelink/get_properties` | `device_id` | Property values |
| `ewelink/set_property` | `device_id`, `property`, `value` | Set result (**requires license**) |
| `ewelink/execute_action` | `device_id`, `action` | Action result (**requires license**) |

**Parameter convention:** eWeLink tools use `device_id` (snake_case).
Cross-platform tool `device/specs` uses `deviceId` (camelCase).

**Property examples:**
- `switch`: `on` / `off` (single channel)
- `switches`: JSON array `[{"switch": "on", "outlet": 0}]` (multi-channel)

**Workflow (steps 3-4 use parent skill tools):**
1. `auth/ewelink_login` → login with email/phone and password
2. `ewelink/refresh` → refresh device list from cloud
3. `device/list` with `{"filter": [], "platform": "ewelink"}` → list devices
4. `device/specs` with `{"deviceId": "xxx"}` → get property definitions
5. `ewelink/set_property` → control (e.g., `property: "switch"`, `value: "on"`)

### Device Control Example

```json
{
  "name": "ewelink/set_property",
  "arguments": {
    "device_id": "DEVICE_ID",
    "property": "switch",
    "value": "on"
  }
}
```

## License

`ewelink/set_property` and `ewelink/execute_action` require a license. `ewelink/get_properties` works without license.
Activate via `license/set` tool.
