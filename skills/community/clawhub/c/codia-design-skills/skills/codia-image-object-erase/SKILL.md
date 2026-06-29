---
name: codia-image-object-erase
description: Erase objects from images with Codia Design CLI. Trigger when the user asks to remove unwanted objects, props, clutter, or defects from an image they can edit.
api: image-object-erase
endpoint: POST /v2/open/image/object_erase
cli: codia-design image object-erase
credits_per_call: 13
sync: true
response_type: image_urls
---

# codia-image-object-erase

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Use the mask image to specify the area to be erased, and use inpaint to fill it in and return a clean image.

## CLI Command

```bash
codia-design image object-erase \
  --image <PATH|URL> \
  --mask <PATH|URL> \
  [--model MODEL] \
  [--download-dir DIR] \
  [--no-download] \
  [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Source image (local path or HTTPS URL) |
| `--mask` | path \| URL | yes | — | mask image, the size must be exactly the same as the source image |
| `--model` | string | no | server default | Optional `codia_image_v2`, `nano_banana_2`, `nano_banana_pro`; omit for default cleanup behavior |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | Write JSON results to file |

## Mask Format

The mask image has the same size as the source image (pixel-level correspondence):

- **White (255, 255, 255)** = Erase and inpaint this area
- **Black (0, 0, 0)** = Leave this area unchanged
- Grayscale values produce transitional blending effects; it is recommended to binarize to pure black and white to obtain clear edges

## Response

```json
{
  "ok": true,
  "data": {
    "image_urls": ["https://cdn.codia.ai/erased/result.png"]
  }
}
```

By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image object-erase \
  --image ./photo.png \
  --mask ./mask.png \
  --model nano_banana_pro \
  --download-dir ./outputs \
  --out result.json

node -e "console.log(require('./result.json').data.local_file)"
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image and mask sizes do not match, or the image cannot be accessed | Check that the two images are exactly the same size |
| 402 | Insufficient credits | |
| 429 | Rate limit exceeded | Retry after backing off |

**Credits**: 13 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 26 credits (2x estimate); this does not block generation. · **Duration**: Synchronous, usually < 15s
