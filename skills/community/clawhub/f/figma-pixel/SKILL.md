---
name: figma-pixel
description: Figma-to-frontend visual QA workflow for building pages from Figma designs and tightening existing implementations. Captures the target page, exports the selected Figma frame, runs pixel and layout comparisons, and produces local reports that guide spacing, typography, color, and structure fixes. Use when a user provides a Figma URL and asks to build, recreate, compare, match, restyle, or improve a web UI.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata:
  openclaw:
    emoji: 📐
    requires:
      env:
        - FIGMA_TOKEN
---

# Figma Pixel

## Overview

Use this skill when a user shares a Figma link and wants to build a page from that design or bring an existing implementation closer to it.
Treat Figma as the source of truth.

This skill has two layers:
- **Scripts** — automated: parse Figma URLs, fetch API data, export reference images, render pages with Playwright, run pixelmatch/OpenCV comparison, and generate reports.
- **Agent** — guided: the LLM reads Figma API data and diff reports, then writes or edits HTML/CSS to fix mismatches. Layout fixes are made by the agent, not by the scripts.

The scripts do not auto-patch code. They produce the data and artifacts the agent needs to make accurate, Figma-grounded fixes.

This skill should behave in a production-ready way:
- require a valid `FIGMA_TOKEN`
- prefer stable scripted flows over ad-hoc commands
- **never create working folders, scratch files, or runtime artifacts inside the implementation project directory** — all run outputs go under the skill's own `figma-pixel-runs/` directory (i.e. alongside this SKILL.md file)
- reuse shared Figma artifacts when possible
- stop clearly on real blockers instead of silently degrading

## Setup

Prerequisites:
- `FIGMA_TOKEN` must be set
- the target page must be reachable through a stable local or remote URL
- the implementation project must allow normal page rendering, fonts, and asset loading
- the runtime environment must already provide the required Node.js packages and browser executable

Install these packages in the host environment before using the skill:

```bash
npm install playwright pixelmatch pngjs @techstark/opencv-js --save-prod
npx playwright install chromium
```

On Linux, Chromium may also require system libraries:

```bash
apt-get update && apt-get install -y libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libx11-xcb1 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpangocairo-1.0-0 libgtk-3-0
```

This skill does not install dependencies at runtime.
Without these packages, system libraries, and a working browser executable, the skill will not work fully and some flows will fail immediately.
If required packages are missing, stop and report the missing dependency clearly.

Read `references/setup.md` for environment expectations.

## Workflow

1. Read the Figma source.
2. Parse the Figma URL and fetch or reuse Figma data.
3. Check fonts used in the design and ask the user whether to connect them.
4. Export the Figma reference image.
5. Open the implementation through the most stable available URL.
6. Capture the current rendered page.
7. Compare the implementation against the design.
8. Agent makes visible layout fixes based on Figma data and diff results.
9. Re-run comparison and summarize the result. Stop — further iterations only on explicit user request.

**Never run the pipeline (or any comparison/capture script) without explicit user instruction.** Each pipeline run must be triggered by the user — do not auto-run after fixes, do not run "to verify", do not run multiple times in a row without asking between each.

Use `scripts/run-pipeline.cjs` as the primary orchestration entry point.
Prefer the pipeline over one-off script combinations unless you are debugging a specific failing stage.

Token discipline for this skill:
- Prefer compact artifacts first: `run-result.json`, `pipeline-summary.json`, `final/report.json`, `figma/viewport.json`, `figma/export-image-result.json`.
- Avoid large raw files unless the compact artifacts are insufficient.
- **Always read the diff image and the reference image visually** after each comparison run. Visual inspection catches issues (wrong asset types, missing logos, wrong colors) that numeric reports alone miss.
- Keep progress updates short and spend tokens on fixes and verification.

## Step 1, read the Figma source

