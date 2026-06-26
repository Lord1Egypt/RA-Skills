# Playbook: Design Audit & Review

Read-only inspection workflow for evaluating design-system compliance, component usage, variable coverage, and accessibility basics. Produces a structured audit report without modifying the file.

**When to use:** Before a cleanup migration, as a periodic health check, or when a user asks "how well does this screen follow the design system?" See [workflow-selection.md](../workflow-selection.md).

---

## Step 1: Visual Baseline

```
get_screenshot(fileKey, nodeId)
```

Note first impressions:
- Overall visual consistency (colors, spacing, typography feel cohesive?)
- Obvious outliers (one-off colors, inconsistent card styles, alignment breaks)
- Accessibility red flags (very small text, low-contrast areas)

---

## Step 2: Structural Inspection

```
get_metadata(fileKey, nodeId)
```

From the metadata, evaluate:

| Aspect | What to Check |
|--------|--------------|
| **Auto-layout usage** | Are sections using auto-layout or manual positioning? |
| **Naming** | Descriptive node names or generic "Frame 42" / "Group 17"? |
| **Nesting depth** | Excessive nesting (>5-6 levels) suggests structural issues |
| **Sizing modes** | Mix of FIXED/HUG/FILL — is it intentional or inconsistent? |

---

## Step 3: Variable Binding Coverage {#binding-audit}

Measure what percentage of fills and strokes are bound to variables vs hardcoded.

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const nodes = frame.findAll(n =>
  (n.fills?.length > 0) || (n.strokes?.length > 0)
);

let fills = { bound: 0, unbound: 0 };
let strokes = { bound: 0, unbound: 0 };

for (const n of nodes) {
  if (n.fills) {
    for (const f of n.fills) {
      if (f.type === "SOLID") {
        f.boundVariables?.color ? fills.bound++ : fills.unbound++;
      }
    }
  }
  if (n.strokes) {
    for (const s of n.strokes) {
      if (s.type === "SOLID") {
        s.boundVariables?.color ? strokes.bound++ : strokes.unbound++;
      }
    }
  }
}

return {
  fills: { ...fills, coverage: `${Math.round(fills.bound / (fills.bound + fills.unbound) * 100)}%` },
  strokes: { ...strokes, coverage: `${Math.round(strokes.bound / (strokes.bound + strokes.unbound) * 100)}%` }
};
```

**Interpretation:**
- **>80%** — well-tokenized, minor cleanup needed
- **40-80%** — partial adoption, section-by-section cleanup recommended
- **<40%** — largely hardcoded, full [design-system-cleanup](design-system-cleanup.md) needed

---

## Step 4: Component Usage Audit {#component-audit}

Check whether the frame uses component instances vs manual constructions.

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const instances = frame.findAll(n => n.type === "INSTANCE");
const allNodes = frame.findAll(() => true);

const componentNames = {};
for (const inst of instances) {
  const name = inst.mainComponent?.name || "unknown";
  componentNames[name] = (componentNames[name] || 0) + 1;
}

return {
  totalNodes: allNodes.length,
  instanceCount: instances.length,
  instanceRatio: `${Math.round(instances.length / allNodes.length * 100)}%`,
  components: componentNames
};
```

**What to flag:**
- Repeated visual patterns that are NOT instances → candidate for component extraction or replacement
- Detached instances (instances that were detached from their main component) → may need re-linking
- Low instance ratio on screens that should be component-heavy (lists, cards, navigation)

---

## Step 5: Unique Color Inventory {#color-inventory}

List all unique colors used in the frame, distinguishing bound from unbound.

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const nodes = frame.findAll(n => n.fills?.length > 0);
const colors = {};

