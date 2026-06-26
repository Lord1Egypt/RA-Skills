---
name: tuya
description: Tuya/Smart Life platform tools. QR code auth, device DP property read/write.
version: 1.2.31
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Tuya Platform Tools

> **Parent skill:** [SKILL.md](../SKILL.md) — provides cross-platform tools (`device/list`, `device/specs`, `platform/status`) and MCP endpoint config.

## Authorization

### QR Code Authorization Flow

Tuya uses QR code scanning for authorization via the Smart Life / Tuya app.

**Step 1: Get user code**

Open the Smart Life (涂鸦智能) or Tuya app on your phone:
- Go to **My (我的) → Settings (设置) → Account & Security (账号与安全)**
- Find your **User Code (用户代码)**, e.g. `AxNmcp2`

**Step 2: Generate QR code**

```json
{
  "name": "auth/tuya_qr",
  "arguments": { "user_code": "YOUR_USER_CODE" }
}
```

Returns:
```json
{
  "success": true,
  "qr_url": "tuyaSmart--qrLogin/?token=xxx",
  "token": "xxx",
  "expire_time": 300
}
```

**Step 3: Scan QR code**

Convert `qr_url` to a QR code image and scan it with the Smart Life / Tuya app.
Confirm the authorization on the app when prompted.

**Step 4: Check scan status**

Poll until authorized (within 5 minutes):
```json
{
  "name": "auth/tuya_qr_status",
  "arguments": {
    "token": "QR_TOKEN_FROM_STEP_2",
    "user_code": "YOUR_USER_CODE"
  }
}
```

Returns on success:
```json
{ "success": true, "status": "success" }
```

Other statuses: `"error"` (not scanned / expired), `"scanned"` (scanned but not confirmed).

**Step 5: Refresh device list**

```json
{
  "name": "tuya/refresh",
  "arguments": {}
}
```

### Other Auth Tools

| Tool | Description |
|------|-------------|
| `auth/tuya_logout` | Clear Tuya authorization |
| `auth/platforms` | Check auth status for all platforms |

### Check Authorization Status

```json
{
  "name": "auth/platforms",
  "arguments": {}
}
```

Look for the `tuya` entry to verify `authenticated: true`.

## Device Control

| Tool | Arguments | Returns |
|------|-----------|---------|
| `tuya/get_properties` | `device_id`, `codes` (opt) | DP property values |
| `tuya/set_property` | `device_id`, `code`, `value` | Set result (**requires license**) |
| `tuya/refresh` | — | Refresh device list from cloud |

**Parameter convention:** Tuya tools use `device_id` (snake_case).
Cross-platform tool `device/specs` uses `deviceId` (camelCase).

**Workflow (steps 2-3 use parent skill tools):**
1. `auth/tuya_qr` → authorize (first time only)
2. `device/list` with `{"filter": [], "platform": "tuya"}` → list devices
3. `device/specs` with `{"deviceId": "xxx"}` → get DP definitions (codes)
4. `tuya/set_property` → control (e.g., `code: "switch_1"`, `value: true`)

### Device Control Example

```json
{
  "name": "tuya/set_property",
  "arguments": {
    "device_id": "DEVICE_ID",
    "code": "switch_1",
    "value": true
  }
}
```

## License

`tuya/set_property` requires a license. `tuya/get_properties` works without license.
Activate via `license/set` tool.