- Start from the Figma URL the user provided.
- Use `scripts/parse-figma-url.cjs` to extract file key and node id.
- Use `scripts/fetch-figma-api.cjs` to fetch file and node data when API access is available.
- Use Figma API output and Figma screenshots as the visual truth.
- Prefer the exact requested frame/node over guessing from nearby content.
- Read visual properties directly from Figma API data whenever available instead of approximating them by eye.
- Treat Figma fills, strokes, effects, typography, corner radius, bounds, spacing, and image references as authoritative implementation inputs.

Read `references/figma.md` for the expected Figma input layer.

## Step 2, prepare the reference image

- Start each comparison run by creating a dedicated run folder with `scripts/init-run-dir.cjs`.
- Store all outputs under the skill's `figma-pixel-runs/<project-slug>/<run-id>/` directory — this folder lives next to SKILL.md, not inside the implementation project.
- Reuse shared Figma artifacts under `figma-pixel-runs/<project-slug>/shared/figma/` so repeated runs for the same file/node do not refetch the same Figma file, node, and reference image every time.
- Save the Figma-derived reference image in that run directory.
- Do not create ad-hoc working folders or scratch assets inside the implementation project for Figma processing, such as `.figma-source`, temporary export caches, or other non-project runtime files. Keep working files in the run directory or shared cache only.
- Derive viewport width and height from the Figma frame/node bounds, not from hardcoded values.
- Derive block, card, panel, image, and section width and height from Figma bounds instead of eyeballing proportions.
- Match section spacing from Figma, including padding, gap, inter-section spacing, and internal content spacing.
- Treat the exported Figma reference PNG as the exact visual target for comparison only. Without the reference image, visual matching is unreliable.
- **Never use the whole Figma frame/page export as the implementation itself.** Do not place the full reference PNG/SVG/PDF/canvas export into the page as a hero image, background image, visual layer, screenshot layer, or hidden overlay. A valid implementation must be real HTML/CSS structure for the page sections, text, layout, backgrounds, dividers, spacing, and typography.
- Before finalizing a build-from-Figma task, scan implementation files and fail the work if they reference full-frame exports such as `reference-image.png`, `figma-reference.png`, `full-page.png`, `screenshot.png`, or any exported image whose dimensions match the root Figma frame. Remove those references and implement the layout with markup/CSS instead.
- Use real Figma-derived screenshots, exports, or crops only for localized visual content inside the design. Do not invent placeholder preview images, surrogate mock panels, or decorative stand-ins when the Figma design already shows the real visuals.
- When the design includes embedded preview panels, screenshots, or UI previews, prefer inserting those localized child-node images instead of recreating approximate placeholders.
- **If a child FRAME or GROUP node contains a complex UI mockup** (panel, component showcase, screenshot, tool window, or any multi-element composition that would require significant HTML/CSS to recreate), **export only that child node as PNG via the Figma images API and reference it with `<img>`**. Do not export the root/page frame for this purpose. The Figma images API endpoint is `GET /v1/images/{fileKey}?ids={nodeId}&format=png&scale=2`. Save exported child-node PNGs to the implementation project's public/static directory and reference them directly. This is the single most impactful action for pixel accuracy — hand-coded approximations of UI mockups will always diverge from the Figma reference.
- If the Figma node uses image fills or exportable assets, extract and use those assets instead of substituting similar images.
- Keep the viewport/frame size explicit.
- Preserve enough metadata to trace the comparison later: URL, node id, size, label.

Read `references/artifacts.md` for the expected artifact set.

## Step 2b, check and connect fonts

After fetching Figma data, extract the list of unique font families used in the design.
Read `fontFamily` values from `figma/design-tokens.json` (typography array) if available, or from `figma-node.json` directly.

**First classify each font as system or non-system — do not import system fonts.** System fonts ship with the OS; adding `<link>` / `@import` for them does nothing on the target platform but may trigger unnecessary network requests and makes the CSS misleading. Only non-system fonts need to be connected.

