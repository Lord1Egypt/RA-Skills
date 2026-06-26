---
name: designkit-ecommerce-a-plus-detail
description: Use when users want A+ detail-page planning and detail-image generation from 1-3 product images, with runtime guidance defaulting to Simplified Chinese.
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

# DesignKit Ecommerce A+ Detail

A+ 详情页双阶段工作流：先生成详情策划方案，再生成详情图。
公开元数据可偏英文或双语，运行时分步提问与结果说明默认使用简体中文。

## User Quick Start (CN)

给终端里的 Agent 直接说下面任意一句即可：

1. 最短说法

`帮我做 A+ 详情页，这是产品图：https://example.com/p1.jpg`

2. 常用完整说法

`帮我做 A+ 详情页。产品图：https://example.com/p1.jpg, https://example.com/p2.jpg；商品卖点与要求：轻量、防水、适合通勤；平台/市场/语言/比例：亚马逊/美国/英文/970:600；模块：首屏主视觉、核心卖点图、使用场景图。`

3. 使用本地图片路径

`帮我做 A+ 详情页，产品图在 /path/to/product.jpg`

说明：使用本地路径时，图片会上传到 DesignKit / OpenClaw 远程服务处理。

## User Input Contract

- 产品图：1-3 张（URL 或本地路径）
- 必填：商品卖点与要求（`product_info`）
- 可选：平台、市场、语言、比例、模块

如果用户不填可选项，默认值：

- `platform`: `amazon`
- `market`: `US`
- `language`: `English`
- `aspect_ratio`: `970:600`
- `selected_modules`: `首屏主视觉,核心卖点图,使用场景图,多角度图,场景氛围图,商品细节图`

## User Interaction Expectation

Agent 与用户对话应保持 3 步即可完成：

1. 先收产品图（1-3 张）
2. 再收商品卖点与要求
3. 最后确认配置（平台/市场/语言/比例/模块），未提供则走默认值

## Public Installation Posture

- Explain this capability in product terms such as A+ detail page, detail-page plan, or detail image set.
- Only process image URLs or local file paths explicitly provided by the user.
- If local image paths are provided, clearly indicate that those images will be uploaded to DesignKit / OpenClaw.
- Do not expose credentials, raw payloads, internal headers, or local script paths unless explicitly requested.

## Required Flow

### 1. Product Images (1-3)

- Ask for product images first when missing.
- Accept either URL(s) or local image path(s).
- The image count must be between 1 and 3.
- If more than 3 images are provided, ask the user to reduce to 3 or fewer before execution.

### 2. Product Selling Points And Requirements

After images are received, ask for `product_info` (商品卖点与要求) before execution.

### 3. Configuration

Then collect or confirm these fields:

- `platform`
- `market`
- `language`
- `aspect_ratio`
- `selected_modules`

Defaults if user skips:

- `platform`: `amazon`
- `market`: `US`
- `language`: `English`
- `aspect_ratio`: `970:600`
- `selected_modules`: `首屏主视觉,核心卖点图,使用场景图,多角度图,场景氛围图,商品细节图`

### 4. Two-Step Execution (Required)

1. Submit and poll detail-page planning.
2. Show the planned modules to the user.
3. Generate detail images only after plan output is available (and user confirmation if needed).

Note:

- `detail_plan_submit` uses `step=3` internally (fixed).

### 5. Regen

If the user requests regeneration of a specific generated image, call regen with `task_id`, then continue poll.

## Commands

```bash
bash __SKILL_DIR__/../../scripts/run_ecommerce_a_plus_detail.sh detail_plan_submit --input-json '<json>'
bash __SKILL_DIR__/../../scripts/run_ecommerce_a_plus_detail.sh detail_plan_poll --input-json '<json>'
bash __SKILL_DIR__/../../scripts/run_ecommerce_a_plus_detail.sh detail_render_submit --input-json '<json>'
bash __SKILL_DIR__/../../scripts/run_ecommerce_a_plus_detail.sh detail_render_regen --input-json '<json>'
bash __SKILL_DIR__/../../scripts/run_ecommerce_a_plus_detail.sh detail_render_poll --input-json '<json>'
```

These command lines are internal execution guidance for the agent. Do not quote them to end users unless they explicitly ask for technical details.

## Runtime And Safety

- Requires `DESIGNKIT_OPENCLAW_AK`.
- API base defaults to `https://openclaw-designkit-api.meitu.com`; override with `DESIGNKIT_WEBAPI_BASE` when needed (for example `https://designkit-webapi.designkit.com`).
- Local uploads are limited to `JPG/JPEG/PNG/WEBP/GIF` image files.
- Local images may be uploaded to the remote DesignKit / OpenClaw API.
- Request logging is off by default. If `OPENCLAW_REQUEST_LOG=1` is enabled, sensitive values remain redacted.

## Output Directory

`detail_render_poll` downloads generated images using this priority:

1. `output_dir` from `input-json`
2. `DESIGNKIT_OUTPUT_DIR`
3. `./output/` when current working directory contains `openclaw.yaml`
4. `{OPENCLAW_HOME}/workspace/visual/output/designkit-ecommerce-a-plus-detail/`
5. `~/.openclaw/workspace/visual/output/designkit-ecommerce-a-plus-detail/`
6. `~/Downloads/`

The output directory must not point inside the skill repository.

## Result Handling

- `detail_plan_poll`: return structured `modules` when parsing succeeds, plus raw message fallback.
- `detail_render_poll`: return `media_urls` and local saved paths after all module images finish.
- Any failure: show `user_hint` instead of dumping raw internals.

## Error Guide

| `error_type` | User-facing action |
| --- | --- |
| `CREDENTIALS_MISSING` | Ask user to configure `DESIGNKIT_OPENCLAW_AK` |
| `PARAM_ERROR` | Ask user to correct missing/invalid input (including image count > 3) |
| `UPLOAD_ERROR` | Ask user to check image format/network and retry |
| `API_ERROR` | Ask user to retry or adjust inputs |
| `TEMPORARY_UNAVAILABLE` | Ask user to retry later or increase wait timeout |
| `DOWNLOAD_ERROR` | Ask user to retry download step |
