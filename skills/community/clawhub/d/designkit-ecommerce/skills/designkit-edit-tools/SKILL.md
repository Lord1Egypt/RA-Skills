---
name: designkit-edit-tools
description: >-
  Use when users ask to remove backgrounds, output transparent/white background
  images, or restore blurry photos. Trigger on requests like background removal,
  transparent/white background output, and image restoration.
version: "1.0.2"
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
    homepage: https://www.designkit.com/openClaw
---

# Designkit Edit Tools

## Overview

General-purpose image editing capabilities in the Designkit atomic layer.
Each capability has clear inputs/outputs, can run independently, and can be reused
by upper-layer workflows.

## Capabilities

| Capability | Action | Status | Description |
|------|---------|------|------|
| Background removal | `sod` | ✅ Active | Extract the main subject from the background |
| Image restoration | `image_restoration` | ✅ Active | Improve sharpness and clarity |

## Intent Mapping

| User request examples | Route to |
|----------|--------|
| remove background, transparent background, cutout, matting, background removal | `sod` |
| restore blurry image, image enhancement, sharpen image, super resolution, image restoration | `image_restoration` |

## Follow-up Strategy

### Background Removal (`sod`)

| Missing info | Ask? | Suggested prompt |
|---------|---------|---------|
| No image provided | Required | "Please share the image for background removal (local path or URL)." |
| Background color not specified | No | Use system default |
| Size/aspect not specified | No | Return with original image dimensions |

Typical example:
> User: "Please remove the background from this image."
> Agent: "Please share the image for background removal (local path or URL)."
> User: [provides image]
> Agent: "Great, I will extract the subject from this image now." -> Execute

### Image Restoration (`image_restoration`)

| Missing info | Ask? | Suggested prompt |
|---------|---------|---------|
| No image provided | Required | "Please share the image you want to enhance (local path or URL)." |
| Clarity level not specified | No | Use default high-quality enhancement |

Typical example:
> User: "This image is too blurry, please enhance it."
> Agent: (image already provided) "Great, I will improve this image's clarity now." -> Execute

## Execution

After required parameters are ready, call the unified runner:

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

Replace `__SKILL_DIR__` with the absolute directory path of this SKILL.md.
The script automatically uploads local image files.

## Result Handling

Parse the script JSON output:
- `ok: true` -> extract URLs from `media_urls` and show as `![Result](url)`
- `ok: false` -> read `error_type` and `user_hint`, then provide actionable guidance

| `error_type` | User-facing guidance |
|-------------|------------|
| `CREDENTIALS_MISSING` | Guide setup using `user_hint` |
| `AUTH_ERROR` | Guide AK check using `user_hint` |
| `ORDER_REQUIRED` | Ask user to get credits at https://www.designkit.com/ |
| `PARAM_ERROR` | Ask user to complete/fix parameters using `user_hint` |
| `UPLOAD_ERROR` | Check network or try another image |
| `API_ERROR` | Try another image |

## Boundaries

This skill only handles atomic image editing operations.
Route the following to another skill:

| Not handled here | Route to |
|------|------|
| Multi-step ecommerce listing set generation | `designkit-ecommerce-product-kit` |