For system fonts, reference them directly in a `font-family` stack with appropriate OS-level fallbacks. When a design splits a single family into display/text variants, prefer a single font variable with the display family rather than two CSS variables — unless the user explicitly asks for the split.

**For non-system fonts, automatically connect them without asking the user.** Do not stop or prompt — just add them.

- If the fonts are already present in the implementation (referenced in CSS or loaded via a font provider), skip and proceed.
- For each missing non-system font, add a `<link rel="preconnect">` + `<link rel="stylesheet">` for Google Fonts (or the appropriate CDN) to the implementation's HTML `<head>`.
- For CSS-only projects, add `@import url(...)` at the top of the main stylesheet.
- Playwright already waits for `document.fonts.ready`, so no extra delay is needed.

If you cannot confidently classify a family as system vs non-system (obscure corporate font, custom foundry name, etc.), ask the user once rather than guessing — importing the wrong family or missing one both cause layout reflow.

## Step 2c, extract implementation spec (spec-first)

After fetching Figma data and before writing any HTML/CSS, run:

```bash
node scripts/extract-implementation-data.cjs <path-to-figma-node.json>
```

This produces `implementation-spec.json` in the same directory as `figma-node.json`.
When using `run-pipeline.cjs`, this file is generated automatically — check `artifacts.implementationSpec` in the run result.

The spec gives you in one file:
- `viewport` — exact frame dimensions (width × height)
- `sections[]` — full annotated node tree with `bounds` (relative to root 0,0), `fill`, `stroke` (including `individualStrokeWeights` + `dashPattern` when present), `cornerRadius`, `layout` (auto-layout mode/padding/gap), `effects`
- `texts[]` — flat list of every text node with `characters`, `style`, and (when present) `styledRuns[]`
- `fonts[]` — unique font families used
- `colors[]` — all fill colors sorted by frequency, as `{ hex, count }`
- `warnings[]` — nodes with `visible=false`, invisible fills, and TEXT nodes with inline style overrides

**Use `implementation-spec.json` as the primary reference when building or fixing layout.** Avoid repeated ad-hoc queries against the raw `figma-node.json` — the spec captures everything needed in a single structured pass.

**Read `warnings[]` immediately — before writing a single line of HTML or CSS.** Every entry is either a hidden node, an invisible fill, or a TEXT node that contains inline style overrides. Do not skip this check.

**Check `styledRuns[]` on every TEXT entry before writing markup.** When a `texts[]` entry has `styledRuns`, the text contains mixed styling — bold spans, colour changes, or font-weight overrides. Render each run using the appropriate inline element (`<strong>`, `<em>`, or `<span>`) with styles derived from `styledRuns[].style`. Ignoring `styledRuns` produces flat-weight text that causes layout reflow and pixel mismatches. Each run: `{ start, end, characters, style }` where `style` is already the merged result of the base style and the Figma override.

