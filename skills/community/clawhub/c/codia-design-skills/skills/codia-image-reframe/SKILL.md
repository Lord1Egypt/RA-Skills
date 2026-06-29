---
name: codia-image-reframe
description: Reframe images into new aspect ratios with Codia Design CLI. Trigger when the user asks to adapt an image for posters, billboards, square social posts, banners, thumbnails, or packaging layouts.
api: image-reframe
endpoint: POST /v2/open/image/reframe
cli: codia-design image reframe
credits_per_call: varies
sync: true
response_type: image_urls
---

# codia-image-reframe

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Expand the image canvas to a new resolution, and AI generates the fill content (similar to how Photoshop generates extensions).

## CLI Command

```bash
codia-design image reframe \
  --image <PATH|URL> \
  --resolution WxH \
  [--model MODEL] \
  [--download-dir DIR] \
  [--no-download] \
  [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | source image |
| `--resolution` | string | yes | — | Target resolution, such as `1920x1080` |
| `--model` | string | no | `nano_banana_2` | Optional model override; see the `codia-image-generate` skill model table |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | |

## Response

```json
{ "ok": true, "data": { "image_urls": ["https://cdn.codia.ai/reframe/result.png"] } }
```

By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image reframe \
  --image ./portrait.png \
  --resolution 1920x1080 \
  --download-dir ./outputs \
  --out result.json
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | Missing image or resolution | |
| 402 | Insufficient credits | |

**Credits**: varies by model and resolution; see `codia-image-generate` pricing table. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated cost; this does not block generation. · **Duration**: Synchronous
