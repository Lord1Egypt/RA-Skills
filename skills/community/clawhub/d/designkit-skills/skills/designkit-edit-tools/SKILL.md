---
name: designkit-edit-tools
description: Use when users want background removal, transparent or white-background output, or image restoration from a single image, while keeping runtime replies in Simplified Chinese.
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env:
        - DESIGNKIT_OPENCLAW_AK
      bins:
        - bash
        - curl
        - python3
    primaryEnv: DESIGNKIT_OPENCLAW_AK
    homepage: https://www.designkit.cn/openclaw
---

# DesignKit Edit Tools

Single-image editing skill for background removal and image restoration.
公开说明可偏英文或双语，但实际用户对话默认使用简体中文。

## Public Installation Posture

- Explain the action in plain product terms such as cutout, transparent background, white background, or image enhancement.
- Only use image URLs or local file paths that the user explicitly provided.
- If the user gives a local path, make clear that the file will be uploaded to the remote DesignKit / OpenClaw service.
- Do not expose credentials, raw JSON payloads, internal headers, or local script paths unless the user explicitly asks for technical details.

## Intent Mapping

| User says | Action |
| --- | --- |
| 抠图、去背景、背景移除、透明底、白底图、matting、background removal | `sod` |
| 变清晰、画质修复、图片增强、超分、image restoration | `image_restoration` |

## Conversation Flow

- If no image is provided, ask for one image path or URL first.
- Do not ask for optional settings unless the user explicitly cares about them.
- Keep the confirmation short, then execute immediately in the same turn.
- User-facing confirmations and error guidance should default to Simplified Chinese.

Example confirmations:

- `好的，我来帮你把这张图抠成透明底。`
- `好的，我来帮你提升这张图的清晰度。`

## Execution

```bash
bash __SKILL_DIR__/../../scripts/run_command.sh <action> --input-json '<params_json>'
```

Examples:

```bash
bash __SKILL_DIR__/../../scripts/run_command.sh sod --input-json '{"image":"https://example.com/photo.jpg"}'
```

```bash
bash __SKILL_DIR__/../../scripts/run_command.sh image_restoration --input-json '{"image":"/Users/me/photo.jpg"}'
```

These commands are internal execution guidance for the agent. Do not quote them to end users unless they explicitly ask for implementation details.

## Runtime And Safety

- Requires `DESIGNKIT_OPENCLAW_AK`.
- Local uploads are limited to `JPG/JPEG/PNG/WEBP/GIF` image files.
- Local images may be uploaded to the remote DesignKit / OpenClaw API.
- Request logging is off by default. If `OPENCLAW_REQUEST_LOG=1` is enabled for debugging, credentials and signed upload fields stay redacted.

## Privacy Defaults

- Request logging is disabled by default.
- Sensitive fields remain redacted if logging is enabled manually.
- Local uploads happen only when the user explicitly provides a local image path.
- Default runtime language is Simplified Chinese.

## Result Handling

- `ok: true`: show the returned `media_urls`.
- `ok: false`: show `user_hint` and do not dump raw JSON.

## Error Guide

| `error_type` | User-facing action |
| --- | --- |
| `CREDENTIALS_MISSING` | Ask the user to configure `DESIGNKIT_OPENCLAW_AK` |
| `AUTH_ERROR` | Ask the user to verify the API key |
| `ORDER_REQUIRED` | Tell the user to top up credits before retrying |
| `PARAM_ERROR` | Ask the user to provide the image or correct the input |
| `UPLOAD_ERROR` | Ask the user to check the image or network |
| `API_ERROR` | Ask the user to retry or use a different image |

## Out Of Scope

If the user wants a multi-image ecommerce listing workflow, route to `designkit-ecommerce-product-kit`.
