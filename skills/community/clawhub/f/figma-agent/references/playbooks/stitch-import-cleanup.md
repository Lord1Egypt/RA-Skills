# Playbook: Stitch Import Cleanup

Post-import cleanup for screens generated via HTML-to-Figma (Stitch). Stitch output is structurally usable but contains predictable artifacts that must be fixed before the screen is production-ready.

**When to use:** After any HTML-to-Figma / Stitch import, or when inspecting a frame that shows Stitch-typical issues (fixed text boxes, decimal dimensions, missing auto-resize). See [workflow-selection.md](../workflow-selection.md).

---

## Step 1: Screenshot and Identify Artifacts

```
get_screenshot(fileKey, nodeId)
```

Stitch imports typically show:
- Text that appears correct initially but **breaks on any edit** (fixed-size text boxes)
- Dimensions with decimal pixel values (e.g., `113.63px`, `247.5px`)
- SVG layout proxies where native nodes would be more editable
- Missing variable bindings (all colors are hardcoded hex)
- Flat structure instead of semantic auto-layout grouping

---

## Step 2: Fix Text Auto-Resize {#text-autoresize}

The most critical Stitch artifact. Stitch exports text nodes with `textAutoResize: "NONE"` and exact decimal widths. Any subsequent plugin write (even unrelated fills changes) can trigger a re-render that reflows text.

### Scan for Fixed Text Nodes

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const fixedTexts = frame.findAll(
  n => n.type === "TEXT" && n.textAutoResize === "NONE"
);
return fixedTexts.map(t => ({
  id: t.id, name: t.name,
  width: t.width, height: t.height,
  autoResize: t.textAutoResize
}));
```

### Apply Auto-Resize Fix

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const fixedTexts = frame.findAll(
  n => n.type === "TEXT" && n.textAutoResize === "NONE"
);
for (const t of fixedTexts) {
  await figma.loadFontAsync(t.fontName);
  t.textAutoResize = "WIDTH_AND_HEIGHT";
}
return { fixed: fixedTexts.length };
```

**Choosing the resize mode:**

| Mode | When to Use |
|------|------------|
| `"WIDTH_AND_HEIGHT"` | Default — text flows freely, safest post-import choice |
| `"HEIGHT"` | Text should fill a fixed column width (e.g., card body, sidebar paragraph) |
| `"NONE"` | Never after Stitch import — this is the problem state |

**Important:** Always `await figma.loadFontAsync(t.fontName)` before changing text properties. See [plugin-api-gotchas.md#promises](../plugin-api-gotchas.md#promises).

**Batch size:** Process 10-20 text nodes per `use_figma` call. Group by parent section for easier validation.

---

## Step 3: Fix Decimal Dimensions {#decimal-fix}

Stitch often produces sub-pixel widths/heights. These are harmless visually but create noise and can cause alignment drift in auto-layout.

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const nodes = frame.findAll(n =>
  (n.width !== Math.round(n.width)) ||
  (n.height !== Math.round(n.height))
);
for (const n of nodes) {
  if (n.width !== Math.round(n.width)) n.resize(Math.round(n.width), n.height);
  if (n.height !== Math.round(n.height)) n.resize(n.width, Math.round(n.height));
}
return { rounded: nodes.length };
```

**Caution:** Only round dimensions on leaf nodes or containers where rounding won't break layout. Skip nodes inside tight auto-layout where a 1px shift could cascade. Validate after rounding.

---

## Step 4: Evaluate SVG Nodes

Stitch may generate SVG nodes for elements that are better as native Figma structures.

Check the SVG decision matrix in [core-rules.md](../core-rules.md):
- **Icons/logos** from external sources → keep as SVG
- **Layout elements** (dividers, backgrounds, shapes) → consider replacing with native nodes for auto-layout compatibility and variable binding
- **Complex illustrations** → keep as SVG

This step is judgment-based. For a quick cleanup pass, flag SVGs but don't convert unless they block further work.

---

## Step 5: Validate

```
get_screenshot(fileKey, nodeId)
```

Compare against the pre-cleanup screenshot from Step 1:
1. **Text** — should look identical but now survives edits
2. **Dimensions** — check alignment didn't shift visibly
3. **Layout** — verify no auto-layout parents collapsed from rounding

If text reflows unexpectedly after the fix, the node may need `"HEIGHT"` mode instead of `"WIDTH_AND_HEIGHT"` (fixed-width context like a card or sidebar).

---

## Follow-Up Workflows

After Stitch cleanup, the frame is structurally stable. Common next steps:

- **[Color Tokenization](color-tokenization.md)** — bind hardcoded colors to variables
- **[Design System Cleanup](design-system-cleanup.md)** — migrate toward components and tokens
- **[Screen Review Loop](screen-review-loop.md)** — targeted visual fixes

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Editing colors/layout before fixing text auto-resize | Any write can trigger text reflow in unfixed nodes |
| Setting all text to `WIDTH_AND_HEIGHT` without checking context | Column-width text needs `HEIGHT` mode |
| Rounding dimensions on auto-layout parents | Can break child sizing — round leaf nodes first |
| Skipping font loading before text property changes | Silent failure or error — see [gotchas#promises](../plugin-api-gotchas.md#promises) |
| Doing cleanup and tokenization in the same pass | Separate concerns — fix structure first, then bind tokens |
