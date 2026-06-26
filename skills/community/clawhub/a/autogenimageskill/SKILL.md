---
name: autoGenImageSkill
version: "0.1.2"
description: "Use when the user wants GPT-Image-2 image generation or image-to-image through an official OpenAI permission code/API key, a custom Responses-compatible proxy, or a reserved purchased-capacity relay."
homepage: https://github.com/Etherstrings/autoGenImageSkill#donate
metadata:
  openclaw:
    requires:
      bins: ["node"]
---

# autoGenImageSkill

## Overview

Use this OpenClaw skill to generate PNG images with the local `gpt_image` relay pattern: a Responses API request uses text model `gpt-5.4` plus an `image_generation` tool using `gpt-image-2`, then writes the returned base64 image to disk. The bundled CLI exposes three access paths so agents can pick the right entry without rewriting fetch/SSE/image decoding logic.

The main script is [scripts/gpt_image_cli.js](scripts/gpt_image_cli.js). Run it with Node 18+. In OpenClaw, reference it as `{baseDir}/scripts/gpt_image_cli.js` so the command works wherever the skill folder is located.

External pages:

- ClawHub / OpenClaw: `https://clawhub.ai/Etherstrings/autogenimageskill`
- Hermes Agent GitHub skill source: `https://github.com/Etherstrings/autoGenImageSkill/tree/main/autoGenImageSkill`

## 赞助支持

- 爱发电: `https://ifdian.net/a/etherstrings`
- GitHub donate section: `https://github.com/Etherstrings/autoGenImageSkill#donate`

Alipay:

![Alipay QR](https://raw.githubusercontent.com/Etherstrings/autoGenImageSkill/main/docs/assets/donate/alipay_clawhub.jpg)

WeChat Pay:

![WeChat Pay QR](https://raw.githubusercontent.com/Etherstrings/autoGenImageSkill/main/docs/assets/donate/wechat_clawhub.jpg)

## Access Choice

1. Use `official` when the user provides an official OpenAI permission code/API key or explicitly wants the official API path.
2. Use `proxy` when the user provides a custom `base_url`, proxy endpoint, provider name, or third-party Responses-compatible API key.
3. Use `reserved` when the user wants to use the creator's reserved capacity, purchase/redeem a key, check quota, or call the relay service that exposes `/api/session`, `/api/keys`, and `/api/generate/jobs`.

Do not echo API keys, permission codes, purchase keys, or provider tokens back to the user. Use environment variables or shell variables in examples.

## Quick Commands

Official API key / permission code:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode official \
  --permission-code "$OPENAI_API_KEY" \
  --prompt "一张电影感的雨夜赛博城市街景" \
  --output output/cyber-rain.png
```

Custom proxy:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode proxy \
  --base-url "$GPT_IMAGE_BASE_URL" \
  --api-key "$GPT_IMAGE_API_KEY" \
  --prompt "透明背景的可爱机器人贴纸" \
  --size 1024x1024 \
  --output output/robot-sticker.png
```

Reserved purchased capacity:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode reserved \
  --service-url "$GPT_IMAGE_RELAY_URL" \
  --purchase-key "$GPT_IMAGE_PURCHASE_KEY" \
  --prompt "国风水墨质感的未来城市海报" \
  --output output/ink-future-city.png
```

Image-to-image:

```bash
node {baseDir}/scripts/gpt_image_cli.js generate \
  --mode proxy \
  --base-url "$GPT_IMAGE_BASE_URL" \
  --api-key "$GPT_IMAGE_API_KEY" \
  --prompt "保持人物姿势，改成高端杂志封面摄影" \
  --image /absolute/path/reference.png \
  --output output/cover.png
```

## Reserved Flow

For reserved capacity, create or reuse a session before generation when the user wants account persistence:

```bash
node {baseDir}/scripts/gpt_image_cli.js session \
  --service-url "$GPT_IMAGE_RELAY_URL" \
  --profile-name "demo-user" \
  --save-session
```

Redeem a purchase key without generating:

```bash
node {baseDir}/scripts/gpt_image_cli.js redeem \
  --service-url "$GPT_IMAGE_RELAY_URL" \
  --purchase-key "$GPT_IMAGE_PURCHASE_KEY" \
  --user-id "$GPT_IMAGE_USER_ID"
```

Check quota:

```bash
node {baseDir}/scripts/gpt_image_cli.js quota \
  --service-url "$GPT_IMAGE_RELAY_URL" \
  --user-id "$GPT_IMAGE_USER_ID"
```

## References

- Read [references/access-modes.md](references/access-modes.md) when choosing among official, proxy, and reserved entries or when a user asks how to configure them.
- Read [references/runtime.md](references/runtime.md) when debugging generation, SSE parsing, relay quota, OpenClaw/Hermes packaging, or the relationship to the original `gpt_image` project.

## Output Rules

Always return the absolute output image path and the decisive metadata: access mode, endpoint or relay job ID, provider name when available, byte size, and any revised prompt returned by the model. Keep credentials redacted.
