# Playbook: Screen Review Loop

Inspect an existing design, isolate issues, make targeted fixes, and validate. Use when fixing or adjusting an existing Figma screen — not when building from scratch.

**When to use:** The user wants to fix, adjust, or improve an existing design. The screen already exists on canvas. See [workflow-selection.md](../workflow-selection.md).

---

## Step 1: Screenshot for Visual Inspection

Start with a visual baseline — never edit blind.

```
get_screenshot(fileKey, nodeId)
```

Study the screenshot to understand:
- Overall layout and structure
- Obvious visual issues (misalignment, wrong colors, clipped text, broken spacing)
- Which specific areas need attention

**If the frame is large or complex:** Use `get_metadata` first to understand the node tree, then screenshot specific sub-sections rather than the full frame.

---

## Step 2: Understand the Structure

If the screenshot reveals issues but the cause isn't obvious:

```
get_metadata(fileKey, nodeId)
```

The sparse XML output reveals:
- Auto-layout configuration (direction, padding, gap)
- Node hierarchy and naming
- Sizing modes (FIXED, HUG, FILL)
- Variable bindings (or lack thereof)

Cross-reference the metadata with the visual issue to identify the root cause. Common root causes:

| Visual Symptom | Likely Structural Cause |
|---------------|----------------------|
| Text clipped or truncated | `textAutoResize: "NONE"` — needs `"HEIGHT"` or `"WIDTH_AND_HEIGHT"` |
| Uneven spacing | Inconsistent `itemSpacing` or manual padding instead of auto-layout gap |
| Color inconsistency | Hardcoded hex instead of variable binding |
| Element not filling width | Missing `layoutSizingHorizontal: "FILL"` or not appended to auto-layout parent |
| Overlapping elements | Missing auto-layout on parent, or absolute positioning |
| Decimal dimensions | Sub-pixel values from HTML-to-Figma import |

---

## Step 3: Isolate the Real Issue

**Critical:** Identify the minimal set of nodes that need changes. Do not conflate multiple unrelated issues into one fix.

1. From the screenshot + metadata, list each distinct issue
2. For each issue, identify the specific node(s) affected (by ID or name)
3. Prioritize: structural issues first (layout, sizing), then visual (colors, typography)

Example issue list:
- `Header/Title` — text clipped, needs `textAutoResize: "HEIGHT"`
- `Card Grid` — cards not filling width, need `layoutSizingHorizontal: "FILL"`
- `Sidebar/BG` — hardcoded `#F5F5F5`, should bind to `colors/neutral/50`

---

## Step 4: Targeted Edits

Fix each issue with a focused `use_figma` call. Group related fixes (same section, same type of fix) but never mix unrelated changes.

### One Fix Per Call (Complex Issues)
```js
const node = await figma.getNodeByIdAsync("TARGET_ID");
// Fix the specific property
node.textAutoResize = "HEIGHT";
return { fixed: node.name, property: "textAutoResize", value: "HEIGHT" };
```

### Batched Fix (Repetitive Same-Type Issues)
```js
// Fix all text nodes with NONE resize in a section
const section = await figma.getNodeByIdAsync("SECTION_ID");
const textNodes = section.findAll(n => n.type === "TEXT" && n.textAutoResize === "NONE");
for (const t of textNodes) {
  t.textAutoResize = "HEIGHT";
}
return { fixed: textNodes.length, property: "textAutoResize" };
```

**Key rules:**
- Always set page context explicitly (see [plugin-api-gotchas.md#page-context](../plugin-api-gotchas.md#page-context))
- For paint bindings, preserve opacity (see [plugin-api-gotchas.md#opacity](../plugin-api-gotchas.md#opacity))
- For FILL sizing, appendChild first (see [plugin-api-gotchas.md#append-before-fill](../plugin-api-gotchas.md#append-before-fill))

---

## Step 5: Validate Again

After each fix (or batch of related fixes):

```
get_screenshot(fileKey, nodeId)
```

Compare against:
1. The original screenshot (Step 1) — did the fix improve the identified issue?
2. The intended design — does it match what the user expects?
3. Unintended side effects — did fixing one thing break another?

**If the fix didn't work:**
1. Re-read the error or screenshot
2. Check [plugin-api-gotchas.md](../plugin-api-gotchas.md) for known failure patterns
3. Apply a corrected fix — do not retry the identical code
4. See [core-rules.md — Read -> Understand -> Fix -> Retry](../core-rules.md)

**If the fix introduced a new issue:**
- Undo the change if possible (revert the specific property)
- If not easily reversible, fix the side effect in a separate targeted call

---

## Step 6: Run the Done Gate Before Reporting Success

When all identified issues appear resolved, do not report success yet. Run the applicable gates from [core-rules.md](../core-rules.md) — Validation Gates.

### Required check sequence

1. **Structural checks first**
   - `get_metadata(fileKey, nodeId)` to confirm the edited nodes are structurally correct
   - verify parent container, node hierarchy, layout settings, instance integrity, and text content as needed
2. **Variable checks when relevant**
   - if colors/tokens/variables were changed, confirm with `get_variable_defs`
3. **Visual confirmation second**
   - final `get_screenshot` of the full frame
   - confirm the requested visual issue is actually resolved and no regression was introduced
4. **Only then summarize completion**

### Minimum completion questions

Before saying "done," answer:
- Is the originally requested issue actually fixed?
- Is there any placeholder/default content still present?
- Did the fix preserve real component instances where required?
- Did the fix introduce a new regression elsewhere?
- Does the screenshot confirm the intended final state?

If any answer is uncertain, do one more read/fix pass instead of reporting success.

---

## Avoiding Unnecessary Rebuilds

The review loop is about **surgical fixes**, not reconstruction. Rebuild only when:

- The structural approach is fundamentally wrong (e.g., manual positioning where auto-layout is needed across the entire frame)
- More than 70% of nodes need changes — at that point, rebuilding is cheaper
- The user explicitly requests a rebuild

In all other cases, fix what's broken and leave working parts untouched. A targeted fix that takes 1-2 `use_figma` calls is always preferable to a rebuild that takes 5-10 calls and risks introducing new issues.

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Editing without screenshotting first | You don't know the current state — fixes may target the wrong issue |
| Rebuilding a section because one node is wrong | Destroys working elements, wastes calls |
| Mixing unrelated fixes in one `use_figma` call | If one fix fails, all fixes in the call are lost |
| Not validating after each fix | Regressions go undetected, compound into larger problems |
| Skipping `get_metadata` for structural issues | Screenshots show symptoms; metadata reveals causes |
