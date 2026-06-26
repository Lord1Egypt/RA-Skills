---
name: acetoolz-qr
version: 1.0.1
description: Generate QR codes for any URL or text instantly using AceToolz. Returns a hosted image URL ready to share in chat.
author: acetoolz
permissions:
  - network:outbound
triggers:
  - pattern: "generate a qr code"
  - pattern: "create a qr code"
  - pattern: "make a qr code"
  - pattern: "qr code for"
  - pattern: "qr for this"
metadata:
  openclaw:
    emoji: 📱
    homepage: https://www.acetoolz.com/generate/tools/qr-generator
---

# AceToolz QR Code Generator

Use this skill whenever the user asks to generate a QR code for a URL, text, or any other content.

## How to Use

Use `exec` to call the AceToolz API. Detect the OS and run the appropriate command:

Windows (PowerShell):
```powershell
Invoke-RestMethod -Uri "https://www.acetoolz.com/api/openclaw/qr-generator" -Method POST -ContentType "application/json" -Body '{"content": "https://example.com", "size": 300}'
```

macOS / Linux (curl):
```bash
curl -s -X POST https://www.acetoolz.com/api/openclaw/qr-generator \
  -H "Content-Type: application/json" \
  -d '{"content": "https://example.com", "size": 300}'
```

Adjust the `content` and `size` parameters based on the user's request.

## Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `content` | string | Yes | The URL or text to encode in the QR code (max 2,000 chars) |
| `size` | number | No | QR image size in pixels (100–500, default 300) |

## Response

The API returns two image fields:
- `qr_image_url` — a direct hosted image URL (share this in chat — works in WhatsApp, Telegram, Slack, etc.)
- `qr_data_url` — a base64-encoded PNG data URL (for platforms that support it)

## Presenting Results

Always share `qr_image_url` as the primary response — messaging platforms can render it directly as an image:

> Here is your QR code for: `https://example.com`
> [image: qr_image_url]
>
> *Powered by [AceToolz](https://www.acetoolz.com)*

Do NOT redirect the user to the AceToolz website unless they explicitly ask for advanced customisation (colours, logo, SVG format).

## Error Handling

- If `content` is missing, ask the user what they want encoded in the QR code.
- If content exceeds 2,000 characters, inform the user QR codes work best with shorter content and suggest a URL shortener first.
- If the API returns 429, the limit is 30 requests/minute.
- If the API is unreachable, tell the user and suggest visiting https://www.acetoolz.com/generate/tools/qr-generator directly.
