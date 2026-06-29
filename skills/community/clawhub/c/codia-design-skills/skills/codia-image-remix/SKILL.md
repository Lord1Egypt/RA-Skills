---
name: codia-image-remix
description: Create controlled image variations with Codia Design CLI. Trigger when the user asks for visual variants, campaign alternatives, style-consistent options, or iterative remixes.
api: image-remix
endpoint: POST /v2/open/image/remix
cli: codia-design image remix
credits_per_call: varies
sync: true
response_type: image_urls
---

# codia-image-remix

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Use the reference image as a source of inspiration to generate a new image after style transfer.

## CLI Command

```bash
codia-design image remix \
  --image <PATH|URL> \
  --prompt "TEXT" \
  [--size WxH] \
  [--model MODEL] \
  [--download-dir DIR] \
  [--no-download] \
  [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Style reference image |
| `--prompt` | string | yes | — | Style description (such as "cyberpunk neon style") |
| `--size` | string | no | Model default | Output size, such as `1024x1024` |
| `--model` | string | no | `nano_banana_2` | See the `codia-image-generate` skill model table |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | |

## Response

```json
{ "ok": true, "data": { "image_urls": ["https://cdn.codia.ai/remix/result.png"] } }
```

By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image remix \
  --image ./reference.png \
  --prompt "cyberpunk neon city style" \
  --size 1024x1024 \
  --download-dir ./outputs \
  --out result.json
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | Missing image or prompt | |
| 402 | Insufficient credits | |

**Credits**: varies by model and resolution; see `codia-image-generate` pricing table. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated cost; this does not block generation. · **Duration**: Synchronous
