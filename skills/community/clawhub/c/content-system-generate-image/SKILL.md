---
name: generate-image
description: Generate article companion images for the content factory pipeline. Use when Codex needs article images, infographic cards, inline visuals, or a PNG exported from an article markdown draft before preview or publishing.
---

# Generate Image

Generate the image asset for an article draft as an independent executor. On ClawHub, this skill is published as `content-system-generate-image`.

## Quick Start

Run the default command:

```bash
.venv/bin/python -m skill_runtime.cli run-skill generate-image --input content-production/drafts/ai-content-system-article.md
```

## Prepare Source Article

Start from an article markdown draft that already has a stable title, structure, and core message. Use the article content to infer the primary visual theme and the most useful image role, such as header art, infographic card, or inline supporting visual.

The default remote image backend is:

```text
provider: openai
api base: https://new.suxi.ai/v1
model: nano-nx
```

This is meant for the 香蕉画图 endpoint, which is treated as an OpenAI-compatible image API.

## Follow Generation Workflow

1. Read the article draft and extract the topic, tone, and the strongest visualizable idea.
2. Generate the preferred image through the shared runtime in `skills/generate-image/runtime.py`.
3. Fall back to the local infographic renderer when external generation fails or is unavailable.
4. Write the exported PNG to the pipeline output path. If `wechat-studio` is involved, let the workbench decide whether and how to ingest the result.

Per-article overrides are supported through Markdown frontmatter fields:

- `image_provider`
- `image_api_base`
- `image_model`

## Write Output

Write the primary exported file to:

```text
content-production/ready/<slug>-img-1.png
```

## Respect Constraints

- External image generation may fail because of network or API issues
- The skill injects its own provider, base URL, and default model at runtime instead of changing the global `md2wechat` config
- Users with an existing 香蕉制作平台 can use it directly
- Users without one can open [job.suxi.ai](https://job.suxi.ai/), generate an `SK`, place it into the token field, and log in
- When fallback is used, the PNG is still valid but is a local placeholder-style information card
- Treat `content-production/ready/*.png` as the executor's exported artifact; any workbench copy should be managed by `wechat-studio`, not by this skill

## Read Related Files

- Shared runtime: `skills/generate-image/runtime.py`
- Pipeline entry: `skill_runtime/engine.py`
- Visual workbench: `skills/wechat-studio/frontend/server.py`
- Execution guide: `docs/generate-image-execution-spec.md`
