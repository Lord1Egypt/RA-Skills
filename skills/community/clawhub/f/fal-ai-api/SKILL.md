---
name: fal-ai
description: |
  fal.ai API integration with managed API key authentication. Run AI models for image generation, video generation, audio processing, and more.
  Use this skill when users want to generate images (Flux, SDXL), create videos (Minimax), upscale images, transcribe audio, or run other AI models on fal.ai.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# fal.ai

Access the fal.ai queue API with managed API key authentication. Run 1000+ AI models including image generation (Flux, SDXL), video generation (Minimax), image upscaling, text-to-speech, and more.

## Quick Start

```bash
# Generate an image with Flux Schnell
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "a tiny cute cat",
    "image_size": "square_hd",
    "num_images": 1
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/fal-ai/{native-api-path}
```

The gateway proxies requests to `queue.fal.run`. For model inference, paths follow the pattern:

```
/fal-ai/fal-ai/{model-id}
/fal-ai/fal-ai/{model-id}/requests/{request_id}/status
/fal-ai/fal-ai/{model-id}/requests/{request_id}
/fal-ai/fal-ai/{model-id}/requests/{request_id}/cancel
```

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your fal.ai API key connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=fal-ai&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'fal-ai'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "7355bd0b-8aaf-4c58-9122-a1e3d454414d",
    "status": "PENDING",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "fal-ai",
    "method": "API_KEY"
  }
}
```

Open the returned `url` in a browser to enter your fal.ai API key.

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## API Reference

### Queue API

The fal.ai queue API provides asynchronous model inference with status polling.

#### Submit Request

Submit a request to run a model. Returns immediately with a request ID.

```bash
POST /fal-ai/fal-ai/{model-id}
Content-Type: application/json

{
  "prompt": "model-specific parameters",
  ...
}
```

**Response:**
```json
{
  "status": "IN_QUEUE",
  "request_id": "3229f185-a99a-48c0-a292-e25bf9baaeba",
  "response_url": "https://queue.fal.run/fal-ai/flux/requests/3229f185-a99a-48c0-a292-e25bf9baaeba",
  "status_url": "https://queue.fal.run/fal-ai/flux/requests/3229f185-a99a-48c0-a292-e25bf9baaeba/status",
  "cancel_url": "https://queue.fal.run/fal-ai/flux/requests/3229f185-a99a-48c0-a292-e25bf9baaeba/cancel",
  "queue_position": 0
}
```

#### Check Status

Poll for request status until completion.

```bash
GET /fal-ai/fal-ai/{model-id}/requests/{request_id}/status
```

**Response (IN_PROGRESS):**
```json
{
  "status": "IN_PROGRESS",
  "request_id": "3229f185-a99a-48c0-a292-e25bf9baaeba"
}
```

**Response (COMPLETED):**
```json
{
  "status": "COMPLETED",
  "request_id": "3229f185-a99a-48c0-a292-e25bf9baaeba",
  "metrics": {
    "inference_time": 0.3334658145904541
  }
}
```

#### Get Result

Retrieve the completed result.

```bash
GET /fal-ai/fal-ai/{model-id}/requests/{request_id}
```

**Response (image generation):**
```json
{
  "images": [
    {
      "url": "https://v3b.fal.media/files/...",
      "width": 1024,
      "height": 1024,
      "content_type": "image/jpeg"
    }
  ],
  "timings": {
    "inference": 0.1587670766748488
  },
  "seed": 761506470,
  "prompt": "a tiny cute cat"
}
```

#### Cancel Request

Cancel a queued or in-progress request.

```bash
PUT /fal-ai/fal-ai/{model-id}/requests/{request_id}/cancel
```

### Popular Models

#### Flux Schnell (Fast Image Generation)

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "a serene mountain landscape at sunset",
    "image_size": "landscape_16_9",
    "num_images": 1,
    "num_inference_steps": 4
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Parameters:**
- `prompt` (required): Text description of the image
- `image_size`: `square_hd`, `square`, `portrait_4_3`, `portrait_16_9`, `landscape_4_3`, `landscape_16_9`
- `num_images`: Number of images to generate (default: 1)
- `num_inference_steps`: Number of steps (default: 4)
- `seed`: Random seed for reproducibility

#### Fast SDXL (Stable Diffusion XL)

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "a futuristic city skyline at night",
    "negative_prompt": "blurry, low quality",
    "image_size": "landscape_16_9",
    "num_images": 1
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/fast-sdxl', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Parameters:**
- `prompt` (required): Text description
- `negative_prompt`: What to avoid in the image
- `image_size`: Output dimensions
- `num_images`: Number of images
- `guidance_scale`: CFG scale (default: 7.5)
- `num_inference_steps`: Number of steps

#### Clarity Upscaler (Image Upscaling)

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "image_url": "https://example.com/image.jpg",
    "scale": 2
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/clarity-upscaler', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Parameters:**
- `image_url` (required): URL of the image to upscale
- `scale`: Upscale factor (2, 4)

#### Minimax Video Generation

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "prompt": "A cat playing with a ball in slow motion"
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/minimax/video-01', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

#### F5-TTS (Text-to-Speech)

```bash
python <<'EOF'
import urllib.request, os, json

