---
name: api-device-live
description: "Closeli Device Live Query API. Used to obtain the Web live playback link for a specified device and supports real-time viewing of the device feed. Use when: You need to remotely view the device's live feed, or integrate live streaming capability into a webpage or third-party system. ⚠ Security requirement: You must set AI_GATEWAY_API_KEY in `~/.openclaw/.env` (written automatically by the \"Set API Key\" action in OpenClaw clients) and use least-privilege credentials."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      configPaths: ["~/.openclaw/.env"]
    primaryEnv: "AI_GATEWAY_API_KEY"
---

# Device Live Link API

`POST /api/device/live` is used to obtain the H5 player live link for a specified device. The API verifies device ownership and then returns a player URL that can be opened directly in a browser.

## ⚠️ Display Rules (MUST be strictly followed)

The script outputs structured data in JSON format, which is the expected behavior. The display rules below are formatting instructions for the agent: the agent MUST parse the JSON output from the script, convert it into a user-friendly format according to the following rules before displaying it, and MUST NOT display the raw JSON directly.

The script output includes the `_device_name` field (device name), which is used for display.

1. When `code == 0` and `data` contains `live_url`, MUST use Markdown link format:

📺 Live stream of "Living Room Camera":

[▶️ Click to open live player](https://example.com/h5player/pro/autoPlay_credentials.html?...)

Key rules:
- Get the device name from `_device_name` and display it as "device name" instead of the MAC address
- If `_device_name` is empty, use the MAC address with the `xxxxS_` prefix removed as a fallback
- `live_url` MUST be output using Markdown link syntax `[text](url)`, and MUST NOT be output as bare URL text
- Use `▶️ Click to open live player` as the link text

2. When `code != 0`, reply: "API call failed, error code {code}, reason: {message}"

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
- You MUST use a least-privilege API_KEY to avoid reusing high-privilege credentials. This skill only requires permission to retrieve device live links

## Network Access Declaration

This skill only accesses the following endpoints (all under AI_GATEWAY_HOST):

| Endpoint | Method | Purpose |
|------|------|------|
| /api/device/list | POST | Obtain device name mapping |
| /api/device/live | POST | Obtain device live link |

The script does not access any other network resources.

## Quick Start

```bash
python3 get_live_url.py --device-id "xxxxS_aabbccddeeff"
```

## Request Format

### Request Body

| Parameter Name | Type | Required | Description |
|--------|------|------|------|
| device_id | string | Yes | Device ID, format: `xxxxS_<mac>`, cannot be empty |

## Response Format

```json
{
  "code": 0,
  "message": "success",
  "request_id": "<32-character request trace ID>",
  "data": {
    "live_url": "https://example.com/h5player/pro/autoPlay_credentials.html?t=k7qp2vx9nb4ml8wr3ty6sa"
  },
  "_device_name": "Living Room Camera"
}
```

### data Field

| Parameter Name | Type | Description |
|--------|------|------|
| live_url | string | H5 player live link, which can be opened directly in a browser or WebView |

## Error Codes

| Error Code | HTTP Status Code | Description |
|--------|------------|------|
| 1001 | 401 | api_key not provided (missing Authorization header or incorrect format) |
| 1002 | 401 | api_key is invalid or disabled |
| 2001 | 400 | Missing required parameter (`device_id` is empty, or the device does not belong to the current user) |
| 3001 | 502 | Internal gateway service call failed |
| 5000 | 500 | Internal error |

## Notes

- `device_id` cannot be empty, otherwise error code 2001 is returned
- If the device does not belong to the current user, an error is returned directly
- **IMPORTANT**: `device_id` is case-sensitive. The prefix MUST be lowercase `xxxxS_`, NOT uppercase `XXXXS_`. The script will auto-correct the case, but the agent SHOULD always pass the correct lowercase format
- The returned `live_url` only contains a 22-character short-lived token (expires in 120 seconds by default). After the H5 player loads, it automatically calls `/api/player/exchange` to exchange it for the real playback credential. No sensitive information (`apiKey`, `productKey`, stream token, `deviceId`) is included in the URL
- Global request timeout is 120 seconds
