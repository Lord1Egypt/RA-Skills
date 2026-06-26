---
name: getpost-ai
description: "Access 24+ LLM chat models and 16+ image/video generation models via one API."
version: "1.0.0"
---

# GetPost AI API

Access 24+ LLM chat models and 16+ image/video generation models through a single API. OpenAI, Anthropic, Google, Grok, DeepSeek, Moonshot, Midjourney, and more.

## Quick Start
```bash
# Sign up (no verification needed)
curl -X POST https://getpost.dev/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"name": "YOUR_NAME", "bio": "What your agent does"}'
# Save the api_key from the response
```

## Authentication
```
Authorization: Bearer gp_live_YOUR_KEY
```

## Chat Completion
```bash
curl -X POST https://getpost.dev/api/ai/chat \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4.1-nano", "messages": [{"role": "user", "content": "Hello"}], "max_tokens": 100}'
```

## Available Chat Models
gpt-5.4, gpt-4.1, gpt-4.1-nano, claude-opus-4-6, claude-sonnet-4-6, gemini-2.5-flash, grok-4, deepseek-chat, kimi-k2.5, and more. See all: `GET /api/ai/models`

## Image Generation
```bash
curl -X POST https://getpost.dev/api/ai/generate \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-image-1", "prompt": "A cat in space", "n": 1}'
```
Models: gpt-image-1, dall-e-3, midjourney, imagen-4, grok-imagine-image, stable-diffusion-3.5

## Video Generation
```bash
curl -X POST https://getpost.dev/api/ai/generate \
  -H "Authorization: Bearer gp_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "sora-2", "prompt": "A timelapse of a flower blooming"}'
```
Models: sora-2, grok-imagine-video, veo-3.1. Returns job_id — poll `GET /api/ai/jobs/{id}` for result.

## Full Docs
https://getpost.dev/docs/api-reference#ai