data = json.dumps({
    "gen_text": "Hello world, this is a test of fal ai text to speech."
}).encode()

req = urllib.request.Request('https://gateway.maton.ai/fal-ai/fal-ai/f5-tts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Request Status Values

| Status | Description |
|--------|-------------|
| `IN_QUEUE` | Request received, waiting for runner |
| `IN_PROGRESS` | Model is processing the request |
| `COMPLETED` | Processing finished, result available |
| `FAILED` | Processing failed (check error details) |

### Request Headers

| Header | Description |
|--------|-------------|
| `X-Fal-Request-Timeout` | Server-side deadline in seconds |
| `X-Fal-Runner-Hint` | Session affinity for routing |
| `X-Fal-Queue-Priority` | `normal` (default) or `low` |
| `X-Fal-No-Retry` | Disable automatic retries |

## Complete Workflow Example

```bash
python <<'EOF'
import urllib.request, os, json, time

api_key = os.environ["MATON_API_KEY"]
base_url = "https://gateway.maton.ai/fal-ai"

# 1. Submit request
data = json.dumps({
    "prompt": "a beautiful sunset over the ocean",
    "image_size": "landscape_16_9",
    "num_images": 1
}).encode()

req = urllib.request.Request(f'{base_url}/fal-ai/flux/schnell', data=data, method='POST')
req.add_header('Authorization', f'Bearer {api_key}')
req.add_header('Content-Type', 'application/json')
submit_response = json.load(urllib.request.urlopen(req))
request_id = submit_response['request_id']
print(f"Submitted: {request_id}")

# 2. Poll for completion
while True:
    req = urllib.request.Request(f'{base_url}/fal-ai/flux/requests/{request_id}/status')
    req.add_header('Authorization', f'Bearer {api_key}')
    status_response = json.load(urllib.request.urlopen(req))
    print(f"Status: {status_response['status']}")

    if status_response['status'] == 'COMPLETED':
        break
    elif status_response['status'] == 'FAILED':
        print("Request failed")
        exit(1)

    time.sleep(1)

# 3. Get result
req = urllib.request.Request(f'{base_url}/fal-ai/flux/requests/{request_id}')
req.add_header('Authorization', f'Bearer {api_key}')
result = json.load(urllib.request.urlopen(req))
print(f"Image URL: {result['images'][0]['url']}")
EOF
```

## Code Examples

### JavaScript

```javascript
const submitRequest = async () => {
  // Submit
  const submitRes = await fetch('https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    },
    body: JSON.stringify({
      prompt: 'a tiny cute cat',
      image_size: 'square_hd',
      num_images: 1
    })
  });
  const { request_id } = await submitRes.json();

  // Poll
  let status = 'IN_QUEUE';
  while (status !== 'COMPLETED') {
    await new Promise(r => setTimeout(r, 1000));
    const statusRes = await fetch(
      `https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/${request_id}/status`,
      { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
    );
    status = (await statusRes.json()).status;
  }

  // Get result
  const resultRes = await fetch(
    `https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/${request_id}`,
    { headers: { 'Authorization': `Bearer ${process.env.MATON_API_KEY}` } }
  );
  return await resultRes.json();
};
```

### Python (requests)

```python
import os
import time
import requests

api_key = os.environ["MATON_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}"}

# Submit
response = requests.post(
    "https://gateway.maton.ai/fal-ai/fal-ai/flux/schnell",
    headers=headers,
    json={"prompt": "a tiny cute cat", "image_size": "square_hd", "num_images": 1}
)
request_id = response.json()["request_id"]

# Poll
while True:
    status = requests.get(
        f"https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/{request_id}/status",
        headers=headers
    ).json()["status"]
    if status == "COMPLETED":
        break
    time.sleep(1)

# Get result
result = requests.get(
    f"https://gateway.maton.ai/fal-ai/fal-ai/flux/requests/{request_id}",
    headers=headers
).json()
print(result["images"][0]["url"])
```

## Notes

- The gateway proxies to `queue.fal.run` for model inference
- All model requests are queued - poll for status until completion
- Model parameters vary by model - check fal.ai documentation for specifics
- Image URLs from fal.ai CDN are temporary - download or store them
- Video generation models may take longer to complete
- Use webhooks for long-running tasks (add `?fal_webhook=URL` to submit request)
- IMPORTANT: When piping curl output to `jq`, environment variables may not expand correctly. Use Python examples instead.

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing fal-ai connection or invalid request |
| 401 | Invalid or missing Maton API key |
| 422 | Invalid model parameters |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from fal.ai API |

### Troubleshooting

1. **Check connection exists:**
```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=fal-ai&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

2. **Verify path format:** Paths must start with `/fal-ai/fal-ai/{model-id}`

3. **Check model exists:** Some model IDs include organization prefix (e.g., `fal-ai/flux/schnell`)

## Resources

- [fal.ai Documentation](https://fal.ai/docs)
- [Model Gallery](https://fal.ai/models)
- [Queue API Reference](https://fal.ai/docs/model-endpoints/queue)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
