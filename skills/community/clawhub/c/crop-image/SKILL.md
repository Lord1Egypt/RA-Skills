---
name: crop-image
description: >
  Use this skill when an AI agent needs to crop images through the deployed Crop
  Image service. Trigger this for URL-based cropping (`POST /crop`) and
  file-upload cropping (`POST /crop/upload`), especially when returning
  production URLs and handling API-level errors.
version: "0.1.0"
tags:
  - image-processing
  - crop
  - fastapi
  - api
license: MIT
compatibility:
  claude_code: ">=1.0.0"
  claude_desktop: ">=1.0.0"
metadata:
  version: "0.1.0"
  homepage: "https://imageclaw.net"
  docs: "https://api.imageclaw.net/docs"
  api_base_url: "https://api.imageclaw.net"
  maintainer: "imageclaw"
---

# Crop Image Skill

## Service Endpoints

- API Base URL: `https://api.imageclaw.net`
- Health: `https://api.imageclaw.net/health`
- Crop by URL: `https://api.imageclaw.net/crop`
- Crop by Upload: `https://api.imageclaw.net/crop/upload`
- Docs: `https://api.imageclaw.net/docs`

## Execute Crop by URL

1. Validate input fields:
- `url` must be a reachable image URL.
- `width` and `height` must be integers in `[1, 4096]`.

2. Call endpoint:

```bash
curl -sS -X POST "https://api.imageclaw.net/crop" \
  -H "content-type: application/json" \
  -d '{
    "url": "https://picsum.photos/800/600",
    "width": 256,
    "height": 256
  }'
```

3. Return response fields:
- `cropped_url`
- `original_size`
- `face_detected`

## Execute Crop by Upload

1. Prefer upload mode for user-provided local files.

2. Call endpoint:

```bash
curl -sS -X POST "https://api.imageclaw.net/crop/upload" \
  -F "file=@/absolute/path/to/photo.jpg" \
  -F "width=256" \
  -F "height=256"
```

3. Return response fields:
- `cropped_url`
- `original_size`
- `face_detected`

## Error Handling

- HTTP `400`: invalid image source or decode failure
- HTTP `422`: validation failure (invalid URL, invalid width/height)
- HTTP `500`: service or configuration failure

When failure occurs:
1. Return the original status code and `detail`.
2. Ask caller to change input for `400/422`.
3. Retry only for transient `500` or network timeout.

## Success Example

```json
{
  "cropped_url": "https://crop.imagebee.net/crops/1772761350_b8050bd6ec26.jpg",
  "original_size": [800, 600],
  "face_detected": false
}
```

## Failure Example

```json
{
  "detail": "Not an image: content-type is application/json"
}
```
