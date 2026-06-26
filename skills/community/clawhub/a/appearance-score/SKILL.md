---
name: appearance-score
description: >-
  Multi-face appearance / attractiveness scoring: POST multipart image to Synerunify
  predict API. Apply when the user asks in English (e.g. face attractiveness score,
  beauty rating, appearance score for a photo) or Chinese (颜值打分、外观评分、给照片人脸打分).
---

# Appearance scoring (predict)

## Endpoint

- **Method**: `POST`
- **URL**: `https://synerunify.com/api/process/appearance/predict`
- **Content-Type**: `multipart/form-data`
- **Field**: `image` (required; image file; use a real image MIME such as `image/jpeg`)
- **Query**: Omit; server defaults apply.

## Response JSON

Top level:

- `code`: `200` means success
- `message`: human-readable status text
- `data`: present on success; may be incomplete on failure

Inside `data`:

- `count`: number of scored faces
- `size`: `{ "width", "height" }` of the original image in pixels
- `faces`: array of items with:
  - `region`: `{ x1, y1, x2, y2, width, height }` in original-image pixels
  - `score`: float; you may `round` for display

On errors or no faces, read `message`; `data.faces` may be empty.

## Examples

**curl**

```bash
curl -sS -X POST "https://synerunify.com/api/process/appearance/predict" \
  -F "image=@/path/to/photo.jpg"
```

**Python**

```python
import requests

url = "https://synerunify.com/api/process/appearance/predict"
with open("photo.jpg", "rb") as f:
    r = requests.post(url, files={"image": ("photo.jpg", f, "image/jpeg")}, timeout=120)
r.raise_for_status()
payload = r.json()
if payload.get("code") != 200:
    raise RuntimeError(payload.get("message", "API error"))
faces = payload["data"]["faces"]
scores = [round(f["score"]) for f in sorted(faces, key=lambda x: x["region"]["x1"])]
```

## Agent rules

1. Upload only via multipart field **`image`**; do not append query params; do not switch to JSON/Base64 unless the API docs explicitly say so.
2. When multiple faces are present, sort by `region.x1` (left-to-right) before reporting scores.
3. On failure, surface `message` and the HTTP status first.
