---
name: creaa-ai
description: Creaa AI - Generate and edit images, plus generate videos via Creaa.ai API. Text-to-image, image edit, text-to-video, image-to-video with multiple AI models.
user-invocable: true
homepage: https://creaa.ai
---
metadata: {"openclaw":{"requires":{"env":["CREAA_API_KEY"]},"primaryEnv":"CREAA_API_KEY"}}

# Creaa AI - Image, Edit & Video Generation

Generate and edit AI images, and generate AI videos directly from your terminal using the Creaa API.

Get your API key at: https://creaa.ai/profile -> API Keys
Top up API credits at: https://creaa.ai/pricing

## Available Models

### Image Models

| Model ID | Name | Credits/Image | Free Daily | Default Ratio | Max Ref Images | Capabilities |
|----------|------|--------------|-----------|---------------|----------------|-------------|
| `seedream-5.0` | Seedream 5.0 | 4 | 10 | 1:1 | 4 | text_to_image, image_to_image |
| `nano-banana-2` | Nano Banana 2 | 10 | 5 | auto | 14 | text_to_image, image_to_image, multi_image_edit |
| `nano-banana-pro` | Nano Banana Pro | 20 | 1 | auto | 10 | text_to_image, image_to_image, multi_image_edit |
| `gpt-image-1.5` | GPT Image 1.5 | 15 | 0 | 1:1 | 10 | text_to_image, image_to_image, multi_image_edit |
| `z-image-turbo` | Z-Image Turbo | 1 | - | 1:1 | - | text_to_image |

**Aspect ratio options per model:**
- `seedream-5.0`: auto, 1:1, 3:4, 4:3, 16:9, 9:16, 2:3, 3:2, 21:9
- `nano-banana-2` / `nano-banana-pro`: auto, 1:1, 9:16, 16:9, 3:2, 2:3
- `gpt-image-1.5`: 1:1, 3:2, 2:3
- `z-image-turbo`: 1:1, 9:16, 16:9

### Video Models

| Model ID | Name | Credits/sec | Durations (sec) | Default Duration | Capabilities |
|----------|------|------------|-----------------|-----------------|-------------|
| `veo-3.1` | Veo 3.1 | 22 | 8 | 8 | text_to_video, image_to_video |
| `seedance-2.0` | Seedance 2.0 | 25 | 5, 10, 15 | 5 | text_to_video, image_to_video |
| `sora-2-pro` | Sora 2 Pro | 12 | 4, 8, 12, 16, 20 | 12 | text_to_video, image_to_video |
| `seedance-1.5-pro` | Seedance 1.5 Pro | 12 | 5, 8, 12 | 5 | text_to_video, image_to_video, first_last_frame |
| `kling-3.0` | Kling 3.0 | 25 | 5, 10, 15 | 5 | text_to_video, image_to_video |
| `hailuo-2.3` | Hailuo 2.3 | 25 | 6, 10 | 6 | text_to_video, image_to_video |
| `runway-gen-4.5` | Runway Gen-4.5 | 30 | 5, 10 | 5 | image_to_video |

**Aspect ratio options per model:**
- `veo-3.1`: 16:9, 9:16
- `seedance-2.0`: 9:16, 16:9, 1:1, 3:4, 4:3
- `sora-2-pro`: 9:16, 16:9
- `seedance-1.5-pro`: 9:16, 16:9, 1:1, 3:4, 4:3
- `kling-3.0`: 16:9, 9:16
- `hailuo-2.3`: 9:16, 16:9
- `runway-gen-4.5`: 16:9, 9:16, 1:1, 4:3, 3:4, 21:9

## Available Commands

All generation and edit tasks are asynchronous: submit a task, get a `task_id`, then poll for results.

### Generate Image

**Step 1: Submit task**
```bash
curl -s -X POST "https://creaa.ai/api/open/v1/images/generate" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Source: openclaw" \
  -d '{
    "prompt": "<user prompt here>",
    "model": "<model_id>",
    "aspect_ratio": "<ratio>",
    "n": <count>
  }'
```

