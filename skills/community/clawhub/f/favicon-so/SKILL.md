---
name: favicon-so
description: favicon.so project API reference — covers the favicon fetch API and image-to-favicon-package convert API. Use when working on API routes, building integrations, debugging favicon fetch/convert behavior, or adding new endpoints to this project.
license: MIT
metadata:
  author: favicon.so
  version: 1.0.0
---

# favicon.so API

## API 1: Favicon Fetch

Fetch any website's favicon by domain.

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/favicon?url={domain}` | Fetch favicon with full options |
| GET | `/{domain}` | Short URL, returns favicon image directly |

### Parameters

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | yes | Domain or URL (e.g. `github.com`) |
| `raw` | string | no | Set to `"true"` for JSON metadata instead of image |

### Response Modes

**Image mode (default):**
Returns binary image data with headers:
- `Content-Type`: actual image MIME type
- `Cache-Control: public, max-age=604800`
- `Access-Control-Allow-Origin: *`

**JSON mode (`raw=true`):**
```json
{
  "url": "https://github.githubassets.com/favicons/favicon.svg",
  "format": "image/svg+xml",
  "isDefault": false
}
```

### Implementation

- Source: `app/api/favicon/route.ts` and `app/[locale]/[domain]/route.ts`
- Core logic: `lib/fetchFavicon.ts` — tries HTML parsing, `/favicon.ico`, Google, DuckDuckGo fallbacks
- Domain validation: `lib/utils.ts` — `normalizeDomain()`, `isValidDomain()`
- Falls back to a default SVG icon when all sources fail

## API 2: Image Convert

Convert any image into a complete favicon package with all sizes.

### Endpoint

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/convert` | Upload image, get favicon package |

### Request

**Content-Type:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `image` | File | yes | Image file (PNG, JPG, WebP, GIF, BMP, TIFF) |

Also accepts raw image bytes with `Content-Type: image/*` or `application/octet-stream`.

### Query Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `format` | string | — | Set to `"json"` for base64 JSON output instead of ZIP |

### Response

**ZIP mode (default):**
Returns `application/zip` containing 10 files:
- `favicon.ico` (multi-resolution: 16, 32, 48, 64, 128)
- `favicon-16x16.png`, `favicon-32x32.png`, `favicon-48x48.png`, `favicon-64x64.png`, `favicon-128x128.png`
- `apple-touch-icon.png` (180×180)
- `android-chrome-192x192.png`, `android-chrome-512x512.png`
- `site.webmanifest`

**JSON mode (`format=json`):**
```json
{
  "files": {
    "favicon-16x16.png": { "size": 1234, "base64": "iVBOR..." },
    "favicon.ico": { "size": 5678, "base64": "AAAB..." },
    ...
  }
}
```

### Implementation

- Source: `app/api/convert/route.ts`
- Image processing: `jimp` (pure JS, Cloudflare Workers compatible)
- ICO generation: custom multi-resolution ICO builder
- ZIP packaging: `jszip`
- CORS enabled, no auth required

## Architecture Notes

- All API routes are in `app/api/` and skip the i18n middleware
- The `[locale]/[domain]/route.ts` catch-all serves as a short URL for favicon fetch
- Reserved paths (`search`, `convert`, `api`, `generator`, `skill`, `mcp`) are excluded from the domain catch-all
- Client-side convert page (`app/[locale]/convert/page.tsx`) uses WASM (Photon + resvg) for browser-native processing
- Server-side convert API uses `jimp` for Node.js/Workers compatibility
