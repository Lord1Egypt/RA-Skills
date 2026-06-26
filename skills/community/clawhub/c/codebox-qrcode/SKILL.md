---
name: codebox-qrcode
description: Generate, manage, and track QR codes via CodeBox API. Create dynamic QR codes with 200+ style templates, track scans with analytics (device, location, time), batch generate up to 20 codes, and manage QR code lifecycle. Supports dynamic (trackable) and static modes.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - CODEBOX_API_KEY
      bins:
        - curl
    primaryEnv: CODEBOX_API_KEY
    emoji: "📱"
    homepage: https://www.codebox.club
---

# CodeBox QR Code Skill

Generate, manage, and track QR codes using the CodeBox API.

## Setup

The user needs a CodeBox API key. Get one at https://www.codebox.club/zh/dashboard/apikeys

Set the environment variable:
```
CODEBOX_API_KEY=cb_sk_xxxxxxxxxxxxxxxx
```

## API Base URL

All requests go to `https://www.codebox.club/api/v1/plugin`

## Authentication

Every request must include:
```
Authorization: Bearer $CODEBOX_API_KEY
```

## Available Actions

### 1. Generate QR Code

**POST** `https://www.codebox.club/api/v1/plugin/generate`

Use this to create a new QR code. Supports dynamic (trackable, updatable URL) and static modes.

```bash
curl -X POST https://www.codebox.club/api/v1/plugin/generate \
  -H "Authorization: Bearer $CODEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "https://example.com",
    "mode": "DYNAMIC",
    "name": "My QR Code",
    "templateId": "classic-black",
    "errorCorrectionLevel": "M"
  }'
```

**Parameters:**
- `content` (required): URL or text to encode
- `mode`: `DYNAMIC` (default, trackable) or `STATIC` (no tracking, free)
- `name`: Display name for the QR code
- `templateId`: Style template ID (use list_templates to browse)
- `keywords`: Array of keywords for automatic template matching (e.g. `["christmas", "holiday"]`)
- `errorCorrectionLevel`: `L`, `M` (default), `Q`, or `H`

**Response includes:** `id`, `shortUrl`, `qrCodeUrl` (PNG image), `targetUrl`

### 2. Batch Generate

**POST** `https://www.codebox.club/api/v1/plugin/batch-generate`

Generate up to 20 QR codes in a single request. Each item is processed independently (partial failure supported).

```bash
curl -X POST https://www.codebox.club/api/v1/plugin/batch-generate \
  -H "Authorization: Bearer $CODEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"content": "https://example.com/1", "name": "Link 1"},
      {"content": "https://example.com/2", "name": "Link 2", "templateId": "ocean-blue"}
    ]
  }'
```

### 3. List QR Codes

**GET** `https://www.codebox.club/api/v1/plugin/qrcodes`

```bash
curl "https://www.codebox.club/api/v1/plugin/qrcodes?page=1&size=10" \
  -H "Authorization: Bearer $CODEBOX_API_KEY"
```

**Query params:** `page`, `size` (max 50), `mode` (STATIC/DYNAMIC/AI), `keyword`

### 4. Get Scan Analytics

**POST** `https://www.codebox.club/api/v1/plugin/analytics`

```bash
curl -X POST https://www.codebox.club/api/v1/plugin/analytics \
  -H "Authorization: Bearer $CODEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "qrCodeId": "xxx",
    "startDate": "2026-01-01",
    "endDate": "2026-03-23"
  }'
```

Returns: total scans, unique scans, time series, device/browser/OS breakdown, location stats.

### 5. Update Dynamic QR Code

**POST** `https://www.codebox.club/api/v1/plugin/update`

Change the target URL, name, or status of a dynamic QR code.

```bash
curl -X POST https://www.codebox.club/api/v1/plugin/update \
  -H "Authorization: Bearer $CODEBOX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "xxx",
    "targetUrl": "https://new-destination.com",
    "name": "Updated Name"
  }'
```

**Parameters:** `id` (required), `targetUrl`, `name`, `status` (READY/EXPIRED/DELETED)

### 6. Delete QR Code

**DELETE** `https://www.codebox.club/api/v1/plugin/qrcodes/{id}`

```bash
curl -X DELETE "https://www.codebox.club/api/v1/plugin/qrcodes/xxx" \
  -H "Authorization: Bearer $CODEBOX_API_KEY"
```

### 7. Clone QR Code

**POST** `https://www.codebox.club/api/v1/plugin/qrcodes/{id}/clone`

```bash
curl -X POST "https://www.codebox.club/api/v1/plugin/qrcodes/xxx/clone" \
  -H "Authorization: Bearer $CODEBOX_API_KEY"
```

### 8. Export Scan Events

**GET** `https://www.codebox.club/api/v1/plugin/qrcodes/{id}/scans`

```bash
curl "https://www.codebox.club/api/v1/plugin/qrcodes/xxx/scans?page=1&size=20" \
  -H "Authorization: Bearer $CODEBOX_API_KEY"
```

**Query params:** `page`, `size` (max 100), `startDate`, `endDate`

### 9. Browse Templates

**GET** `https://www.codebox.club/api/v1/plugin/catalog`

```bash
curl "https://www.codebox.club/api/v1/plugin/catalog?keyword=christmas&limit=10" \
  -H "Authorization: Bearer $CODEBOX_API_KEY"
```

**Query params:** `category`, `keyword`, `limit` (default 20)

## Rules

- Always use `$CODEBOX_API_KEY` from environment, never ask the user for it inline.
- Default to `DYNAMIC` mode unless the user explicitly asks for static QR codes.
- When the user describes a style (e.g. "Christmas themed", "blue ocean"), use the `keywords` parameter in the generate call for automatic template matching, or call the catalog endpoint first to find a matching `templateId`.
- Dynamic QR codes consume 1 credit per generation. Static QR codes are free.
- When generating multiple QR codes, prefer batch-generate (max 20) over individual calls.
- The `qrCodeUrl` in the response is a direct link to the PNG image — you can share this URL directly.
- The `shortUrl` is the trackable redirect link to share with end users.

## Error Handling

- **403 with code `CREDIT_EXHAUSTED`**: User is out of credits. Tell them to recharge at https://www.codebox.club/zh/dashboard/pricing
- **401**: Invalid API key. Ask user to check their key at https://www.codebox.club/zh/dashboard/apikeys
- **400**: Bad request — check required parameters.
