# Cleaning up degraded / AI-generated art before production

Some art that comes in for a "drop" isn't clean vector — it's **"fake vector":**
a logo an image model generated (or someone up-scaled from a tiny JPEG) that
*looks* crisp in a 200px thumbnail but is actually a soft raster full of the
defects below. Nobody notices at thumbnail size. Then it prints at **13″** and
the flaws are obvious and un-sellable.

This is the step where you catch that — the same "you have eyes, the pipeline
doesn't" discipline as the mockup [self-review](self_review.md), applied to the
*art itself* before you size and drop it. **Look at the art at production scale,
decide if it's degraded, and if so clean it deterministically first.**

## Recognize the defects (this is the judgment call)

Zoom in (or render the art large and `Read` it). You're looking for the
signature of generated / mangled flat art:

| Defect | What it looks like | Why it matters at 13″ |
|---|---|---|
| **Ghosting** | a faint offset *second copy* of the marks; doubled edges | prints as a blurry shadow next to every edge |
| **Haze / bleed** | a desaturated fog around the inks, on transparency or over a fill | muddy halo, dirty edges |
| **Faded / broken outline** | a stroke that thins, breaks up, or disappears along its length (classic: one side of a word is crisp, the other side "fades out") | outline looks like it's dissolving |
| **Jagged / uneven width** | an outline that should be one weight wobbles thick↔thin and waves | reads as sloppy, not a real logo |
| **Soft / blurry edges** | no crisp ink boundary; everything slightly out of focus | fuzzy print, no snap |

The tell that ties them together: **the art is clearly *meant* to be a few flat
spot-color inks with crisp uniform edges, but the pixels don't deliver that.**
That gap between intent and pixels is what you're fixing. If the art is already
clean flat vector-style color, or it's a photograph, this doesn't apply — skip it.

## The principle: clean up ≠ regenerate

A human artist handed this file for a 13″ print does **not** try to salvage the
blurry pixels, and does **not** feed it to an image generator to "redo it" — a
generative model would rewrite the letterforms, mangle the text, and invent
details, i.e. produce a *different* logo. They rebuild it as what it was always
meant to be: **the handful of inks it already contains, snapped clean, broken
strokes rejoined, edges re-rendered crisp.**

That is exactly what `scripts/cleanup_art.py` does, and it is **deterministic —
no model-generated pixels** (same rule as the rest of this skill). It only
re-expresses inks that are already present; it never invents art. Reach for a
generative model **only** if the user explicitly asks for a redesign and accepts
that the letterforms/text will change — and say so first.

## Procedure

### 1. Get the true inks — prefer the decoration's declared colors
The cleanup keys on the real ink colors. The **best** source is the decoration's
own color list (`colors[].rgb_hex` from `decoration_get_production_readiness`) —
that's ground truth, operator-entered. Pass them with `--inks`:

```bash
python3 scripts/cleanup_art.py --input /tmp/thumb.png \
    --inks '#26296B,#A0202C,#FFFFFF'      # decoration colors[].rgb_hex
```

If there's no declared list, let it auto-detect (`--colors N`), but **auto-detect
is a fallback and can lump a small ink (a thin red outline) into a big fill** —
verify the reported `inks` look right, and prefer declared colors whenever you
have them.

### 2. Run the cleanup
```bash
python3 scripts/cleanup_art.py --input /tmp/thumb.png \
    --inks '#26296B,#A0202C,#FFFFFF' \
    --method vector \                      # default; crispest edges for print
    --output /tmp/thumb_clean.png
```
It classifies every pixel to its nearest ink (dropping the haze/ghost),
despeckles + closes each ink mask to rejoin broken outlines, and re-renders each
mask crisp at print resolution — the **vector** method traces the mask and
smooths it with a **corner-preserving** filter (pins sharp letter corners, smooths
only the straight runs), so you get clean edges *without* rounding off the
letterforms. It writes the cleaned PNG plus a **`*_proof.png`** and a JSON receipt
(ink palette, per-ink pixel counts, params, print size, and a `review_checklist`).

### 3. Self-review the proof (required — do not skip)
`Read` the `*_proof.png`. It shows before vs after on gray and on a dark garment,
plus a **zoom on the outline detail where the defects hide.** Judge it against the
`review_checklist`:

