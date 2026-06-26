---
name: IMA Nano Banana Image Generator
version: 1.1.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: nano banana, nano banana 2, nano banana pro, image generation, gemini image, text to image, image to image, ima studio, ai-nano-banana
argument-hint: "[text prompt or image URL]"
description: >
  Nano Banana-only image generation on IMA Open API. Supports text_to_image and image_to_image 
  with gemini-3.1-flash-image (budget) and gemini-3-pro-image (premium). Deterministic size/ratio 
  mapping, 512/1K/2K/4K resolution. Requires IMA_API_KEY.
requires:
  env:
    - IMA_API_KEY
  primaryCredential: IMA_API_KEY
  credentialNote: >
    IMA_API_KEY is sent to api.imastudio.com for generation APIs and to
    imapi.liveme.com only when image_to_image uses local file upload.
persistence:
  readWrite:
    - ~/.openclaw/memory/ima_prefs.json
    - ~/.openclaw/logs/ima_skills/
  retention: Logs are auto-cleaned after 7 days; preferences remain until user deletes them.
---

# IMA Nano Banana Image Generator

## Scope

This skill is for IMA Open API image generation with strict Nano Banana scope:

- Task types: `text_to_image`, `image_to_image`
- Allowed model IDs only:
  - `gemini-3.1-flash-image`
  - `gemini-3-pro-image`
- Always execute through bundled script: `scripts/ima_image_create.py`

Out of scope:

- Video or non-image tasks
- Non-IMA providers
- Non-Nano-Banana model families (for example SeeDream, Midjourney)
- Handcrafted API requests (do not bypass script)

## Quick Runbook (Authoritative)

If any later section conflicts with this runbook, follow this runbook.

1. Confirm request is in scope (IMA + Nano Banana image generation/editing).
2. Resolve `task_type`:
   - No reference image -> `text_to_image`
   - With reference image/edit request -> `image_to_image`
3. Resolve model:
   - Premium/best quality -> `gemini-3-pro-image`
   - Cheapest/budget -> `gemini-3.1-flash-image` + `--size 512`
   - Otherwise -> `gemini-3.1-flash-image`
4. Resolve parameters:
   - Size -> `--size` (`512`,`1K`,`2K`,`4K`)
   - Ratio -> `--extra-params` JSON (for example `{"aspect_ratio":"16:9"}`)
5. If user asks `8K`, explain unsupported and downgrade to `4K`.
6. For `image_to_image`, require at least one input image.
7. For remote image URLs:
   - Prefer `https://`
   - If user gives `http://`, ask for `https://` URL or local file
8. Endpoint policy is fixed:
    - Main API: `https://api.imastudio.com`
    - Upload API: `https://imapi.liveme.com`
    - No CLI/env override for these domains in this skill.
9. Run only `scripts/ima_image_create.py`; do not call API endpoints manually.
10. Use messaging Step 0-4 flow. If `message` tool is unavailable, use normal replies with same content.
11. On success, prefer rendered media output; if media unsupported, return URL + model + elapsed/credit summary.

## FAQ (For Ambiguous Inputs)

### Q1) How to map intent to `task_type`?

| Situation | `task_type` |
|---|---|
| Prompt-only generation | `text_to_image` |
| Edit/transform from URL/local image | `image_to_image` |

### Q2) How to map user wording to model?

| User wording | model_id | Extra rule |
|---|---|---|
| 默认 / 平衡 / Banana2 / NB2 | `gemini-3.1-flash-image` | none |
| 最便宜 / budget / cheap | `gemini-3.1-flash-image` | force `--size 512` |
| 最好 / 高质量 / Pro / premium | `gemini-3-pro-image` | none |

### Q3) How to set ratio and size?

| Target | Setting |
|---|---|
| Size (`512`,`1K`,`2K`,`4K`) | `--size` |
| Aspect ratio (`1:1`,`16:9`,`9:16`,`4:3`,`3:4`) | `--extra-params '{"aspect_ratio":"16:9"}'` |

`8K` is not supported; downgrade to `4K`.

### Q4) What placeholder substitutions are required?

- `{baseDir}` -> current skill root path
- `{user_id}` -> real user/session id string

## User-Facing Messaging Protocol

### Step 0: Acknowledge immediately

Use a short warm reply in user language, for example:

- `收到，马上开始生成。`
- `OK, generating now.`

### Step 1: Start notification

```text
🎨 开始生成图片，请稍候…
• 模型：[Model Name]
• 预计耗时：[X~Y 秒]
• 消耗积分：[N pts]
```

### Step 2: Progress notification

