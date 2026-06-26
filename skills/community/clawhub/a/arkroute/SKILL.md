---
name: arkroute
description: Generate images and videos with 25+ visual AI models (Seedream, FLUX, GPT Image, Kling, Seedance) through one unified API. OpenAI-compatible + MCP server.
version: 1.1.0
metadata:
  openclaw:
    requires:
      env:
        - ARKROUTE_API_KEY
      bins:
        - curl
    primaryEnv: ARKROUTE_API_KEY
    envVars:
      - name: ARKROUTE_API_KEY
        required: true
        description: ArkRoute API key. Get one free at https://ark-route.com/dashboard
    emoji: "🎨"
    homepage: https://ark-route.com
---

# ArkRoute — Visual AI Model Router

Generate images and videos with **25+ visual AI models** through one unified API.
One API key, one format, all the best visual AI models.

## Why ArkRoute?

- **25+ models** — Seedream 3.0, FLUX.1, GPT Image 1, Kling, Seedance, Recraft, and more
- **OpenAI-compatible** — Drop-in replacement, same format you already know
- **MCP Server** — Works with Claude, Cursor, OpenClaw agents out of the box
- **Pay-per-use** — Credit-based pricing, no subscriptions. Free tier included
- **China model access** — ByteDance Seedream/Seedance, Kling, and other models typically hard to access outside China

## Setup

1. Get your free API key at [ark-route.com/dashboard](https://ark-route.com/dashboard)
2. Set the environment variable:

```bash
export ARKROUTE_API_KEY="your-api-key-here"
```

## Usage — Image Generation

```bash
curl -X POST https://api.ark-route.com/v1/images/generations \
  -H "Authorization: Bearer $ARKROUTE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "seedream-3.0", "prompt": "A futuristic city at sunset", "size": "1024x1024"}'
```

### Python

```python
from openai import OpenAI
client = OpenAI(api_key="your-key", base_url="https://api.ark-route.com/v1")
response = client.images.generate(model="seedream-3.0", prompt="A futuristic city at sunset", size="1024x1024")
print(response.data[0].url)
```

## MCP Server

ArkRoute exposes a native MCP endpoint:

```json
{
  "mcpServers": {
    "arkroute": {
      "url": "https://api.ark-route.com/mcp",
      "headers": { "Authorization": "Bearer YOUR_ARKROUTE_API_KEY" }
    }
  }
}
```

## Available Models

| Model | Provider | Type | Cost |
|-------|----------|------|------|
| Seedream 3.0 | ByteDance | Image | $0.020 |
| FLUX.1 Schnell | Black Forest | Image | $0.003 |
| GPT Image 1 | OpenAI | Image | $0.040 |
| Seedance 2.0 | ByteDance | Video | $0.200 |
| Kling 2.0 | Kuaishou | Video | $0.300 |

[Full pricing →](https://ark-route.com/pricing)

## Links

- [Dashboard](https://ark-route.com/dashboard)
- [Playground](https://ark-route.com/playground)
- [Pricing](https://ark-route.com/pricing)