- **Outlines** crisp, continuous, uniform width? (the fade/break/jaggies gone?)
- **Corners** of letters/marks still sharp — not rounded by the smoothing?
- **Letterforms / text unchanged** — nothing merged, dropped, or invented?
- **Ghost/haze gone**, no stray specks, colors match the true inks?
- Anything that was **missing** (not just faded) is still missing — this tool
  can't add a mark that isn't there. Flag it if so.

Good → continue the drop with the cleaned PNG. Off → tune and re-run (below).
Same discipline, same spirit as the mockup loop: **the customer sees the reviewed
result, not the first pass.**

### 4. Tune when the review finds a problem
Layer one change at a time; re-run; re-read the proof.

| What you see in the proof | Change |
|---|---|
| Sharp corners look rounded / letters softened | `--corner-deg 30` (protect more corners) and/or `--smooth-iters 8` (smooth less) |
| Outline still broken / not rejoined | `--close 2` (or `3`) to bridge bigger gaps |
| Haze/ghost still present | `--tolerance 45` (snap tighter) and/or `--alpha-min 140` (drop faint pixels) |
| A real thin/faint mark got dropped | `--tolerance 90` (snap looser) and/or `--alpha-min 70` |
| Tiny real details erased as "specks" | `--min-speck 6` |
| Edges too soft (raster method) | switch to `--method vector`, or lower the raster ramp |
| Still fighting curve smoothness at huge sizes | raise `--supersample 6`, or set `--long-edge-px` to your target |

Don't ping-pong a value's direction; if you overshoot, you're close — accept the
better result. If two or three tuned runs still don't nail it, hand back the best
with a one-line note on what's off (e.g. "the R in the emblem is genuinely missing
a leg in the source — needs a redraw, not a cleanup").

### 5. Feed the cleaned PNG into the normal drop
Use `/tmp/thumb_clean.png` as the input to `prepare_dtf_production.py` (size to
the location box, 300 DPI) and `extract_colors.py`, then upload — the standard
[production-ready](production_ready.md) flow from there. Cleanup slots in **after**
you pull the thumbnail / knock out any plate, and **before** you size it.

## Faithful vs. "improved" — stay on the cleanup side of the line

Cleanup restores *intent*; it does not redesign. Keep these straight:

- **Preserve intended style.** If letters are drawn **hollow** (outline + inline,
  garment shows through the center), that's a design choice — keep it. Don't
  "helpfully" flood the centers solid. (The West Football wordmark is exactly
  this: `WEST` is solid-filled, `FOOTBALL` is hollow. Both are correct.)
- **Preserve counters.** The holes in O/A/B/R/D stay open — the tracer treats them
  as holes automatically; don't fill them.
- **Snap colors, don't restyle them.** Cleanup maps pixels to the inks that are
  already there. Changing the palette, adding a color, or recoloring is a design
  change — ask.
- **Can't invent.** Faded/broken = restorable (the ink is thinly there). *Missing*
  = not restorable here; flag it for a human redraw.
- **When intent is genuinely ambiguous**, ask — show the rendered options, the
  same way the knockout flow does for `flood` vs `color-to-alpha`.

## When to use something else

- **Photographic** subject → this is for flat art; use `remove_background.py`
  (rembg) to isolate a photo subject.
- **Solid plate to knock out** (logo on a white/colored background) → do the
  [knockout](../SKILL.md#background-removal-flat-art-vs-photos) first
  (`knockout_color.py`), then clean up if still degraded.
- **Redesign / new artwork / restyle** → out of scope for cleanup; that's
  generative/manual design work — confirm with the user before going there.
- **Already-clean art** → don't "clean" crisp vector-style art for no reason;
  you'll only risk softening good corners. Only run this when the art is actually
  degraded.

## Worked example — West Football (AI-generated)

Source: a 1024² PNG that reads fine as a thumbnail. At size: `WEST` had a ghosted
double outline; `FOOTBALL`'s navy outline **faded out and broke up** on the left
half and wobbled in width; desaturated haze around everything; soft edges.

```bash
python3 scripts/cleanup_art.py --input west.png \
    --inks '#26296B,#A0202C,#FFFFFF' --method vector --output west_clean.png
```

Receipt: 3 inks (navy/red/white), output ≈ 3953×2702 px = **13.18×9.01″ @ 300 DPI**.
Proof review: ghosting/haze gone; the `FOOTBALL` navy outline is now solid and
uniform across the whole word; edges crisp; W/E/S/T corners still sharp; hollow
`FOOTBALL` centers preserved. One judgment call confirmed by sampling the source —
the hollow letters are *intended*, not a defect — so they were kept, not filled.
Result was production-ready to size and drop.
