# CodeBox API Reference

## Overview

CodeBox (码盒) is a smart QR code generation platform at https://www.codebox.club

- 200+ style templates (brand, industry, holiday, art, business card)
- Dynamic QR codes with real-time scan tracking
- Analytics: device, browser, OS, location, time series
- Webhook support for scan and creation events

## Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/plugin/generate | Generate a QR code |
| POST | /api/v1/plugin/batch-generate | Batch generate (max 20) |
| GET | /api/v1/plugin/qrcodes | List QR codes (paginated) |
| DELETE | /api/v1/plugin/qrcodes/{id} | Soft delete a QR code |
| POST | /api/v1/plugin/qrcodes/{id}/clone | Clone a QR code |
| GET | /api/v1/plugin/qrcodes/{id}/scans | Export scan events |
| POST | /api/v1/plugin/analytics | Get scan analytics |
| POST | /api/v1/plugin/update | Update dynamic QR code |
| GET | /api/v1/plugin/catalog | Browse style templates |

## QR Code Modes

- **DYNAMIC**: Creates a short link redirect. Trackable, URL can be updated later. Costs 1 credit.
- **STATIC**: Encodes content directly. No tracking. Free.

## Template Categories

- Brand templates (e.g. tech-gradient, ocean-blue)
- Industry templates (e.g. restaurant, real-estate)
- Holiday/Festival templates (e.g. christmas, spring-festival)
- Art templates (e.g. watercolor, pixel-art)
- Business card templates

## Credit System

- Free tier: 5 QR code credits + 5 AI credits per month (auto-reset)
- Paid credits never expire
- Static QR codes and template browsing are always free
- Dynamic QR codes consume 1 credit each

## Response Format

All endpoints return JSON. Successful responses:
```json
{
  "success": true,
  "data": { ... }
}
```

Error responses:
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

## Common Error Codes

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| CREDIT_EXHAUSTED | 403 | No credits remaining |
| NOT_FOUND | 404 | QR code not found |
| UNAUTHORIZED | 401 | Invalid or missing API key |
| RATE_LIMITED | 429 | Too many requests |

## Full Documentation

- API Docs: https://www.codebox.club/docs/api
- Authentication: https://www.codebox.club/docs/authentication
- SDK (TypeScript): https://www.codebox.club/docs/sdk
- MCP Server: https://www.codebox.club/docs/mcp
- Webhooks: https://www.codebox.club/docs/webhooks
