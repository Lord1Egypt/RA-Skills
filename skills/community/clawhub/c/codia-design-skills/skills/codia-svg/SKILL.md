---
name: codia-svg
description: Create, inspect, or retrieve SVG vectorization tasks with Codia Design CLI. Trigger when the user asks to vectorize a logo, icon, or image into SVG.
api: svg
endpoint: POST /v2/open/svg_converter/create  +  GET /v2/open/svg_converter/result/:record_id  +  GET /v2/open/svg_converter/limit
cli: codia-design svg
credits_per_call: 13
sync: false
response_type: task
---

# codia-svg

## Runtime And Auth

Use the local `codia-design` CLI for this feature. Before calling the API, verify that `codia-design` is available. If it is missing and global npm installs are allowed, install it with `npm install -g @codia-ai/codia-design-cli`. Then check `codia-design auth status`; if it is not connected, run `codia-design auth login --platform codex` or bind an API key with `codia-design auth set --api-key api_key_xxx`. Never print API keys or `~/.codia/design-skills/config.json`.

Vectorize raster images (PNG/JPG/WebP/GIF) to SVG (asynchronous task).

## Workflow

### Step 1: Submit conversion task

```bash
codia-design svg create --image <PATH|URL> [--name OUTPUT_NAME]
```

| Flag | Type | Required | Description |
|---|---|---|---|
| `--image` | path \| URL | yes | Local image path, or public HTTPS URL |
| `--name` / `--file_name` | string | no | Output file name (without extension) |

Response (`SvgConverterCreateResponse`):

```json
{
  "ok": true,
  "data": {
    "record_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

Poll the results using the returned `record_id`.

---

### Step 2: Polling results

```bash
codia-design svg get --id <RECORD_ID>
```

| Flag | Type | Required | Description |
|---|---|---|---|
| `--id` / `--task_id` | string | yes | `record_id` returned in step 1 |

Response (`SvgConverterGetResponse`):

```json
{
  "ok": true,
  "data": {
    "svg_url": "https://cdn.codia.ai/output/logo.svg",
    "svg_convert_status": 2
  }
}
```

`svg_convert_status` value (**integer**):

| Value | Meaning |
|---|---|
| `1` | doing — Converting, continue polling |
| `2` | complete — Complete, read `svg_url` |
| `3` | failed — failed, resubmit |

The recommended polling interval is 3–5 seconds.

---

### Step 3 (optional): Query limit

```bash
codia-design svg limit
```

Response (`SvgConverterLimitResponse`):

```json
{
  "ok": true,
  "data": {
    "pic_height": 4096,
    "pic_width": 4096,
    "file_size": 10485760,
    "layer_credit_unit": 13
  }
}
```

| Field | Description |
|---|---|
| `pic_height` / `pic_width` | Input the maximum size of the image (pixels) |
| `file_size` | Maximum input file size (bytes), 10 MB = 10485760 |
| `layer_credit_unit` | Number of credits consumed for each conversion. Public Open API v2 currently prices `svg create` at 13 credits/create. |

## Full Example

```bash
# submit
codia-design svg create --image ./logo.png --out create.json
RECORD_ID=$(node -e "console.log(require('./create.json').data.record_id)")

# Poll until complete
while true; do
  codia-design svg get --id "$RECORD_ID" --out status.json
  STATUS=$(node -e "console.log(require('./status.json').data.svg_convert_status)")
  [ "$STATUS" = "2" ] && break
  [ "$STATUS" = "3" ] && echo "Failed" && exit 1
  sleep 3
done

SVG_URL=$(node -e "console.log(require('./status.json').data.svg_url)")
curl -o output.svg "$SVG_URL"
```

## Input Limits

The maximum size and file size of input images depend on the plan level:

| Packages | Maximum resolution | Maximum file size |
|---|---|---|
| Free | 1440×1440 | 5 MB |
| Starter | 1024×1024 | 2 MB |
| Pro | 4096×4096 | 4 MB |

At runtime, you can use `codia-design svg limit` to query the actual limit in effect for the current account (the return value has been calculated based on the package).

## Errors & Billing

| HTTP | Meaning | Fix |
|---|---|---|
| 400 | The image is invalid or exceeds the size/file size limit | Call `svg limit` first to confirm the limit |
| 402 | Insufficient credits | Recharge and try again |
| 429 | Rate limit exceeded | Retry after backing off |

**Credits**: 13 credits/create on Open API v2; `get` and `limit` do not consume credits. After `create` completes, the CLI checks `available_credits` and reminds the user if the remaining balance is below 26 credits (2x estimate); this does not block generation. · **Duration**: asynchronous
