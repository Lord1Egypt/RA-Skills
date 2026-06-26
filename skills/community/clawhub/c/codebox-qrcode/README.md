# codebox-qrcode

Generate, manage, and track QR codes with [CodeBox](https://www.codebox.club) — a smart QR code platform with 200+ style templates and real-time scan analytics.

## What it does

- **Generate QR codes** with customizable styles from 200+ templates
- **Track scans** with analytics: device, location, browser, time series
- **Batch generate** up to 20 QR codes in one call
- **Manage lifecycle**: update target URLs, rename, delete, clone
- **Browse templates**: search by keyword or category

## Setup

1. Sign up at [codebox.club](https://www.codebox.club)
2. Create an API key at [Dashboard > API Keys](https://www.codebox.club/zh/dashboard/apikeys)
3. Set the environment variable:

```bash
export CODEBOX_API_KEY=cb_sk_xxxxxxxxxxxxxxxx
```

## Example Usage

> Generate a QR code for my website https://example.com with a Christmas theme

> Show me scan stats for QR code abc123

> Create 5 QR codes for these URLs: url1, url2, url3, url4, url5

> Change the target of QR code abc123 to https://new-url.com

## Credits

- Dynamic QR codes: 1 credit each
- Static QR codes: free
- Free tier: 5 credits/month (auto-reset)
- Paid credits never expire

## Links

- Website: https://www.codebox.club
- API Docs: https://www.codebox.club/docs/api
- SDK: https://www.npmjs.com/package/@codebox.club/sdk
- MCP Server: https://www.codebox.club/docs/mcp
