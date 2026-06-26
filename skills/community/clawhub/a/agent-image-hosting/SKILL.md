---
name: agentimghost
description: AgentImgHost REST API for uploading, listing, and deleting images. Returns direct public CDN URLs.
homepage: https://agent-img.com
metadata:
  {
    "openclaw":
      { "emoji": "🖼️", "requires": { "env": ["AGENTIMGHOST_API_KEY"] }, "primaryEnv": "AGENTIMGHOST_API_KEY" },
  }
---

# SKILL.md — AgentImgHost Image Upload Guide

This document teaches AI agents, bots, and scripts how to upload images to **AgentImgHost** and use the returned public URL.

---

## Overview

AgentImgHost provides a **REST API** for uploading images. After a successful upload, the service returns the **direct public URL** — no intermediate proxying. The image is immediately accessible worldwide via CDN.

---

## Authentication

All API requests require a **Bearer token** in the `Authorization` header.

```
Authorization: Bearer aih_your_token_here
```

You can find your token in the **Account** section of the web dashboard at `https://agent-img.com/account`.

---

## Upload an Image

```
POST https://agent-img.com/api/upload
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `file` | multipart/form-data | The image file to upload |

```bash
curl -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/path/to/image.png"
```

### Response (201 Created)

```json
{
  "url": "https://agent-img.com/a1b2c3def456/7f8e9a0b1c2d.png",
  "id": "7f8e9a0b1c2d",
  "filename": "screenshot.png",
  "size_bytes": 48291,
  "expires_at": null
}
```

| Field | Description |
|-------|-------------|
| `url` | **Direct public CDN URL** — use this in your responses/messages |
| `id` | Unique image ID (UUID hex) |
| `filename` | Original filename |
| `size_bytes` | File size in bytes |
| `expires_at` | ISO 8601 expiry date, or `null` if no expiry |

---

## Delete an Image

```bash
curl -X DELETE https://agent-img.com/api/images/{image_id} \
  -H "Authorization: Bearer aih_your_token_here"
```

**Response:**
```json
{ "deleted": "7f8e9a0b1c2d" }
```

---

## Resizing Images Before Upload

If your image exceeds the file-size limit for your plan (Free: 1 MB, Pro: 2 MB, Business: 5 MB), resize it before uploading.

1. **Get the image** — use an existing file, or generate/download one.
2. **Check the file size** — it must be under your plan's limit.
3. **If too large, resize it** using the commands below.
4. **Upload** the resized image.

### macOS (built-in `sips`)

```bash
# Scale the longest edge to 1600px (preserves aspect ratio)
sips -Z 1600 /path/to/image.png

# Upload
curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/path/to/image.png"
```

### Linux (ImageMagick `convert` / `magick`)

```bash
# Scale the longest edge to 1600px (preserves aspect ratio)
convert /path/to/image.png -resize 1600x1600 /path/to/image.png
# or with ImageMagick 7+
magick /path/to/image.png -resize 1600x1600 /path/to/image.png

# Upload
curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/path/to/image.png"
```

### Reducing quality (JPEG)

If resizing dimensions alone isn't enough, reduce JPEG quality:

```bash
# macOS — lower quality to 80%
sips -s formatOptions 80 /path/to/image.jpg

# Linux (ImageMagick)
convert /path/to/image.jpg -quality 80 /path/to/image.jpg
```

### Converting PNG → JPEG for smaller size

PNG files are often much larger than JPEG. Convert when transparency isn't needed:

```bash
# macOS
sips -s format jpeg /path/to/image.png --out /path/to/image.jpg

# Linux (ImageMagick)
convert /path/to/image.png -quality 85 /path/to/image.jpg
```

### One-liner: resize + upload

```bash
# macOS — resize to 1600px max, then upload in one line
sips -Z 1600 /tmp/shot.png && curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/tmp/shot.png"

# Linux — same with ImageMagick
convert /tmp/shot.png -resize 1600x1600 /tmp/shot.png && curl -s -X POST https://agent-img.com/api/upload \
  -H "Authorization: Bearer aih_your_token_here" \
  -F "file=@/tmp/shot.png"
```

> **Tip:** Start with 1600px max dimension. If still over the limit, try 1200px or 800px, or reduce JPEG quality to 70–80%.

---

## Error Codes

| Status | Meaning |
|--------|---------|
| `401` | Invalid or missing API token |
| `413` | File too large for your plan |
| `415` | Unsupported file type (must be an image) |
| `429` | Image limit reached and circular overwrite is disabled |
| `500` | Server error — try again |

---

## Supported Image Formats

`JPEG`, `PNG`, `GIF`, `WebP`, `AVIF`, `SVG`, `BMP`, `TIFF`

---

## Plan Limits

| Plan | Max Images | Max File Size | Price |
|------|-----------|---------------|-------|
| Free | 100 | 1 MB | Free |
| Pro | 1,000 | 2 MB | $1/month |
| Business | 10,000 | 5 MB | $5/month |
| Custom | Unlimited | Custom | Contact us |

Manage your plan at `https://agent-img.com/account`.

---

## Circular Overwrite

By default, when you reach your image limit, the **oldest image is automatically deleted** to make room for the new upload. You can disable this in **Settings** (`https://agent-img.com/config`) to get a `429` error instead.

---

## URL Structure

All image URLs follow this pattern:

```
https://agent-img.com/{user_folder}/{image_uuid}.{ext}
```

- `user_folder` — your unique folder (UUID hex, assigned at registration)
- `image_uuid` — UUID hex assigned to each upload
- `ext` — file extension based on content type

URLs are **permanent** while your plan is active. After plan cancellation, images are retained for the grace period defined by your plan before being deleted.
