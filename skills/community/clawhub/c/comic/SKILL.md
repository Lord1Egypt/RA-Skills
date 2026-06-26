---
name: comic
description: Generate educational or narrative comic pages with structured art, tone, layout, and language decisions and bundled generation tooling. Use when the user asks to create a knowledge comic, tutorial comic, biography comic, educational comic, or a multi-page comic sequence.
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "📖", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm", "zip"] } } }
---

# Comic Generation (`comic`)

## Reference Images (Important)

If you use reference images (image-to-image / series reference / consistency refs):

- Reference images must be public URLs.
- **HTTPS is strongly recommended.**
- `http://` may work but is insecure and can be blocked by some networks.
- Local file paths and `data:` URLs are not supported by the WeryAI gateway.


Generate educational or narrative comic pages: a knowledge comic, tutorial comic, biography comic, educational comic, or a multi-page comic sequence — structured art, tone, layout, and language decisions included.

This skill turns source material into a sequence of comic pages.

Maintain the art and tone mapping when the bundled generation runtime updates, and re-check recent runtime behavior if a newer version changes page rendering.

Before the first generation run in a new OpenClaw or local instance, run:

```bash
npm run ensure-ready -- --project . --workflow comic
```

This step is mandatory. It reads the doctor report and automatically runs `bootstrap` when local script dependencies such as `pdf-lib` are still missing.

If the report shows a missing `IMAGE_GEN_API_KEY` and the user approves, run `npm run setup -- --project . --workflow comic --persist-api-key` when the key is already in env, or persist it to `.image-skills/comic/.env` on the user's behalf, then continue the comic workflow without leaving this skill.

When this skill is first connected, tell the user that the default generation model is **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`). Also tell them it can be switched later whenever another model fits the task better.

Script:

- `scripts/scaffold.ts`
- `scripts/build-prompts.ts`
- `scripts/build-batch.ts`
- `scripts/merge-to-pdf.ts`

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/comic/` (project) and/or `~/.image-skills/comic/` (home).


## Use Cases

- knowledge comics
- tutorial comics
- biography comics
- multi-page narrative image sequences

Not a good fit for:

- a single cover image
- a dense one-page infographic
- a RedNote card series

## Core Dimensions

1. `art`
2. `tone`
3. `layout`
4. `aspect`

See:

- [references/dimensions.md](references/dimensions.md)
- [references/character-template.md](references/character-template.md)
- [references/storyboard-template.md](references/storyboard-template.md)
- [references/prompt-template.md](references/prompt-template.md)

## Commands

| Script | Purpose |
| --- | --- |
| `scripts/scaffold.ts` | Initialize storyboard, characters, and page prompts |
| `scripts/build-prompts.ts` | Regenerate page prompts from `storyboard.md` |
| `scripts/build-batch.ts` | Generate `batch.json` from page prompts |
| `scripts/merge-to-pdf.ts` | Merge page images into a single PDF |
| `scripts/package-delivery.mjs` | Prepare delivery bundle with manifest and previews |
| `npm run generate` | Generate page images |
| `./scripts/vendor/compression-runtime/scripts/main.ts` | Compress output for delivery |

## Workflow

### Step 1: Initialize Working Files

Create the working directory:

```bash
${BUN_X} {baseDir}/scripts/scaffold.ts \
  --output-dir comic/topic-slug \
  --title "Comic Title" \
  --topic "Topic summary" \
  --art ligne-claire \
  --tone neutral \
  --layout standard \
  --aspect 3:4 \
  --scope standard \
  --lang en \
  --panels 3 \
  --pages 4
```

This creates:

- `analysis.md`
- `storyboard.md`
- `characters/characters.md`
- `prompts/00-cover.md`
- `prompts/01-page.md`
- ...

### Step 2: Understand the Content

Extract:

- the main story arc or knowledge arc
- the characters
- the key scenes
- the target aspect ratio
- the expected total content scope and number of pages
- the target panel density per page
- the user's language, especially if dialogue or captions appear on the page

### Step 3: Choose `art`, `tone`, and `layout`

Default priorities:

