---
name: codia-remove-bg
description: Remove image backgrounds with Codia Design CLI. Trigger when the user asks for cutouts, transparent product images, background removal, or ecommerce-ready isolated assets.
api: remove-bg
endpoint: POST /v2/open/remove_bg
cli: codia-design remove-bg
credits_per_call: 13
sync: true
response_type: image_url
---

# codia-remove-bg

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Automatically identify and remove the image background, returning a PNG with a transparent background.

## CLI Command

```bash
codia-design remove-bg --image <PATH|URL> [--download-dir DIR] [--no-download] [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Local image path, or public HTTPS URL |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | Write JSON results to file |

## Response

```json
{
  "ok": true,
  "data": {
    "image_url": "https://cdn.codia.ai/nobg/product.png"
  }
}
```

> Note: `remove-bg` returns `image_url` (singular), other image tools return `image_urls` (plural array).

| Field | Type | Description |
|---|---|---|
| `data.image_url` | string | Transparent PNG CDN URL after removing the background |
| `data.local_file` | string | CLI default local file path after download; absent with `--no-download` |
| `data.local_files` | string[] | CLI default local file paths after download; absent with `--no-download` |

## Usage Example

```bash
codia-design remove-bg --image ./product.png --download-dir ./outputs --out result.json
node -e "console.log(require('./result.json').data.local_file)"
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image is invalid or inaccessible | |
| 402 | Insufficient credits | |
| 429 | Rate limit exceeded | Retry after backing off |

**Credits**: 13 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 26 credits (2x estimate); this does not block generation. · **Duration**: Synchronous, usually < 5s
