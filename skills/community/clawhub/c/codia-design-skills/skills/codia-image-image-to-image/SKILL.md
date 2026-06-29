---
name: codia-image-image-to-image
description: Generate a new image from one or more reference images with Codia Design CLI. Trigger when the user asks to transform, restyle, or create variants from existing visual references.
api: image-image-to-image
endpoint: POST /v2/open/image/image_to_image
cli: codia-design image image-to-image
credits_per_call: varies
sync: true
response_type: image_urls
---

# codia-image-image-to-image

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Based on the reference picture, AI picture editing is performed according to the text description.

## CLI Command

```bash
codia-design image image-to-image \
  --image <PATH|URL> \
  --prompt "TEXT" \
  [--model MODEL] \
  [--size WxH] \
  [--quality low|medium|high] \
  [--background transparent|opaque] \
  [--download-dir DIR] \
  [--no-download] \
  [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Reference image |
| `--prompt` | string | yes | — | Edit description (eg "make it nighttime") |
| `--model` | string | no | `nano_banana_2` | See the `codia-image-generate` skill model table |
| `--size` | string | no | Model default | Requested output size, such as `1024x1024`; providers may normalize the final size |
| `--quality` | string | no | — | Only `gpt_image` supports: `low` / `medium` / `high` |
| `--background` | string | no | — | Only `gpt_image` supports: `transparent` / `opaque` |
| `--download-dir` | path | no | `.` | Directory for downloaded image output |
| `--no-download` | flag | no | false | Return JSON only; do not download image output |
| `--out` | path | no | stdout | |

## Response

```json
{ "ok": true, "data": { "image_urls": ["https://cdn.codia.ai/i2i/result.png"] } }
```

By default the CLI downloads `data.image_urls` and appends `data.local_file` and `data.local_files` to the JSON response. Use `--no-download` only for JSON-only workflows.

## Usage Example

```bash
codia-design image image-to-image \
  --image ./day.png \
  --prompt "make it night time with city lights" \
  --download-dir ./outputs \
  --out result.json
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | Missing image or prompt | |
| 402 | Insufficient credits | |

**Credits**: varies by model and resolution; see `codia-image-generate` pricing table. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 2x the estimated cost; this does not block generation. · **Duration**: Synchronous, usually 5–15s