- `art`: `ligne-claire`
- `tone`: `neutral`
- `layout`: `standard`
- `aspect`: `3:4`
- `scope`: `standard`
- `panels`: `3`

Recommended rules:

- educational explanation -> `ligne-claire` + `neutral`
- high-energy storytelling -> `manga` + `action`
- warm storytelling -> `ligne-claire` + `warm`
- ink or wuxia-like themes -> `ink-brush` + `dramatic`

### Step 4: Map to the Bundled Runtime

The bundled image runtime does not directly understand comic page grammar, so:

- map `art` to `--style`
- write `tone`, `layout`, camera language, and panel logic into the prompt body
- create one prompt per page
- prefer batch execution for multi-page comics

Recommended mapping:

| comic art | runtime `--style` |
| --- | --- |
| `ligne-claire` | `flat-illustration` |
| `manga` | `manga` |
| `realistic` | `photoreal` |
| `ink-brush` | `ink-brush` |
| `chalk` | `chalk` |

### Step 5: Refine `storyboard.md`, Then Build Prompts

Save at least:

- `analysis.md`
- `storyboard.md`
- `characters/characters.md`
- `characters/characters.png`
- `prompts/00-cover.md`
- `prompts/01-page.md`

When the storyboard is ready, generate prompt files automatically:

```bash
${BUN_X} {baseDir}/scripts/build-prompts.ts \
  --storyboard comic/topic-slug/storyboard.md \
  --output-dir comic/topic-slug/prompts
```

Each page prompt should clearly describe:

- the page goal
- the characters and scene
- the cross-page continuity anchors
- the panel structure
- the intended panel count
- the target language for any text on the page

Character consistency rules:

- default to the strongest continuity strategy: generate one canonical `characters/characters.png` first, then reuse that same reference for every page
- create `characters/characters.md` before generating multi-page comics
- generate `characters/characters.png` as a reference sheet before page generation
- if the chosen model supports `--ref`, pass the same `characters/characters.png` to every page
- if the chosen model does not support `--ref`, copy the key character descriptions into every page prompt
- include page-level continuity anchors in `storyboard.md` so outfit, props, location, and scene progression stay aligned from page to page
- each page prompt should include previous-page context and next-page hook so the sequence reads like one comic, not isolated posters

Recommended sequence:

1. finish `storyboard.md`
2. finish `characters/characters.md`
3. generate `characters/characters.png`
4. make sure every page in `storyboard.md` includes `Continuity Anchors`
5. batch-generate all comic pages

### Step 6: Build `batch.json`

When page prompts are ready, generate a batch file:

```bash
${BUN_X} {baseDir}/scripts/build-batch.ts \
  --prompts comic/topic-slug/prompts \
  --storyboard comic/topic-slug/storyboard.md \
  --ref comic/topic-slug/characters/characters.png \
  --output comic/topic-slug/batch.json \
  --images-dir comic/topic-slug \
  --model "$M" \
  --jobs 4
```

The script:

- reads `00-cover.md`, `01-page.md`, `02-page.md`, and so on
- maps comic `art` from `storyboard.md` into runtime `--style` when possible
- defaults to the same shared character reference sheet for every page from `storyboard.md` when `--ref` is not explicitly overridden

Default best-performing strategy:

1. generate `characters/characters.png` first
2. keep that sheet as the canonical look for faces, outfits, props, and palette
3. reuse the same reference for every cover/page task
4. only fall back to text-only continuity when the chosen model cannot reliably use references

### Step 7: Run Generation

Generate the character sheet first:

```bash
${BUN_X} {baseDir}/npm run generate \
  --promptfiles characters/characters.md \
  --style manga \
  --image comic/topic-slug/characters/characters.png \
  --ar 4:3 \
  -m "$M"
```

Single-page example:

```bash
${BUN_X} {baseDir}/npm run generate \
  --promptfiles prompts/02-page.md \
  --style manga \
  --ref comic/topic-slug/characters/characters.png \
  --image comic/topic-slug/02-page.png \
  --ar 3:4 \
  -m "$M"
```

Batch example:

```bash
${BUN_X} {baseDir}/npm run generate \
  --batchfile comic/topic-slug/batch.json \
  --jobs 4
```