**Before writing or editing ANY text-bearing CSS, read `typography-map.json`.** `run-pipeline.cjs` generates it next to `implementation-spec.json` (path under `artifacts.typographyMap`). It is a deduped list of every unique text style in the design — each entry has `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `lineHeightPx`, `letterSpacing`, `color`, `occurrences`, and `samples`. Use these values verbatim for every text rule. Do not eyeball typography from the reference image, do not default to "none" on `letter-spacing` or `1` on `line-height`. Every one of the six typography fields — family, size, weight, style, line-height, letter-spacing — must come from `typography-map.json`.

**Before writing or editing ANY margin / padding / gap, read `spacing-map.json`.** `run-pipeline.cjs` generates it next to `implementation-spec.json` (path under `artifacts.spacingMap`). It is a flat list of every auto-layout container with its `mode`, `paddingTop/Right/Bottom/Left`, `itemSpacing`, and `bounds`, plus a `summary` of unique gap and padding values used in the design. Each entry has a `path` breadcrumb (e.g. `Section > Content > Texts`) so you can locate the exact Figma node for any container you render. Cite a concrete entry when picking a spacing value — if no auto-layout node matches the element you are styling, that is a blocker, not an invitation to guess.

**Before writing or editing ANY border / outline / divider CSS, read `strokes-map.json`.** `run-pipeline.cjs` generates it next to `implementation-spec.json` (path under `artifacts.strokesMap`). It is a flat list of every node with a visible Figma stroke — each entry has `path` (breadcrumb), `bounds`, `color`, `weight`, `align`, `sides[]` (which of top/right/bottom/left are active), `perSideWeight`, `dashPattern`, and `cornerRadius/cornerRadii`, plus a `summary` of unique colors, weights, and side-distribution. **Partial strokes (single-side borders like a header's bottom divider or a footer's top divider) are the most commonly missed property** — Figma expresses them via `individualStrokeWeights`, and they render as thin horizontal or vertical lines that are easy to dismiss as diff artifacts. Every `border*` / `outline*` / horizontal or vertical divider in CSS must trace to an entry here. If a section header or footer appears in `strokes-map.json` with `sides: ["bottom"]` or `sides: ["top"]`, that is a required `border-bottom` / `border-top` — do not treat it as optional decoration. For light backgrounds Figma usually uses a dark stroke color and vice versa; always read `color` from the entry rather than guessing from the section background.

To generate these manually (if running scripts individually instead of via the pipeline):

```bash
node scripts/extract-typography.cjs <path-to-implementation-spec.json>
node scripts/extract-spacing-map.cjs <path-to-implementation-spec.json>
node scripts/extract-strokes-map.cjs <path-to-implementation-spec.json>
```

Read `references/scripts.md` for the exact argument format and output contract.

## Step 3, build initial implementation (if starting from scratch)

Skip this step if an implementation already exists — go directly to Step 4.

If no implementation exists yet:
- Read `implementation-spec.json` (from Step 2c) for frame bounds, layout structure, colors, typography, spacing, and component hierarchy.
- Detect the project type from context: check for `package.json`, framework config files (`next.config.*`, `vite.config.*`, `nuxt.config.*`, etc.), or ask the user if unclear.
- Create the implementation using the conventions of the detected stack — follow its standard file and component conventions, and match the styling approach already used in the project.
- Use Figma-derived values for all properties — do not invent defaults.
- Do not add placeholder content or lorem ipsum when Figma already defines real content.
- After creating the file(s), continue to Step 4.

## Step 4, open the implementation stably

Prefer the most stable path that avoids unnecessary build-tool churn.

Use this order:
1. Existing stable local URL provided by the user.
2. Static serve of already-built files.
3. Static serve directly from source for simple HTML/CSS pages.
4. Project dev/build pipeline only when needed and healthy.

Do not get stuck debugging Vite, bundlers, or optional native dependencies unless the user explicitly wants pipeline repair.
If the page can be served statically, prefer that.

## Step 4, capture the current render

- Use `scripts/render-page.cjs` for deterministic capture.
- Wait for fonts and images.
- Disable animations and transitions before screenshotting.
- Capture full-page when comparing full-page designs.
- Record failed requests and bad responses.

If browser lookup is flaky, use `CHROMIUM_PATH` or `PLAYWRIGHT_MODULE_PATH` as explicit overrides.

## Step 5, compare the result

Use the available comparison tooling to produce a reliable visual diff.
Prefer the existing scripted comparison flow.
Use Playwright render capture and pixelmatch as the primary reliable comparison path.
When available, run the optional Node.js post-processing step after `pixelmatch` to group raw pixel differences into larger mismatch regions.

Always try to produce these artifacts:
- reference image
- rendered screenshot
- diff-region report when the runtime is available
- diff image
- mismatch percentage
- machine-readable report

`run-pipeline.cjs` runs a tile comparison automatically (300px horizontal bands) and writes `pixelmatch/tile-report.json`. Read `tileCompare.topMismatchTiles` from the run result to identify the highest-mismatch vertical zones first. Each tile entry includes `sectionName` and `sectionRelativeY` — use these to know which section to inspect without manually dividing by section height.

**Visually inspect top mismatch tiles before looking at the full-page diff.** For each top tile, crop the reference, screenshot, and diff images at the exact tile y-coordinates and read them with the Read tool. Use `scripts/crop-tile.cjs` for precise cropping (platform crop tools like `sips` use unreliable coordinate systems):

```bash
node scripts/crop-tile.cjs <src.png> <dst.png> <y> <height>
```

Tile-level inspection identifies the actual cause of each mismatch zone — missing borders, wrong icon direction, layout shift from text height differences — rather than guessing from the full-page view.

After inspecting the top tiles, **read all three full-page images** (reference, screenshot, diff) using the Read tool for a structural overview. Full-page inspection catches issues that span multiple tiles: wrong section count, missing sections, wrong page height, or broad color/background mismatches.

OpenCV runs **per tile** on the top 3 highest-mismatch bands (not on the full image), so it works correctly for full-page designs of any height without WASM memory issues. Each reported region includes `tileY` (the tile's absolute Y offset) and `y` (absolute Y coordinate in the full image).

After each run, `run-result.json` is written to the run directory as soon as pixelmatch and tile comparison finish — before OpenCV. Read it first: it contains `mismatch` (diffPercent), `delta` (change vs previous run), `tileCompare.topMismatchTiles`, and `artifacts` paths. If the pipeline crashes after tile comparison, `run-result.json` still exists with the essential data.

## Step 6, make visible layout fixes

This step is performed by the agent, not by the scripts.
The agent uses Figma API data, reference images, and diff reports from previous steps to decide what to change, then edits the implementation files (HTML, CSS, assets) directly.

Before making fixes, read `tileCompare.topMismatchTiles` from `run-result.json` to identify the highest-mismatch vertical zones. Each tile includes `y` (absolute pixel offset), `sectionName`, and `sectionRelativeY`. Fix the highest-mismatch sections first, then move to lower-mismatch areas.

Prioritize the biggest contributors first:
- wrong section backgrounds
- missing or duplicated structural blocks
- wrong hero height or heading scale
- wrong section spacing and proportions
- missing right-column content in comparison sections
- missing repeated footer/meta rows when present in design
- oversized or undersized preview panels
- extra bottom whitespace or wrong page ending
- mismatched colors, corner radius, typography, or imagery

Prefer visible, direct fixes over refactors.
Do not implement nodes where `visible === false` in the Figma API — these are hidden layers and must be skipped entirely. Check `visible` on every node before using its content, fills, or dimensions.
Do not invent new content if the design already defines it.
Do not replace real preview visuals with invented placeholders when Figma already provides the real screenshot or crop source.
Use Figma API data and screenshots to ground spacing, sizing, structure, embedded preview imagery, color decisions, corner radius, borders, effects, and typography.
Do not invent page, section, card, or preview colors when the Figma file already defines them. Read and match section backgrounds, text colors, fills, borders, and accents directly from the Figma source.
Matching colors directly from Figma can materially reduce mismatch and should be preferred over manual palette guessing.
Read and apply `cornerRadius` or `rectangleCornerRadii` from Figma for cards, buttons, inputs, images, and preview panels instead of defaulting to generic border radius values.
Match typography from Figma, including font family, font size, font weight, line height, letter spacing, and text alignment.
Match borders and visible effects from Figma, including stroke width, stroke color, shadow, blur, and opacity when they materially affect the rendered result. Consult `strokes-map.json` for every border decision — including partial/single-side strokes (header bottom dividers, footer top dividers, card outlines). A thin horizontal line visible in the diff is almost always a missing `border-bottom` / `border-top` from a node with `individualStrokeWeights` set on one side; do not dismiss such lines as antialiasing or rendering artifacts.
Use the correct Figma-derived assets for images, thumbnails, screenshots, and fills. If an asset cannot be extracted from Figma, report the blocker clearly instead of silently substituting an incorrect image.
Prefer exact layout dimensions from Figma bounds over approximate CSS values. Avoid "close enough" sizing when the design provides exact measurements.

## Step 7, re-run and summarize

After each pass, read `run-result.json` first — it is the single compact source of truth for a run:
- `mismatch` — diffPercent for this run
- `delta` — change vs the previous run (negative = improvement)
- `previousRun` — `{ runId, diffPercent }` of the run before this one
- `tileCompare.topMismatchTiles` — ranked zones to fix next, each with `sectionName` and `sectionRelativeY`
- `artifacts.*` — paths to all generated files

Summarize:
- current mismatch percentage and delta vs previous run
- top remaining mismatch tiles
- biggest visible changes made
- blockers, if any

When checking prior results, prefer `run-result.json` over rereading large markdown or raw tool logs.

`final/report.json` and `final/summary.md` are generated by `run-pipeline.cjs` automatically. If they are missing (pipeline crashed before reaching that step), run:

```bash
node scripts/generate-layout-report.cjs \
  --output <run-dir>/final \
  --figma <figma-url> \
  --page <page-url> \
  --viewport <WxH> \
  --reference <run-dir>/figma/reference-image.png \
  --screenshot <run-dir>/capture/captured-page.png \
  --diff <run-dir>/pixelmatch/diff.png \
  --pixelmatch-report <run-dir>/pixelmatch/report.json
