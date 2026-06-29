---
name: codia-image-upscale
description: Upscale images with Codia Design CLI. Trigger when the user asks to increase resolution, enhance output quality, prepare final assets, or improve generated images.
api: image-upscale
endpoint: POST /v2/open/image/upscale
cli: codia-design image upscale
credits_per_call: 16
sync: true
response_type: image_urls
---

# codia-image-upscale

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

AI enlarges image resolution and improves clarity.

## CLI Command

```bash
codia-design image upscale --image <PATH|URL> [--model MODEL] [--download-dir DIR] [--no-download] [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Local image path, or public HTTPS URL |
| `--model` | string | no | `codia_image_v2` | Optional `ideogram_v3`, `nano_banana_2`, `nano_banana_pro`, `gpt_image` |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | Write JSON results to file |

## Response

```json
{ "ok": true, "data": { "image_urls": ["https://cdn.codia.ai/upscaled/result.png"] } }
```

`data.image_urls[0]` is the enlarged image CDN URL. By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image upscale --image ./photo.png --download-dir ./outputs --out result.json
node -e "console.log(require('./result.json').data.local_file)"
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image is invalid or inaccessible | |
| 402 | Insufficient credits | |

**Credits**: starts at 16 credits/request; varies by model and resolution. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated cost; this does not block generation. · **Duration**: Synchronous
