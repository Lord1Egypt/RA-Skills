# Input Handler — Figma URL

## Applies to
- `figma.com/design/...` URLs
- `figma.com/file/...` URLs

## Requirements

Requires the **Figma MCP** to be connected. If not connected, stop and tell the user to connect it first.

## Process

### Step 1 — Connect and explore

```
# Get design context and component overview
mcp: get-design-context <figma-url>

# Get variable/token definitions
mcp: get_variable_defs <figma-url>
```

### Step 2 — Extract frame data

For each target frame/screen:
- Absolute positions and sizes of all layers
- Fill colors (expand variables to actual values with `get_variable_defs`)
- Typography (font family, size, weight, line-height)
- Border radius, borders, shadows
- Component instances and their variants

### Step 3 — Compute spacing

Same as Sketch: use absolute position math to derive padding/gap from layer coordinates:
```
padding_top = child.absoluteY - parent.absoluteY
gap = next_sibling.absoluteY - (current_sibling.absoluteY + current_sibling.height)
```

### Step 4 — Variable resolution

Figma variables map directly to design tokens. Resolve them:
```
Figma variable: color/primary → var(--color-primary)
Figma variable: spacing/md → var(--spacing-md)
```

If Figma variables don't match universal token names, create a mapping table and note it in assumptions.log.

### Step 5 — Mark precision

Figma files provide exact values — all measurements are `[EXACT]`. Only mark `[ESTIMATED]` for values computed from visual inspection rather than layer data.

## Fallback when MCP unavailable

Ask user to export target frames as PNG screenshots, then switch to `screenshot.md` handler. Note the precision downgrade in assumptions.log:
```
[NOTE] Input downgraded from Figma to screenshot — precision reduced to ±5-10px
```
