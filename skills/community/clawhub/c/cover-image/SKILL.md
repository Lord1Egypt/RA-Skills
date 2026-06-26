---
name: cover-image
description: Generate article cover images with structured dimensions and bundled generation tooling. Use when the user asks to create a cover image, article cover, blog header, newsletter hero image, or banner-style key visual.
metadata: { "pattern": ["generator", "pipeline"], "openclaw": { "emoji": "🖼️", "primaryEnv": "IMAGE_GEN_API_KEY", "requires": { "env": ["IMAGE_GEN_API_KEY"], "anyBins": ["bun", "npx"], "bins": ["node", "npm"] } } }
---

# Cover Image Generation (`cover-image`)

## Reference Images (Important)

If you use reference images (image-to-image / series reference / consistency refs):

- Reference images must be public URLs.
- **HTTPS is strongly recommended.**
- `http://` may work but is insecure and can be blocked by some networks.
- Local file paths and `data:` URLs are not supported by the WeryAI gateway.


This skill turns a vague "make a cover image" request into a stable set of structured decisions instead of starting from scratch every time.

Script:

- `scripts/scaffold.ts`
- `scripts/build-batch.ts`

## Safety & Scope

- **Network**: This skill calls the WeryAI gateway over HTTPS (`https://api.weryai.com`).
- **Auth**: Uses `IMAGE_GEN_API_KEY`. The key is never printed. It may be persisted **only** when you explicitly run `npm run setup -- --persist-api-key`.
- **Reference images**: Must be public URLs (`https://` recommended). `http://` may work but is insecure. Local file paths and `data:` URLs are rejected.
- **No arbitrary shell**: The generation runtime does not execute arbitrary shell commands.
- **Files written**: Output images and optional local config under `.image-skills/cover-image/` (project) and/or `~/.image-skills/cover-image/` (home).


## Use Cases

- article cover images
- blog headers or hero images
- newsletter covers
- banner-style key visuals
- any single visual that should feel like a cover rather than an infographic or comic

## Core Dimensions

Choose these six dimensions, then assemble the prompt:

1. `type`
2. `palette`
3. `rendering`
4. `text`
5. `mood`
6. `aspect`

See [references/dimensions.md](references/dimensions.md).

## Commands

| Script | Purpose |
| --- | --- |
| `scripts/scaffold.ts` | Initialize `brief.md` and `prompts/cover.md` |
| `scripts/build-batch.ts` | Generate `batch.json` from multiple prompt variants |
| `npm run generate` | Generate the cover image |
| `./scripts/vendor/compression-runtime/scripts/main.ts` | Compress output for delivery |

## Workflow

### Step 1: Initialize Working Files

Create the working directory:

```bash
${BUN_X} {baseDir}/scripts/scaffold.ts \
  --output-dir cover-image/topic-slug \
  --topic "Why Habits Stick" \
  --concept "A repeating loop turning into visible momentum" \
  --type conceptual \
  --palette elegant \
  --rendering editorial \
  --text title-only \
  --mood balanced \
  --aspect 16:9 \
  --lang en
```

This creates:

- `brief.md`
- `prompts/cover.md`

### Step 2: Understand the Content

Extract:

- the main theme
- the target reader
- the keywords
- whether the content fits a person, a scene, or an abstract metaphor
- whether title text needs to appear
- the user's language, when it matters for on-canvas text

### Step 3: Choose the Dimensions

Default priorities:

- `type`: `conceptual`
- `palette`: `elegant`
- `rendering`: `editorial` or `poster`
- `text`: `title-only`
- `mood`: `balanced`
- `aspect`: `16:9`

If the user explicitly specifies style, mood, or aspect ratio, follow that preference.

Language rules:

- default to the source content language
- if the cover includes a title or subtitle, state the target language explicitly in the prompt

### Step 4: Refine `brief.md` and `prompts/cover.md`

Use `brief.md` to lock the audience, concept, and references before polishing the final prompt.

Make sure `prompts/cover.md` clearly states:

- the article or video topic
- the main visual concept or metaphor
- the chosen `type / palette / rendering / text / mood / aspect`
- the target language for any on-canvas text

### Step 5: Build `batch.json` for Variants

If you want to explore multiple cover directions, put several prompt files in `prompts/`, for example:

- `01-editorial.md`
- `02-poster.md`
- `03-cinematic.md`

Then generate a batch file:

```bash
${BUN_X} {baseDir}/scripts/build-batch.ts \
  --prompts cover-image/topic-slug/prompts \
  --output cover-image/topic-slug/batch.json \
  --images-dir cover-image/topic-slug \
  --model "$M" \
  --jobs 3
```

