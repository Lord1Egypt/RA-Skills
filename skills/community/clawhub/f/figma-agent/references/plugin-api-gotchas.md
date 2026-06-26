# Plugin API Gotchas

Known failure modes and sharp edges when working with `use_figma` (Figma Plugin API via MCP). Consult this before writing Plugin API code and after any unexpected error.

---

## 1. `use_figma` Atomicity

Each `use_figma` call executes as a single atomic JavaScript block. There is no shared state between calls — variables, references, and node handles do not persist.

**Implication:** Everything needed for a write operation must be self-contained within one call. Fetch nodes, create elements, and configure them in the same block.

---

## 2. Page Context Reset {#page-context}

`figma.currentPage` may not point to the expected page between calls. The plugin context can reset.

**Fix:** Always explicitly set the page at the start of each `use_figma` call:
```js
const page = figma.root.children.find(p => p.name === "Page Name");
// or by index: figma.root.children[0]
```

Never assume `figma.currentPage` is correct from a previous call.

---

## 3. `setBoundVariableForPaint` Returns New Paint {#paint-binding}

`setBoundVariableForPaint` does **not** mutate the existing paint in place. It returns a **new paint object** that must be assigned back to the node's fills/strokes array.

**Wrong:**
```js
node.fills[0].setBoundVariableForPaint(variable, "color");
```

**Correct:**
```js
const fills = [...node.fills];
fills[0] = figma.variables.setBoundVariableForPaint(fills[0], variable, "color");
node.fills = fills;
```

---

## 4. Opacity Reset Bug {#opacity}

When binding a variable to a paint via `setBoundVariableForPaint`, the paint's opacity may reset to 1.0, discarding the original opacity value.

**Fix:** Preserve and restore opacity explicitly:
```js
const fills = [...node.fills];
const originalOpacity = fills[0].opacity;
fills[0] = figma.variables.setBoundVariableForPaint(fills[0], variable, "color");
fills[0] = { ...fills[0], opacity: originalOpacity };
node.fills = fills;
```

Always check opacity before and after variable binding operations. See also [core-rules.md](core-rules.md) — validate-after-write.

---

## 5. `textAutoResize` Stitch Fix {#text-autoresize}

Stitch imports (HTML-to-Figma) often produce text nodes with fixed-size bounding boxes instead of auto-resizing text. This makes text uneditable in practice.

**Fix:** After Stitch import, reset text auto-resize:
```js
textNode.textAutoResize = "WIDTH_AND_HEIGHT"; // or "HEIGHT" for fixed-width
```

Common values: `"NONE"` (fixed), `"HEIGHT"` (width-fixed, height auto), `"WIDTH_AND_HEIGHT"` (fully auto).

See [playbooks/stitch-import-cleanup.md](playbooks/stitch-import-cleanup.md) for the full cleanup workflow.

---

## 6. Node-ID Conversion {#node-id}

Figma URLs use `-` as separator in node IDs (`123-456`), but the API expects `:` (`123:456`).

**Always convert** before passing to any tool:
```
URL:  ?node-id=123-456
API:  nodeId: "123:456"
```

Within `use_figma` code, node IDs returned by the Plugin API already use `:` format.

---

## 7. `saveVersionHistoryAsync` Not Supported {#no-save-version}

`figma.saveVersionHistoryAsync()` is **not available** in the MCP plugin context. Programmatic version checkpoints cannot be created.

**Workaround:** For large or risky edits, ask the user to manually save a version in Figma before proceeding. Build section-by-section with validation to minimize the blast radius of any single write. See [core-rules.md](core-rules.md) — Batch-Write Heuristic.

---

## 8. appendChild Before FILL Sizing {#append-before-fill}

When using `layoutSizingHorizontal: "FILL"` or `layoutSizingVertical: "FILL"`, the node must be appended to a parent with auto-layout **before** setting the sizing mode. Setting FILL on a detached node throws or silently fails.

**Correct order:**
```js
const child = figma.createFrame();
parent.appendChild(child);
child.layoutSizingHorizontal = "FILL";
```

---

## 9. Await All Promises {#promises}

Many Plugin API methods are async (`findOne`, `loadFontAsync`, `importComponentByKeyAsync`). Missing `await` causes silent failures or race conditions.

**Rule:** Always `await` async operations. When in doubt, `await` it.

```js
// Wrong: font not loaded before setting characters
figma.loadFontAsync({ family: "Inter", style: "Regular" });
textNode.characters = "Hello";

// Correct
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
textNode.characters = "Hello";
```

---

## 10. Post-Error Protocol {#post-error}

When a `use_figma` call fails:

1. **Read the error** — the MCP returns the error message from the plugin runtime.
2. **Check this file** — match the error against known gotchas above.
3. **Check the screenshot** — use `get_screenshot` to see what actually happened on canvas.
4. **Fix the specific issue** — do not rewrite from scratch; make a targeted correction.
5. **Retry with the fix** — re-run only the failed portion, not the entire workflow.

If the same error persists after two targeted fix attempts, re-evaluate the approach. Consider whether the operation is supported in the plugin context.

See [core-rules.md](core-rules.md) — Read -> Understand -> Fix -> Retry.

---

## 11. 20KB Response Limit {#response-limit}

`use_figma` returns a maximum of 20KB per call. If your code returns large data (node trees, variable lists), it will be truncated.

**Fix:** Filter and limit return data within the plugin code. Return only what you need.

---

## 12. No Image/Asset Import {#no-images}

`figma.createImage()` and `loadImageAsync` are **not available** in the MCP plugin context. You cannot programmatically import images or custom fonts.

**Workaround:** Use placeholder rectangles with descriptive names. The user can manually replace them with images afterward.
