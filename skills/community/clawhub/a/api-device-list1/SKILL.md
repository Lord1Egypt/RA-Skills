---
name: api-device-list
description: "Closeli Device List Query API. Used to retrieve the device list under the current account and return basic information such as device name, MAC, and IMEI. Use when: You need to see which devices are under the account, or obtain device identifiers before calling other device APIs. ⚠ Security requirement: You must set AI_GATEWAY_API_KEY in `~/.openclaw/.env` (written automatically by the \"Set API Key\" action in OpenClaw clients) and use least-privilege credentials."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      configPaths: ["~/.openclaw/.env"]
    primaryEnv: "AI_GATEWAY_API_KEY"
---

# Device List Query API

`POST /api/device/list` is used to query all devices bound to the currently authenticated user. This API does not require a request body. The device list is automatically associated through the api_key.

## ⚠️ Display Rules (MUST Be Strictly Followed)

The script outputs structured data in JSON format, which is the expected behavior. The following display rules are formatting instructions for the agent: the agent MUST parse the JSON output from the script and convert it into a user-friendly format according to the rules below before displaying it, and MUST NOT display the raw JSON directly.

1. When `code == 0` and `data` is not empty, display it as a table:

| MAC Address | Device Name |
|----------|----------|
| aabbccddeeff | Living Room Camera |

Key rule: `device_id` MUST remove the `xxxxS_` prefix before being displayed as the MAC address. The table header MUST be written as "MAC Address" and MUST NOT be written as "Device ID".

2. When `data` is an empty array, reply: "There are no devices bound under the current account."
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
- TLS certificate verification is enabled by default and MUST NOT be disabled in production environments (disabling it introduces man-in-the-middle attack risks, allowing attackers to intercept the API_KEY and device data)
- Before use, you MUST confirm that AI_GATEWAY_HOST points to a trusted domain
- You MUST use a least-privilege API_KEY and avoid reusing high-privilege credentials. This skill only requires device list query permission

## Network Access Declaration

This skill only accesses the following endpoints (all are paths under AI_GATEWAY_HOST):

| Endpoint | Method | Purpose |
|------|------|------|
| /api/device/list | POST | Query the list of devices bound to the user |

The script does not access any other network resources.

## Quick Start

```bash
python3 list_devices.py
```

## Authentication Method

Bearer Token authentication is used. The script automatically carries `Authorization: Bearer <api_key>` in the request header.

## Request Format

### Request Headers

| Parameter Name | Type | Required | Description |
|--------|------|------|------|
| Content-Type | string | Yes | `application/json` |
| Authorization | string | Yes | `Bearer <api_key>`, a 32-character hexadecimal string |

### Request Body

No request body is required.

## Response Format

```json
{
  "code": 0,
  "message": "success",
  "request_id": "<32-character request trace ID>",
  "data": [
    {
      "device_id": "xxxxS_aabbccddeeff",
      "device_name": "Living Room Camera"
    }
  ]
}
```

### `data` Field (Device Array)

| Parameter Name | Type | Description |
|--------|------|------|
| device_id | string | Device ID, format: `xxxxS_<mac_address>`. All subsequent device APIs use this format |
| device_name | string | Device name, a user-defined device alias |

## Error Codes

| Error Code | HTTP Status Code | Description |
|--------|------------|------|
| 1001 | 401 | api_key not provided (missing Authorization header or incorrect format) |
| 1002 | 401 | api_key is invalid or disabled |
| 3001 | 502 | Internal gateway service call failed |
| 3004 | 502 | Internal gateway service call failed |
| 5000 | 500 | Internal error |

## Notes

- The `device_id` format is `xxxxS_<mac>`, which is the identifier used by all subsequent device-related APIs
- **IMPORTANT**: `device_id` is case-sensitive. The prefix MUST be lowercase `xxxxS_`, NOT uppercase `XXXXS_`. The script will auto-correct the case, but the agent SHOULD always pass the correct lowercase format
- The global request timeout is 120 seconds
