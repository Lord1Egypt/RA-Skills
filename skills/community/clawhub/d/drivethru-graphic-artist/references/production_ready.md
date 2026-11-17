# Making art production-ready — "dropping" a DTF decoration

**Production-ready** (internally: *dropping the art*) means driving a
`decoration` record to the **`done`** state. This almost always applies to
decorations whose `decoration_method` is **DTF**. It is deterministic
image work — take the decoration's **real** thumbnail, size it to the location,
render it at 300 DPI, and record the facts back into Odoo. **No pixels are
model-generated** (same principle as the mockup pipeline).

You drive this through the `drivethru_mcp` **`decoration_*`** MCP tools plus the
two skill scripts below. Give the agent a decoration id and it does the rest.

> **Transport — two rules.**
> 1. Every **non-image** step below (readiness, sizes, colors, state, sample) is
>    an **MCP tool call** — invoke it directly, like any other tool. There is
>    **no `/call` route**; a 404 from one is a hand-rolled request that shouldn't
>    exist, so call the tool instead, and don't go hunting for an
>    `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` to POST against for it.
> 2. Moving image **bytes** is the one place raw HTTP is right — only to keep
>    megabytes of base64 out of your token stream: **download** a `cdn_url` that
>    `decoration_get_image` returns for a large/offloaded image (step 2), and
>    **upload** the production file with `upload_production_file.py` when
>    `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` are set (step 5). Both byte paths still hit
>    the same 20 MB server guard as the tools.

## What `done` requires (DTF)

`decoration_get_production_readiness` returns a `blocking_gaps` list that mirrors
Odoo's own gate. To reach `done` a DTF decoration needs:

- `dtf_production_png` uploaded (→ `decoration_production_ready`)
- non-zero `size_width` **and** `size_height` (inches)
- `colors` populated **and** `len(colors) == color_count`
- a printed sample, if `artwork_module_custom.dtf_sample_required` is on
- a `design_id` whose own `state == 'done'`
- a real `name` (must not contain the word "decoration")

## The procedure

### 1. Read the current state
`decoration_get_production_readiness { decoration_id }`. Confirm `is_dtf` is
true, note the `location.max_width` / `max_height` (inches) and the current
`blocking_gaps`. If the location has no max set, fall back to
[`location_dimensions.json`](location_dimensions.json), matching by location
name (adult column unless the order is youth).

### 2. Pull the thumbnail
`decoration_get_image { model:"decoration", record_id, field:"image" }`. A small
image returns inline `data_base64`; a large or CDN-offloaded one returns a
`cdn_url` instead (with a note saying so) — that's **expected, not an error**.
When you get a `cdn_url`, fetch it directly with the container's HTTP client
(`curl` / `requests`) so the bytes skip your token stream. Save the result to a
temp file.

**If the thumbnail has a solid background (e.g. a logo on a plate) and needs a
clean cutout, knock the color out with `scripts/knockout_color.py` — not rembg.**
A DTF thumbnail is flat art, so color-keying gives crisp edges with no halo;
rembg (`remove_background.py`) is for photographic subjects and leaves a soft
fringe on a logo. Do **not** read print intent from the thumbnail's background —
a white plate does not tell you whether white prints. The decoration's **color
list** tells you that, so drive the cutout from it.

**Analyze first, with the declared inks.** Pass `colors[].rgb_hex` from the
readiness call as `--expect-colors`:

```bash
python3 scripts/knockout_color.py --input /tmp/thumb.png --analyze \
    --expect-colors '#000000,#FFFFFF'   # <- the decoration's colors[].rgb_hex
```

Read the receipt:
- `key_is_declared_ink` **true** → the background color prints → keep it →
  `--mode flood` (die-cut; enclosed areas of that color stay).
- `key_is_declared_ink` **false** → it's background → knock it out →
  `--mode color-to-alpha` (default; the garment shows through open/interior areas).
- Let `enclosed_fraction` / `decision_matters` calibrate your care: near-zero means
  the modes are equivalent here; large means it's a consequential call.

Then cut with the chosen mode:

```bash
python3 scripts/knockout_color.py --input /tmp/thumb.png --output /tmp/thumb_cut.png \
    --mode color-to-alpha --expect-colors '#000000,#FFFFFF'
```

**The color list is a guide, not gospel** — it's operator-entered and can be
stale. So when `decision_matters` is true, **`Read` the cutout before moving on**
(same self-review discipline): confirm the plate is gone, edges are clean, and any
interior color you meant to keep is still there. Ask the user only when the inks
don't resolve it or contradict what you see — showing both rendered options. Then
feed the cutout into step 3. Running `extract_colors.py` on a proper cutout also
yields a clean color list (transparent plate ignored) instead of a stray white.

> **Thumbnails vs production files.** The cutout is the *production* file
> (`dtf_production_png`); it belongs on transparency. Don't overwrite the `image`
> thumbnail with it — a bare cutout makes a poor thumbnail (white art vanishes in
> the DB). If a thumbnail needs to be legible, render one with
> `scripts/thumbnail_card.py` (art over a neutral gray/checker card). Thumbnails
> today carry whatever background was supplied — don't assume they're normalized.

### 2.5 Clean up degraded / AI-generated art (if needed)
Before you size it, **look at the art at production scale.** A DTF file prints at
up to 13″ — defects invisible in the DB thumbnail are glaring there. If the art is
degraded / AI-generated — **ghosting, desaturated haze, faded or broken outlines,
jagged uneven strokes, soft edges** — clean it first, or you'll drop a bad file.

