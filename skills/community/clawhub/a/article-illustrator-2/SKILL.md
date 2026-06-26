---
name: article-illustrator
description: Generate multiple illustrations for an article with structured type and style decisions and bundled generation tooling. Use when the user asks to create illustrations for an article, add images to a post, or generate visuals for sections of a long text.
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "✏️", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# Article Illustration (`article-illustrator`)

## Reference Images (Important)

If you use reference images (image-to-image / series reference / consistency refs):

- Reference images must be public URLs.
- **HTTPS is strongly recommended.**
- `http://` may work but is insecure and can be blocked by some networks.
- Local file paths and `data:` URLs are not supported by the WeryAI gateway.


Generate multiple illustrations for an article, add images to a post, or generate visuals for sections of a long text — with structured type and style decisions and automatic Markdown insertion.

This article illustration workflow analyzes long-form content, identifies the best illustration positions, generates multiple coordinated images, and can insert those image references back into the article Markdown. Use it when you need to create illustrations for an article, add images to a post, or generate visuals for sections of a long text.

Important: keep the article structure readable, preserve the author's section flow, and only add illustrations where they clarify or strengthen the post.

Scripts:

- `scripts/scaffold.ts`
- `scripts/build-prompts.ts`
- `scripts/build-batch.ts`
- `scripts/insert-images.ts`

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/article-illustrator/` (project) and/or `~/.image-skills/article-illustrator/` (home).


## Use Cases

- add illustrations to article sections
- create visuals for tutorials, methods, reviews, and explainers
- keep multiple article images visually consistent

Not a good fit for:

- a single cover image
- a dense one-page infographic
- a sequential comic narrative

## Example Prompts

- `Illustrate my article about habit systems with minimal editorial images`
- `Add visuals to each section of this tutorial post`
- `Generate 4 illustrations for my review article in watercolor style`

## Core Dimensions

1. `type`: what the illustration is doing
2. `style`: the visual language

See:

- [references/types-and-styles.md](references/types-and-styles.md)
- [references/outline-template.md](references/outline-template.md)
- [references/prompt-template.md](references/prompt-template.md)

## Commands

| Script | Purpose |
| --- | --- |
| `scripts/scaffold.ts` | Initialize `outline.md` and per-illustration prompts |
| `scripts/build-prompts.ts` | Regenerate prompts from `outline.md` |
| `scripts/build-batch.ts` | Generate `batch.json` from illustration prompts |
| `scripts/insert-images.ts` | Insert image references into article Markdown |
| `scripts/illustrate-article.mjs` | Run the recommended end-to-end article illustration workflow |
| `npm run generate` | Generate illustrations |
| `./scripts/vendor/compression-runtime/scripts/main.ts` | Compress output for delivery |

## Workflow

### Recommended Default Workflow

For normal use, prefer the high-level orchestrator. It keeps `outline.md`, prompts, `batch.json`, and generated images on disk for inspection, but runs the full workflow for you:

```bash
node {baseDir}/scripts/illustrate-article.mjs \
  --article article.md \
  --output-dir illustrations/topic-slug \
  --project "$(pwd)"
```

This default path runs:

1. `ensure-ready`
2. `scaffold --article`
3. `build-prompts`
4. `build-batch`
5. `generate`
6. `insert-images`

Use the lower-level commands below when you want to inspect or customize each stage manually.

### Step 1: Initialize `outline.md` and Prompt Files

Create the working directory:

```bash
${BUN_X} {baseDir}/scripts/scaffold.ts \
  --article article.md \
  --output-dir illustrations/topic-slug \
  --topic "Habit systems" \
  --style minimal \
  --density per-section \
  --lang en \
  --illustrations 3
```

This creates:

- `outline.md`
- `prompts/01-framework-topic.md`
- `prompts/02-flowchart-topic.md`
- `prompts/03-summary-topic.md`

When `--article` is provided, `outline.md` now prefers real Markdown headings from the article and generates `Position` entries such as `after-heading: Why Habit Systems Work`. It only falls back to placeholder headings when the article does not provide enough usable headings.

### Step 2: Analyze the Article

Extract:

- content type: technical, tutorial, narrative, methodology, review
- 2 to 5 core arguments
- where illustrations add the most value
- whether each image should explain, visualize structure, or set tone
- the user's language, especially if labels or section text appear in the image

### Step 3: Choose `type`, `style`, and `density`

Default priorities:

- `type`: `mixed`
- `style`: `minimal`
- `density`: `per-section`

Recommended rules:

- technical explanation -> `framework` or `infographic`
- process explanation -> `flowchart`
- comparative review -> `comparison`
- historical development -> `timeline`
- emotional or narrative writing -> `scene`

### Step 4: Map to the Bundled Runtime

The bundled image runtime currently exposes one structured visual argument, `--style`, so:

- map `style` to `--style`
- write `type`, `density`, and section purpose into the prompt body
- prefer batch generation when there are multiple illustrations

Recommended mapping:

| illustrator style | runtime `--style` |
| --- | --- |
| `minimal` | `editorial` |
| `notion` | `flat-illustration` |
| `blueprint` | `infographic` |
| `watercolor` | `watercolor` |
| `elegant` | `editorial` |
| `poster` | `poster` |

### Step 5: Refine `outline.md`, Then Build Prompts

Save at least:

- `outline.md`
- `prompts/01-framework-topic.md`
- `prompts/02-scene-topic.md`

Each outline entry should include:

- `Position`
- `Purpose`
- `Visual Content`
- `Filename`

Recommended `Position` syntax:

- `after-heading: <heading>`
- `before-heading: <heading>`
- `after-text: <snippet>`
- `end`

When the outline is ready, generate prompt files automatically:

```bash
${BUN_X} {baseDir}/scripts/build-prompts.ts \
  --outline illustrations/topic-slug/outline.md \
  --output-dir illustrations/topic-slug/prompts \
  --topic "Habit systems" \
  --audience "general reader" \
  --style minimal \
  --density per-section \
  --lang en \
  --aspect 16:9
