---
name: designkit-ecommerce-product-kit
description: Use when users want ecommerce listing images, product hero/detail images, or a multi-step product-image workflow from an existing product photo, with runtime guidance defaulting to Simplified Chinese.
version: "1.8.0"
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

# DesignKit Ecommerce Product Kit

Multi-step ecommerce image workflow for product hero images and detail images.
公开元数据可偏英文或双语，但分步提问、确认和结果说明默认使用简体中文。

## Public Installation Posture

- Explain the workflow in product terms such as listing image set, hero image, detail image, or marketplace pack.
- Only process product image URLs or local file paths that the user explicitly provides.
- If a local product image path is provided, make clear that the file will be uploaded to the remote DesignKit / OpenClaw service.
- Do not expose credentials, raw request or response payloads, internal headers, or local script paths unless the user explicitly asks for technical details.

## Required Flow

### 1. Product Image

If the user has not provided a product image, ask for one URL or local image path first.

### 2. Selling Points And Style Preference

After receiving the product image:

- ask only for selling points and style preference
- do not ask for platform, country, language, or ratio in the same reply
- if useful, offer a suggested selling-point summary the user can accept or edit
- ask this step in Simplified Chinese

### 3. Listing Configuration

Only after the user responds to step 2, ask for:

- platform
- market / country
- language
- aspect ratio

Default values if the user skips this step:

- platform: `amazon`
- market: `US`
- language: `English`
- aspect ratio: `1:1`

If the user already provided config together with the selling-point reply, accept it and skip this extra question.
Ask this configuration step in Simplified Chinese as well.

### 4. Style Selection Is Optional

Only enter the style-selection flow when the user clearly asks for a specific style direction or wants to review style options.

- if the user says `没有`, `随便`, `自动`, or gives no style direction, skip style selection
- do not invent styles yourself
- if style options are shown, the final chosen `brand_style` must come directly from the API response

### 5. Render And Download

After the staged inputs are complete:

1. submit the render task
2. poll until complete
3. download the generated images locally
4. show the result images and tell the user where they were saved

If the user points to a specific generated image and asks for regeneration, call `render_regen` with `transfer_id` and `task_id`, then continue with `render_poll`.

## API Value Mapping

| User-facing choice | API value |
| --- | --- |
| 亚马逊 | `amazon` |
| 淘宝 | `taobao` |
| Temu | `temu` |
| 拼多多 | `pinduoduo` |
| TikTok Shop | `tiktok_shop` |
| 美国 | `US` |
| 中国 | `CN` |
| 俄罗斯 | `RU` |
| 日本 | `JP` |
| 西班牙 | `ES` |
| 英语 | `English` |
| 中文 | `Chinese` |
| 俄语 | `Russian` |
| 日语 | `Japanese` |
| 西班牙语 | `Spanish` |

## Commands

```bash
bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh style_create --input-json '<json>'
bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh style_poll --input-json '<json>'
bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh render_submit --input-json '<json>'
bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh render_regen --input-json '<json>'
bash __SKILL_DIR__/scripts/run_ecommerce_kit.sh render_poll --input-json '<json>'
```

These commands are internal execution guidance for the agent. Do not quote them to end users unless they explicitly ask for implementation details.

## Output Directory

`render_poll` downloads generated images using this priority:

1. `output_dir` from `input-json`
2. `DESIGNKIT_OUTPUT_DIR`
3. `./output/` when the current working directory contains `openclaw.yaml`
4. `{OPENCLAW_HOME}/workspace/visual/output/designkit-ecommerce-product-kit/`
5. `~/.openclaw/workspace/visual/output/designkit-ecommerce-product-kit/`
6. `~/Downloads/`

The output directory must not point inside the skill repository.

## Runtime And Safety

- Requires `DESIGNKIT_OPENCLAW_AK`.
- Local uploads are limited to `JPG/JPEG/PNG/WEBP/GIF` image files.
- Local product images may be uploaded to the remote DesignKit / OpenClaw API.
- Generated images are downloaded back to the local output directory.
- Request logging is off by default. If `OPENCLAW_REQUEST_LOG=1` is enabled for debugging, credentials and signed upload fields stay redacted.

## Privacy Defaults

- Request logging is disabled by default.
- Sensitive headers and signed upload data stay redacted if logging is enabled manually.
- Local images are uploaded only when the user explicitly provides a local path for the requested task.
- Default runtime language is Simplified Chinese.

## Result Handling

- show progress updates while polling if progress data is available
- on success, render the result images and report the save path
- on failure, show `user_hint` instead of raw JSON
