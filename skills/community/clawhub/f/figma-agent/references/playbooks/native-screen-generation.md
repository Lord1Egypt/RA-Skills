# Playbook: Native Screen Generation

Production-ready screen creation in native Figma using design-system variables, components, and auto-layout.

**When to use:** The user wants a fully editable, design-system-aligned screen. This is the default production path. See [workflow-selection.md](../workflow-selection.md) for when HTML-to-Figma is more appropriate.

---

## ⚠️ Section-Relative Positioning

If a new screen is based on an existing one inside a Section or Frame, coordinates must stay relative to the same parent container, not the page.

Authoritative rule: [core-rules.md](../core-rules.md) — Conditional Rules: Section-Relative Positioning.

**Concrete failure case:**
- Section `v_04` is on the page at `(x=11779, y=10307)`
- Source screen lives inside that Section
- CC reads `y=10307` as a page coordinate instead of a local coordinate
- Result: the new screen lands on the page, not inside the Section

**Validation check:** After building, confirm the new screen is actually a child of the intended Section/Frame.

---

## Step 0: Hard Fork, State Variant or New Build

Before planning a rebuild, answer this first:

> Is this new screen more than roughly 50% structurally identical to an existing screen?

- **YES** -> go directly to [State-Screen Workflow](#state-screen-workflow). Do not continue into the fresh-build steps below.
- **NO** -> continue to Step 1 and follow the normal new-screen build flow.

If the answer is YES, also trigger the Section-Relative Positioning rule from [core-rules.md](../core-rules.md).

See [workflow-selection.md](../workflow-selection.md) — Screen State Variants: Copy + Edit vs Rebuild.

---

## Step 1: Understand the Job

Before touching the canvas:

- What screen/view is being built? (login, dashboard, settings, etc.)
- What is the target file and page? Get `fileKey` and target `nodeId` if appending to existing work.
- Are there reference designs or screenshots? Use `get_screenshot` on existing frames if available.
- What is the rough structure? Identify 3-5 major sections.

---

## Step 2: Inspect Existing Context

Follow [Local-Context-First](../core-rules.md) order:

1. **Current file variables:** `get_variable_defs(fileKey, nodeId)` — what tokens are available?
2. **Existing screens:** `get_metadata(fileKey, nodeId)` on sibling frames — what patterns are already established?
3. **Code Connect:** `get_code_connect_map(fileKey, nodeId)` — are there component-to-code mappings?
4. **Library search:** `search_design_system(query, fileKey)` — only if local sources are insufficient.

**Do not skip this step.** Building without context leads to inconsistent designs that ignore the file's established conventions.

---

## State-Screen Workflow

When the requested screen is primarily a new **state/step/variant** of an existing screen, do not default to rebuilding.

**Preferred flow:**
1. Identify the reference screen
2. Duplicate the reference screen using a real copy/clone path that preserves working component structure
3. Place the copy correctly relative to the same parent container/section
4. Edit only the delta: changed content, changed state, added/removed elements
5. Validate the result with structural checks first, then screenshot confirmation

**Use this workflow when:**
- building step 2 from step 1
- creating alternate states of the same flow
- keeping the same shell/layout while changing internals
- preserving existing component instances is lower risk than rebuilding

**Do not use this workflow when:**
- the layout is substantially different
- the original screen is poorly built and should not be propagated
- a clean rebuild is lower risk

**Critical copy rule:** Do not manually reconstruct the shell when this workflow applies. The point is to preserve working structure, instances, and layout decisions, then change only what is necessary.

---

## Step 3: Plan the Sections

Decompose the screen into buildable sections. Each section will be one `use_figma` call.

Example for a settings screen:
1. Page frame (outer container with auto-layout)
2. Header (title, breadcrumbs, actions)
3. Sidebar navigation
4. Content area with form sections
5. Footer / action bar

This decomposition drives the execution order. See [core-rules.md — Batch-Write Heuristic](../core-rules.md).

---

## Step 4: Create the Root Frame

First `use_figma` call — create the page-level container:

```js
const page = figma.root.children.find(p => p.name === "Target Page");
// Always set page explicitly — see plugin-api-gotchas.md#page-context

const frame = figma.createFrame();
frame.name = "Settings Screen";
frame.resize(1440, 900);
frame.layoutMode = "VERTICAL";
frame.primaryAxisAlignItems = "MIN";
frame.counterAxisAlignItems = "MIN";
frame.paddingTop = 0;
frame.paddingBottom = 0;
frame.paddingLeft = 0;
frame.paddingRight = 0;

page.appendChild(frame);
return { nodeId: frame.id, name: frame.name };
```

**Validate:** `get_screenshot` on the new frame. Confirm it exists and is positioned correctly.

---

## Step 5: Build Section by Section

For each section identified in Step 3:

1. **Write the section** in one `use_figma` call containing 1-3 related components/groups.
2. **Use resolved variables** — load variables at the top of each call (see [prompting-patterns.md — Variable-First](../prompting-patterns.md)).
3. **Bind colors to variables** — never use raw hex for design-system colors. Watch for the opacity bug (see [plugin-api-gotchas.md#opacity](../plugin-api-gotchas.md#opacity)).
4. **appendChild before FILL** — set `layoutSizingHorizontal: "FILL"` only after appending to parent (see [plugin-api-gotchas.md#append-before-fill](../plugin-api-gotchas.md#append-before-fill)).
5. **Await all promises** — `loadFontAsync`, `importComponentByKeyAsync`, etc. (see [plugin-api-gotchas.md#promises](../plugin-api-gotchas.md#promises)).

**After each section:** Validate with `get_screenshot`. Compare against intent. Fix issues before moving to the next section.

---

## Step 6: Validate the Complete Screen

After all sections are built:

1. `get_screenshot` of the full frame — check overall layout, spacing, alignment.
2. `get_variable_defs` on the frame — verify variable bindings are in place.
3. Compare against the original reference/intent.

---

## Step 7: Targeted Fixes

If issues are found during validation:

- **Isolate the issue** — which specific node or section is wrong?
- **Fix surgically** — edit only the affected node(s) in a focused `use_figma` call.
- **Do not rebuild** entire sections unless the structural approach is fundamentally wrong.
- **Re-validate** after each fix.

See [core-rules.md — Read -> Understand -> Fix -> Retry](../core-rules.md).

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Building the entire screen in one `use_figma` call | Fragile, any error wastes everything, hard to debug |
| Skipping `get_variable_defs` and using hardcoded colors | Produces designs disconnected from the design system |
| Not validating after each section | Errors compound silently |
| Rebuilding from scratch after a minor issue | Wasteful, destroys working sections |
| Not setting page context explicitly | Nodes may land on the wrong page (see [plugin-api-gotchas.md#page-context](../plugin-api-gotchas.md#page-context)) |
