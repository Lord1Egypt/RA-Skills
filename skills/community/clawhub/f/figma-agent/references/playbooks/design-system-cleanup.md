# Playbook: Design System Cleanup

Incremental migration from hardcoded values to design-system variables and components. Works section-by-section to avoid destructive big-bang rewrites.

**When to use:** A file or frame has inconsistent styling — hardcoded colors, raw pixel values, manual spacing — that should be migrated to design-system tokens. See [workflow-selection.md](../workflow-selection.md).

---

## Step 1: Assess the Current State

Before changing anything, understand what exists.

### Screenshot + Metadata

```
get_screenshot(fileKey, nodeId)
get_metadata(fileKey, nodeId)
```

### Run Variable Discovery

Follow [variable-discovery.md](variable-discovery.md) Steps 1-4 to understand:
- What local variables/styles exist
- What library variables are connected
- Current binding coverage (% of fills/strokes bound)

### Categorize the Gaps

Create a mental inventory of what needs migration:

| Category | Example | Priority |
|----------|---------|----------|
| **Colors** | Hardcoded `#1A1A1A` instead of `colors/neutral/900` | High — visual consistency |
| **Spacing** | Manual padding `16px` instead of `spacing/400` variable | Medium — layout consistency |
| **Typography** | Raw font size `14` instead of text style or variable | Medium — scalability |
| **Corner radius** | Hardcoded `8` instead of `radius/md` variable | Low — cosmetic |
| **Components** | Manual card recreation instead of instance | High — maintainability |

---

## Step 2: Plan Section-by-Section Migration {#incremental-approach}

**Critical rule:** Never attempt a full-frame or full-file cleanup in one pass. Break the frame into logical sections and migrate one at a time.

**Section examples:**
- Header / navigation
- Hero / banner area
- Content cards / grid
- Sidebar
- Footer

For each section, the migration order is:
1. **Structure** — fix layout mode, auto-layout, sizing
2. **Colors** — bind fills and strokes to variables
3. **Typography** — apply text styles or variables
4. **Spacing** — bind padding, gap, margins to variables
5. **Components** — replace manual constructions with component instances

This order matters: fixing structure first prevents layout breaks when other properties change.

---

## Step 3: Migrate Colors (Per Section)

This is the most common cleanup task. Follow [color-tokenization.md](color-tokenization.md) for the full workflow, applied to one section at a time.

**Quick reference for the binding pattern:**

```js
const node = await figma.getNodeByIdAsync("NODE_ID");
const variable = await figma.variables.getVariableByIdAsync("VAR_ID");
const fills = [...node.fills];
const origOpacity = fills[0].opacity;
fills[0] = figma.variables.setBoundVariableForPaint(fills[0], variable, "color");
fills[0] = { ...fills[0], opacity: origOpacity };
node.fills = fills;
```

See [plugin-api-gotchas.md#paint-binding](../plugin-api-gotchas.md#paint-binding) and [plugin-api-gotchas.md#opacity](../plugin-api-gotchas.md#opacity) for the two mandatory safety patterns.

---

## Step 4: Migrate Spacing and Sizing (Per Section)

Bind numeric properties to FLOAT variables where available:

```js
const node = await figma.getNodeByIdAsync("NODE_ID");
const spacingVar = await figma.variables.getVariableByIdAsync("SPACING_VAR_ID");

// Bind padding
node.setBoundVariable("paddingTop", spacingVar);
node.setBoundVariable("paddingBottom", spacingVar);
node.setBoundVariable("paddingLeft", spacingVar);
node.setBoundVariable("paddingRight", spacingVar);

// Bind gap
node.setBoundVariable("itemSpacing", spacingVar);
```

`setBoundVariable` (on node, not paint) works for: `width`, `height`, `paddingTop/Right/Bottom/Left`, `itemSpacing`, `cornerRadius`, `topLeftRadius`, `topRightRadius`, `bottomLeftRadius`, `bottomRightRadius`.

---

## Step 5: Replace Manual Constructions with Component Instances

If the file has components (local or library) that match manually built elements:

```js
// Import a library component by key
const component = await figma.importComponentByKeyAsync("COMPONENT_KEY");
const instance = component.createInstance();

// Position it where the manual construction was
instance.x = manualNode.x;
instance.y = manualNode.y;
parent.appendChild(instance);

// Remove the manual construction
manualNode.remove();
```

**Judgment call:** Only replace when the component is a clear match. Partial matches create more problems than hardcoded nodes. When unsure, leave it and flag for design review.

---

## Step 6: Validate After Each Section {#section-validation}

After completing a section:

```
get_screenshot(fileKey, nodeId)
```

Check:
1. **Visual match** — the section should look identical to before (or intentionally improved)
2. **No regressions** — adjacent sections not affected
3. **Binding correctness** — run a quick binding coverage check on the section

```js
const section = await figma.getNodeByIdAsync("SECTION_ID");
const all = section.findAll(n => n.fills?.length > 0);
let bound = 0, total = 0;
for (const n of all) {
  for (const f of n.fills) {
    if (f.type === "SOLID") { total++; f.boundVariables?.color ? bound++ : null; }
  }
}
return { bound, total, coverage: `${Math.round(bound/total*100)}%` };
```

**Only proceed to the next section when the current one validates clean.**

---

## Step 7: Progress Summary

After each section or at the end of a session, report:

- Sections completed vs remaining
- Binding coverage improvement (before vs after per section)
- Issues flagged for design review (ambiguous tokens, missing variables, structural problems)
- Recommended next steps

---

## Incremental Over Perfect

This playbook is designed for incremental improvement, not perfection in one pass:

- **Session-safe:** Each section is independent — you can stop after any section and resume later
- **Non-destructive:** Original values are replaced with variable bindings, not deleted — if a binding is wrong, it can be unbound
- **Scope-controlled:** Resist the urge to fix "one more thing" outside the current section

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Full-frame cleanup in one pass | Too large, hard to debug, partial failure wastes all work |
| Migrating colors before fixing structure | Layout changes reflow content, making color work harder to validate |
| Creating new variables during cleanup | Scope creep — cleanup binds to existing tokens; variable creation is a separate workflow |
| Replacing partial-match components | Creates broken instances that are worse than hardcoded nodes |
| Skipping section validation | Regressions compound — catch them per section, not at the end |
| Mixing multiple migration types in one `use_figma` call | If one fails, you lose all changes in that call |
