---
name: api-device-status
description: "Closeli Device Status Query API. Used to query the current status of specified devices and supports determining whether a device is online, offline, or sleeping. Use when: You need to confirm whether a device is currently available, or check device status before live streaming or event queries. ⚠ Security requirement: You must set AI_GATEWAY_API_KEY in `~/.openclaw/.env` (written automatically by the \"Set API Key\" action in OpenClaw clients) and use least-privilege credentials."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      configPaths: ["~/.openclaw/.env"]
    primaryEnv: "AI_GATEWAY_API_KEY"
---

# Device Status Query API

`POST /api/device/status` is used to batch query the online/offline status of devices.

## ⚠️ Display Rules (MUST be strictly followed)

The script outputs structured data in JSON format, which is the expected behavior. The display rules below are formatting instructions for the agent: the agent MUST parse the JSON output from the script, convert it into a user-friendly format according to the following rules before displaying it, and MUST NOT display the raw JSON directly.

The script output includes the `_device_names` field (device_id → device_name mapping), which is used to display device names.

1. When `code == 0` and `data` is not empty, display it as a table:

| Device Name | MAC Address | Status |
|----------|----------|------|
| Living Room Camera | aabbccddeeff | 🟢 Online |
| Front Door Camera | 112233445566 | 🔴 Offline |

Key rules:
- Look up the device name corresponding to `device_id` from `_device_names`; if not found, display "Unknown Device"
- `device_id` MUST be displayed as the MAC address after removing the `xxxxS_` prefix
- Status mapping: `"online"` → `🟢 Online`, `"offline"` → `🔴 Offline`

2. When `data` is an empty `{}`, reply: "None of the requested devices belong to the current user. No queryable devices are available."
3. When `code != 0`, reply: "API call failed, error code {code}, reason: {message}"

## Prerequisites

The script depends on httpx. If it is not installed, the script will prompt `python3 -m pip install httpx`.

## Configuration Declaration

This skill depends on the following configuration items. The agent and user MUST confirm that they are correctly configured before running.

### Required Configuration

| Configuration Item | Delivery Method | Description |
|--------|----------|------|
| AI_GATEWAY_API_KEY | `~/.openclaw/.env` (persistent, written by OpenClaw clients), command line `--api-key` (temporary override) | API key used for API authentication. CLI flag takes precedence over the file when both present |

### Optional Configuration

| Configuration Item | Delivery Method | Default Value | Description |
|--------|----------|--------|------|
| AI_GATEWAY_HOST | `~/.openclaw/.env` | `https://ai-open.icloseli.com` | Gateway address |
| AI_GATEWAY_VERIFY_SSL | `~/.openclaw/.env` | true | Set to false to disable TLS certificate verification (development environments only) |

### Configuration Source

The script reads `~/.openclaw/.env` as the single persistent configuration source. This file is shared by all skills and uses the format `KEY=VALUE` (one entry per line). OpenClaw clients write to this file when the user updates settings. The script does NOT read any `AI_GATEWAY_*` environment variables — env variables are intentionally ignored to avoid stale Gateway-process snapshots overriding the user's latest config.

## Security Notes

- The shared credential file `~/.openclaw/.env` is readable by all skills under the same user. Ensure file permissions are restricted (e.g. `chmod 600 ~/.openclaw/.env`) and that only the OpenClaw service user has access. The IM clients write to this file under that user's home directory.
- TLS certificate verification is enabled by default. You MUST NOT disable it in production environments (disabling it introduces man-in-the-middle attack risks, and attackers may intercept API_KEY and device data)
- Before use, you MUST confirm that AI_GATEWAY_HOST points to a trusted domain
- You MUST use a least-privilege API_KEY to avoid reusing high-privilege credentials. This skill only requires device status query permission

## Network Access Declaration

This skill only accesses the following endpoints (all under AI_GATEWAY_HOST):

| Endpoint | Method | Purpose |
|------|------|------|
| /api/device/list | POST | Obtain device name mapping |
| /api/device/status | POST | Query device online/offline status |

The script does not access any other network resources.

## Quick Start

```bash
python3 check_status.py --device-ids "xxxxS_aabbccddeeff"
```

Query multiple devices (comma-separated):

```bash
python3 check_status.py --device-ids "xxxxS_aabbccddeeff,xxxxS_112233445566"
```

## Request Format

### Request Body

| Parameter Name | Type | Required | Description |
|--------|------|------|------|
| device_ids | string[] | Yes | Device ID list, cannot be an empty array. Format: `xxxxS_<mac>` |

## Response Format

```json
{
  "code": 0,
  "message": "success",
  "request_id": "<32-character request trace ID>",
  "data": {
    "xxxxS_aabbccddeeff": { "status": "online" },
    "xxxxS_112233445566": { "status": "offline" }
  },
  "_device_names": {
    "xxxxS_aabbccddeeff": "Living Room Camera",
    "xxxxS_112233445566": "Front Door Camera"
  }
}
```

### data Field (Map Structure)

The key is `device_id`, and the value is the status object:

| Parameter Name | Type | Description |
|--------|------|------|
| status | string | Device status, value is `"online"` or `"offline"` |

## Error Codes

| Error Code | HTTP Status Code | Description |
|--------|------------|------|
| 1001 | 401 | api_key not provided |
| 1002 | 401 | api_key is invalid or disabled |
| 2001 | 400 | Missing required parameter (`device_ids` is an empty array) |
| 3001 | 502 | Internal gateway service call failed |
| 3002 | 502 | Internal gateway service call failed |
| 3004 | 502 | Internal gateway service call failed |
| 5000 | 500 | Internal error |

## Notes

- `device_ids` cannot be an empty array, otherwise error code 2001 is returned
- **IMPORTANT**: `device_id` is case-sensitive. The prefix MUST be lowercase `xxxxS_`, NOT uppercase `XXXXS_`. The script will auto-correct the case, but the agent SHOULD always pass the correct lowercase format
- Devices that do not belong to the current user are silently filtered and do not return an error
- Global request timeout is 120 seconds
