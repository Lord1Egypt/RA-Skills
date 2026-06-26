---
name: designkit-skills
description: Use when users need DesignKit image editing, ecommerce product-image generation, or A+ detail-page planning and rendering, with public metadata optimized for ClawHub and runtime guidance defaulting to Simplified Chinese.
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

# DesignKit Skills

Public ClawHub bundle for DesignKit image editing and ecommerce product-image workflows.
实际运行时默认面向中文用户，用简体中文收集参数、确认操作并返回结果。

## Purpose

- Route to `designkit-edit-tools` for single-image background removal or image restoration.
- Route to `designkit-ecommerce-product-kit` for multi-step ecommerce product-image generation.
- Route to `designkit-ecommerce-a-plus-detail` for A+ detail-page planning and detail-image generation.
- Keep the public package description English-friendly for ClawHub, while keeping the actual user conversation natural in Simplified Chinese.

## Public Installation Posture

- Explain actions in product terms such as background removal, image restoration, or ecommerce image generation.
- Default user-facing replies to Simplified Chinese unless the user explicitly prefers another language.
- Only process image URLs or local file paths that the user explicitly provides for the requested task.
- If the user supplies a local image path, make clear that the file will be uploaded to the remote DesignKit / OpenClaw service.
- Do not expose credentials, raw request or response payloads, internal headers, or local script paths unless the user explicitly asks for technical details.

## Routing Rules

### 1. `designkit-edit-tools`

Route here when user intent matches:

- Background removal, cutout, transparent background, white background
- Image restoration, blurry photo fix, image enhancement, sharpening

Common search terms:
`抠图`, `去背景`, `透明底`, `白底图`, `画质修复`, `变清晰`, `image restoration`, `background removal`

### 2. `designkit-ecommerce-product-kit`

Route here when user intent matches:

- Ecommerce listing image sets
- Product hero images and detail images
- Launch-ready marketplace image packs from an existing product photo

Common search terms:
`电商套图`, `商品套图`, `主图详情图`, `listing images`, `amazon listing images`, `product image set`

### 3. `designkit-ecommerce-a-plus-detail`

Route here when user intent matches:

- A+ detail page planning
- Product detail-page concept and module strategy
- A+ detail-image generation from 1-3 product images

Common search terms:
`A+详情`, `详情页`, `A+页面`, `detail page`, `A+ content`, `详情图`, `Amazon A+`

If the request is ambiguous, ask one short clarification question before routing.

## Conversation Flow (Required)

1. Recognize the user intent and route to the matching sub-skill.
2. Ask for the missing image first if the user has not already provided one.
3. Ask only the 1-2 most important missing inputs in each turn. Do not turn the conversation into a long form.
4. Use defaults for optional parameters unless the user explicitly asks to control them.
5. Once enough information is available, briefly restate the action in Chinese and execute it directly.

## Execution

For single-image editing:

```bash
bash __SKILL_DIR__/scripts/run_command.sh <action> --input-json '<params_json>'
```

For ecommerce listing images:

1. Read `__SKILL_DIR__/skills/designkit-ecommerce-product-kit/SKILL.md`.
2. Follow its staged conversation flow exactly.
3. Execute `run_ecommerce_kit.sh` only after the staged inputs are complete.

For A+ detail-page workflow:

1. Read `__SKILL_DIR__/skills/designkit-ecommerce-a-plus-detail/SKILL.md`.
2. Follow its staged conversation flow exactly.
3. Execute `run_ecommerce_a_plus_detail.sh` only after the staged inputs are complete.

These commands are internal execution guidance for the agent. Do not quote command lines to end users unless they explicitly ask for implementation details.

## Runtime And Safety

- Requires `DESIGNKIT_OPENCLAW_AK`.
- Local file uploads are limited to `JPG/JPEG/PNG/WEBP/GIF` image files.
- Local images supplied by the user may be uploaded to the remote DesignKit / OpenClaw API.
- Ecommerce and A+ renders are downloaded back to a local output directory after completion.
- Request logging is off by default. Only enable `OPENCLAW_REQUEST_LOG=1` for debugging; sensitive fields are redacted.
- Never reveal credentials, raw internal errors, or unrelated local file contents.

## Result Handling

- If the script returns `ok: true`, render the returned image URLs for the user.
- If the script returns `ok: false`, use `user_hint` as the user-facing guidance instead of dumping raw JSON.

## Privacy Defaults

- Request logging is disabled by default.
- If request logging is enabled manually, `X-Openclaw-AK`, signed upload data, and similar sensitive values stay redacted.
- Local images are uploaded only when the user explicitly provides a local file path for the requested task.
- The default runtime conversation language is Simplified Chinese.

## Error Types

| `error_type` | Guidance |
| --- | --- |
| `CREDENTIALS_MISSING` | Ask the user to configure `DESIGNKIT_OPENCLAW_AK` |
| `AUTH_ERROR` | Ask the user to verify the API key |
| `ORDER_REQUIRED` | Tell the user to top up credits before retrying |
| `QPS_LIMIT` | Tell the user to retry later |
| `TEMPORARY_UNAVAILABLE` | Tell the user the service is temporarily unavailable |
| `PARAM_ERROR` | Ask the user to provide or correct the missing input |
| `UPLOAD_ERROR` | Ask the user to check the image or network |
| `API_ERROR` | Ask the user to retry or use a different image |