| Model | Typical Duration | Poll Interval | Push Interval |
|---|---:|---:|---:|
| `gemini-3.1-flash-image` | 20–40s | 5s | 15s |
| `gemini-3-pro-image` | 60–120s | 5s | 30s |

Progress format:

```text
⏳ 正在生成中… [P]%
已等待 [elapsed]s，预计最长 [max]s
```

`P = min(95, floor(elapsed / max * 100))` until success.

### Step 3: Success notification

```text
✅ 图片生成成功！
• 模型：[Model Name]
• 耗时：预计 [X~Y]s，实际 [actual]s
• 消耗积分：[N pts]
🔗 原始链接：{image_url}
```

Prefer media attachment; fallback to plain text message if media is not supported.

### Step 4: Failure notification

```text
❌ 图片生成失败
• 原因：[natural language reason]
• 建议：[retry strategy or model switch]
需要我帮你重试吗？
```

After Step 4, stop. Do not send duplicate completion messages.

## Command Templates (Minimal)

```bash
# 1) List models
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key "$IMA_API_KEY" \
  --task-type text_to_image \
  --list-models

# 2) text_to_image (default/premium/budget/ratio via params)
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key "$IMA_API_KEY" \
  --task-type text_to_image \
  --model-id gemini-3.1-flash-image \
  --prompt "a cute puppy on grass" \
  --size 1K \
  --extra-params '{"aspect_ratio":"1:1"}' \
  --user-id {user_id} \
  --output-json
# Notes:
# - Premium: set --model-id gemini-3-pro-image
# - Cheapest: keep flash model and set --size 512

# 3) image_to_image with remote URL input
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key "$IMA_API_KEY" \
  --task-type image_to_image \
  --model-id gemini-3.1-flash-image \
  --prompt "turn into oil painting" \
  --input-images "https://example.com/photo.jpg" \
  --user-id {user_id} \
  --output-json

# 4) image_to_image with local file input
python3 {baseDir}/scripts/ima_image_create.py \
  --api-key "$IMA_API_KEY" \
  --task-type image_to_image \
  --model-id gemini-3.1-flash-image \
  --prompt "turn into oil painting" \
  --input-images "./local-photo.jpg" \
  --user-id {user_id} \
  --output-json
```

## Security And Data Handling

### Network domains

| Domain | Usage | Trigger |
|---|---|---|
| `api.imastudio.com` | Product list, create task, poll detail | All generation tasks |
| `imapi.liveme.com` | Upload token + file upload | `image_to_image` with local files |

**Why two domains?**
- `api.imastudio.com`: IMA's image generation API (handles task orchestration)
- `imapi.liveme.com`: IMA's media storage infrastructure (handles large file uploads)
- Both services are **owned and operated by IMA Studio**

### Credential flow

| Credential | Where Sent | Why |
|---|---|---|
| `IMA_API_KEY` | `api.imastudio.com` | Open API auth (`Authorization: Bearer ...`) |
| `IMA_API_KEY` | `imapi.liveme.com` | Upload-token auth for local image uploads |

Notes:
- Upload signing uses shared built-in credentials (same as ima-image-ai skill).
- No API key is sent to presigned upload hosts during binary upload.
- API domains are fixed in script and not user-overridable.
- Never print or persist raw API keys in chat or repo files.

### Local persistence

| Path | Purpose | Retention |
|---|---|---|
| `~/.openclaw/memory/ima_prefs.json` | Per-user model preference cache | Until removed |
| `~/.openclaw/logs/ima_skills/` | Operational logs | Auto-cleaned after 7 days |

## Error Handling Playbook

| Error pattern | User-facing explanation | Suggested action |
|---|---|---|
| `401` / unauthorized | API key invalid or unauthorized | Regenerate key: https://www.imaclaw.ai/imaclaw/apikey |
| `4008` / insufficient points | Credits are insufficient | Recharge: https://www.imaclaw.ai/imaclaw/subscription |
| `6009` / `6010` / invalid attribute | Parameter-rule mismatch | Retry with defaults or lower complexity |
| timeout | Task took too long | Retry with faster/lower-cost setup |
| network / rate limit | Temporary connectivity/limit issue | Wait and retry |

Fallback messages:

- Chinese: `图片生成遇到问题，请稍后重试或换个模型试试。`
- English: `Image generation encountered an issue, please retry or switch model.`

## Quick Defaults

1. Default model: `gemini-3.1-flash-image`
2. Premium model: `gemini-3-pro-image`
3. Cheapest profile: flash model + `--size 512`
4. Max output: `4K`
5. Recommended ratios: `1:1`, `16:9`, `9:16`, `4:3`, `3:4`
