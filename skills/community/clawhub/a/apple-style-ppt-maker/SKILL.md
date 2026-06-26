---
name: apple-style-ppt-maker
description: Create Apple-style minimalist presentation slides through a strict JSON-first workflow. Use when an agent must clarify user requirements, lock topic/content/structure, produce per-slide text plus visual specifications, generate 2K WebP images (Nano Banana Pro), support page-level redesign/regeneration, and export the final deck to PPTX.
homepage: https://github.com/herve-ves/open-apple-style-ppt-maker-skill
metadata: {"clawdbot":{"emoji":"🍎","requires":{"bins":["uv"],"env":["APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY","GEMINI_API_KEY"]},"primaryEnv":"APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY"}}
---

# Apple Style PPT Maker

## Overview

Drive a deterministic presentation pipeline for Apple-style minimalist decks.
Enforce requirement clarification, strict schema validation, full-plan review, consistent slide rendering, selective page regeneration, and PPTX export.

## Workflow

0. Check `uv` availability. If missing, stop and ask the user to install `uv`.
1. Clarify requirements with the user.
2. Build and validate `slides_plan.json`.
3. Get user review for the full JSON plan before image generation.
4. Generate all slide images at default `2K` and `webp`.
5. Run result review and regenerate specific pages when requested.
6. Export slides to `final.pptx`.

## Step 0: Verify uv

Run:

```bash
uv --version
```

If the command fails:
- stop the workflow immediately
- ask the user to install `uv`
- continue only after `uv` is available

## Step 1: Clarify Requirements

Use a friendly, conversational tone.
Do not expose internal schema field names to the user.

Ask in natural language and confirm:
- this deck's core topic
- target audience and meeting context
- expected speaking duration and target page count
- desired tone and language
- must-keep points and sensitive points to avoid

Follow user input language by default.
Do not generate images before all clarification items are confirmed.

Internal mapping rule (do not show to user):
- map the confirmed answers to the internal requirement fields used by the JSON plan

## Step 2: Build Structured Slide JSON

Create `slides_plan.json` and validate it against [references/slides-schema.json](references/slides-schema.json).
Start from [references/slides-plan-template.json](references/slides-plan-template.json) when you need a fast baseline.

Use [references/apple-style-spec.md](references/apple-style-spec.md) to keep visual consistency and style quality.

Define both content and visual intent for each page:
- text payload (`on_slide_text`)
- visual blueprint (`visual_blueprint`)
- consistency checks (`consistency_checks`)

## Step 3: Review Full Plan Before Rendering

Always show the complete `slides_plan.json` to the user.
Pause until the user approves the full plan.
Apply edits to the JSON plan first, then render images.

## Step 4: Generate Slide Images

Run:

```bash
uv run scripts/generate_slides.py --plan slides_plan.json --out outputs/deck_a
```

Defaults:
- resolution: `2K`
- format: `webp`
- aspect ratio: `16:9`
- model: `gemini-3-pro-image-preview` (Nano Banana Pro path)

Generated files:
- `images/slide-XX.webp`
- `prompts/slide-XX.prompt.md`
- `meta/slide-XX.meta.json`
- `deck_manifest.json`

## Step 5: Review and Regenerate Specific Page

Run:

```bash
uv run scripts/regenerate_slide.py \
  --plan slides_plan.json \
  --slide 4 \
  --change "Simplify data narrative and increase whitespace" \
  --out outputs/deck_a
```

Behavior:
- Regenerate only the target slide.
- Snapshot prior image, prompt, and metadata to `history/`.
- Update manifest revision metadata.

## Step 6: Export PPTX

Run:

```bash
uv run scripts/export_pptx.py \
  --images-dir outputs/deck_a/images \
  --output-pptx outputs/deck_a/final.pptx
```

## Environment

Set one of:
- `APPLE_STYLE_PPT_MAKER_GEMINI_API_KEY`
- `GEMINI_API_KEY`

Optional:
- place `.env` in current directory
- place `.env` in this skill directory

Dependency management:
- each executable script uses PEP 723 inline metadata
- run scripts with `uv run ...` so dependencies bootstrap automatically

## Notes

- Keep style and spacing consistent across all pages.
- Prefer concise, readable text over dense paragraphs.
- Use regeneration instead of re-rendering the entire deck for isolated edits.
