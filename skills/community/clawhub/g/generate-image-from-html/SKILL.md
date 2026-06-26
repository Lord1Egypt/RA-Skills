---
name: generate-image
description: "Generate a PNG image from HTML content or a public URL using headless Chromium. Supports custom dimensions, retina quality, full-page screenshots, cookie consent handling, and dynamic parameters."
---

# Generate Image

## What It Does
Renders a webpage or HTML content to a PNG image using headless Chromium. Supports URL screenshots and HTML-to-image rendering with full customization.

## When to Use
- Take a screenshot of a live webpage
- Render HTML/CSS to a PNG image (social cards, banners, certificates)
- Generate full-page scrollable screenshots
- Create retina-quality images with custom dimensions

## Required Inputs
You must provide **one** of:
- `html_content` — raw HTML string to render
- `url` — a public URL to screenshot

## Authentication
Send your API key in the `CLIENT-API-KEY` header.

Get your **free API key** at [https://pdfapihub.com](https://pdfapihub.com). Full API documentation is available at [https://pdfapihub.com/docs](https://pdfapihub.com/docs).

## Use Cases
- **Social Media Cards** — Generate OG images, Twitter cards, or Instagram story images from HTML templates
- **Email Banners** — Create personalized email header images with dynamic content
- **Website Screenshots** — Capture full-page or viewport screenshots of live websites for monitoring or previews
- **Certificate Images** — Render certificates as PNG images for sharing on social media
- **Product Mockups** — Generate product images with dynamic text overlays
- **Thumbnail Generation** — Create consistent thumbnail images for blog posts or video previews
- **QR Code Cards** — Render HTML with embedded QR codes as shareable images

## Key Options
| Parameter | Description |
|-----------|-------------|
| `output_format` | `url` (default), `base64`, `both`, `image`/`png`/`binary`/`file` |
| `width` / `height` | Output image dimensions in pixels |
| `deviceScaleFactor` | 1 (default), 2 for retina quality |
| `full_page` | `true` for full scrollable screenshot (URL mode) |
| `wait_until` | `load`, `domcontentloaded`, `networkidle`, `commit` |
| `cookie_accept_text` | Auto-click cookie consent before screenshot |
| `font` | Google Font names, pipe-separated |
| `dynamic_params` | Key-value object for `{{placeholder}}` replacement |

## Rate Limits
| Tier | Requests/min |
|------|-------------|
| Free/Basic/Pro | 10 |
| Enterprise | 30 |
| Business | 100 |

## Example Usage
```bash
curl -X POST https://pdfapihub.com/api/v1/generateImage \
  -H "CLIENT-API-KEY: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{
    "html_content": "<div style=\"padding:40px;background:#4F46E5;color:white;\"><h1>Hello {{name}}</h1></div>",
    "dynamic_params": { "name": "World" },
    "width": 800,
    "height": 400,
    "output_format": "url"
  }'
```

## Notes
- Files are automatically deleted after 30 days
- Maximum output file size depends on your plan tier
