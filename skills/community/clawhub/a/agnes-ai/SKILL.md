name: agnes-ai
description: Wraps the Agnes AI API for image and video generation. Use when the user asks to generate images, pictures, photos, or videos with Agnes AI. Two image models: agnes-image-2.0-flash (image-to-image, multi-image) and agnes-image-2.1-flash (high-density text-to-image). OpenAI-compatible protocol. Requires an API key provided on first use.
---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Agnes AI — Image & Video Generation

## Overview

Agnes AI provides image and video generation models accessible through an OpenAI-compatible HTTP API.
Use this skill whenever the user wants to generate images or videos with Agnes AI.

* **API Base URL**: `https://apihub.agnes-ai.com/v1`
* **Auth**: Bearer token (`AGNES_API_KEY`)
* **Protocol**: OpenAI-compatible request/response format

## Model Selection

| User Intent                                                      | Model                     | Endpoint                        |
| ---------------------------------------------------------------- | ------------------------- | ------------------------------- |
| Generate images from text (high info density preferred)            | `agnes-image-2.1-flash`  | `POST /v1/images/generations`  |
| Edit/existing image, image-to-image, multi-image composition      | `agnes-image-2.0-flash`  | `POST /v1/images/generations`  |
| Generate videos, clips, animations                               | `agnes-video-v2.0`      | `POST /v1/video/generations`   |

**Model choice guidance:**
- Default to `agnes-image-2.1-flash` for text-to-image (better high-information-density output)
- Use `agnes-image-2.0-flash` when the user provides an input image for editing, style transfer, or multi-image composition
- If unsure, ask the user which model they prefer, or default to `agnes-image-2.1-flash` for text-to-image

## API Key Setup

**IMPORTANT**: Before any image or video generation, you MUST check for the API key.
Do NOT proceed to call the API without a valid key. This check happens the first time
the user asks you to generate something with Agnes (not during skill installation).

### Checking for the Key

When the skill is triggered (user asks to generate an image/video), check these locations in order:

1. Environment variable `AGNES_API_KEY`
2. File `~/.agnes-ai/api_key`

### If No Key Found

**Immediately stop** and ask the user:

> 要使用 Agnes AI 生成功能，需要先配置 API Key。请提供你的 Agnes AI API Key，我会安全存储在本地。
> （获取方式：登录 https://apihub.agnes-ai.com 后在控制台查看）

Do NOT attempt to call the API without a key.

### Saving the Key

Save the key the user provides by writing it to `~/.agnes-ai/api_key` (plain text, no trailing newline).
Then set the environment variable for the current session:

```bash
mkdir -p ~/.agnes-ai
echo -n "sk-your-key-here" > ~/.agnes-ai/api_key
export AGNES_API_KEY="sk-your-key-here"
```

After saving, proceed with the generation request.

Never echo or log the API key value in any user-visible output.

## Image Generation

Trigger: user asks to generate / create / make an image, picture, photo, illustration, poster, or visual with Agnes.

### Model Selection Logic

1. If the user provides an input image (image-to-image, editing, style transfer) → use `agnes-image-2.0-flash`
2. If the user wants multi-image composition → use `agnes-image-2.0-flash`
3. Default (text-to-image) → use `agnes-image-2.1-flash`

### Call the API

Use the bundled script (`scripts/generate.py` in the same directory as this SKILL.md) for reliable execution.
The script requires Python3 (standard library only, no dependencies):

```bash
# Text-to-image (agnes-image-2.1-flash, default)
python3 scripts/generate.py image \
  --prompt "<prompt>" \
  --size "<size>" \
  --output "<output_path>"

# Image-to-image (agnes-image-2.0-flash)
python3 scripts/generate.py image \
  --prompt "<prompt>" \
  --image "<input_image_url_or_path>" \
  --size "<size>" \
  --output "<output_path>"

# Multi-image composition (agnes-image-2.0-flash)
python3 scripts/generate.py image \
  --prompt "<prompt>" \
  --image "url1" "url2" \
  --size "<size>" \
  --output "<output_path>"
```

