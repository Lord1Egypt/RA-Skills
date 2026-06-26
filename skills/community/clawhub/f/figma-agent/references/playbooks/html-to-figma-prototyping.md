# Playbook: HTML-to-Figma Prototyping

Rapid layout generation using `generate_figma_design` (Stitch/HTML-to-Figma). Trades production-readiness for iteration speed.

**When to use:** Rapid concept exploration, complex CSS layouts, existing web pages as starting points, or when speed matters more than design-system alignment. See [workflow-selection.md](../workflow-selection.md) for the full decision matrix.

---

## What This Mode Is Good For

- **Layout speed:** Complex CSS grids, flexbox layouts, and responsive structures that are tedious to replicate node-by-node in native Figma.
- **Auto-layout leverage:** HTML flex/grid structures often convert to Figma auto-layout, giving you a structural head start.
- **Visual reference:** Quickly materializing a concept so stakeholders can react to something concrete.
- **Starting point for native refinement:** Generate the skeleton, then migrate to design-system tokens and components.

## What This Mode Is NOT

HTML-to-Figma output is **never automatically production-ready**. It is a draft artifact. Specifically:

- Colors are hardcoded hex, not variable-bound
- Text nodes use fixed bounding boxes, not auto-resize (see [plugin-api-gotchas.md#text-autoresize](../plugin-api-gotchas.md#text-autoresize))
- No design-system component instances — everything is raw frames and shapes
- SVGs may replace what should be native Figma nodes
- Dimensions may contain decimal/sub-pixel values
- Spacing is absolute, not token-based

**Communicate this internally:** Frame the output as "rapid draft for layout reference" — not as a deliverable. Anyone receiving the file should know follow-up cleanup is required.

---

## Step 1: Generate the Draft

Use `generate_figma_design` with the HTML/CSS source or a description of the target layout.

- For existing web pages: provide the URL or HTML
- For new concepts: describe the layout structure explicitly — "3-column dashboard with sidebar, header, and card grid"
- Keep expectations calibrated: this is step 1 of a multi-step process

---

## Step 2: Screenshot and Evaluate

Immediately after generation:

1. `get_screenshot` of the output frame
2. Evaluate the structural result — does the layout capture the intended structure?
3. Note areas that need cleanup (list them explicitly before proceeding)

---

## Step 3: SVG Evaluation

HTML-to-Figma often produces SVGs where native nodes would be better.

| SVG Type | Action |
|----------|--------|
| Icons/logos imported from the source | **Keep** — original fidelity matters |
| Layout elements (backgrounds, dividers, decorative shapes) | **Replace** with native rectangles/lines |
| Text rendered as SVG paths | **Replace** with text nodes + `loadFontAsync` |
| Complex illustrations | **Keep** — impractical to recreate natively |

General rule: if the SVG needs variable bindings, auto-layout participation, or future editing, convert to native. See [core-rules.md — SVG Decision Matrix](../core-rules.md).

---

## Step 4: Cleanup Pass

Address issues in priority order via targeted `use_figma` calls:

### 4a. Text Auto-Resize
Fix fixed-size text boxes. Batch 5-10 text nodes per call:
```js
const nodes = figma.currentPage.findAll(n => n.type === "TEXT" && n.textAutoResize === "NONE");
for (const n of nodes.slice(0, 10)) {
  n.textAutoResize = "WIDTH_AND_HEIGHT"; // or "HEIGHT" for fixed-width containers
}
```
See [plugin-api-gotchas.md#text-autoresize](../plugin-api-gotchas.md#text-autoresize).

### 4b. Decimal Dimensions
Round sub-pixel values to integers:
```js
node.resize(Math.round(node.width), Math.round(node.height));
```

### 4c. Missing Auto-Layout
Add auto-layout to container frames that should have it but don't.

### 4d. Hardcoded Colors (Optional at This Stage)
If the prototype will be refined further, defer color tokenization to the [Color Tokenization playbook](color-tokenization.md). If this is a one-off reference, hardcoded colors are acceptable.

---

## Step 5: Validate

After cleanup:
1. `get_screenshot` — does the cleaned-up version still match the intended layout?
2. Check that text is editable (not trapped in SVG or fixed boxes)
3. Confirm auto-layout works by checking resize behavior conceptually

---

## When to Stop Here vs Continue to Native

| Scenario | Decision |
|----------|----------|
| Stakeholder review / concept validation | **Stop** — the draft is sufficient |
| One-off reference for a developer | **Stop** — add variable bindings only if needed |
| Design that will be iterated on by designers | **Continue** — run Color Tokenization, replace SVGs, add component instances |
| Production design-system artifact | **Continue** — or consider starting with [Native Screen Generation](native-screen-generation.md) instead |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Treating HTML-to-Figma output as production-ready | Hardcoded values, no design-system integration |
| Skipping the screenshot evaluation step | Issues compound during cleanup |
| Rebuilding everything natively after generation | Defeats the purpose — cleanup is cheaper than rebuild |
| Not communicating the draft status to stakeholders | Sets false expectations about design-system compliance |
