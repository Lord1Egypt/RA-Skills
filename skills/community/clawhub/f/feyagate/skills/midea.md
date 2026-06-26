---
name: midea
description: Midea platform tools. Account/password auth, read/write device properties (AC, appliances).
version: 1.2.31
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Midea Platform Tools

> **Parent skill:** [SKILL.md](../SKILL.md) — provides cross-platform tools (`device/list`, `device/specs`, `platform/status`) and MCP endpoint config.

## Authorization

### Account Login

Midea uses account/password login via the Meiju (美居) app credentials.

**Login:**

```json
{
  "name": "auth/midea_login",
  "arguments": {
    "account": "YOUR_PHONE_OR_EMAIL",
    "password": "YOUR_PASSWORD",
    "cloud": "meiju"
  }
}
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `account` | Yes | Meiju app phone number or email |
| `password` | Yes | Meiju app password |
| `cloud` | No | Cloud type: `meiju` (美居, default) or `msmart` (MSmartHome) |

Returns on success:
```json
{
  "success": true,
  "auth_status": {
    "authenticated": true,
    "cloud": "meiju",
    "home_group_id": "18503420",
    "token_remaining_seconds": 7200
  },
  "device_count": 0
}
```

Token is valid for 7200 seconds (2 hours). Re-login when expired.

**Refresh device list after login:**

```json
{
  "name": "midea/refresh",
  "arguments": {}
}
```

### Other Auth Tools

| Tool | Description |
|------|-------------|
| `midea/refresh` | Refresh device list from cloud |
| `auth/midea_logout` | Clear Midea authorization |

### Check Authorization Status

```json
{
  "name": "auth/platforms",
  "arguments": {}
}
```

Look for the `midea` entry to verify `authenticated: true`.

## Device Control

| Tool | Arguments | Returns |
|------|-----------|---------|
| `midea/get_properties` | `device_id` | Property values |
| `midea/set_property` | `device_id`, `property`, `value` | Set result (**requires license**) |
| `midea/execute_action` | `device_id`, `action` | Action result (**requires license**) |

**Parameter convention:** Midea tools use `device_id` (snake_case).
Cross-platform tool `device/specs` uses `deviceId` (camelCase).

**Common properties:**
- `power`: `0` / `1` (off/on)
- `temperature`: number (e.g., `26`)
- `mode`: string (`cool`, `heat`, `auto`)
- `fan_speed`: string (`low`, `medium`, `high`)

**Workflow (steps 3-4 use parent skill tools):**
1. `auth/midea_login` → login with account/password
2. `midea/refresh` → refresh device list from cloud
3. `device/list` with `{"filter": [], "platform": "midea"}` → list devices
4. `device/specs` with `{"deviceId": "xxx"}` → get property/action definitions
5. `midea/set_property` → control (e.g., `property: "power"`, `value: 1`)

### Device Control Example

```json
{
  "name": "midea/set_property",
  "arguments": {
    "device_id": "DEVICE_ID",
    "property": "power",
    "value": 1
  }
}
```

## License

`midea/set_property` and `midea/execute_action` require a license. `midea/get_properties` works without license.
Activate via `license/set` tool.
