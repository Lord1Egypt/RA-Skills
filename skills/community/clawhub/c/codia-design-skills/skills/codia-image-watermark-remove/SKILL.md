---
name: codia-image-watermark-remove
description: Remove watermarks from permitted images with Codia Design CLI. Trigger only for user-owned or authorized images when the user asks to clean a watermark or overlay.
api: image-watermark-remove
endpoint: POST /v2/open/image/watermark_remove
cli: codia-design image watermark-remove
credits_per_call: 13
sync: true
response_type: image_urls
---

# codia-image-watermark-remove

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Automatically detect and remove image watermarks.

## CLI Command

```bash
codia-design image watermark-remove --image <PATH|URL> [--download-dir DIR] [--no-download] [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Image with watermark |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | |

## Response

```json
{ "ok": true, "data": { "image_urls": ["https://cdn.codia.ai/nowm/result.png"] } }
```

By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image watermark-remove --image ./watermarked.png --download-dir ./outputs --out result.json
node -e "console.log(require('./result.json').data.local_file)"
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image is invalid or inaccessible | |
| 402 | Insufficient credits | |

**Credits**: 13 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 26 credits (2x estimate); this does not block generation. · **Duration**: Synchronous
