# Script API Reference

Quick reference for every script in `scripts/`. All paths are relative to the skill root.

---

## `parse-figma-url.cjs`

```
node scripts/parse-figma-url.cjs <figma-url>
```

**Input:** any Figma URL (design, proto, file).  
**Output (stdout):** JSON with `{ fileKey, nodeId, url, pathname }`.  
**Errors:** exits 1 if URL is not parseable.

---

## `fetch-figma-api.cjs`

```
node scripts/fetch-figma-api.cjs <figma-url> [output-dir]
```

**Input:**
- `figma-url` — full Figma URL (must include `node-id` for node data)
- `output-dir` — directory to write JSON files (default: `figma-pixel-runs/project/run-id/figma`)

**Env:** `FIGMA_TOKEN` must be set.

**Output (stdout):** `{ ok, fileKey, nodeId, nodePath }`.  
**Files written:**
- `<output-dir>/figma-node.json` — raw Figma node API response

**Notes:** The script writes to exactly the `output-dir` you provide. Always pass an explicit path.

---

## `extract-implementation-data.cjs`  ⬅ spec-first step

```
node scripts/extract-implementation-data.cjs <figma-node-json> [output-path] [max-depth]
```

**Input:**
- `figma-node-json` — path to `figma-node.json` from `fetch-figma-api.cjs`
- `output-path` — where to write `implementation-spec.json` (default: same dir as input)
- `max-depth` — tree walk depth (default: 6)

**Output (stdout):** `{ ok, outputPath, viewport, sections, texts, richTextNodes, fonts, warnings, topColors }`.  
**Files written:** `implementation-spec.json` — full annotated tree with:
- `sections[]` — top-level frames with `bounds` (relative to root 0,0), `fill`, `stroke`, `cornerRadius`, `layout` (auto-layout), `effects`
- `texts[]` — flat list of every text node with `characters`, `style`, and (when present) `styledRuns[]`
  - `styledRuns[]` — present when the node contains inline style overrides (e.g. a bold phrase inside a regular paragraph). Each run: `{ start, end, characters, style }` where `style` is the fully merged style for that span. Use these to emit `<strong>`, `<em>`, or `<span>` elements — do not ignore them.
- `fonts[]` — unique font families
- `colors[]` — unique fill colors sorted by frequency
- `warnings[]` — hidden nodes (`visible=false`), invisible fills, TEXT nodes with inline style overrides

**When to use:** run this right after `fetch-figma-api.cjs`, before writing any HTML/CSS.  
It replaces ad-hoc `python3 -c` queries against the raw JSON.

---

## `extract-typography.cjs`  ⬅ typography gate

```
node scripts/extract-typography.cjs <implementation-spec.json> [output-path]
```

**Input:**
- `implementation-spec.json` — output of `extract-implementation-data.cjs`
- `output-path` — where to write `typography-map.json` (default: same dir as input)

**Output (stdout):** `{ ok, outputPath, count }`.  
**Files written:** `typography-map.json` — deduped list of every unique text style used in the design. Each entry:
- `key` — internal dedupe key
- `fontFamily`, `fontSize`, `fontWeight`, `fontStyle`, `lineHeightPx`, `letterSpacing`, `color` — the six+1 typography fields from Figma
- `occurrences` — how many text nodes share this style
- `samples[]` — up to three example `characters` strings

**When to use:** `run-pipeline.cjs` generates this automatically alongside `implementation-spec.json`. Read it before writing or editing any text-bearing CSS. Every typography field on every text rule must come from here — eyeballing letter-spacing or line-height is the single most common cause of residual pixel mismatch.

---

## `extract-spacing-map.cjs`  ⬅ spacing gate

```
node scripts/extract-spacing-map.cjs <implementation-spec.json> [output-path]
```

**Input:**
- `implementation-spec.json` — output of `extract-implementation-data.cjs`
- `output-path` — where to write `spacing-map.json` (default: same dir as input)

**Output (stdout):** `{ ok, outputPath, count }`.  
**Files written:** `spacing-map.json` — flat list of every auto-layout container. Each entry:
- `id`, `name`, `path` — Figma node id, name, and breadcrumb (e.g. `Section > Content > Texts`)
- `mode` — `HORIZONTAL` | `VERTICAL`
- `paddingTop`, `paddingRight`, `paddingBottom`, `paddingLeft`, `itemSpacing` — the five spacing values
- `bounds` — absolute `{ x, y, width, height }`

Also includes a `summary` block with `uniqueGaps` and `uniquePaddings` — the distinct values used across the design, sorted by frequency.

**When to use:** `run-pipeline.cjs` generates this automatically alongside `implementation-spec.json`. Read it before writing or editing any `margin` / `padding` / `gap` in CSS. Every spacing value must trace to a specific container entry here — picking round defaults (16, 24, 32) by eye is the other common cause of residual pixel mismatch.

---

## `extract-strokes-map.cjs`  ⬅ strokes/borders gate

```
node scripts/extract-strokes-map.cjs <implementation-spec.json> [output-path]
```

**Input:**
- `implementation-spec.json` — output of `extract-implementation-data.cjs`
- `output-path` — where to write `strokes-map.json` (default: same dir as input)

**Output (stdout):** `{ ok, outputPath, count }`.
**Files written:** `strokes-map.json` — flat list of every node with a visible Figma stroke. Each entry:
- `id`, `name`, `type`, `path` — Figma node id, name, and breadcrumb (e.g. `Section > Header`)
- `bounds` — absolute `{ x, y, width, height }`
- `color` — stroke color hex (e.g. `#222222`)
- `weight` — base `strokeWeight`
- `align` — `INSIDE` | `OUTSIDE` | `CENTER`
- `sides[]` — which of `top` / `right` / `bottom` / `left` actually carry a stroke (derived from `individualStrokeWeights`; all four when the stroke is uniform)
- `perSideWeight` — exact per-side weight (`{top, right, bottom, left}`); use this for `border-top-width` etc.
- `dashPattern` — `strokeDashes` array when present, otherwise `null`
- `cornerRadius`, `cornerRadii` — for rendering rounded borders

