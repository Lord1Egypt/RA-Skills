---
name: custom-infographic
description: Generate a professional infographic from an article, document, URL, or topic, using the baoyu layout x style system (21 layouts x 21 styles). Original author 宝玉 (JimLiu); ported & customized by j3ffyang. Use when the user asks to create an infographic, 信息图, visual summary, 可视化, or a high-density information image, or wants an article turned into a visual poster.
license: MIT
compatibility: opencode
metadata:
  author: 宝玉 (JimLiu)
  upstream: https://github.com/JimLiu/baoyu-skills#baoyu-infographic
  version: 1.56.1
---

# Infographic Generator

Adapted from [baoyu-infographic](https://github.com/JimLiu/baoyu-skills) v1.56.1 (ported via Hermes Agent) for opencode. Customized by j3ffyang to comply with the opencode standard and this repo's `imgs/` convention. Image generation uses OpenRouter image models through `scripts/generate_image.py`. Pitfall 6 gives the key requirement and the fallback.

Two dimensions: **layout** (information structure) × **style** (visual aesthetics). Freely combine any layout with any style. Never mix two styles in one image (Pitfall 4).

## When to Use

Trigger this skill when the user asks for an infographic, a visual summary, or an information graphic. Trigger it also on "信息图", "可视化", or "高密度信息大图". The user gives content: text, a file path, a URL, or a topic. The user can also give layout, style, aspect ratio, or language.

*Note*: Image generation needs `OPENROUTER_API_KEY` and an image-capable model. Step 6 names the default model. If the key is missing or the call fails, still produce `analysis.md`, `structured-content.md`, and `prompts/infographic.md` for external use. See Pitfall 6 and `references/workflow-example.md`.

## Options

| Option | Values |
|--------|--------|
| Layout | 21 options (see Layout Gallery), default: bento-grid |
| Style | 21 options (see Style Gallery), default: craft-handmade |
| Aspect | `landscape` (16:9), `portrait` (9:16), `square` (1:1), or a custom W:H — the resolution rule is in Step 5 |
| Language | en, zh, ja, etc. |

## Terms

One name per object, used the same way everywhere below.

| Term | Means | Not |
|---|---|---|
| image | the generated picture file | sheet, render, chart, diagram |
| prompt | the assembled file under `prompts/` | template (`references/base-prompt.md`), structured content |
| checker | `scripts/check_prompt_text.py` | gate, linter, pre-flight |

## Layout Gallery

| Layout | Best For |
|--------|----------|
| `linear-progression` | Timelines, processes, tutorials |
| `binary-comparison` | A vs B, before-after, pros-cons |
| `comparison-matrix` | Multi-factor comparisons |
| `hierarchical-layers` | Pyramids, priority levels |
| `tree-branching` | Categories, taxonomies |
| `hub-spoke` | Central concept with related items |
| `structural-breakdown` | Exploded views, cross-sections |
| `bento-grid` | Multiple topics, overview (default) |
| `iceberg` | Surface vs hidden aspects |
| `bridge` | Problem-solution |
| `funnel` | Conversion, filtering |
| `isometric-map` | Spatial relationships |
| `dashboard` | Metrics, KPIs |
| `periodic-table` | Categorized collections |
| `comic-strip` | Narratives, sequences |
| `story-mountain` | Plot structure, tension arcs |
| `jigsaw` | Interconnected parts |
| `venn-diagram` | Overlapping concepts |
| `winding-roadmap` | Journey, milestones |
| `circular-flow` | Cycles, recurring processes |
| `dense-modules` | High-density modules, data-rich guides |

Full definitions: `references/layouts/<layout>.md`

## Style Gallery

| Style | Description |
|-------|-------------|
| `craft-handmade` | Hand-drawn, paper craft (default) |
| `claymation` | 3D clay figures, stop-motion |
| `kawaii` | Japanese cute, pastels |
| `storybook-watercolor` | Soft painted, whimsical |
| `chalkboard` | Chalk on black board |
| `cyberpunk-neon` | Neon glow, futuristic |
| `bold-graphic` | Comic style, halftone |
| `aged-academia` | Vintage science, sepia |
| `corporate-memphis` | Flat vector, vibrant |
| `technical-schematic` | Blueprint, engineering |
| `origami` | Folded paper, geometric |
| `pixel-art` | Retro 8-bit |
| `ui-wireframe` | Grayscale interface mockup |
| `subway-map` | Transit diagram |
| `ikea-manual` | Minimal line art |
| `knolling` | Organized flat-lay |
| `lego-brick` | Toy brick construction |
| `pop-laboratory` | Blueprint grid, coordinate markers, lab precision |
| `morandi-journal` | Hand-drawn doodle, warm Morandi tones |
| `retro-pop-grid` | 1970s retro pop art, Swiss grid, thick outlines |
| `hand-drawn-edu` | Macaron pastels, hand-drawn wobble, stick figures |

Full definitions: `references/styles/<style>.md`

## Recommended Combinations

| Content Type | Layout + Style |
|--------------|----------------|
| Timeline/History | `linear-progression` + `craft-handmade` |
| Step-by-step | `linear-progression` + `ikea-manual` |
| A vs B | `binary-comparison` + `corporate-memphis` |
| Hierarchy | `hierarchical-layers` + `craft-handmade` |
| Overlap | `venn-diagram` + `craft-handmade` |
| Conversion | `funnel` + `corporate-memphis` |
| Cycles | `circular-flow` + `craft-handmade` |
| Technical | `structural-breakdown` + `technical-schematic` |
| Metrics | `dashboard` + `corporate-memphis` |
| Educational | `bento-grid` + `chalkboard` |
| Journey | `winding-roadmap` + `storybook-watercolor` |
| Categories | `periodic-table` + `bold-graphic` |
| Product Guide | `dense-modules` + `morandi-journal` |
| Technical Guide | `dense-modules` + `pop-laboratory` |
| Trendy Guide | `dense-modules` + `retro-pop-grid` |
| Educational Diagram | `hub-spoke` + `hand-drawn-edu` |
| Process Tutorial | `linear-progression` + `hand-drawn-edu` |

Default: `bento-grid` + `craft-handmade`

## Keyword Shortcuts

If the user input contains one of these keywords, **select** the associated layout. Offer the associated styles first in Step 3. Skip content-based layout inference.

If a shortcut has **Prompt Notes**, append them to the generated prompt (Step 5) as additional style instructions.

| User Keyword | Layout | Recommended Styles | Default Aspect | Prompt Notes |
|--------------|--------|--------------------|----------------|--------------|
| 高密度信息大图 / high-density-info | `dense-modules` | `morandi-journal`, `pop-laboratory`, `retro-pop-grid` | portrait | — |
| 信息图 / infographic | `bento-grid` | `craft-handmade` | landscape | Minimalist: clean canvas, ample whitespace, no complex background textures. Simple cartoon elements and icons only. |

## Output Structure

```
infographic/{topic-slug}/
├── source.md
├── analysis.md
├── structured-content.md
└── prompts/infographic.md

final image → imgs/<YYMMDD>-<slug>.png
```

Working files live in `infographic/{topic-slug}/`. The final image always lands in `imgs/`, following this repo's `YYMMDD-slug` filename convention (see `ai-thoughts/AGENTS.md`).

- `{topic-slug}`: 2-4 words kebab-case from the topic. If that folder already exists, append `-YYYYMMDD-HHMMSS`.
- Final image name: `imgs/<YYMMDD>-<slug>.png`. `<slug>` is a 2-4 word kebab-case name. `<YYMMDD>` is the current date. When the source is an ai-thoughts article, use that article's `YYMMDD` prefix instead, so the image shares it.

## Core Principles

- Preserve source data faithfully. Do not summarize or rephrase it. Strip any credentials, API keys, tokens, or secrets before you write an output file.
- Define learning objectives before structuring content
- Structure for visual communication (headlines, labels, visual elements)
- Report to the user in short, actionable updates. Add detail only when the user asks.

## Workflow

### Step 1: Setup & Analyze

**Load references**: Read `references/analysis-framework.md` from this skill.

1. Save source content (file path or paste → `source.md` using `write`)
   - **Backup rule**: If `source.md` exists, rename to `source-backup-YYYYMMDD-HHMMSS.md`
2. Analyze: topic, data type, complexity, tone, audience
3. Detect source language and user language
4. Extract design instructions from user input
5. Save analysis to `analysis.md`
   - **Backup rule**: If `analysis.md` exists, rename to `analysis-backup-YYYYMMDD-HHMMSS.md`

See `references/analysis-framework.md` for detailed format.

### Step 2: Generate Structured Content → `structured-content.md`

Transform content into infographic structure:
1. Title and learning objectives
2. Sections with: key concept, content (verbatim), visual element, text labels
3. Data points (all statistics/quotes copied exactly)
4. Design instructions from user

**Rules**: Markdown only. Do not add new information. Core Principles and Pitfalls 1–2 govern data fidelity and secret stripping.

See `references/structured-content-template.md` for detailed format.

### Step 3: Recommend Combinations

**3.1 Check Keyword Shortcuts first.** If the user input matches a keyword in the **Keyword Shortcuts** table, select that layout. Offer the associated styles first. Skip content-based layout inference.

**3.2 Otherwise**, recommend 3-5 layout×style combinations based on:
- Data structure → matching layout
- Content tone → matching style
- Audience expectations
- User design instructions

### Step 4: Confirm Options

Use the `question` tool to confirm options with the user. Ask all three in one call when they apply — skip Q3 when the source language already matches the user's:

**Q1 — Combination**: Present the 3–5 layout×style combos from Step 3 with their rationale. Ask the user to pick one.

**Q2 — Aspect**: Ask for aspect ratio preference (landscape/portrait/square or custom W:H).

**Q3 — Language**: Ask which language the text content should use.

If the user already specified all options, skip Step 4.

### Step 5: Generate Prompt → `prompts/infographic.md`

**Backup rule**: If `prompts/infographic.md` exists, rename to `prompts/infographic-backup-YYYYMMDD-HHMMSS.md`

**Load references**: Read the selected layout from `references/layouts/<layout>.md` and style from `references/styles/<style>.md`.

Combine:
1. Layout definition from `references/layouts/<layout>.md`
2. Style definition from `references/styles/<style>.md`
3. Base template from `references/base-prompt.md`
4. Structured content from Step 2
5. **One text-accuracy block. Put every renderable string there, and nowhere else.** The block sits near the top of the prompt. These rules prevent duplication:
   - Wrap every renderable string in backticks. Write every reference to a string as **plain text without backticks**. That covers a constraint sentence, a note to spell a string exactly, and a per-cell imagery hint. Then the backticked spans are exactly the renderable set.
   - Do **not** append a second label dump at the end of the prompt. The base template deliberately has no `Text labels:` tail. Do not add one.
   - Do **not** repeat cell headings in the layout guidance, the style guidance, or the per-cell imagery notes. Refer to cells by position.
   - Prose carries *meaning*. If a sentence would contain an exact label string, rephrase the sentence.
   - State that each string appears **exactly once**. State that no word outside the block may appear as text.
   - For CJK content (Chinese, Japanese, Korean), add two things to the block. First, name every rare or look-alike character with its forbidden substitutes (菂 not 药、蔷 not 蓄、茄 not 茹、蕊 not 芯). Second, state that every string and every card appears **exactly once**.
   - Never tell the model to drop the least important label. Name the protected lists instead. Without them it drops a required chip: `Markdown` once vanished from a stack cell.

**Resolve `{{ASPECT_RATIO}}` here. This is the only place.**
- Named preset: `landscape` → `16:9`, `portrait` → `9:16`, `square` → `1:1`.
- A custom W:H ratio passes only if the model accepts it. Gemini accepts `16:9`, `9:16`, `1:1`, `3:4`, `4:3`, `21:9`, `1:4`, `4:1`, `1:8`, `8:1`. For any other ratio, use the nearest accepted ratio and tell the user.

Save the assembled prompt to `prompts/infographic.md` using `write`.

### Step 6: Generate Image

**The checker (hard stop).** Before generating, run the checker on the assembled prompt:

```bash
python .opencode/skills/custom-infographic/scripts/check_prompt_text.py \
  infographic/{topic-slug}/prompts/infographic.md
```

It fails with exit 1 in three cases. A backticked string appears more than once. A second label enumeration is present. With `--strings <file>`, an expected string is missing. **Do not generate after a failure. Fix the prompt and run the checker again.**

Run the bundled generator with the prompt from Step 5. Write the final image to `imgs/` with the repo-convention filename:

```bash
python .opencode/skills/custom-infographic/scripts/generate_image.py \
  --prompt infographic/{topic-slug}/prompts/infographic.md \
  --output imgs/{YYMMDD}-{slug}.png \
  --aspect 16:9
```

- The final image goes to `imgs/<YYMMDD>-<slug>.png` (repo convention, see Output Structure) — never to `infographic/{topic-slug}/`.
- `--aspect` takes the value resolved in Step 5 — do not re-derive it here.
- The default model is `google/gemini-3.1-flash-image`. Pass `--model` to use another one. Pitfall 6 gives the key requirement and the fallback.
- If the call fails, follow this order: **retry once → change `--model` → deliver the prompt-only outputs** (Pitfall 6). A second refusal from the *same* model points at the model, not the prompt. On 2026-11-12 `google/gemini-3.1-flash-image` returned `content: null` twice for a prompt that `google/gemini-nano-banana-2.1` produced first try. A refusal leaves the previous image in place. Check the size or mtime before you claim success.
- **Backup rule**: If the target `imgs/<YYMMDD>-<slug>.png` already exists, rename it to `imgs/<YYMMDD>-<slug>-backup-YYYYMMDD-HHMMSS.png` before writing. Never overwrite silently.

### Step 7: Output Summary

Report the topic, layout, style, aspect, language, output path (`imgs/<YYMMDD>-<slug>.png`), and the files you created.

## References

- `references/analysis-framework.md` — Analysis methodology
- `references/structured-content-template.md` — Content format
- `references/base-prompt.md` — Prompt template
- `references/layouts/<layout>.md` — 21 layout definitions
- `references/styles/<style>.md` — 21 style definitions
- `references/workflow-example.md` — Example workflow when image generation is unavailable
- `scripts/generate_image.py` — OpenRouter image generator (Step 6)
- `scripts/check_prompt_text.py` — the checker: fails a prompt that would duplicate a string (Step 6)

## Pitfalls

1. **Data integrity is paramount** — never summarize, paraphrase, or alter source statistics. "73% increase" must stay "73% increase", not "significant increase".
2. **Strip secrets** — always scan source content for API keys, tokens, or credentials before including in any output file.
3. **One message per section.** Each section carries one clear concept. An overloaded section reduces readability.
4. **Style consistency.** Apply the style definition from the references file across the whole image. Do not mix styles.
5. **Aspect ratio support** — Step 5 holds the only resolution rule. The generation call never re-maps a ratio.
6. **API availability.** Generation fails without `OPENROUTER_API_KEY`, or when the model cannot output images. Verify the key first. Step 6 gives the recovery order: retry, change model, and only then deliver the prompt-only outputs. Tell the user.
7. **Verify the render, not just the prompt** — the Text Accuracy block defined in Step 5 is mandatory. After generation, check every rendered string against that list with a vision model (e.g. `opencode run --model openrouter/z-ai/glm-4.6v --file`). Garbled, misspelled, dropped or doubled text means the image is not deliverable — fix the prompt and re-render. For a number or a short identifier, crop that region to 300% and read it again. A full-frame look misses a single wrong digit.
8. **Check CJK glyphs one by one.** Treat CJK rendering as a hard requirement, not a nice-to-have. After generation, compare every rendered glyph against the expected list, character by character. Use a vision model, or read the image directly. Watch for rare characters replaced by a common look-alike (菂→药、蔷→蓄、茄→茹), Simplified/Traditional swaps, dropped or doubled characters, and wrong-but-plausible variants. If any glyph is wrong, stop. Do not deliver the image. **Talk to the user** and offer three options: accept a documented variant, re-render with another model, or rephrase the label. Never ship a mis-rendered name silently.
9. **No duplicated data, text or image.** The image must not repeat a text string (names, labels, the title, an arc line) or duplicate imagery (echoed illustrations, cloned cells). **Prevent it at the prompt.** Use one enumeration only (Step 5). Add no trailing label dump. Do not repeat cell headings in the layout guidance. **A clean check is necessary, not sufficient.** The checker reads the prompt and never the pixels (Pitfall 16). Verify the finished image too (Pitfalls 7, 8). If duplicates appear, regenerate or simplify the layout. Never deliver duplicated content.
10. **Describe cells by geometry, never by content.** The layout section may say *where* a cell sits and *what shape* fills it. It must not say what the picture depicts. A sentence like "a neat stack of five books beside a cart of thirty" is read as content and drawn wherever it fits, often twice. The checker passes because no string repeated, but the illustration does. Put meaning in the abstract closing paragraph only. Keep the layout section positional: "middle-right card, two halves, left calm, right piled." Observed 2026-11-04 on the `261022-agent-not-model` image. Two renders duplicated the comparison and the loop card, until the layout prose was reduced to pure geometry.
11. **A proper noun shared between the title and a label is duplication the checker cannot see.** The checker compares whole backticked strings. A ring label `HERMES` passes even when the subtitle already reads `HERMES AGENT ON A DISCORD SERVER`. Read the finished image for shared *words*, not only shared strings. Rename one side: subtitle or label, never both. Observed 2026-11-08 on the `261107-hermes-discord-private` image. The first render repeated the product name. A neutral subtitle fixed it.
12. **Change one variable at a time from the last good image.** A re-render that alters a string *and* a layout sentence can regress the whole composition. On 2026-11-08 the second image shifted every ring label one band inward. It also moved the centre label into a callout and merged two boxes. The prompt change had looked harmless. Keep the prompt that produced the last good image. Change exactly one line and re-render. On regression, revert to that prompt instead of layering another fix.
13. **A border that exists is not a border that reads.** A thin accent stroke can close a rectangle on all four sides and still look open once the image is scaled down. Ten pixels from a neighbouring band's white border, the two lines merge into one. Two prompt changes travel together here, and this is the documented exception to Pitfall 12. Draw the accented border at roughly twice the other stroke weights. Keep at least half a band-height between bands. Verify at the size the image will be *displayed*, not at 1:1. Observed 2026-11-10 on `261105-hermes-skill-costs`: the amber edge vanished in the banner but was intact in the full-size file.
14. **A re-render orphans its derivatives.** If a banner or other crop already exists for this image (`imgs/<name>-banner-twitter.png`), ask before you replace it. `resize-for-banner` requires that confirmation. Regenerate the derivative from the new image in the same step, and say so in the report. Otherwise the article and the social card show different pictures, and only one of them is the one you approved.
15. **A 200 with no image is a model failure, not a prompt failure.** `generate_image.py` exits 1 with `no images in response`. It leaves any previous file untouched, so a rerun whose stderr nobody reads looks like a successful render. Check the output's size or mtime. After two identical refusals, change `--model` instead of retrying a third time. On 2026-11-12 `google/gemini-3.1-flash-image` returned `content: null` twice. `google/gemini-nano-banana-2.1` rendered that prompt on the first attempt.
16. **A clean prompt can still render a duplicate.** The checker inspects the prompt, never the pixels. It passed while the image carried `TABLES BECOME SCREENSHOTS` twice, once mid-frame and once in the caption strip. Two defences, both in the layout section. First, name the zone each string lives in: "the caption exists only in the caption strip, the channel label only in the channel". Second, do not offer a decorative text slot. A title block described as "a heading, a rule, and one smaller line under the rule" will take whichever label has nowhere else to go. On 2026-11-12 the subtitle line swallowed `LINKEDIN`, which then vanished from its platform.
17. **Say what must NOT appear in the gap.** A layout that describes "two masses and the empty space between them" invites a third one. The model drew a third box in the channel and put the channel label inside it, so the label read as a platform. Add the negative explicitly: "no third slab, box or block anywhere in the channel". The same prompt then re-renders correctly. This is one added constraint, so it does not break Pitfall 12. Absence needs to be stated, not implied.

18. **A label set with no stated pairing gets shuffled.** Two strings can share one slot: a component name and its descriptor, or a heading and its subtitle. The renderer then assigns them arbitrarily, and the checker cannot see it, because every string still appears exactly once. Either state the pairing, or delete one of the two strings so each slot has one candidate. `hub-spoke` on 2026-11-12 needed two re-renders. The hub took a tool name, and the descriptors landed under the wrong nodes. Removing the descriptors fixed it.

## Credits

- **Original author**: 宝玉 (JimLiu) — the baoyu layout × style system, [JimLiu/baoyu-skills](https://github.com/JimLiu/baoyu-skills) v1.56.1.
- **Ported & customized by**: j3ffyang — OpenCode adaptation and this repo's `imgs/` output convention.