Or call the API directly with curl:

```bash
# Text-to-image (agnes-image-2.1-flash)
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.1-flash",
    "prompt": "<prompt>",
    "size": "<size>"
  }'

# Image-to-image (agnes-image-2.0-flash)
curl -s -X POST "https://apihub.agnes-ai.com/v1/images/generations" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-image-2.0-flash",
    "tags": ["img2img"],
    "prompt": "<prompt>",
    "size": "<size>",
    "extra_body": {
      "image": ["<input_image_url>"],
      "response_format": "url"
    }
  }'
```

### Parameters

| Parameter         | Description                                                              | Default       |
| ----------------- | ------------------------------------------------------------------------ | ------------- |
| `prompt`          | Text description of the desired image (required)                         | —             |
| `size`            | Image dimensions. Supported: `1024x1024`, `1792x1024`, `1024x1792`  | `1024x1024`  |
| `n`               | Number of images to generate                                             | `1`           |
| `extra_body.image`| Input image URL(s) for image-to-image or multi-image tasks              | —             |
| `tags`            | Task type tag, e.g. `["img2img"]` for image-to-image                  | —             |

### Recommended Prompt Structure

```
[Subject] + [Scene / Environment] + [Style] + [Lighting] + [Composition] + [Quality Requirements]
```

Example:
```
A luminous floating city above a misty canyon at sunrise, cinematic realism, wide-angle composition, rich architectural details, soft golden light, high visual density
```

For image-to-image, also describe what to change AND what to preserve:
```
Transform the scene into a rain-soaked cyberpunk night with neon reflections while preserving the original composition and main subject layout.
```

### Response Handling

The API returns an OpenAI-compatible response:

```json
{
  "data": [
    {
      "url": "https://..."
    }
  ],
  "usage": {
    "generated_images": 1
  }
}
```

The `url` field contains a temporary download link. Download the image with `curl` or `wget` and save locally.
If `b64_json` is present, decode it with `base64 -d` to get the raw image bytes.

After saving the image file locally, deliver it to the user — display a preview if your platform supports it,
or attach the file to your response. Tell the user where the file was saved.

## Video Generation

Trigger: user asks to generate / create / make a video, clip, animation, or motion content with Agnes.

### Call the API

Use the bundled script (`scripts/generate.py` in the same directory as this SKILL.md`):

```bash
python3 scripts/generate.py video \
  --prompt "<prompt>" \
  --duration <seconds> \
  --output "<output_path>"
```

Or call the API directly with curl:

```bash
curl -s -X POST "https://apihub.agnes-ai.com/v1/video/generations" \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-video-v2.0",
    "prompt": "<prompt>",
    "duration": <seconds>
  }'
```

### Parameters

| Parameter  | Description                                      | Default |
| ---------- | ------------------------------------------------ | ------- |
| `prompt`   | Text description of the desired video (required) | —       |
| `duration` | Video duration in seconds                        | `5`     |

### Response Handling

Video generation is asynchronous. The API returns a task ID:

```json
{
  "id": "task_abc123",
  "status": "processing"
}
```

Poll for completion:

```bash
curl -s "https://apihub.agnes-ai.com/v1/video/generations/<task_id>" \
  -H "Authorization: Bearer $AGNES_API_KEY"
```

When `status` becomes `completed`, the response contains a `url` or `output` field with the video download link.
Download it and deliver to the user.

The bundled `scripts/generate.py` script handles polling automatically — prefer using it over raw curl.

## Supported Image Sizes

* `1024x1024` — square (default)
* `1792x1024` — landscape
* `1024x1792` — portrait

## Error Handling

If the API returns a non-200 status:

1. Check that the API key is valid and has not expired
2. Verify the prompt is not empty and does not violate content policy
3. If the error persists, tell the user the error message and suggest checking their Agnes AI dashboard

## After Generation

After successfully generating and saving an image or video file:

1. Tell the user the file path and deliver/attach the file to them
2. For images: show a preview or display the file if your platform supports inline rendering
3. For videos: provide a way for the user to view or download the file