Also includes a `summary` block with `uniqueColors`, `uniqueWeights`, `sideDistribution` (how often each side is used), and `allSidesCount` / `partialSidesCount` (how many strokes are full-box vs single-side).

**When to use:** `run-pipeline.cjs` generates this automatically alongside `implementation-spec.json`. Read it before writing or editing any `border*` / `outline*` / divider CSS. Partial strokes (single-side borders) are the most commonly missed property in pixel-perfect work — they appear as thin lines in the diff and are easy to dismiss as antialiasing artifacts. Every border in CSS must trace to a concrete entry here.

---

## `export-figma-image.cjs`

```
node scripts/export-figma-image.cjs <figma-url> <output-png-path>
```

**Input:** full Figma URL, output path for PNG.  
**Env:** `FIGMA_TOKEN`.  
**Output (stdout):** `{ ok, outputPath, width, height }`.  
**Files written:** PNG of the exported Figma node.

---

## `init-run-dir.cjs`

```
node scripts/init-run-dir.cjs <project-slug> [run-id]
```

**Input:**
- `project-slug` — e.g. `figma-pixel-07`
- `run-id` — ISO timestamp (default: generated)

**Output (stdout):** `{ ok, runDir, projectDir, subdirs, sharedDirs, manifestPath }`.  
**Files written:** run directory structure under `figma-pixel-runs/<slug>/<run-id>/`.

---

## `render-page.cjs`

```
node scripts/render-page.cjs <page-url> <output-png-path> <viewport-width> <viewport-height>
```

**Input:** URL, output path, width, height.  
**Output (stdout):** `{ ok, url, outputPath, viewport, pageScrollHeight, failedRequests, badResponses }`.  
**Files written:** full-page PNG screenshot.

**Notes:** waits for `document.fonts.ready` before capture. Disable animations via CSS if needed.

---

## `pixelmatch-runner.cjs`

```
node scripts/pixelmatch-runner.cjs <reference-png> <screenshot-png> <diff-output-png>
```

**Output (stdout):** `{ width, height, diffPixels, diffPercent, diffPath }`.  
**Files written:** visual diff PNG.

---

## `tile-compare.cjs`

```
node scripts/tile-compare.cjs <reference-png> <screenshot-png> [output-json] [tile-height]
```

**Input:** reference PNG, screenshot PNG, optional output path, optional tile height (default: 300).  
**Output (stdout):** `{ ok, width, height, tileHeight, tileCount, tiles[], topMismatchTiles[] }`.  
**Files written:** `tile-report.json` at the output path if provided.

**`tiles[]` fields:** `{ tileIndex, y, height, diffPixels, diffPercent }` — one entry per 300px band.  
**`topMismatchTiles[]`:** top 5 tiles sorted by `diffPercent` descending.

**Notes:** use `topMismatchTiles[].y` to locate which vertical zone needs the most attention before running OpenCV or making fixes. `run-pipeline.cjs` runs this automatically and writes `pixelmatch/tile-report.json`.

---

## `opencv-analyze-diff.cjs`

```
node scripts/opencv-analyze-diff.cjs <reference-png> <screenshot-png> <diff-png> <output-report-json> [figma-node-json]
```

**Input:** reference, screenshot, diff PNGs, output path, optional figma-node.json for region-to-layer mapping.  
**Output (stdout):** `{ ok, largestRegions, summary, annotatedDiff, differenceRegionCount }`.  
**Files written:**
- `<output-report-json>` — JSON report with regions and their sizes, zones, and matched Figma layers
- `<output-report-json>` without `.json` + `-annotated.png` — diff with bounding boxes drawn

**Notes:** `largestRegions[].figmaLayers` maps each diff region to the Figma nodes that overlap it.  
Use `summary[]` for a human-readable list of the top-5 mismatches with layer names.

---

## `generate-layout-report.cjs`

```
node scripts/generate-layout-report.cjs \
  --output <dir> \
  --figma <url> \
  --page <url> \
  --viewport <WxH> \
  --reference <png> \
  --screenshot <png> \
  --diff <png> \
  [--pixelmatchReport <json>] \
  [--opencvReport <json>]
```

**Output:** `report.json` + `summary.md` in `<output-dir>`.

---

## `run-pipeline.cjs`

```
node scripts/run-pipeline.cjs <figma-url> <page-url> [project-slug] [run-id] [--compare-only]
```

**Input:**
- `figma-url` — full Figma URL
- `page-url` — URL of the running implementation
- `project-slug` — folder name under `figma-pixel-runs/` (default: `project`)
- `run-id` — ISO timestamp (default: generated)
- `--compare-only` — skip Figma fetch, use cached data

**Output (stdout):** full `run-result.json` with all artifact paths, mismatch %, and top issues.

**Note:** this orchestrates the full pipeline (fetch → screenshot → pixelmatch → opencv → report).  
It does NOT call `extract-implementation-data.cjs` — run that separately before the build step.

---

## `extract-design-tokens.cjs`

```
node scripts/extract-design-tokens.cjs <figma-node-json> [output-path]
```

**Output:** `design-tokens.json` with fills, typography, spacing, corner-radius, strokes.  
Less detailed than `extract-implementation-data.cjs`; kept for backwards compatibility.