**Parameters:**
- `prompt` (required): Image description
- `model` (optional): Model ID from the image models table above. Default: `nano-banana-2`
- `aspect_ratio` (optional): Aspect ratio like `1:1`, `16:9`, `9:16`. Must match the model's supported ratios. Default varies by model.
- `n` (optional): Number of images, 1-4. Default 1

**Response:**
```json
{
  "success": true,
  "task_id": "abc123-def456",
  "task_type": "image",
  "model": "nano-banana-2"
}
```

**Step 2: Poll status** (wait 5-10 seconds between polls for images)
```bash
curl -s "https://creaa.ai/api/open/v1/tasks/<task_id>" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "X-Source: openclaw"
```

**Status Response (completed):**
```json
{
  "success": true,
  "task_id": "abc123-def456",
  "status": "completed",
  "progress": 1.0,
  "result_url": "https://...",
  "result_urls": ["https://...", "https://..."]
}
```

Image generation typically takes 10-60 seconds. Poll every 5 seconds.

### Edit Image

Use this endpoint for:
- Single-image edit: `image_url` or `image_data` (base64)
- Multi-image reference edit / composition: `image_urls` or `image_data_list` (base64)

**Step 1: Submit task (with URL)**
```bash
curl -s -X POST "https://creaa.ai/api/open/v1/images/edit" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Source: openclaw" \
  -d '{
    "prompt": "<edit prompt here>",
    "image_url": "https://...",
    "model": "<model_id>",
    "aspect_ratio": "<ratio>",
    "n": <count>
  }'
```

**Step 1: Submit task (with base64 image data)**
```bash
curl -s -X POST "https://creaa.ai/api/open/v1/images/edit" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Source: openclaw" \
  -d '{
    "prompt": "<edit prompt here>",
    "image_data": "data:image/png;base64,iVBOR...",
    "model": "<model_id>",
    "aspect_ratio": "<ratio>",
    "n": <count>
  }'
```

**Single-image edit parameters:**
- `prompt` (required): Edit instruction
- `image_url` (option A): Public source image URL
- `image_data` (option B): Base64-encoded image data. Supports `data:image/png;base64,...` prefix or raw base64 string. Max 20MB.
- `model` (optional): Model ID from the image models table above. Default: `nano-banana-2`
- `aspect_ratio` (optional): Must match the model's supported ratios
- `n` (optional): Number of output images, 1-4. Default 1

Provide either `image_url` or `image_data` for single-image edit. If both are provided, `image_url` takes priority.

**Multi-image edit / composition example:**
```bash
curl -s -X POST "https://creaa.ai/api/open/v1/images/edit" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Source: openclaw" \
  -d '{
    "prompt": "<combine these references into one result>",
    "image_urls": ["https://...", "https://..."],
    "model": "nano-banana-2",
    "aspect_ratio": "16:9",
    "n": 1
  }'
```

You can also use `image_data_list` with base64 strings instead of `image_urls`.

**Multi-image edit notes:**
- `image_urls` or `image_data_list`: 2-N images, where N depends on the model
- Max reference images by model:
  - `seedream-5.0`: up to 4 input images
  - `nano-banana-2`: up to 14 input images
  - `nano-banana-pro`: up to 10 input images
  - `gpt-image-1.5`: up to 10 input images
- Only models with `multi_image_edit` capability support this mode
- URLs must be public `http(s)` URLs; base64 data is uploaded to storage automatically

**Response:**
```json
{
  "success": true,
  "task_id": "abc123-def456",
  "task_type": "image_edit",
  "model": "nano-banana-2"
}
```

**Step 2: Poll status**
```bash
curl -s "https://creaa.ai/api/open/v1/tasks/<task_id>" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "X-Source: openclaw"
```

**Status Response (completed):**
```json
{
  "success": true,
  "task_id": "abc123-def456",
  "status": "completed",
  "progress": 1.0,
  "result_url": "https://...",
  "result_urls": ["https://...", "https://..."]
}
```

Image editing typically takes 10-90 seconds. Poll every 5 seconds.

### Generate Video

**Step 1: Submit task**
```bash
curl -s -X POST "https://creaa.ai/api/open/v1/videos/generate" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Source: openclaw" \
  -d '{
    "prompt": "<user prompt here>",
    "model": "<model_id>",
    "mode": "<text_to_video|image_to_video>",
    "duration": <seconds>,
    "aspect_ratio": "<ratio>"
  }'
```