for (const n of nodes) {
  for (const f of n.fills) {
    if (f.type === "SOLID") {
      const hex = `#${Math.round(f.color.r*255).toString(16).padStart(2,'0')}${Math.round(f.color.g*255).toString(16).padStart(2,'0')}${Math.round(f.color.b*255).toString(16).padStart(2,'0')}`;
      if (!colors[hex]) colors[hex] = { count: 0, bound: 0, unbound: 0 };
      colors[hex].count++;
      f.boundVariables?.color ? colors[hex].bound++ : colors[hex].unbound++;
    }
  }
}

// Sort by count descending
const sorted = Object.entries(colors).sort((a,b) => b[1].count - a[1].count);
return sorted.slice(0, 25); // Top 25 colors
```

This reveals:
- **Dominant colors** — should all be tokenized
- **One-off colors** — potential inconsistencies or intentional accents
- **Near-duplicates** — e.g., `#1A1A1A` and `#1B1B1F` that should be the same token

---

## Step 6: Accessibility Basics {#accessibility}

Quick checks that don't require external tools.

### Text Size Check

```js
const frame = await figma.getNodeByIdAsync("FRAME_ID");
const textNodes = frame.findAll(n => n.type === "TEXT");
const small = textNodes.filter(n => n.fontSize < 12);
const sizes = {};
for (const t of textNodes) {
  const s = `${t.fontSize}px`;
  sizes[s] = (sizes[s] || 0) + 1;
}
return {
  totalText: textNodes.length,
  belowMinimum: small.map(t => ({ name: t.name, size: t.fontSize })),
  sizeDistribution: sizes
};
```

**Guidelines:**
- Body text below 12px is generally problematic for readability
- Below 10px is a red flag in almost all contexts
- Font size distribution should show a limited set of sizes (consistent type scale)

### Contrast Awareness

Full WCAG contrast calculation is complex in plugin code, but flag obvious risks:
- Light text on light backgrounds (both fills with high lightness)
- Very thin font weights (<300) at small sizes
- Text over images without overlay/scrim

Report these as "flagged for manual contrast check" — automated WCAG scoring is beyond the scope of a quick audit.

---

## Step 7: Generate Audit Report

Compile findings into a structured summary for the user:

```markdown
## Audit Report: [Frame Name]

### Variable Coverage
- Fills: X% bound (Y/Z)
- Strokes: X% bound (Y/Z)
- Assessment: [well-tokenized / partial / needs migration]

### Component Usage
- X instances out of Y nodes (Z%)
- Top components: [list]
- Manual patterns flagged: [list or "none"]

### Color Inventory
- X unique colors found
- Top unbound: [hex, count] (suggest token mapping)
- Near-duplicates: [pairs]

### Typography
- X text nodes, Y unique sizes
- Below minimum (12px): [list or "none"]
- Type scale consistency: [consistent / scattered]

### Accessibility Flags
- [list of flagged items or "no flags"]

### Recommendations
1. [Prioritized next steps — link to relevant playbooks]
```

---

## Linking to Action Playbooks

Based on audit findings, recommend the appropriate next workflow:

| Finding | Recommended Playbook |
|---------|---------------------|
| Low variable coverage | [Color Tokenization](color-tokenization.md) → [Design System Cleanup](design-system-cleanup.md) |
| Stitch artifacts (fixed text, decimal dims) | [Stitch Import Cleanup](stitch-import-cleanup.md) |
| Missing components | [Design System Cleanup](design-system-cleanup.md) |
| Visual issues | [Screen Review Loop](screen-review-loop.md) |
| Need to understand available tokens first | [Variable Discovery](variable-discovery.md) |

---

## Anti-Patterns

| Anti-Pattern | Why It Fails |
|-------------|-------------|
| Making changes during an audit | Audit is read-only — mixing reads and writes confuses the baseline |
| Reporting raw numbers without interpretation | "42% coverage" means nothing without context — say what to do about it |
| Auditing an entire file at once | Audit per frame/screen — file-level aggregation loses actionable detail |
| Skipping the screenshot | Numbers alone miss visual inconsistencies that metadata can't reveal |
| Running full audit when user asked a specific question | Adapt scope — a "check colors" request doesn't need a typography audit |
