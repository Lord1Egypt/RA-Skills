---
name: canvas-poster-kit
description: Design single-image posters, banners and infographics as production-ready PNG files using the HTML <canvas> 2D API, with built-in multi-resolution export (1x / 2K / 4K+) via ctx.setTransform matrix scaling — no code rewrite needed. Use this skill whenever the user asks for a 海报 (poster), 单图视觉 deliverable, promotional graphic, event banner, or asks to export a canvas design at higher resolution / multiple sizes / 2K / 4K, even if they never say the word "canvas". Also covers: topic-driven palette selection, programmatic color extraction from reference images (PIL sampling, not eyeballing), surgical canvas text edits, and browser-based visual QA with pixel verification.
---

# Canvas Poster Kit

Design posters as HTML `<canvas>` drawings and export them at multiple resolutions from the same drawing code. Everything here was learned from shipping real posters across three production iterations (dark-tech conference poster → warm empathy poster → multi-resolution export refactor).

## Why canvas (and when NOT to use it)

Canvas gives you pixel-perfect programmatic control: gradients, glow shadows, exact color zones, and a one-line PNG export (`toDataURL`). Choose it when the deliverable is a **single static image**.

- Data charts (bar/line/pie) → use a charting skill instead.
- Slide decks → use a PPT skill instead.
- Multi-page documents → use document tooling.

## Workflow

1. **Brief** — Clarify: topic, audience, text content, size/orientation, any reference image.
2. **Palette (topic-driven)** — Match palette to *topic semantics*, not aesthetics alone. Dark-tech (`#000814` bg + neon cyan) fits AI/tech; warm cream + coral fits empathy/kindness topics. See `references/design-patterns.md`.
3. **Reference image?** — Extract colors programmatically (PIL resize → Counter → corner/strip sampling). Faithful extraction beats "similar vibe". Echo the reference's structural framework (strips, bands) in the layout.
4. **Build** — Start from `assets/template.html` (the multi-resolution engine). Replace the placeholder `draw*()` sections with your content. Keep W/H as *logical* dimensions.
5. **QA in browser** — See `references/browser-qa.md`: open via headless browser, eval render checks, verify PNG signature, PIL pixel-zone sampling.
6. **Deliver + multi-res** — The template ships with 1x / 2K / 4K download buttons out of the box.

## Multi-resolution export (the core pattern)

Never rewrite drawing code for higher resolution. Scale the transform matrix instead:

```js
function applyScale(scale) {
  canvas.width  = W * scale;   // internal pixels grow
  canvas.height = H * scale;
  canvas.style.width  = W + 'px';  // display size stays constant
  canvas.style.height = H + 'px';  // → preview never jumps
  ctx.setTransform(scale, 0, 0, scale, 0, 0);  // all coordinates/fonts/shadows auto-scale
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';
}

function download(scale) {
  requestAnimationFrame(() => {   // let "Rendering…" status paint first
    applyScale(scale);
    render();                      // your existing draw functions, unchanged
    const link = document.createElement('a');
    link.download = `poster_${scale}x.png`;
    link.href = canvas.toDataURL('image/png');
    link.click();
    applyScale(1); render();       // restore preview
  });
}
```

Why this works: `setTransform(scale,0,0,scale,0,0)` scales the entire drawing matrix, so every coordinate, `fillText` size, `shadowBlur` and `lineWidth` in existing code scales N× automatically. Full details, memory limits and failure modes: `references/multi-resolution.md`.

## Visual QA

After generating, verify before delivering:

1. Render check: eval `JSON.stringify({w: canvas.width, h: canvas.height})` after `applyScale(4); render()` — expect `{w: W*4, h: H*4}`.
2. PNG check: `toDataURL()` must start with `data:image/png;base64,iVBORw0K`.
3. Pixel-zone check: run `scripts/qa_poster.py` to sample expected background/accent colors at known coordinates.
4. Text check: grep the HTML for every `fillText` string the user asked to include; after text-removal edits, expect **zero** matches for removed strings (keep surrounding shape-drawing code intact — remove only the `fillText` lines).

## Surgical text edits

User asks to remove/change specific text? `grep -n "<exact string>" index.html` → locate the `ctx.fillText(...)` call → edit/remove that line only. Never touch gradients, lines, or shape code around it. Verify with grep: zero matches post-edit.

## Pitfalls (learned the hard way)

- **Internal px ≠ display px.** After `applyScale(4)`, `canvas.width` is 4× but `canvas.style.width` must stay at logical size, or the page layout jumps.
- **4K + shadowBlur is heavy.** Defer renders behind `requestAnimationFrame` or the UI freezes before the status message paints.
- **Icon semantics.** Verify every glyph/icon against card *meaning*, not visual availability. A writing-hand icon on a "partnership" card is wrong even if it looks fine.
- **Don't repeat last topic's palette** when the user praises it — praise ≠ reuse request. Match palette to the *new* topic.
- **Read-only dirs.** Some upload dirs are read-only; write intermediate files to a writable subdir.

## Environment self-check

Run before building:
- Node or a headless browser (for QA): `agent-browser` / Playwright / `chromium --headless`
- Python 3 + PIL: `python3 -c "import PIL"` (QA script dependency)
- No build step, no dependencies — the poster is one self-contained `index.html`
