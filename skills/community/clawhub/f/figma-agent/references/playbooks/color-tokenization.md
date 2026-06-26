# Playbook: Color Tokenization

Audit unbound colors, map them to design-system variables, and apply bindings safely. Use after HTML-to-Figma import, design-system migration, or whenever hardcoded colors need to be replaced with variable bindings.

**When to use:** A frame or file contains hardcoded hex colors that should be bound to design-system variables. See [workflow-selection.md](../workflow-selection.md).

---

## Step 1: Discover Available Variables

Before mapping colors, know what variables exist.

### Local Variables First
```js
const collections = await figma.variables.getLocalVariableCollectionsAsync();
for (const c of collections) {
  const vars = [];
  for (const id of c.variableIds) {
    vars.push(await figma.variables.getVariableByIdAsync(id));
  }
  // Filter to COLOR type
  const colorVars = vars.filter(v => v.resolvedType === "COLOR");
  return colorVars.map(v => ({ name: v.name, id: v.id }));
}
```

### Library Variables (Only If Local Is Insufficient)
Use `search_design_system(query, fileKey)` to find variables from connected libraries. Library variables can be imported via `figma.variables.importVariableByKeyAsync(key)`.

**Important:** Local and library variables are distinct. Local variables are resolved via `getLocalVariableCollectionsAsync`. Library variables require import. Do not mix the discovery methods.

---

## Step 2: Audit Unbound Fills

Scan target nodes for fills that are not bound to variables. Process fills and strokes **separately** — they have different semantic meaning and may map to different tokens.

### Fills Audit
```js
const target = await figma.getNodeByIdAsync("TARGET_NODE_ID");
const nodes = target.findAll(n => n.fills && n.fills.length > 0);
const unboundFills = [];
for (const n of nodes) {
  for (let i = 0; i < n.fills.length; i++) {
    const fill = n.fills[i];
    if (fill.type === "SOLID" && !fill.boundVariables?.color) {
      unboundFills.push({
        nodeId: n.id,
        nodeName: n.name,
        fillIndex: i,
        hex: figma.util.rgba(fill.color, fill.opacity),
        opacity: fill.opacity
      });
    }
  }
}
return unboundFills;
```

### Strokes Audit
Same pattern, but iterate `n.strokes` instead of `n.fills`. Strokes often map to border/outline tokens which differ from fill tokens.

**Output:** A list of `{ nodeId, hex, opacity, fillIndex/strokeIndex }` tuples ready for mapping.

---

## Step 3: Map Colors to Variables

Match each unbound hex to the closest design-system variable. This is a judgment step:

| Hex Value | Likely Variable | Confidence |
|-----------|----------------|------------|
| `#1A1A1A` | `colors/neutral/900` | High — exact match |
| `#1B1B1F` | `colors/neutral/900` | Medium — close but not exact |
| `#FF6B35` | `colors/accent/500` | High — matches brand accent |
| `#E8E8E8` | `colors/neutral/200` | Medium — could be 100 or 200 |

**Rules for mapping:**
- Exact hex match = bind immediately
- Close match (within a few shades) = bind to nearest token, note the delta
- No reasonable match = leave unbound; flag for design review
- **Never invent new variables** during tokenization — only bind to what exists

---

## Step 4: Apply Bindings Safely {#apply-bindings}

Critical: `setBoundVariableForPaint` has two known sharp edges. Both must be handled in every binding operation.

### The Paint-Binding Pattern {#paint-binding-pattern}

`setBoundVariableForPaint` returns a **new paint object** — it does not mutate in place. You must reassign the fills/strokes array. See [plugin-api-gotchas.md#paint-binding](../plugin-api-gotchas.md#paint-binding).

### The Opacity Preservation Pattern {#opacity-preservation}

`setBoundVariableForPaint` **resets opacity to 1.0**. You must save and restore opacity explicitly. See [plugin-api-gotchas.md#opacity](../plugin-api-gotchas.md#opacity).

### Combined Correct Pattern

```js
const node = await figma.getNodeByIdAsync("NODE_ID");
const variable = await figma.variables.getVariableByIdAsync("VAR_ID");

// Bind fill at index 0
const fills = [...node.fills];
const originalOpacity = fills[0].opacity;  // 1. Save opacity
fills[0] = figma.variables.setBoundVariableForPaint(fills[0], variable, "color");  // 2. Bind
fills[0] = { ...fills[0], opacity: originalOpacity };  // 3. Restore opacity
node.fills = fills;  // 4. Reassign array
```

### Batching Strategy

Bind 5-10 nodes per `use_figma` call when applying the same variable or same category of variables. Group by variable, not by node proximity.

```js
// Good: all primary-fill bindings in one call
const nodesToBind = ["1:23", "1:45", "1:67"];
const variable = await figma.variables.getVariableByIdAsync("VAR_ID");
for (const id of nodesToBind) {
  const node = await figma.getNodeByIdAsync(id);
  const fills = [...node.fills];
  const origOpacity = fills[0].opacity;
  fills[0] = figma.variables.setBoundVariableForPaint(fills[0], variable, "color");
  fills[0] = { ...fills[0], opacity: origOpacity };
  node.fills = fills;
}
```

---

## Step 5: Validate Bindings

After each batch of bindings:

1. **`get_screenshot`** — visual check that colors haven't shifted unexpectedly
2. **`get_variable_defs`** on the target frame — confirm variables are bound
3. **Spot-check opacity** — verify nodes that had non-1.0 opacity still look correct

If a color looks wrong after binding:
- Check the variable resolves to the expected hex in the current mode (light/dark)
- Check opacity was preserved (most common issue)
- Check the correct fill/stroke index was targeted

---

## Step 6: Handle Strokes

Repeat Steps 4-5 for strokes. The pattern is identical but uses `node.strokes` instead of `node.fills`:

```js
const strokes = [...node.strokes];
const origOpacity = strokes[0].opacity;
strokes[0] = figma.variables.setBoundVariableForPaint(strokes[0], variable, "color");
strokes[0] = { ...strokes[0], opacity: origOpacity };
node.strokes = strokes;
```

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Binding fills and strokes in the same audit pass | Different semantic meaning, different tokens |
| Forgetting to preserve opacity | Silent visual regression — colors appear correct but transparency is lost |
| Mutating `fills[0]` directly without array reassignment | Figma ignores in-place mutations; the binding is silently dropped |
| Creating new variables during tokenization | Scope creep — tokenization binds to existing tokens, variable creation is a separate workflow |
| Binding without validating via screenshot | You won't catch opacity bugs or wrong-mode color resolution |