**Parameters:**
- `prompt` (required): Video description
- `model` (optional): Model ID from the video models table above. Default: `veo-3.1`
- `mode` (optional): `text_to_video` (default) or `image_to_video`
- `image_url` (option A, required for image_to_video): URL of the source image
- `image_data` (option B, required for image_to_video): Base64-encoded image data. Supports `data:image/png;base64,...` prefix or raw base64 string. Max 20MB.
- `duration` (optional): Duration in seconds, must match the model's supported durations. Default varies by model.
- `aspect_ratio` (optional): e.g. `16:9`, `9:16`, `1:1`. Must match the model's supported ratios.

For `image_to_video` mode, provide either `image_url` or `image_data`. If both are provided, `image_url` takes priority.

**Response:**
```json
{
  "success": true,
  "task_id": "abc123-def456",
  "task_type": "video",
  "model": "veo-3.1"
}
```

**Step 2: Poll status** (wait 15 seconds between polls for videos)
```bash
curl -s "https://creaa.ai/api/open/v1/tasks/<task_id>" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "X-Source: openclaw"
```

**Status Response (completed):**
```json
{
  "success": true,
  "task_id": "abc123-def456",
  "status": "completed",
  "progress": 1.0,
  "result_url": "https://..."
}
```

Status values: `pending` -> `processing` -> `completed` or `failed`.
Video generation typically takes 60-300 seconds. Poll every 15 seconds.

### Unified Task Status Endpoint
Image generation, image edit, and video tasks all use the same status endpoint:
```bash
curl -s "https://creaa.ai/api/open/v1/tasks/<task_id>" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "X-Source: openclaw"
```

Keep polling until `status` is `completed` or `failed`.
- For images: poll every 5 seconds
- For videos: poll every 15 seconds

### List Available Models
```bash
curl -s "https://creaa.ai/api/open/v1/models" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "X-Source: openclaw"
```

Returns full model catalog with pricing, supported aspect ratios/durations, capabilities, and `max_upload_images` for image-edit models.

### Check Usage
```bash
curl -s "https://creaa.ai/api/open/v1/usage" \
  -H "Authorization: Bearer $CREAA_API_KEY" \
  -H "X-Source: openclaw"
```

Usage is tracked against the API key's own credit pool (`api_credits`), not the website account balance.

## Billing Notes

- Open API requests charge the API key credit pool, not the user's main website balance.
- If task submission fails before the job is queued, credits are refunded immediately.
- If a queued task fails, credits are refunded automatically.
- For image generation and image editing, partial success is billed by successful outputs; unused credits are refunded automatically.
- For video generation, successful jobs keep the full charge; failed jobs are refunded in full.

## Model Selection Tips

**Image models:**
- `seedream-5.0` - Best quality, great default choice (10 free daily)
- `nano-banana-2` - Best default for multi-image editing / composition (5 free daily)
- `nano-banana-pro` - Higher quality image editing (1 free daily)
- `gpt-image-1.5` - Strong image editing option via Replicate-backed path
- `z-image-turbo` - Free, fastest generation

**Video models:**
- `veo-3.1` - Highest quality, 8s fixed duration (22 credits/sec)
- `sora-2-pro` - Best value with long durations up to 20s (12 credits/sec)
- `seedance-1.5-pro` - Affordable with first_last_frame support (12 credits/sec)
- `seedance-2.0` - High quality, flexible durations (25 credits/sec)
- `runway-gen-4.5` - Image-to-video only, high quality

## Error Handling

If any API call returns `"success": false`, display the error message to the user. Common errors:
- `invalid_api_key`: The API key is missing or wrong. User should check their key at https://creaa.ai/profile
- `rate_limit_exceeded`: Too many requests per minute. Wait and retry.
- `Insufficient credits`: Not enough credits. User should top up at https://creaa.ai/pricing
- `Only public http(s) image URLs are allowed`: The image URL points to localhost, private network, or a non-http(s) source.
- `Model <id> does not support multi_image_edit`: The requested model can edit a single image but cannot do multi-image composition.