The script reads `Rendering style:` and `Aspect ratio:` from each prompt file when possible, then maps them into generation task fields.

### Step 6: Map to the Bundled Runtime

The bundled image runtime currently exposes one structured style argument, `--style`, so:

- map `rendering` to `--style`
- write `palette`, `type`, `text`, and `mood` into the prompt body
- keep using `--ref` when the user provides references

Recommended mapping:

| cover rendering | runtime `--style` |
| --- | --- |
| `editorial` | `editorial` |
| `poster` | `poster` |
| `cinematic` | `cinematic` |
| `watercolor` | `watercolor` |
| `flat-vector` | `flat-illustration` |
| `ink-brush` | `ink-brush` |
| `chalk` | `chalk` |
| `manga` | `manga` |
| `anime` | `anime` |
| `photoreal` | `photoreal` |
| `3d-render` | `3d-render` |
| `infographic` | `infographic` |

### Step 7: Build the Prompt

Use [references/prompt-template.md](references/prompt-template.md). Make sure to:

- put the topic and subject in the first paragraph
- describe cover composition and visual focus in the second paragraph
- describe palette, mood, and text treatment in the third paragraph
- request reserved title space instead of relying on the model to typeset well
- state the title language explicitly if the cover needs on-canvas text

### Step 8: Run Generation

Generate through the bundled runtime at `npm run generate`.

On first use in a new project, run `npm run ensure-ready -- --project <your-project> --workflow cover` from this skill directory before generation starts. This reads the doctor report and auto-runs `bootstrap` if local script dependencies are still missing. If the report shows a missing `IMAGE_GEN_API_KEY` and the user approves, run `npm run setup -- --project <your-project> --workflow cover --persist-api-key` when the key is already in env, or persist it to `.image-skills/cover-image/.env` on the user's behalf, then continue without leaving this workflow.

When this skill is first connected, tell the user that the default generation model is **Nano Banana 2** (`GEMINI_3_1_FLASH_IMAGE`). Also tell them it can be switched later whenever another model fits the task better.

Example:

```bash
${BUN_X} {baseDir}/npm run generate \
  --promptfiles prompts/cover.md \
  --style editorial \
  --image cover-image/topic-slug/cover.png \
  --ar 16:9 \
  -m "$M"
```

Batch example:

```bash
${BUN_X} {baseDir}/npm run generate \
  --batchfile cover-image/topic-slug/batch.json \
  --jobs 3
```

If the user has not chosen a model yet, follow this skill's model-selection rules first.

## Output Convention

Suggested output directory:

```text
cover-image/<topic-slug>/
```

Suggested minimum files:

- `brief.md`
- `prompts/cover.md`
- `batch.json`
- `cover.png`

If the content comes directly from chat instead of a file, it is also useful to save the summary or title into `source.md` for reproducibility.

## Iteration

When the user wants changes after seeing the generated cover:

- **Style mismatch** ("wrong style", "too busy") → change `rendering` / `--style`, re-generate. Keep other dimensions.
- **Color issues** ("too dark", "wrong colors") → adjust `palette` in the prompt body, re-generate.
- **Composition issues** ("bad layout", "title position is off") → revise the composition and text-space description in `prompts/cover.md`, re-generate.
- **Want to explore alternatives** → create additional prompt variants in `prompts/`, use `build-batch.ts` to generate multiple options in one batch.
- **Minor tweaks with reference** → if the model supports `--ref`, use the current output as reference with adjusted prompt to refine.

Only re-generate the specific image that needs changes. Do not re-run the entire workflow from scratch unless the user wants a fundamentally different direction.

## Definition of Done

- `brief.md` and `prompts/cover.md` exist in the output directory.
- The generated cover image matches the chosen `type / palette / rendering / text / mood / aspect`.
- The image is shown directly to the user with a summary of the parameters used.
- A compressed webp version is produced for delivery.

## When Not to Use It

Choose a different higher-level skill for:

- multi-page knowledge comics
- multi-card RedNote image series
- dense infographics
- pure product cutout or white-background product shots

## Delivery

When the cover image is ready:

1. **Show the image directly** — do not just print a file path.
2. Briefly state what was generated: style, aspect ratio, model used.
3. Ask if the user wants changes or is satisfied.
4. **Auto-compress**: once the user confirms, run the bundled compression runtime to produce a webp version for web/social upload. Deliver both the original and the compressed file.

```bash
${BUN_X} {baseDir}/./scripts/vendor/compression-runtime/scripts/main.ts cover-image/topic-slug/cover.png -f webp -q 80
```

Internal checklist (for agent, not shown to user): chosen `type / palette / rendering / text / mood / aspect`, model, whether `--style` or `--ref` was used, compression done.
