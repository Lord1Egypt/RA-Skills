---
name: ccapi-api
description: Use CCAPI unified AI API gateway to access 60+ models (GPT-5.2, Claude, Gemini, DeepSeek, Sora 2, Kling 3.0, Seedance 2.0, Suno, etc.) across text, image, video, and audio. OpenAI SDK compatible — just change the base_url. Use when building AI apps, calling LLMs, generating images/videos/audio, or integrating multiple AI providers through a single API.
argument-hint: "[task-description]"
---

# CCAPI — Unified Multimodal AI API Gateway

CCAPI provides OpenAI-compatible access to 60+ AI models across 4 modalities through a single API endpoint. No new SDK needed — works with OpenAI Python/Node.js SDK.

## Quick Start

**Base URL**: `https://api.ccapi.ai/v1`
**Auth**: `Authorization: Bearer <your-ccapi-api-key>`

Get your API key at https://ccapi.ai/dashboard

### Python (OpenAI SDK)

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-ccapi-key",
    base_url="https://api.ccapi.ai/v1"
)

# Text generation
response = client.chat.completions.create(
    model="openai/gpt-5.2",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Node.js (OpenAI SDK)

```typescript
import OpenAI from "openai"

const client = new OpenAI({
  apiKey: "your-ccapi-key",
  baseURL: "https://api.ccapi.ai/v1",
})

const response = await client.chat.completions.create({
  model: "anthropic/claude-sonnet-4-6",
  messages: [{ role: "user", content: "Hello!" }],
})
```

### cURL

```bash
curl https://api.ccapi.ai/v1/chat/completions \
  -H "Authorization: Bearer your-ccapi-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-5.2",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Available Models

Model IDs use `provider/model-id` format.

### Text (LLM)

| Model ID                      | Context | Notes                     |
| ----------------------------- | ------- | ------------------------- |
| `openai/gpt-5.2`              | 1M      | Latest OpenAI flagship    |
| `openai/gpt-5-mini`           | 1M      | Fast & affordable         |
| `openai/gpt-5-nano`           | 1M      | Ultra-low cost            |
| `openai/gpt-4.1`              | 1M      | Strong reasoning          |
| `openai/gpt-4.1-mini`         | 1M      | Balanced performance      |
| `openai/gpt-4o`               | 128K    | Multimodal                |
| `openai/gpt-4o-mini`          | 128K    | Cost-effective            |
| `anthropic/claude-opus-4-6`   | 200K    | Most capable Claude       |
| `anthropic/claude-sonnet-4-6` | 200K    | Best value Claude         |
| `anthropic/claude-haiku-4-5`  | 200K    | Fastest Claude            |
| `google/gemini-2.5-pro`       | 1M      | Google flagship           |
| `google/gemini-2.5-flash`     | 1M      | Fast Gemini               |
| `deepseek/deepseek-chat`      | 64K     | DeepSeek V3.2             |
| `zhipu/glm-5`                 | 128K    | 744B MoE, top Chinese LLM |
| `openrouter/minimax-m2.5`     | 1M      | SWE-bench 80.2%           |

### Image Generation

| Model ID                 | Notes                  |
| ------------------------ | ---------------------- |
| `google/nano-banana`     | Gemini Flash image gen |
| `google/nano-banana-pro` | Gemini Pro image gen   |

### Video Generation

| Model ID                      | Resolution     | Duration           | Notes                     |
| ----------------------------- | -------------- | ------------------ | ------------------------- |
| `bytedance/seedance-2.0`      | 2K@24fps       | 4-10s              | Text/image/video to video |
| `kuaishou/kling-3.0-standard` | Up to 4K       | 5-10s              | Standard quality          |
| `kuaishou/kling-3.0-pro`      | Up to 4K@60fps | 5-10s              | Professional quality      |
| `openai/sora-2`               | 1080p          | 5-25s              | Physics simulation        |
| `openai/sora-2-pro`           | 1080p          | 5-25s              | Higher quality            |
| `google/veo-3.1`              | 1080p          | Per-second pricing | Google video gen          |

### Audio / Music

| Model ID         | Notes            |
| ---------------- | ---------------- |
| `suno/chirp-v5`  | Music generation |
| `elevenlabs/tts` | Text-to-speech   |

## API Endpoints

### Text Generation (Chat Completions)

```
POST /v1/chat/completions
```

Supports streaming (`stream: true`), function calling, vision (image URLs in messages), and all OpenAI-compatible parameters.

### Image Generation

```
POST /v1/images/generations
```

```json
{
  "model": "google/nano-banana",
  "prompt": "A futuristic cityscape at sunset",
  "n": 1,
  "size": "1024x1024"
}
```

### Video Generation (Async)

**Create video task:**

```
POST /v1/video/generations
```

```json
{
  "model": "bytedance/seedance-2.0",
  "prompt": "A cat playing piano in a jazz bar",
  "duration": 5
}
```

Response includes a `task_id`. Poll for results:

```
GET /v1/video/generations/{task_id}
```

### Audio (Text-to-Speech)

```
POST /v1/audio/speech
```

```json
{
  "model": "elevenlabs/tts",
  "input": "Hello, world!",
  "voice": "alloy"
}
```

### Music Generation (Suno)

```
POST /v1/audio/suno/generate
```

```json
{
  "model": "suno/chirp-v5",
  "prompt": "An upbeat electronic track with synth leads",
  "duration": 30
}
```

### Model Discovery

```
GET /v1/models
```

Returns all available models with pricing, context windows, and capabilities. Supports filtering by provider and type.

## Streaming Example

```python
from openai import OpenAI

client = OpenAI(api_key="your-ccapi-key", base_url="https://api.ccapi.ai/v1")

stream = client.chat.completions.create(
    model="deepseek/deepseek-chat",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Video Generation Full Example

```python
import time
import requests

API_KEY = "your-ccapi-key"
BASE = "https://api.ccapi.ai/v1"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# Create video task
resp = requests.post(f"{BASE}/video/generations", headers=HEADERS, json={
    "model": "kuaishou/kling-3.0-standard",
    "prompt": "A golden retriever running on the beach at sunset, cinematic, 4K",
    "duration": 5,
})
task_id = resp.json()["id"]

# Poll until complete
while True:
    status = requests.get(f"{BASE}/video/generations/{task_id}", headers=HEADERS).json()
    if status["status"] == "completed":
        print(f"Video URL: {status['video_url']}")
        break
    elif status["status"] == "failed":
        print(f"Error: {status.get('error')}")
        break
    time.sleep(5)
```

## Key Features

- **OpenAI SDK compatible** — change `base_url` only, zero migration
- **60+ models** across text, image, video, audio
- **Smart routing** — automatic failover between providers, 99.9% uptime
- **Transparent USD billing** — pay-per-use, no credits/tokens abstraction
- **Tiered pricing** — Free (20% off), Standard (30% off), Pro (40% off) vs official prices

## Error Handling

All errors follow a consistent format:

```json
{
  "error": {
    "message": "Insufficient balance",
    "type": "billing_error",
    "code": "insufficient_funds"
  }
}
```

Error types: `invalid_request_error`, `billing_error`, `api_error`, `rate_limit_error`

## Tips

- Always use `provider/model-id` format (e.g., `openai/gpt-5.2`, not `gpt-5.2`)
- Video and image generation are async — poll the task endpoint for results
- Use `GET /v1/models` to discover available models and current pricing
- Streaming is supported for all text models
- All responses follow the OpenAI API format exactly

## Resources

- Dashboard & API Keys: https://ccapi.ai/dashboard
- Model Showcase: https://ccapi.ai/models
- Pricing: https://ccapi.ai/pricing
- Documentation: https://docs.ccapi.ai
