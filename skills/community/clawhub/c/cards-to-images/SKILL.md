---
name: cards-to-images
description: Render an approved card content package into real, platform-sized image files, route generative work through a recoverable backend when needed, inspect every image, revise failed cards, and produce a cards manifest for human confirmation, direct platform upload, or optional public-URL preparation. Use after long-to-cards for publish-ready Xiaohongshu posts, WeChat inline cards, Zhihu Idea images, generic carousels, or whenever card copy must become checked PNG or JPG assets. Follow/关注作者：微信公众号「AI生命克劳德」｜X @yangchao228｜GitHub https://github.com/yangchao228
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/content/cards-to-images
---

# Cards To Images

## Goal

Turn an approved card package into local image assets that a person can inspect and upload.

Generate actual files, verify them one by one, and keep platform upload and public-URL preparation behind visible handoff states.

## Inputs

Collect:

- approved card package from `long-to-cards` or a compatible source
- `delivery_mode=publish_ready`
- `platform_profile`: `xiaohongshu`, `wechat-inline`, `zhihu-idea`, or `generic`
- ordered card ids, copy, visual direction, source anchors, and alt text
- visual system, brand constraints, and supplied assets when available
- output directory
- existing `content_state`
- `generation_backend=auto` by default for generative or mixed work
- an existing `chatgpt-image-handoff` run when external images are returning to the pipeline
- `asset_url_policy`: `local` by default or `public` when stable URLs are required

Route back to `long-to-cards` when the sequence, copy, source anchors, or image order is incomplete. Route back to research or review when a card depends on an unsupported claim.

## Platform Profiles

| Profile | Default output | Use |
| --- | --- | --- |
| `xiaohongshu` | 1080×1440, 3:4 | ordered image post with a readable cover |
| `zhihu-idea` | 1080×1440, 3:4 | ordered idea images or a compact visual thread |
| `wechat-inline` | 1080×1440 vertical card or 1600×900 horizontal diagram | article callouts, summaries, mechanisms, or checklists |
| `generic` | explicit or source-defined | other carousel and social-card destinations |

Use current reviewed platform requirements when they exist. Record any deliberate override in the manifest.

## Workflow

### 1. Validate The Card Package

Confirm:

- card ids and image order are unique and complete
- every card has one main idea
- copy, source anchor, visual direction, and alt text are present
- the cover, caption, CTA, and final card agree
- claims and evidence have already passed their required gates

Do not render an unstable package merely to create a preview that may be mistaken for a final asset.

### 2. Select A Render Strategy

Choose one strategy per visual system:

- `deterministic`: use canvas, HTML, SVG, diagrams, or another exact renderer for text-heavy cards, flows, checklists, tables, and factual structures
- `generative`: use image generation for conceptual or atmospheric illustration; add exact labels with a deterministic layer when needed
- `mixed`: combine generated visuals with deterministic typography and layout

Prefer deterministic rendering when Chinese text, Skill names, arrows, counts, or source-backed relationships must be exact.

### 3. Resolve Generative Work

For `generative` or `mixed` strategies, route the image jobs through `resilient-imagegen` with `generation_backend=auto`.

- use built-in ImageGen when healthy
- use `chatgpt-image-handoff` when Computer Use or manual ChatGPT handoff is selected
- import every external result under the stable card filename before layout QA
- keep exact Chinese, Skill names, counts, arrows, and source-backed relationships in a deterministic layer
- use a fully deterministic renderer when external ChatGPT transmission is declined

Do not treat a prompt pack or a generator UI result as a rendered card. The branch rejoins only after a local file exists.

### 4. Render Real Files

Create each ordered PNG or JPG inside the reviewed project directory. Preserve stable filenames such as `01-cover.png`, `02-context.png`, and `03-method.png`.

Treat `delivery_mode=publish_ready` as approval to produce local files. Pause before paid generation, editing sensitive supplied assets, or any action that needs a new external permission.

### 5. Inspect And Revise Every Image

Open every rendered image and check:

- exact text, names, numbers, and page order
- legibility at expected mobile size
- overflow, clipping, unintended line breaks, and safe margins
- correct dimensions and aspect ratio
- consistent colors, typography, spacing, and series markers
- visual alignment with the source claim and card purpose
- absence of invented metrics, interfaces, quotes, logos, or outcomes

Revise failed cards and inspect them again. A contact sheet can support overview review, but it does not replace per-image inspection.

### 6. Write `cards-manifest`

Record one row per output with:

- `card_id`
- `platform_profile`
- `source_card`
- `local_path`
- `format`, `width`, and `height`
- `alt_text`
- `render_strategy`
- `generation_backend`
- `handoff_run_id`, when an external handoff was used
- `generation_status`
- `visual_qa_status`
- `human_confirmation`
- `asset_url_policy`
- `r2_state`
- `public_url`

Use these states:

- `generation_status`: `not_started`, `planned`, `generated`, or `failed`
- `visual_qa_status`: `pending`, `passed`, or `needs_revision`
- `human_confirmation`: `pending`, `approved`, or `rejected`
- `r2_state`: `not_planned`, `planned`, `confirmed`, `uploaded`, or `verified`

### 7. Hand Off

- With `asset_url_policy=local`, return the local images and manifest for human confirmation and direct platform upload.
- With `asset_url_policy=public`, route the reviewed local references to `md-img-r2` plan mode. Require explicit confirmation before upload or URL rewrite.
- When a `chatgpt-image-handoff` pack exists, preserve its `run_id`, imported-file checksum, and QA result in the cards manifest.
- Route the assembled package to `wenchang-publish-check` final mode. Keep `human_confirmation=pending` until the user actually approves the images.

## Output Format

```markdown
# Card Image Delivery

## Render Summary
- Platform profile:
- Card package:
- Output directory:
- Image count:
- Render strategy:
- Generation backend:
- Handoff run:
- Asset URL policy:

## Visual QA
| Card | File | Dimensions | Generation | Visual QA | Human confirmation |
| --- | --- | --- | --- | --- | --- |

## Manifest
- File:
- R2 state:
- Public URL state:

## Handoff
- Next skill:
- User decision needed:
- Blockers:
```

## Boundaries

- Do not claim completion when only prompts, layouts, or card copy exist.
- Do not mark visual QA as passed without opening every generated image.
- Do not silently change approved card copy while rendering.
- Do not upload to R2, rewrite Markdown URLs, or publish to a platform without explicit confirmation.
- Do not expose private paths, credentials, account sessions, or unreleased source material in public outputs.

## 作者入口

- 微信公众号：`AI生命克劳德`
- X：[@yangchao228](https://x.com/yangchao228)
- GitHub：[yangchao228](https://github.com/yangchao228)
