# designkit-skills

Public DesignKit skill bundle for OpenClaw / ClawHub.
面向中文用户的 DesignKit 技能包，支持抠图、画质修复、电商商品套图和 A+ 详情页。

It covers four common image-production tasks:

- background removal for transparent or white-background outputs
- image restoration for blurry or low-quality photos
- ecommerce listing-image generation from an existing product photo
- A+ detail-page planning and detail-image generation from 1-3 product images

## Public Package Positioning / 对外发布定位

- Public metadata and marketplace copy are written in English or bilingual form so ClawHub can index, review, and display the package more reliably.
- Actual user-facing prompts, confirmations, and result guidance should default to Simplified Chinese unless the user explicitly prefers another language.
- This package is intended for Chinese-language ecommerce and image-editing workflows, but keeps a ClawHub-friendly public surface.

## What It Does / 功能概览

- removing backgrounds from product photos
- generating transparent PNG / clean cutout-style assets
- sharpening blurry images before reuse
- creating hero images and detail images for ecommerce listings
- planning A+ detail modules and rendering detail-page image sets

## Included Skills

- `designkit-skills`: root router for the public bundle
- `designkit-edit-tools`: single-image background removal and restoration
- `designkit-ecommerce-product-kit`: multi-step ecommerce listing-image workflow
- `designkit-ecommerce-a-plus-detail`: two-step A+ detail workflow (planning -> rendering)

## Install

Inspect first:

```bash
clawhub inspect designkit-skills
```

Install from ClawHub:

```bash
clawhub install designkit-skills
```

Install directly from GitHub:

```bash
npx -y skills add https://github.com/meitu/designkit-skills
```

## Required Environment

Get an API key from [DesignKit OpenClaw](https://www.designkit.cn/openclaw), then set:

```bash
export DESIGNKIT_OPENCLAW_AK="AK"
```

## Runtime Language / 交互语言

- Default user-facing language: Simplified Chinese
- Switch to English only when the user explicitly asks or clearly uses English throughout the conversation
- Keep public metadata English-friendly, but keep runtime guidance natural for Chinese users

## Runtime Behavior / 运行行为

- local image paths may be uploaded to the remote DesignKit / OpenClaw API for processing
- ecommerce renders are downloaded back to a local output directory after completion
- A+ detail renders are downloaded back to a local output directory after completion
- request logging is disabled by default
- if `OPENCLAW_REQUEST_LOG=1` is enabled for debugging, credentials and signed upload data stay redacted
- local uploads only accept `JPG/JPEG/PNG/WEBP/GIF` image files

## Public Safety Posture / 安全说明

- Only image URLs or local file paths explicitly provided by the user should be processed.
- Do not browse unrelated local directories or infer local file paths on behalf of the user.
- If a local image path is used, the skill should clearly indicate that the image will be uploaded for remote processing.
- Do not expose credentials, raw request or response payloads, or internal script paths unless the user explicitly asks for technical details.

## Output Directory

Ecommerce renders are downloaded using this priority:

1. `output_dir` from `input-json`
2. `DESIGNKIT_OUTPUT_DIR`
3. `./output/` when the current working directory contains `openclaw.yaml`
4. `{OPENCLAW_HOME}/workspace/visual/output/designkit-ecommerce-product-kit/`
5. `~/.openclaw/workspace/visual/output/designkit-ecommerce-product-kit/`
6. `~/Downloads/`

The workflow creates the directory automatically and refuses to write results inside the skill repository itself.

A+ detail renders follow the same output strategy, with default subdirectory:

- `{OPENCLAW_HOME}/workspace/visual/output/designkit-ecommerce-a-plus-detail/` (or the matching `~/.openclaw/...` fallback)

## Repository Layout

- [`SKILL.md`](./SKILL.md): root router skill
- [`claw.json`](./claw.json): package metadata for ClawHub / OpenClaw
- [`api/commands.json`](./api/commands.json): edit action registry
- [`skills/designkit-edit-tools/SKILL.md`](./skills/designkit-edit-tools/SKILL.md): edit sub-skill
- [`skills/designkit-ecommerce-product-kit/SKILL.md`](./skills/designkit-ecommerce-product-kit/SKILL.md): ecommerce sub-skill
- [`skills/designkit-ecommerce-a-plus-detail/SKILL.md`](./skills/designkit-ecommerce-a-plus-detail/SKILL.md): A+ detail sub-skill
- [`scripts/run_command.sh`](./scripts/run_command.sh): edit executor
- [`scripts/run_ecommerce_kit.sh`](./scripts/run_ecommerce_kit.sh): ecommerce entrypoint
- [`scripts/ecommerce_product_kit.py`](./scripts/ecommerce_product_kit.py): ecommerce workflow logic
- [`scripts/run_ecommerce_a_plus_detail.sh`](./scripts/run_ecommerce_a_plus_detail.sh): A+ detail entrypoint
- [`scripts/ecommerce_a_plus_detail.py`](./scripts/ecommerce_a_plus_detail.py): A+ detail workflow logic

## License

MIT
