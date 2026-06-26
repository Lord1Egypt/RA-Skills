---
name: evez-api-gateway
description: Connect to the EVEZ AI API — an OpenAI-compatible API that's 99% cheaper than GPT-4. Use when routing LLM calls through EVEZ for cost savings, accessing evez-smart/evez-code/evez-fast/evez-vision models, or building apps on top of EVEZ infrastructure. Free tier with 100K tokens/month, Pro at $5/month unlimited.
---

# EVEZ API Gateway

OpenAI-compatible AI API at 99% less than GPT-4. Drop-in replacement.

## Quick Start

```bash
export OPENAI_BASE_URL=https://evez-api2.fly.dev/v1
export OPENAI_API_KEY=evez-your-key
```

```python
from openai import OpenAI
client = OpenAI(base_url="https://evez-api2.fly.dev/v1", api_key="evez-your-key")
response = client.chat.completions.create(model="evez-smart", messages=[{"role": "user", "content": "Hello!"}])
```

## Models

| Model | Base | Best For | 1M Output |
|-------|------|----------|-----------|
| evez-smart | GLM-5.1 | General purpose — smart & fast | $6.00 |
| evez-code | DeepSeek V3.2 | Code generation & reasoning | $6.00 |
| evez-fast | MiniMax M2.5 | Quick balanced responses | $6.00 |
| evez-vision | Kimi K2.5 | Multimodal (text + image) | $6.00 |

Compare: GPT-4o = $17.50, Claude Sonnet = $15.00, Gemini Pro = $7.00

## Pricing

- **Free**: 100K tokens/month — no credit card
- **Pro**: $5/month — unlimited tokens
- **Business**: $25/month — team + SLA

## Features

- ✅ OpenAI-compatible (drop-in replacement)
- ✅ Streaming support (SSE)
- ✅ 4 models including vision
- ✅ API key management
- ✅ Usage tracking
- ✅ 99.9% uptime on Fly.io

## Get API Key

Sign up at https://evez-api2.fly.dev/signup