```

This converts each outline entry into a prompt file such as `01-framework-topic.md` or `02-flowchart-topic.md`.

Consistency strategy for multi-illustration articles:

1. create one canonical `references/series-reference.png` first
2. treat that image as the source of truth for palette, recurring subject, diagram vocabulary, and composition rhythm
3. reuse the same shared reference for every illustration task
4. keep illustration-specific continuity anchors plus previous/next-section context in every prompt
5. if the shared reference image is missing, do not proceed to final batch generation yet

### Step 6: Generate the Shared Series Reference First

Before building the final illustration batch, generate the canonical series reference image:

```bash
${BUN_X} {baseDir}/npm run generate \
  --promptfiles illustrations/topic-slug/references/series-reference.md \
  --style minimal \
  --image illustrations/topic-slug/references/series-reference.png \
  --ar 16:9 \
  -m "$M"
```

This step is the default for multi-illustration articles. Do not skip it when consistency matters.

### Step 7: Build `batch.json` and Generate Images

Build a batch file from the outline and prompt directory:

```bash
${BUN_X} {baseDir}/scripts/build-batch.ts \
  --outline illustrations/topic-slug/outline.md \
  --prompts illustrations/topic-slug/prompts \
  --output illustrations/topic-slug/batch.json \
  --images-dir illustrations/topic-slug \
  --model "$M"
```

Then run the bundled image generator:

On first use in a new project, run `npm run ensure-ready -- --project <your-project> --workflow article` from this skill directory before generation. This reads the doctor report and auto-runs `bootstrap` if local script dependencies are still missing. If the report shows a missing `IMAGE_GEN_API_KEY` and the user approves, run `npm run setup -- --project <your-project> --workflow article --persist-api-key` when the key is already in env, or persist it to `.image-skills/article-illustrator/.env` on the user's behalf, then continue without leaving this workflow.

When this skill is first connected, tell the user that the default generation model is **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`). Also tell them it can be switched later whenever another model fits the task better.

```bash
${BUN_X} {baseDir}/npm run generate --batchfile illustrations/topic-slug/batch.json --json
```

The bundled generator now uses stability-first batch defaults and safer retry/backoff behavior for rate-limit-like failures. It retries submit failures conservatively, retries status polling without blindly resubmitting the same task, and keeps the initial concurrency biased toward reliability over speed.

If only one illustration is needed, a single direct call is still fine.

### Step 8: Insert Images Back into Markdown

After the images are generated, insert references into the article:

```bash
${BUN_X} {baseDir}/scripts/insert-images.ts \
  --article article.md \
  --outline illustrations/topic-slug/outline.md \
  --images-dir illustrations/topic-slug
```

If you do not want to overwrite the original file:

```bash
${BUN_X} {baseDir}/scripts/insert-images.ts \
  --article article.md \
  --outline illustrations/topic-slug/outline.md \
  --images-dir illustrations/topic-slug \
  --output article.with-images.md
```

Default behavior:

- if `--output` is omitted, the original Markdown is backed up first and then updated in place
- image insertion follows `Position` and `Filename` from `outline.md`
- if the same image path is already referenced, that entry is skipped
- missing headings are recoverable by default: `--on-missing-anchor end` appends the image at the end and reports it in the summary
- the command prints a summary so you can see exact inserts vs fallback/skipped/failed entries

## Output Convention

Suggested output directory:

```text
illustrations/<topic-slug>/
```

Suggested minimum files:

- `outline.md`
- `batch.json`
- `prompts/NN-type-slug.md`
- `NN-type-slug.png`
- the updated article Markdown

## Definition of Done

- `outline.md` and per-illustration prompt files exist in the output directory.
- All illustrations are generated and shown alongside their article sections.
- The article Markdown is updated with image references via `insert-images.ts`.
- Illustration count, style, and model are stated in the delivery summary.
- A compressed webp set is produced for delivery.

## Iteration

When the user wants changes after seeing generated illustrations:

- **Style mismatch** ("inconsistent style", "change the style") → change `style` / `--style` for all illustrations, rebuild batch, re-generate. Ask if all or specific ones.
- **Wrong illustration type** ("this one should be a flowchart, not a scene") → update the `type` in `outline.md` for that entry, rebuild its prompt, re-generate only that image.
- **Position wrong** ("this image should be after that paragraph") → update `Position` in `outline.md`, re-run `insert-images.ts`.
- **Too many/few illustrations** → adjust `outline.md`, add or remove entries, rebuild affected prompts.
- **Single image redo** → re-generate only that image with `--promptfiles prompts/NN-type-slug.md`. Keep other images.

After any changes, re-run `insert-images.ts` to update the article Markdown.

## Delivery

When the illustrations are ready:

1. **Show each illustration directly** alongside the section it belongs to. Do not just list file paths.
2. Briefly state: illustration count, style, density.
3. Confirm the article Markdown has been updated with image references.
4. Ask if any illustrations need changes or if the user is satisfied.
5. **Auto-compress**: once confirmed, run the bundled compression runtime on the illustrations directory for web-optimized versions.

```bash
${BUN_X} {baseDir}/./scripts/vendor/compression-runtime/scripts/main.ts illustrations/topic-slug/ -r -f webp -q 80
```

Internal checklist (for agent): illustration count, `type / style / density`, model, insert-images status, compression done.

## Current Scope

This version of `article-illustrator` focuses on:

- article analysis
- illustration planning
- prompt and batch organization
- automatic Markdown image insertion
