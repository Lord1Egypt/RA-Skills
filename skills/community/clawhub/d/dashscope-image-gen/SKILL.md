---
name: dashscope-image-gen
description: Generate images via Alibaba DashScope OpenAI-compatible endpoint (compatible-mode) using qwen-image-max. Use when the user asks for 文生图/图片生成/image generation, wants to call /images/generations, or needs a scriptable CLI tool to create images from prompts.
---

# DashScope Image Generation (qwen-image-max)

Use this skill to generate an image from a text prompt through DashScope **compatible-mode**.

## Quick start

Preferred (no secrets in shell history):

```bash
export DASHSCOPE_API_KEY="..."
./scripts/dashscope_image_gen.py --prompt "a cute robot, watercolor" --out robot.png
```

Optional params (best-effort; support depends on DashScope):

```bash
./scripts/dashscope_image_gen.py --prompt "industrial factory at night" --size 1024x1024 --n 1 --out factory.png
```

## What to do when it fails

1. Re-run with the same command and copy the **HTTP error body**.
2. If the error indicates a different route/payload than OpenAI Images API:
   - Update `scripts/dashscope_image_gen.py` accordingly.
   - Update `references/dashscope-openai-compatible.md` with the correct details.

## Files

- `scripts/dashscope_image_gen.py`: main CLI (calls `POST {baseUrl}/images/generations`)
- `references/dashscope-openai-compatible.md`: endpoint/auth notes