Restore, don't regenerate: snap the art back to its true inks, rejoin the broken
outlines, and re-render crisp — deterministically, **no model-generated pixels**
(a generative model would rewrite the letterforms). Pass the decoration's declared
colors as the ink truth:

```bash
python3 scripts/cleanup_art.py --input /tmp/thumb_cut.png \
    --inks '#000000,#FFFFFF' \            # colors[].rgb_hex from the readiness call
    --output /tmp/thumb_clean.png
```

Then **`Read` the `*_proof.png`** it writes (before/after + an outline zoom) and
self-review it against the receipt's `review_checklist` — outlines crisp and
uniform, corners still sharp, letterforms unchanged, ghost/haze gone. Tune and
re-run if off (see the tuning table in
[`production_cleanup.md`](production_cleanup.md)). If the art is already clean flat
vector, skip this. If a mark is genuinely *missing* (not just faded), cleanup can't
invent it — flag it for a redraw. Feed the cleaned PNG into step 3.

**Full guide, defect-recognition, and tuning: [`production_cleanup.md`](production_cleanup.md).**

### 3. Size + 300 DPI (deterministic)
```bash
python3 scripts/prepare_dtf_production.py \
    --input /tmp/thumb.png \
    --max-width-in <location max_width> --max-height-in <location max_height> \
    --dpi 300 \
    --output /tmp/dtf_production.png
```
It fits the art (aspect-locked) into the location box, stamps 300 DPI, and prints
a receipt with the **actual** `print_inches` (width/height) and `output_px`. Keep
those inches — they become the decoration's size. Pass explicit
`--target-width-in/--target-height-in` only when the order specifies a size.

### 4. Extract the colors
```bash
python3 scripts/extract_colors.py --input /tmp/dtf_production.png --max-colors 6
```
Returns dominant colors as `{rgb_hex, coverage_pct}`. Tune `--max-colors` /
`--min-coverage`, and add `--ignore-white` when the art sits on a white plate you
don't want counted. Sanity-check the list by eye (open the PNG) — drop stray
anti-aliasing colors.

### 5. Upload the production file

A real 300 DPI DTF file is large, and emitting it as base64 through your token
stream is slow and error-prone — that's *why* the HTTP upload path exists. Both
paths below enforce the same 20 MB server guard; pick by whether the upload
credentials are present.

**Preferred when `ODOO_MCP_URL` + `ODOO_MCP_TOKEN` are set — the HTTP upload
helper.** POST the file straight from disk; the bytes never touch your token
stream:
```bash
python3 scripts/upload_production_file.py \
    --file /tmp/dtf_production.png --record-id <id> --field dtf_production_png
# defaults to ODOO_MCP_URL / ODOO_MCP_TOKEN (or pass --base-url / --api-key).
# Prints the server JSON: present + cdn_url/web_url.
```
This POSTs to `/drivethru_mcp/v1/upload`; the server base64-encodes and writes
the field (CDN offload → production-ready), byte-exact.

**Fallback when those env vars aren't set — the `decoration_set_image` MCP
tool.** Needs no extra environment, and writing `dtf_production_png` uploads to
the CDN on save and flips the decoration production-ready:
`decoration_set_image { model:"decoration", record_id, field:"dtf_production_png",
data_base64:<the prepared PNG> }`. A 300 DPI file is almost always too big for
one call, so stream it: split the raw PNG into N slices, base64-encode each on
its own, and send one call per slice sharing an `upload_id` with `chunk_index`
(0-based) + `chunk_count:N`; the field is written when the last slice lands
(`complete:true`).

Either way: if the env vars are missing, use the tool; if they're present, use
the helper — don't invent a `/call` or other route to bridge the two.

### 6. Record the actual size
`decoration_update_fields { decoration_id, fields:{ size_width:<in>, size_height:<in> } }`
using the `print_inches` from step 3.

### 7. Assign the colors
`decoration_match_colors { decoration_id, colors:[{rgb_hex}, ...] }` with the hex
list from step 4. The tool maps each hex to the nearest existing `color` record
(CIEDE2000 over `rgb_hex`), or creates one from the nearest approximate-PANTONE
entry, then sets `colors` + `color_count`. PMS matching lives server-side in Odoo
(that's where the color library and the approximate table are). Note: exact spot
PMS is proprietary — DTF is a full-process print, so treat matched PMS names as
close references, not guarantees.

### 8. Create the print sample
`decoration_create_sample { decoration_id }` — stands up a `decal.demand` sample
already in the **`ready`** state, so it can be printed. Idempotent.

### 9. Try to mark it done
`decoration_set_state { decoration_id, state:"done" }`. Today this will almost
always come back `blocked=true` with **"link a completed design"** — that gate is
expected until it's loosened. Report the remaining gap to the user; everything
else (production file, size, colors, ready sample) is already in place.

## Tips

- Always **look at** the prepared PNG and the extracted colors before uploading
  (same self-review discipline as mockups) — a 300 DPI file at print size is what
  the shop will actually run.
- Re-run `decoration_get_production_readiness` at the end to confirm only the
  design gap (or a sample, if required) remains.
- Only DTF is fully supported here. Embroidery has different production files
  (DST/PNG) and is exempt from the color-count gate.
