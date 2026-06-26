# Playbook: Variable Discovery

Discover and inventory available variables and styles — local, library, and file-level. Use before color tokenization, design-system cleanup, or any workflow that needs to know what tokens exist.

**When to use:** You need to understand what variables and styles are available before applying bindings or evaluating design-system coverage. See [workflow-selection.md](../workflow-selection.md).

---

## Step 1: Discover Local Variables {#local-discovery}

Local variables are the first source to check — see [core-rules.md — Local-Context-First](../core-rules.md).

### List All Local Variable Collections

```js
const collections = await figma.variables.getLocalVariableCollectionsAsync();
const result = [];
for (const c of collections) {
  const vars = [];
  for (const id of c.variableIds) {
    const v = await figma.variables.getVariableByIdAsync(id);
    vars.push({
      name: v.name, id: v.id,
      type: v.resolvedType,
      modes: c.modes.map(m => m.name)
    });
  }
  result.push({ collection: c.name, count: vars.length, variables: vars });
}
return result;
```

### Filter by Type

Common resolved types: `"COLOR"`, `"FLOAT"`, `"STRING"`, `"BOOLEAN"`.

```js
// Color variables only
const colorVars = vars.filter(v => v.resolvedType === "COLOR");

// Spacing/sizing variables
const numberVars = vars.filter(v => v.resolvedType === "FLOAT");
```

### Resolve Variable Values

To see the actual value of a variable in a specific mode:

```js
const variable = await figma.variables.getVariableByIdAsync("VAR_ID");
const collection = await figma.variables.getVariableCollectionByIdAsync(variable.variableCollectionId);
for (const mode of collection.modes) {
  const value = variable.valuesByMode[mode.modeId];
  // value is { r, g, b, a } for COLOR, number for FLOAT, etc.
}
```

**Response size:** Large design systems can have hundreds of variables. Filter by type or collection name within the plugin code to stay under the [20KB response limit](../plugin-api-gotchas.md#response-limit).

---

## Step 2: Discover Library Variables {#library-discovery}

Library variables come from connected external libraries. They require a different discovery method.

### Search Connected Libraries

```
search_design_system(query, fileKey)
```

This searches across connected libraries for components, styles, and variables matching the query. Use specific queries — e.g., `"color primary"`, `"spacing"`, `"radius"`.

### Import Library Variables

Library variables must be imported before use in plugin code:

```js
const imported = await figma.variables.importVariableByKeyAsync("VARIABLE_KEY");
// Now use `imported` like a local variable for binding
```

### Key Differences: Local vs Library

| Aspect | Local Variables | Library Variables |
|--------|----------------|-------------------|
| Discovery method | `getLocalVariableCollectionsAsync()` | `search_design_system` MCP tool |
| Available immediately | Yes | Need `importVariableByKeyAsync` |
| Editable | Yes | No — read-only in consuming files |
| Typical use | File-specific tokens, overrides | Shared design-system tokens |
| ID format | `VariableID:xxx` | Key-based (different from ID) |

**Rule:** Always check local variables first. Only search libraries when local tokens are insufficient. See [core-rules.md — Local-Context-First](../core-rules.md).

---

## Step 3: Discover Styles (Legacy) {#style-discovery}

Styles are the older mechanism (before variables). Some files still use them.

### Local Styles

```js
const paintStyles = await figma.getLocalPaintStylesAsync();
const textStyles = await figma.getLocalTextStylesAsync();
const effectStyles = await figma.getLocalEffectStylesAsync();

return {
  paints: paintStyles.map(s => ({ name: s.name, id: s.id })),
  texts: textStyles.map(s => ({ name: s.name, id: s.id, fontSize: s.fontSize })),
  effects: effectStyles.map(s => ({ name: s.name, id: s.id }))
};
```

### Variables vs Styles

| Aspect | Variables | Styles |
|--------|-----------|--------|
| Multi-mode (light/dark) | Yes — built-in | No — separate styles per mode |
| Binding type | `setBoundVariableForPaint` | `node.fillStyleId = style.id` |
| Granularity | Single value (one color, one number) | Compound (a style can have multiple fills, effects) |
| Preferred for new work | Yes | No — migrate to variables when possible |

**Recommendation:** For new design-system work, prefer variables over styles. When auditing existing files, report both — many files have a mix.

---

## Step 4: Inspect Node Bindings {#node-bindings}

Check what variables/styles are already bound to specific nodes. Useful for auditing coverage.

### Check Variable Bindings on a Node

```js
const node = await figma.getNodeByIdAsync("NODE_ID");
const bindings = {};

// Fill bindings
if (node.fills) {
  bindings.fills = node.fills.map((f, i) => ({
    index: i, bound: !!f.boundVariables?.color
  }));
}
// Stroke bindings
if (node.strokes) {
  bindings.strokes = node.strokes.map((s, i) => ({
    index: i, bound: !!s.boundVariables?.color
  }));
}
// Explicit variable bindings (spacing, sizing, corner radius, etc.)
bindings.explicit = node.boundVariables;

return bindings;
```

### Scan a Frame for Binding Coverage

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const all = frame.findAll(n => n.fills && n.fills.length > 0);
let bound = 0, unbound = 0;
for (const n of all) {
  for (const f of n.fills) {
    if (f.type === "SOLID") {
      f.boundVariables?.color ? bound++ : unbound++;
    }
  }
}
return { bound, unbound, coverage: `${Math.round(bound / (bound + unbound) * 100)}%` };
```

---

## Step 5: MCP-Level Variable Inspection

For a higher-level view without writing plugin code:

```
get_variable_defs(fileKey, nodeId)
```

This returns variable definitions connected to a specific node or frame. Useful for quick checks, but less flexible than plugin-level discovery for file-wide audits.

**Note:** `get_variable_defs` needs a real node ID, not `0:1`. Pass a specific frame or component node. See [plugin-api-gotchas.md#node-id](../plugin-api-gotchas.md#node-id).

---

## Output: What to Report

After discovery, summarize:

1. **Collections found** — names, variable counts, mode names
2. **Type breakdown** — how many COLOR, FLOAT, STRING, BOOLEAN
3. **Binding coverage** — what % of fills/strokes are already bound (if auditing a frame)
4. **Gaps** — unbound colors, missing token categories, styles without variable equivalents
5. **Recommendation** — next workflow: [color-tokenization](color-tokenization.md), [design-system-cleanup](design-system-cleanup.md), or [design-audit-review](design-audit-review.md)

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Calling `search_design_system` before checking local variables | Wastes API calls, may find library tokens that duplicate local ones |
| Returning all variables without filtering by type | Hits 20KB response limit on large design systems |
| Confusing variable IDs with variable keys | IDs are for local use, keys are for library import — they are different |
| Using `get_variable_defs` with node ID `0:1` | Returns nothing useful — needs a real frame/component node |
| Mixing style binding and variable binding on the same property | Creates confusion — pick one system per property |
