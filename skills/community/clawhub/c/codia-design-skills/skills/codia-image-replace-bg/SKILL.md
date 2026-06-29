---
name: codia-image-replace-bg
description: Replace image backgrounds with Codia Design CLI. Trigger when the user asks for studio backgrounds, lifestyle scenes, ecommerce backgrounds, or product scene changes.
api: image-replace-bg
endpoint: POST /v2/open/image/replace_background
cli: codia-design image replace-bg
credits_per_call: 13
sync: true
response_type: image_urls
---

# codia-image-replace-bg

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Keep the main body of the image and replace the background with a text description.

## CLI Command

```bash
codia-design image replace-bg \
  --image <PATH|URL> \
  --prompt "TEXT" \
  [--model MODEL] \
  [--download-dir DIR] \
  [--no-download] \
  [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | source image |
| `--prompt` | string | yes | — | Text description of the new background, the more specific the better |
| `--model` | string | no | `nano_banana_2` | optional `nano_banana_pro`, `ideogram_v3` |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | |

**Prompt suggestion**: Describe the surface material ("clean white marble"), lighting ("soft studio lighting"), and scene ("outdoor sunset").

## Response

```json
{ "ok": true, "data": { "image_urls": ["https://cdn.codia.ai/replaced/result.png"] } }
```

By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image replace-bg \
  --image ./product.png \
  --prompt "clean white marble table with soft studio lighting" \
  --download-dir ./outputs \
  --out result.json
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | Missing image or prompt | |
| 402 | Insufficient credits | |

**Credits**: 13 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 26 credits (2x estimate); this does not block generation. · **Duration**: Synchronous, usually 5–15s
