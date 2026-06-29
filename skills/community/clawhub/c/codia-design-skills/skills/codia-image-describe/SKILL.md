---
name: codia-image-describe
description: Describe and analyze an image with Codia Design CLI. Trigger when the user asks to inspect, summarize, caption, or extract visual details from an image.
api: image-describe
endpoint: POST /v2/open/image/describe
cli: codia-design image describe
credits_per_call: 5
sync: true
response_type: text
---

# codia-image-describe

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Use AI to analyze image content and return natural language descriptions.

## CLI Command

```bash
codia-design image describe --image <PATH|URL> [--model MODEL] [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Local image path, or public HTTPS URL |
| `--model` | string | no | server default | Optional model override; omit unless the user requests a specific model |
| `--out` | path | no | stdout | Write JSON results to file |

## Response

```json
{
  "ok": true,
  "data": {
    "description": "A screenshot of a mobile app showing a product listing page with a search bar at the top, a grid of product cards below, and a bottom navigation bar with Home, Search, Cart, and Profile icons."
  }
}
```

| Field | Type | Description |
|---|---|---|
| `data.description` | string | Natural language description of the image |

## Usage Example

```bash
codia-design image describe --image ./screenshot.png --out desc.json
node -e "console.log(require('./desc.json').data.description)"
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image is invalid or inaccessible | |
| 402 | Insufficient credits | |
| 429 | Rate limit exceeded | Retry after backing off |

**Credits**: 5 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 10 credits (2x estimate); this does not block generation. · **Duration**: Synchronous, usually < 5s
