# SVG Rules

## SVG Requirements

- **Valid SVG 1.1**: Markup must parse correctly in all modern browsers and SVG viewers.
- **Transparent background**: No background rectangle unless explicitly requested. The mark must float on any surface.
- **SVG 1.1 compatible**: Use standard elements (`path`, `circle`, `rect`, `ellipse`, `polygon`, `g`). Avoid CSS animations, filters, and exotic features that may not render consistently.
- **viewBox attribute required**: Always define `viewBox` to ensure scaling. Format: `viewBox="0 0 width height"`. The viewBox should tightly frame the mark with minimal padding (typically 2-5% of dimensions).
- **Organized groups**: Use `<g>` with descriptive `id` attributes for logical sections (e.g., `id="symbol"`, `id="wordmark"`, `id="badge-frame"`).
- **Optimized paths**: Merge overlapping shapes where possible. Use `fill-rule="evenodd"` for complex compound shapes rather than multiple overlapping paths. Avoid redundant nodes. Convert strokes to fills for logos when possible to prevent stroke scaling issues.
- **Strong silhouette**: The mark must have a clear, unified outer contour. No floating elements that break the overall shape unless intentional and justified.

## Scalability Requirements

Assets must remain recognizable at all standard sizes:

| Size | Use Case | Check |
|------|----------|-------|
| 16×16 | Favicon, browser tab | Silhouette must read instantly. No text. No fine detail. |
| 32×32 | Retina favicon, small app icon | Primary symbol must be clear. Minimal detail. |
| 64×64 | App icon, social avatar | Full mark should be readable. Subtle detail acceptable. |
| 512×512 | App store, large display | Full detail, but paths should not be excessively dense. |

**Scalability test**: Mentally blur the mark to 16×16. If the primary shape is still recognizable, it passes. If critical elements merge or disappear, simplify.

## Path Optimization Guidelines

- **Node count**: Keep paths under 100 nodes for simple marks, under 300 for complex illustrative marks. More nodes = larger file size and slower rendering.
- **Curve quality**: Use Bézier curves (`Q`, `C` commands) rather than dense polygonal approximations. Fewer nodes with smooth curves scale better.
- **Compound paths**: Merge shapes that share the same fill into single compound paths when possible. Use `fill-rule="evenodd"` for holes and cutouts.
- **Stroke conversion**: Convert strokes to fills for final logo output to prevent stroke width scaling issues at small sizes. Exception: icon packs designed with intentional stroke-based systems.
- **Decimal precision**: Use 2-3 decimal places for coordinates. More precision is unnecessary and increases file size.
- **No transforms on paths**: Apply transforms to groups (`<g>`) rather than individual path elements when possible. Avoid nested transforms that complicate editing.

## Grouping and ID Conventions

```xml
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g id="symbol">
    <path id="symbol-primary" d="..."/>
    <path id="symbol-accent" d="..."/>
  </g>
  <g id="wordmark">
    <path id="wordmark-text" d="..."/>
  </g>
</svg>
```

- Group by logical component, not by fill color.
- IDs should be descriptive: `symbol`, `wordmark`, `badge-frame`, `icon-body`, `monogram-letter-a`.
- Avoid generic IDs like `path1`, `g2`, `layer3`.

## Asset-Type-Specific SVG Rules

### Logo (Master)
- Full detail, all elements present.
- Tight viewBox with minimal padding.
- All grouping and IDs present.
- This is the canonical version.

### Horizontal Logo
- Symbol left, wordmark right (or reversed for RTL).
- ViewBox should accommodate the full width.
- Maintain clear spacing between symbol and wordmark (typically 0.5×–1× symbol height).

### Stacked Logo
- Symbol top, wordmark below.
- Centered alignment.
- Generous vertical spacing between elements.

### Icon
- Simplified from master. Load `references/icon-simplification.md`.
- Centered in square viewBox.
- No text elements.
- Strong silhouette for instant recognition.

### Favicon
- Further simplified from icon.
- Must read at 16×16.
- Prefer single-color or two-color max.
- Square viewBox, mark centered with minimal padding.
- No gradients, no fine lines, no text.

### App Icon
- Simplified from icon.
- Must read at 64×64 and up.
- Rounded corners may be applied in platform layer, not SVG itself.
- Square viewBox, centered, generous padding (10-15%).
- Avoid text; symbol-only preferred.

### Avatar
- Centered, often circular crop applied by platform.
- Readable at 64×64.
- Simplified like icon but may retain slightly more personality.
- Square viewBox with generous padding.

### Monochrome
- Single-color version of master.
- All fills converted to `#000000` (or currentColor).
- No gradients, no opacity variations, no shadows.
- Verify silhouette strength is maintained without color contrast.

### Reverse
- Light-on-dark version of monochrome.
- Fill color: `#FFFFFF` (or currentColor).
- Verify the mark doesn't feel heavier or lighter than the positive version; adjust stroke weights if needed to maintain optical balance.

### Badge / Emblem / Monogram
- Contained within a frame (circle, shield, crest, etc.) or self-contained letterforms.
- ViewBox should accommodate the full frame.
- Frame and internal elements should be separate groups for flexibility.
- Verify the mark works both with and without the frame.

## Production Readiness Checklist

- [ ] Valid SVG 1.1 markup (no proprietary extensions)
- [ ] viewBox attribute present and correctly sized
- [ ] No background rectangle (transparent)
- [ ] All paths optimized and merged where possible
- [ ] Descriptive IDs on groups and major paths
- [ ] No CSS animations or filters
- [ ] Stroke converted to fill for logos
- [ ] 2-3 decimal precision on coordinates
- [ ] File size under 50KB for logos, under 10KB for icons
- [ ] Recognizable at 16×16, 32×32, 64×64, 512×512
