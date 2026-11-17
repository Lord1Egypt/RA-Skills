# Browser-Based Visual QA

How to verify a canvas poster actually renders correctly — before delivering it. QA passing is not the finish line; delivery is.

## Tooling

Any headless browser works: `agent-browser` (preferred in agent sandboxes), Playwright, or `chromium --headless`. The poster is a single self-contained HTML file — just open it.

With `agent-browser`:
```bash
agent-browser open file:///path/to/poster/index.html
agent-browser eval "JSON.stringify({w: canvas.width, h: canvas.height})"
```

## Check 1 — Render integrity

```js
// Initial state
({ w: canvas.width, h: canvas.height })          // → {w: W, h: H} (logical)

// 4K export state
applyScale(4); render();
({ w: canvas.width, h: canvas.height })          // → {w: W*4, h: H*4}
// ✅ If not exactly 4×, applyScale is mutating the wrong variable

applyScale(1); render();                          // ALWAYS restore preview after
```

## Check 2 — Valid PNG output

```js
canvas.toDataURL().slice(0, 22)
// → "data:image/png;base64"  ✅
// An empty/blank canvas also returns a valid PNG header! That's why Check 3 exists.
```

## Check 3 — Pixel-zone verification (catches blank/broken renders)

Download (or `toDataURL`) the PNG, then run the bundled script:

```bash
# Sample coordinates in LOGICAL design units; --scale converts them:
python3 scripts/qa_poster.py poster_4x.png --scale 4 \
    --expect 3600x5092 \
    --sample 60:120:#000814        # top-left = background color
    --sample 450:300:#00b4d8       # center of an accent element
```

Pick sample points deliberately:
1. A **background** point (proves base fill drew)
2. An **accent** element center (proves shapes drew)
3. A point that differs between **cards and gaps** (proves layout, not just fill)

A blank white canvas passes Checks 1–2 but fails Check 3. This is the check that matters.

## Check 4 — Text completeness (grep, not eyes)

Every string the user asked to include must exist as a `fillText` argument:

```bash
grep -c "Agentic AI Marketplace" index.html       # every required string ≥ 1
```

After a **removal** edit, invert the check: `grep -n "<removed string>" index.html` → expect **zero** matches, and confirm surrounding drawing code (gradient/fillRect calls) survived — remove only the specific `fillText` line(s).

## Check 5 — Human look (if you can view images)

`chromium --headless --screenshot=preview.png file://.../index.html` then view the PNG. If image viewing is available, a 10-second look catches what pixel sampling can't: kerning disasters, overlapping text, a glow that reads as a smudge.

## Delivery checklist

- [ ] All 5 checks pass
- [ ] Poster opens correctly from a fresh browser tab (no stale-cache illusions)
- [ ] File delivered via the proper delivery channel (in agent sandboxes: the file-send tool — an unsent file is an unfinished task)
