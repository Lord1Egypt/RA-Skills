# API Reference — Cutout.Pro Visual API

## Table of Contents

1. [Authentication](#authentication)
2. [Background Remover API](#background-remover-api)
3. [Face Cutout API](#face-cutout-api)
4. [Photo Enhancer API](#photo-enhancer-api)
5. [Common Parameters](#common-parameters)
6. [Response Format](#response-format)
7. [Error Codes](#error-codes)

---

## Authentication

All requests must include the `APIKEY` header:

```
APIKEY: your_api_key_here
```

Base URL: `https://www.cutout.pro`

Request format: All file upload endpoints use `multipart/form-data`; URL mode uses GET requests.

---

## Background Remover API

Automatically detects the foreground (people, animals, products, cartoons, etc.), separates it from the background, and returns a PNG with a transparent background.

### POST /api/v1/matting (Binary Response)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mattingType` | int (URL param) | Yes | Fixed value: `6` |
| `file` | file | Yes | Image file |
| `crop` | bool | No | Crop whitespace (default: false) |
| `bgcolor` | string | No | Background color, hex (e.g. `FFFFFF`) or `blur` |
| `preview` | bool | No | Preview mode, max 500×500, costs 0.25 credits (default: false) |
| `outputFormat` | string | No | Output format: `png`, `webp`, `jpg_<quality>` (default: png) |
| `cropMargin` | string | No | Crop margin, e.g. `30px` or `10%`, only applies when crop=true |

**Response**: PNG image binary, `Content-Type: image/png`

### POST /api/v1/matting2 (Base64 Response)

Same parameters as above, with additional support for:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `faceAnalysis` | bool | No | When true, returns facial landmark data |

**Response**:
```json
{
  "code": 0,
  "data": {
    "imageBase64": "iVBORw0KGgo..."
  },
  "msg": null,
  "time": 1590462453264
}
```

### GET /api/v1/mattingByUrl (Image URL Mode)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mattingType` | int | Yes | Fixed value: `6` |
| `url` | string | Yes | Source image URL |
| `crop` | bool | No | Crop whitespace |
| `bgcolor` | string | No | Background color |
| `preview` | bool | No | Preview mode |
| `outputFormat` | string | No | Output format |
| `cropMargin` | string | No | Crop margin |

---

## Face Cutout API

Precisely segments the face and hair region of people or pets (cats, dogs) in photos. Ideal for avatars, stickers, ID photos, and more.

### POST /api/v1/matting (Binary Response)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mattingType` | int (URL param) | Yes | Fixed value: `3` |
| `file` | file | Yes | Image file |
| `crop` | bool | No | Crop whitespace (default: false) |
| `bgcolor` | string | No | Background color, hex (e.g. `FFFFFF`) |
| `preview` | bool | No | Preview mode (default: false) |
| `outputFormat` | string | No | Output format (default: png) |

**Response**: PNG image binary, `Content-Type: image/png`

### POST /api/v1/matting2 (Base64 Response)

Same parameters as above, with additional support for:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `faceAnalysis` | bool | No | When true, returns 68 facial landmark points |

**Response (with facial landmarks)**:
```json
{
  "code": 0,
  "data": {
    "imageBase64": "iVBORw0KGgo...",
    "faceAnalysis": {
      "face_num": 1,
      "faces": [
        [236.46, 497.67, 1492.75, 2050.21, 236.46, 497.67, 1492.75, 2050.21]
      ],
      "point": [
        [
          [213.59, 1035.07],
          [221.80, 1219.90]
        ]
      ]
    }
  },
  "msg": null,
  "time": 1620798570850
}
```

> `faces` array coordinate order: p1(x,y), p3(x,y), p2(x,y), p4(x,y) (four corners of the face bounding box)
> `point` array returns 68 landmark coordinates in total

### GET /api/v1/mattingByUrl (Image URL Mode)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `mattingType` | int | Yes | Fixed value: `3` |
| `url` | string | Yes | Source image URL |
| `crop` | bool | No | Crop whitespace |
| `bgcolor` | string | No | Background color |
| `preview` | bool | No | Preview mode |
| `outputFormat` | string | No | Output format |

---

## Photo Enhancer API

AI super-resolution enhancement for out-of-focus, low-resolution, pixelated, or damaged photos — one click to HD.

### POST /api/v1/photoEnhance (Binary Response)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | file | Yes | Image file |
| `outputFormat` | string (URL param) | No | Output format: `png`, `webp`, `jpg_<quality>` (default: png) |
| `faceModel` | string (URL param) | No | Processing model: `anime` (cartoon) or `quality` (real photos, default) |

**Response**: HD PNG image binary, `Content-Type: image/png`

### POST /api/v1/photoEnhance2 (Base64 Response)

Same parameters as above.

**Response**:
```json
{
  "code": 0,
  "data": {
    "imageBase64": "iVBORw0KGgo..."
  },
  "msg": null,
  "time": 1590462453264
}
```

### GET /api/v1/photoEnhanceByUrl (Image URL Mode)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `url` | string | Yes | Source image URL |
| `outputFormat` | string | No | Output format (default: png) |
| `faceModel` | string | No | Processing model: `anime` or `quality` (default) |

---

## Common Parameters

### outputFormat

| Value | Description |
|-------|-------------|
| `png` | Lossless, supports transparency (default) |
| `webp` | Modern format, smaller file size |
| `jpg_<quality>` | JPEG compression, quality 0–100, e.g. `jpg_75` |

### bgcolor

| Value | Description |
|-------|-------------|
| Hex color code | e.g. `FFFFFF` (white), `000000` (black) |
| `blur` | Blurred background effect |
| Not provided | Transparent background (default) |

### faceModel (Photo Enhancer only)

| Value | Description |
|-------|-------------|
| `quality` | Best for real photos (default) |
| `anime` | Best for anime/cartoon images |

---

## Response Format

### Success (Binary Mode)
- `Content-Type: image/png` (or webp/jpeg)
- Body: raw image bytes

### Success (Base64 Mode)
```json
{
  "code": 0,
  "data": {
    "imageBase64": "base64_encoded_image_data"
  },
  "msg": null,
  "time": 1590462453264
}
```

### Error Response
```json
{
  "code": 1001,
  "data": null,
  "msg": "Insufficient balance",
  "time": 1590462453264
}
```

---

## Error Codes

| Code | Description | Action |
|------|-------------|--------|
| `0` | Success | — |
| `1001` | Insufficient account balance | Top up credits or use preview mode |
| `1002` | Invalid API Key | Check that the key is correct |
| `1003` | Unsupported image format | Use PNG/JPG/JPEG/BMP/WEBP |
| `1004` | Image resolution exceeds limit | Resize to 4096×4096 or smaller |
| `1005` | File size exceeds limit | Compress to 15 MB or smaller |
| `429` | Rate limit exceeded | Reduce concurrency; max 5 requests/second |

Full error code list: https://www.cutout.pro/apidoc/error-code

---

## Request Examples

### curl (Background Removal, File Upload)
```bash
curl -H 'APIKEY: your_api_key_here' \
  -F 'file=@/path/to/photo.jpg' \
  -f 'https://www.cutout.pro/api/v1/matting?mattingType=6&crop=true' \
  -o out.png
```

### curl (Face Cutout, URL Mode)
```bash
curl -X GET \
  --header 'APIKEY: your_api_key_here' \
  'https://www.cutout.pro/api/v1/mattingByUrl?url=https%3A%2F%2Fexample.com%2Fphoto.jpg&mattingType=3'
```

### curl (Photo Enhancement, File Upload)
```bash
curl -H 'APIKEY: your_api_key_here' \
  -F 'file=@/path/to/blurry.jpg' \
  -f 'https://www.cutout.pro/api/v1/photoEnhance?faceModel=quality' \
  -o hd.png
```

### Python (Background Removal)
```python
import requests

response = requests.post(
    'https://www.cutout.pro/api/v1/matting?mattingType=6',
    files={'file': open('/path/to/photo.jpg', 'rb')},
    headers={'APIKEY': 'your_api_key_here'},
)
with open('out.png', 'wb') as f:
    f.write(response.content)
```

### Python (Face Cutout + Landmarks)
```python
import requests

response = requests.post(
    'https://www.cutout.pro/api/v1/matting2?mattingType=3&faceAnalysis=true',
    files={'file': open('/path/to/portrait.jpg', 'rb')},
    headers={'APIKEY': 'your_api_key_here'},
)
data = response.json()
image_base64 = data['data']['imageBase64']
face_points = data['data']['faceAnalysis']['point']  # 68 landmark points
```

### Python (Photo Enhancement)
```python
import requests

response = requests.post(
    'https://www.cutout.pro/api/v1/photoEnhance2?faceModel=quality',
    files={'file': open('/path/to/blurry.jpg', 'rb')},
    headers={'APIKEY': 'your_api_key_here'},
)
data = response.json()
image_base64 = data['data']['imageBase64']
```
