# Multi-Resolution Canvas Export — Deep Dive

The `setTransform` matrix-scaling pattern from SKILL.md, with the reasoning and edge cases.

## Why matrix scaling (not manual coordinate math)

Three approaches to higher-resolution canvas export:

| Approach | Effort | Risk |
|---|---|---|
| Rewrite all coordinates × N | High | Typos everywhere, unmaintainable |
| `ctx.scale(N, N)` on top of default transform | Low | Cumulative with other transforms; must reset carefully |
| **`ctx.setTransform(N, 0, 0, N, 0, 0)`** | Low | **Deterministic — resets AND scales in one call** |

`setTransform` replaces the entire matrix (no accumulation bugs) and scales everything downstream: coordinates, `fillText` sizes, `shadowBlur`, `lineWidth`, gradient endpoints, even `arc` radii. Existing draw functions run unchanged at any resolution.

## The three size variables (where people go wrong)

```js
canvas.width  = W * scale;      // internal raster — this is what exports
canvas.height = H * scale;
canvas.style.width  = W + 'px'; // CSS display size — MUST stay logical
canvas.style.height = H + 'px'; // or the page layout jumps on export
```

- `canvas.width/height` = raster resolution → grows with scale
- `canvas.style.width/height` = on-page display → stays at logical size
- Forgetting the distinction = the classic "poster doubled in size on my page" bug

Changing `canvas.width` implicitly **clears the canvas and resets the transform**, which is why `applyScale` is called before every `render()`.

## Image smoothing at high DPI

```js
ctx.imageSmoothingEnabled = true;
ctx.imageSmoothingQuality = 'high';
```

Matters when you draw images (logos, photos) inside the poster — cleaner resampling. Pure vector drawing (rects, text, arcs) is re-rasterized at native resolution anyway, so smoothing doesn't hurt. Set it once in `applyScale`, because the context state resets whenever canvas dimensions change.

## Render deferral

```js
flashStatus('Rendering 4K …');          // update DOM
requestAnimationFrame(() => {           // …but draw NEXT frame
  applyScale(4); render(); /* export */ 
});
```

Without the `requestAnimationFrame` wrapper, the browser never paints the "Rendering…" message — the main thread blocks synchronously in the heavy render (4K + `shadowBlur` can take seconds). The user sees a frozen page instead of a progress hint.

## Memory and limits

Internal pixels ≈ memory: 3600×5092×4 bytes ≈ 73 MB — fine. Practical ceilings:

- Browsers cap canvas area (commonly 16,384×16,384 and/or ~268 M px). At 4× a 900×1273 poster you're at ~18 M px — safe.
- Going beyond ~6× on large posters can silently produce a blank export. If an export comes back empty at high scale, suspect the area cap before suspecting your code.

## QA recipe

```js
// In browser console (or agent-browser eval):
applyScale(4); render();
JSON.stringify({ w: canvas.width, h: canvas.height })  // → {"w":3600,"h":5092}
canvas.toDataURL().slice(0, 22)                        // → "data:image/png;base64,"
```

Then restore: `applyScale(1); render();`

For pixel verification of the downloaded file, use `scripts/qa_poster.py` (see SKILL.md).