```

If tooling failed but useful artifacts exist, say so plainly and continue with the best available diff method.
If the page is unreachable, `FIGMA_TOKEN` is missing, or required artifacts cannot be produced, stop and report the blocking reason clearly.
At the end of the task, ask the user whether they want to clean up working files under `figma-pixel-runs/<project-slug>/` before deleting anything.

## Step 8, stop after one run

After summarizing results, stop. Do not ask whether to run another iteration and do not start one automatically.

If the user explicitly requests another pass (e.g. "run again", "fix more", "next iteration"), return to Step 6 and repeat from there. Otherwise the task is done.

## Output contract

When this skill is used, always try to return:
- Figma source used
- reference image path
- rendered screenshot path
- diff image/report path
- mismatch percentage
- short human-readable layout summary
- top visible mismatches
- what was changed
- what failed, if anything
- whether colors, radius, dimensions, spacing, typography, and images were matched or remain incorrect

Before considering the task done, verify this fidelity checklist:
- colors match Figma API values
- corner radius matches Figma
- dimensions match Figma bounds
- spacing, padding, and gaps match Figma — every margin / padding / gap value must trace to a specific container entry in `spacing-map.json`; do not mark done if any value is eyeballed or picked as a round default
- typography matches Figma — verify every one of the six fields (`fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `lineHeightPx`, `letterSpacing`) against `typography-map.json` for each text style used; do not mark done if any field is eyeballed or defaulted
- correct Figma-derived images or exports are used
- no invented placeholders remain where Figma provides real assets

## Security

- **FIGMA_TOKEN**: use a token with the minimum scope needed (read-only file access). Rotate the token if you suspect exposure. The skill does not persist the token in artifacts or logs, but verify your environment before sharing run outputs.
- **Playwright / Chromium**: the render step loads the target page URL in a headless browser. Network requests from the page will be executed. Run in an isolated environment (container, sandbox) if loading untrusted pages.
- **Artifacts**: screenshots and Figma exports under `figma-pixel-runs/` may contain sensitive UI content. Review and clean these folders before sharing or committing them.

## References

- Read `references/figma.md` for the Figma input layer.
- Read `references/workflow.md` for a concise execution checklist.
- Read `references/artifacts.md` for the run directory contract and expected artifact outputs.
- Read `references/scripts.md` for the exact CLI usage of every script, including `extract-implementation-data.cjs`.