### Step 8: Merge Pages into PDF

After page images are ready:

If this skill was distributed as a slim package without `node_modules`, run `npm run bootstrap` from this skill directory once before this step so the local PDF dependency is installed. If you forget, `merge-to-pdf.ts` now prints that exact recovery hint.

```bash
${BUN_X} {baseDir}/scripts/merge-to-pdf.ts comic/topic-slug
```

To choose a specific output path:

```bash
${BUN_X} {baseDir}/scripts/merge-to-pdf.ts comic/topic-slug -o comic/topic-slug/final.pdf
```

The script merges page files in the order `00-cover-*`, `01-page-*`, `02-page-*`, and so on, across `png`, `jpg`, and `jpeg`.

### Step 9: Prepare Delivery Files

When you need a cleaner handoff than a raw table of URLs, prepare a delivery bundle:

```bash
${BUN_X} {baseDir}/scripts/package-delivery.mjs comic/topic-slug
```

This creates:

- `delivery/preview.md` with inline preview entries for small batches
- `delivery/manifest.json` with ordered file metadata
- `delivery/pages/` with copied page images
- `delivery/<topic-slug>-delivery.zip` automatically when the page count is large enough

Delivery rules:

- **Few pages (≤ 5)**: show each page image directly in order (cover → pages). Do not just list file paths.
- **Many pages (> 5)**: show the first 2–3 pages as preview, then provide the PDF and/or zip bundle.
- Always offer the merged PDF as the primary deliverable.
- Ask if any pages need changes before finalizing.
- **Auto-compress**: once confirmed, run the bundled compression runtime on the output directory before packaging.

```bash
${BUN_X} {baseDir}/./scripts/vendor/compression-runtime/scripts/main.ts comic/topic-slug/ -r -f webp -q 80
```

Internal checklist (for agent): `art / tone / layout / aspect`, page count, character reference used, model, PDF generated, compression done.

## Output Convention

Suggested output directory:

```text
comic/<topic-slug>/
```

Suggested minimum files:

- `analysis.md`
- `storyboard.md`
- `characters/characters.md`
- `characters/characters.png`
- `prompts/00-cover.md`
- `prompts/NN-page.md`
- `batch.json`
- `00-cover.png`
- `NN-page.png`
- `<topic-slug>.pdf`

## Re-run Behavior

- `scaffold.ts` on an existing directory overwrites `storyboard.md`, `characters/characters.md`, and all prompt files. Back up before re-scaffolding.
- `build-prompts.ts` overwrites prompt files in `prompts/` based on the current `storyboard.md`.
- `build-batch.ts` overwrites `batch.json`.
- Re-running the bundled generator with `--batchfile` regenerates all pages; keep good pages by removing their entries from `batch.json` first.
- `merge-to-pdf.ts` overwrites the existing PDF.

## Definition of Done

- `storyboard.md`, `characters/characters.md`, and per-page prompt files exist in the output directory.
- All pages are generated and shown to the user in reading order.
- A merged PDF is produced via `merge-to-pdf.ts`.
- Art style, page count, and model are stated in the delivery summary.
- A compressed webp set is produced for delivery.

## Iteration

When the user wants changes after seeing generated comic pages:

- **Art style mismatch** ("wrong style", "switch to ink brush") → change `art` in `storyboard.md`, update `--style` mapping, re-generate affected pages. Ask if all pages or specific ones.
- **Character inconsistency** ("characters look different across pages") → regenerate `characters/characters.png` with more explicit descriptions, then re-generate pages using the updated reference sheet.
- **Panel layout issues** ("bad panels", "this page is too crowded") → revise the specific page in `storyboard.md`, rebuild its prompt, re-generate only that page.
- **Story flow issues** ("wrong order", "need an extra page") → revise `storyboard.md` to add/reorder pages, rebuild prompts for changed pages, re-generate.
- **Single page redo** → re-generate only that page with `--promptfiles prompts/NN-page.md`. Keep other pages.

After any page changes, re-run `merge-to-pdf.ts` to update the PDF.

## Current Scope

This version of `comic` focuses on:

- comic-page workflow
- character consistency
- page-level prompt organization
- single-gateway image execution
