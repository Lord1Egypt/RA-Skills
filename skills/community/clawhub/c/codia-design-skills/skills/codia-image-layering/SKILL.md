---
name: codia-image-layering
description: Convert an image into Codia layering DSL for editable design reconstruction. Trigger when the user asks for layers, structured design data, or editable reconstruction from an image.
api: image-layering
endpoint: POST /v2/open/image/layering
cli: codia-design image layering
credits_per_call: 27
sync: true
response_type: object
---

# codia-image-layering

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Explodes the image into editable layers, returning layer DSL data (JSON-encoded layer tree).

## CLI Command

```bash
codia-design image layering --image <PATH|URL> [--out FILE]
```

## Parameters

| Flag | Type | Required | Default | Description |
|---|---|---|---|---|
| `--image` | path \| URL | yes | — | Local image path, or public HTTPS URL |
| `--out` | path | no | stdout | Write JSON results to file |

> The `--model` parameter is invalid for this endpoint and will not be read by the server.

## Response

```json
{
  "ok": true,
  "data": {
    "type": 0,
    "dsl": "{\"layers\":[...]}"
  }
}
```

| Field | Type | Description |
|---|---|---|
| `data.type` | integer | Hierarchical result type (`0` = standard layer tree) |
| `data.dsl` | string | **JSON string**, which will be parsed into a layer tree object |

### Parse dsl

The `dsl` field is a JSON string (requires secondary parse):

```js
const { data } = require('./result.json');
const layers = JSON.parse(data.dsl);
console.log(layers);
```

The internal structure of dsl describes the type, position, size and image URL of each layer. The specific fields are determined by the content returned by the server.

## Usage Example

```bash
codia-design image layering --image ./composite.png --out result.json
node -e "
const {data} = require('./result.json');
const layers = JSON.parse(data.dsl);
console.log('layers:', JSON.stringify(layers, null, 2));
"
```

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image is invalid or inaccessible | |
| 402 | Insufficient credits | |
| 429 | Rate limit exceeded | Retry after backing off |

**Credits**: 27 credits/request. After the command completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 54 credits (2x estimate); this does not block generation. · **Duration**: Synchronous
