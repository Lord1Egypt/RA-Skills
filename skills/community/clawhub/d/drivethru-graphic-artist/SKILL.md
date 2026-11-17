---
name: drivethru-graphic-artist
description: Graphic-artist tasks for Bacon & Co decorations — (1) generate product mockups by compositing a decoration (logo/graphic) onto a blank product photo (deterministic; no model-generated pixels; self-reviewed), (2) make a DTF decoration "production-ready" / "drop the art" — take the real thumbnail, size it to the decoration location, render at 300 DPI, upload the DTF production file, set size + colors, and create a print sample, driving the decoration toward the 'done' state via the drivethru_mcp decoration_* tools, and (3) clean up degraded / AI-generated flat art before production — deterministically snap it back to its true inks, rebuild faded/broken/jagged outlines, and re-render crisp at print size (fixes the "looks fine as a thumbnail, falls apart at 13 inches" problem). Use whenever the user wants to see a logo on a garment, place artwork on a blank, remove an image background (knock a solid color out of flat art, or segment a photographic subject), tune a print's size/position, clean up / fix / "drop for production" a low-quality or AI-generated logo (ghosting, haze, jagged or fading outlines, soft edges), OR make a decoration production-ready / drop art / get a DTF decoration to done.
version: 0.18.1
emoji: 🎨
metadata:
  openclaw:
    requires:
      bins: [python3]
    envVars:
      MOCKUP_DATA_DIR:
        required: false
        description: >
          Directory for the editable placement-rules catalog and rendered
          mockup outputs. Defaults to `~/.drivethru/mockup`. The bundled
          starter catalog (assets/placement_rules.json) is used read-only
          until the first edit, which seeds an editable copy here.
      MOCKUP_VISION_API_KEY:
        required: false
        description: >
          API key for the independent vision review in the web-image routine
          (web_mockup_job.py / vision_review.py). Falls back to
          OPENROUTER_API_KEY. Without one, mockups are never written.
      MOCKUP_VISION_MODEL:
        required: false
        description: >
          Vision model slug for the review (default anthropic/claude-sonnet-5
          on OpenRouter). MOCKUP_VISION_BASE_URL overrides the
          OpenAI-compatible endpoint (default https://openrouter.ai/api/v1).
    install:
      uv:
        - Pillow>=10.3,<12
        - numpy>=1.24,<3
        - rembg>=2.0.56,<3
        - onnxruntime>=1.18,<2
        - scipy>=1.10,<2
        - opencv-python-headless>=4.8,<6
        - requests>=2.31,<3
---

# Drivethru Graphic Artist — Product Mockups

Take a **blank** product photo plus a **decoration** image and return a
composite **mockup**. Compositing is deterministic image manipulation: Pillow
for transform/compose, [rembg](https://github.com/danielgatis/rembg) (U²-Net
segmentation — *not* generative) for background removal and garment bbox
detection.

**No pixels are ever model-generated.** The compositing pipeline never invokes
a generative model — only fall back to an image model to *create* artwork if
the user *explicitly* asks (e.g. "generate a new logo"), and say so first.

**But you must review your own output.** After composing, you (the model
running this skill) `Read` the rendered PNG, judge the placement, and
re-compose with corrective deltas if it's off — up to 3 attempts — before
returning it. This is judgment, not generation: it only tunes the same numeric
flags a human would. See [Self-review loop](#self-review-loop-required) below.

## The three inputs

1. **Blank** — photo of the product (t-shirt, hoodie, hat, mug, …). Any
   resolution or crop; the garment's bounding box is detected automatically.
2. **Decoration** — the logo/graphic to place. PNG with transparency is ideal.
   For an opaque image, pre-clean it first: a **flat logo on a solid color**
   should go through `knockout_color.py` (crisp edges, no halo — see
   [Background removal](#background-removal-flat-art-vs-photos)); `--auto-remove-bg`
   runs rembg inline and is meant for a *photographic* decoration, not flat art.
3. **Placement** — where it goes: `full_front`, `left_chest`, `right_chest`,
   `center_chest`, `left_sleeve`, `right_sleeve`, `left_leg`, `right_leg`
   (front of that leg on shorts/pants), `full_back`, `back_yoke`, `front`, … (left/right = the **wearer's** — see
   [Left / right means the WEARER's](#left--right-means-the-wearers)).

**Category** (hoodie / tee / hat / mug / …) is helpful but optional. If the
user doesn't say, infer it from the image or chat, or omit it to fall back to
the `_defaults` rules.

## How placement works

Placement rules are **ratios against the detected garment bounding box**, not
absolute pixels or inches, so a youth tee and an adult tee get visually
matching prints. Each rule has `width_ratio`, `x_center_ratio`, `y_top_ratio`,
`rotation_deg`, and an optional `max_height_ratio` (caps print height to fit a
location's height box — e.g. a hoodie full-front print must clear the pocket).
Look-up order: `(category, placement)` → `(_defaults, placement)` → error.

The shipped ratios are reconciled to real industry print dimensions — see
[`references/decoration_spec.md`](references/decoration_spec.md) (with the
canonical placement diagram at `assets/decoration_guide.png`). That's the
ground truth the self-review loop judges against: a chest logo is pocket-sized
(~¼ the width of a full front), a full back equals a full front, etc.

The catalog ships with the skill at `assets/placement_rules.json` (read-only
starter). When the agent adds or refines rules, an editable copy is created in
the data dir (`$MOCKUP_DATA_DIR` or `~/.drivethru/mockup`) and persists there.
See [`references/placement_rules_schema.json`](references/placement_rules_schema.json)
for the exact schema.

## Requirements

- `python3`, plus `uv` on PATH (used to self-bootstrap dependencies).
- **Dependencies install themselves — you never have to `pip install` by hand.**
  Each script ensures its own imports at startup: if `Pillow`/`numpy`/`rembg`
  aren't already importable, it builds a cached venv in the data dir
  (`$MOCKUP_DATA_DIR/.venv`, default `~/.drivethru/mockup/.venv`) with `uv` and
  re-execs into it. Hosts that honor the frontmatter `install.uv` pre-install
  everything and the bootstrap is a no-op; otherwise the first run pays a short
  one-time install. See [`scripts/_bootstrap.py`](scripts/_bootstrap.py).
- Three dependency tiers, so the common flat-art path stays cheap:
  - **light** — `Pillow` + `numpy`. Everything except segmentation and cleanup
    (`knockout_color.py`, `prepare_dtf_production.py`, `extract_colors.py`).
    Installs in ~2 s, no model download.
  - **cleanup** — adds `scipy` + `opencv-python-headless` (a few tens of MB of
    wheels, **no** model download). Only `cleanup_art.py` pulls it in — scipy for
    the despeckle/close morphology, headless OpenCV for the corner-preserving
    vector trace. Works fully offline. (`--method raster` skips OpenCV and needs
    only scipy.)
  - **heavy** — adds `rembg` + `onnxruntime` (~170 MB of wheels **plus** a
    one-time ~170 MB `u2net` model download on first segmentation). Only
    `remove_background.py`, `detect_garment_bbox.py`, and `compose_mockup.py`
    pull it in. The model download needs outbound network once; if it's blocked,
    bbox detection falls back to the full image frame and `--auto-remove-bg`
    errors — but the color-key path (`knockout_color.py`) still works offline.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/compose_mockup.py` | The workhorse: detect bbox, look up rule, scale/rotate/paste, write PNG, print a JSON receipt. |
| `scripts/detect_garment_bbox.py` | Standalone: print the garment bbox JSON for a blank. |
| `scripts/knockout_color.py` | **Flat art:** key a solid background *color* out (logos/line art/decals) → RGBA PNG with clean anti-aliased edges. Color-to-alpha or flood (die-cut); `--analyze` first to see what each mode removes and get a color-list-backed recommendation. The right tool for a logo on a plate — see [Background removal](#background-removal-flat-art-vs-photos). |
| `scripts/remove_background.py` | **Photos:** run rembg (U²-Net segmentation) on a *photographic* subject → RGBA PNG. Wrong tool for flat logos — use `knockout_color.py` for those. |
| `scripts/thumbnail_card.py` | Composite art/cutout onto a neutral gray or checker card → a legible **thumbnail** for the DB `image` field (white art stops vanishing). Human-facing only; never the production file. Optional. |
| `scripts/edit_placement_rule.py` | Schema-validated, atomic mutator for `placement_rules.json` (`show` / `add` / `update` / `remove`). |
| `scripts/cleanup_art.py` | **Fix degraded / AI-generated flat art** (before a drop): snap it to its true inks, rebuild faded/broken/jagged outlines, re-render crisp at print size (corner-preserving vector trace, or `--method raster`). Deterministic — no model-generated pixels. Writes a `*_proof.png` (before/after + outline zoom) to `Read` and self-review. See [`references/production_cleanup.md`](references/production_cleanup.md). |
| `scripts/prepare_dtf_production.py` | Production-ready: fit the real art (aspect-locked) into a location's print box and stamp it at 300 DPI → print-ready PNG + inch/pixel receipt. |
| `scripts/extract_colors.py` | Production-ready: extract dominant colors from art as `#RRGGBB` + coverage (feeds `decoration_match_colors`). |
| `scripts/locations.py` | Decoration location name → wearer-side `placement` / `view` / `image_side` (legs included), and which decorations layer onto the front photo. Odoo sends raw names; this is where they are interpreted. |
| `scripts/web_mockup_job.py` | **Web-image routine, end to end:** plan (`web_mockup_plan`) → fetch → art prep → compose → geometry + vision checks → verified upload to every size variant. JSON out only (plus one live progress line per colour on stderr); reports vision `cost` and placement `tuning`. `run` / `adjust` / `status`. See [`references/web_image_routine.md`](references/web_image_routine.md). |
| `scripts/vision_review.py` | Independent vision QA of a rendered mockup → `{verdict: yes/no, checks, issues[{fix}], usage{cost_usd}}`. Sends the image to a vision model over HTTP so it never enters the agent's context. Used by `web_mockup_job.py`. |
| `scripts/upload_production_file.py` | Production-ready: POST a local production file to Odoo's `/drivethru_mcp/v1/upload` route — server-side base64, no chunking, keeps the (large) file out of your token stream. Preferred for a real 300 DPI file **when `ODOO_MCP_URL` + `ODOO_MCP_TOKEN` are set**; when they're absent, stream the file through the `decoration_set_image` MCP tool instead. Same 20 MB server guard either way. |

## Composing a mockup

```bash
python3 scripts/compose_mockup.py \
    --blank /path/to/blank.jpg \
    --decoration /path/to/logo.png \
    --category hoodie \
    --placement full_front \
    [--auto-remove-bg] \
    [--width-delta-pct 0] [--offset-x-pct 0] [--offset-y-pct 0] \
    [--rotate-deg 0] \
    [--output /path/to/out.png]
```

The script prints JSON with the detected `garment_bbox`, the resolved `rule`,
the `applied` ratios/deltas, and the `output` path. Return the PNG to the user
and add one line in human terms ("55% of the garment width, centered on the
chest, no rotation").

Defaults: rules come from the editable data-dir copy if present, else the
bundled starter; output goes to `<data dir>/out/<uuid>.png`. Override with
`--rules` / `--output`.

## Self-review loop (required)

The ratio rules are a *starting guess*. For a given garment/decoration pair
they can land the print too high, too small, or off-center — and the
deterministic pipeline can't notice, because it has no eyes. You do. **Do not
return the first compose unseen.**

After every compose, run this loop before handing anything to the user:

1. **Compose** with the current flags; note the `output` path from the receipt.
2. **`Read` the output PNG** — actually look at the rendered mockup.
3. **Judge** it against what the placement should look like (centered on the
   chest for `full_front`, small over the pec for `left_chest`, etc.).
4. If it looks good → return it. If it's off and you have attempts left →
   derive corrective deltas and re-compose, **layering them on the previous
   run's flags** (same deltas as the iterative-feedback table: e.g. print
   riding too high → `--offset-y-pct +8`; too small → `--width-delta-pct +12`).
5. **Hard cap: 3 compose attempts.** If attempt 3 still isn't great, return the
   best one and tell the user in one line what's still off and offer to keep
   tuning. Never loop past 3, and never ping-pong a delta's sign — if you
   overshoot, you're close; accept the better result.

The full review checklist (per-placement targets, critique→delta mapping,
oscillation/no-progress guards, what to tell the user) is in
[`references/self_review.md`](references/self_review.md), and the targets there
are anchored to real print dimensions in
[`references/decoration_spec.md`](references/decoration_spec.md). This runs
entirely in-container — you are the reviewer; there is no separate model call.

## Iterative feedback

Mockups are a back-and-forth. When the user says "bigger", "move it up",
"rotate it", layer deltas on top of the **previous** run's args (e.g.
`--width-delta-pct +10`, `--offset-y-pct -5`, `--rotate-deg 5`). Keep a running
record of the current flags so each turn builds on the last. The full
feedback→flags mapping and how to promote a tuned result into a saved default
are in [`references/iterative_feedback.md`](references/iterative_feedback.md).

## Cleaning up degraded / AI-generated art

Some art that comes in isn't clean vector — it's **"fake vector":** a logo an
image model generated (or someone upscaled from a tiny JPEG) that *looks* crisp
at thumbnail size but is a soft raster full of **ghosting, desaturated haze,
faded/broken outlines, jagged uneven strokes, and blurry edges.** You don't see
it in the DB thumbnail; it's glaring once it prints at **13″**. Catching and
fixing that is part of "dropping for production."

**The move is to restore, not regenerate.** A human artist wouldn't salvage the
blurry pixels or feed it to an image generator (which would rewrite the
letterforms and text) — they'd rebuild it as the few flat inks it was always
meant to be. `scripts/cleanup_art.py` does exactly that, **deterministically (no
model-generated pixels):** snap every pixel to its true ink (dropping the
haze/ghost), despeckle + close each ink mask to rejoin broken outlines, and
re-render each mask crisp at print size with a **corner-preserving vector trace**
(smooths the jaggies/waviness without rounding letter corners).

```bash
python3 scripts/cleanup_art.py --input /tmp/thumb.png \
    --inks '#26296B,#A0202C,#FFFFFF' \     # decoration colors[].rgb_hex (best source)
    --output /tmp/thumb_clean.png
```

It writes the cleaned PNG **plus a `*_proof.png`** (before/after on gray + dark,
and a zoom on the outline detail where defects hide) and a JSON receipt with a
`review_checklist`. **`Read` the proof and self-review it** — outlines crisp and
uniform? corners still sharp? letterforms unchanged? ghost/haze gone? — then tune
and re-run if needed. Same eyes-on discipline as the mockup
[self-review](references/self_review.md); the customer sees the reviewed result.

This restores *intent*, it doesn't redesign: it keeps intended style (e.g. hollow
outline letters stay hollow), preserves counters, and **can't invent a mark
that's genuinely missing** (only faded/broken ones) — flag those for a redraw.
Full procedure, the defect-recognition guide, tuning table, and the
faithful-vs-restyle line: **[`references/production_cleanup.md`](references/production_cleanup.md).**

## Making art production-ready (DTF) — "dropping" the art

Separate from mockups: when the user gives you a **decoration id** and asks to
make it **production-ready** / **drop the art** / **get it to done**, you take the
decoration's real thumbnail, size it to its location, render it at **300 DPI**,
upload the DTF production file, set the actual size + colors, and create a print
sample — driving the record toward the `done` state. **First inspect the art at
production scale** — if it's degraded / AI-generated (ghosting, haze, faded or
jagged outlines), clean it up with `cleanup_art.py`
([above](#cleaning-up-degraded--ai-generated-art)) *before* sizing it. This is deterministic image
work (the same *no model-generated pixels* rule applies) and almost always
applies to decorations whose method is **DTF**.

You drive it through the `drivethru_mcp` **`decoration_*`** MCP tools
(`decoration_get_production_readiness` → `decoration_get_image` →
`decoration_set_image` → `decoration_update_fields` → `decoration_match_colors` →
`decoration_create_sample` → `decoration_set_state`) plus the two scripts
`prepare_dtf_production.py` and `extract_colors.py`.

> **How to call these:** the `decoration_*` tools are MCP tools your host
> already exposes — invoke each one **directly as a tool call**, like any other
> tool available to you. Do **not** hand-roll an HTTP request to the Odoo host to
> *invoke* a tool, and do **not** go hunting for an `ODOO_MCP_URL` / `ODOO_MCP_TOKEN`
> to POST against for that: there is **no `/call` REST route**, so a 404 there
> means you invented a URL, not that the MCP is down.
>
> Raw HTTP has exactly **two** legitimate uses here — both for moving image
> *bytes* out of your token stream, never for invoking a tool: **downloading** a
> `cdn_url` that `decoration_get_image` returns for a large/offloaded binary
> (step 2), and **uploading** a real production file with `upload_production_file.py`
> (step 5, when `ODOO_MCP_URL` / `ODOO_MCP_TOKEN` are set). Everything else is a
> tool call.

Start with `decoration_get_production_readiness` — it returns a `blocking_gaps`
list mirroring Odoo's own `done` gate (production file, size, colors, sample,
and a completed linked design). Per-location max print sizes come from the Odoo
`decoration_location` record, with [`references/location_dimensions.json`](references/location_dimensions.json)
(built from the official spec sheet, `references/decoration_spec_sheet.pdf`) as
the fallback.

Note: a decoration can't actually reach `done` without a linked `design` in the
`done` state — expect that gap to remain and report it, after completing every
other step and creating the ready sample.

**Full step-by-step procedure: [`references/production_ready.md`](references/production_ready.md).**

## Batch mockup routine (Mockup Artist Agent)

Separate from the interactive workflow: the **Mockup Artist Agent** runs a
scheduled routine that sweeps Odoo for open decoration requests **assigned to
Zach Tucker**, and — for each one where both a **blank product image** and a
**decoration image** are already attached — generates a mockup and writes it
into the request's `mockup_image` field. Requests missing an input, or that
already have a mockup, are recorded as `skipped` and left alone. Rendering is
the same deterministic pipeline (`compose_mockup.py` + the mandatory
[self-review loop](#self-review-loop-required)); this routine only wraps it
in a per-request loop plus the Odoo read/write plumbing (dotted-path search
across `sale.order.decoration_request_ids`, attachment listing, base64 write
via `decoration_set_image`).

**Full step-by-step procedure, per-outcome logging, and the exact routine
prompt/cron to paste into the agent's Routines page:
[`references/mockup_routine.md`](references/mockup_routine.md).**

## Web-image routine — per-color storefront mockups (Mockup Artist Agent)

A second scheduled routine — **"General Purpose Web image generation
routine"** — images the **storefront catalog**: products built in bulk from
blanks + decorations when a store is created, which arrive with no image. For
each colour it composites the product's front decoration(s) onto that colour's
blank and writes the mockup to every size variant of the colour.

**It is one command — `scripts/web_mockup_job.py run --site-id <id>` — and it
is different from the interactive flow above in three ways that matter:**

- **Do not `Read` or open any image in this routine.** The self-review is done
  by an independent vision model inside the script (`vision_review.py`), which
  returns a yes/no verdict as JSON. Images in your context balloon the session.
- **Do not fetch or write images yourself** — no `decoration_get_image`, no
  `include_binary`, no `product_write` image fields, no chunked
  `decoration_set_image`. The script downloads over HTTP and uploads byte-exact
  through `POST <ODOO_MCP_URL>/upload`, verified.
- **A "no" verdict comes with a fix:** run the job's `next` command
  (`web_mockup_job.py adjust --job <job> --apply-suggested`). Max 3 attempts.

Blank presence and art choice (embroidery/DTF production PNG before the
thumbnail, whose background is removed and verified) are resolved server-side
by the `web_mockup_plan` MCP tool, which returns each decoration's raw location
name. Wearer-side placement is decided in the skill by `scripts/locations.py`.

**Full procedure, hard rules, statuses, and the exact routine prompt:
[`references/web_image_routine.md`](references/web_image_routine.md).**

## Left / right means the WEARER's

Every placement name — `left_chest`, `right_chest`, `left_sleeve`,
`right_sleeve` — refers to the **wearer's** side. Blanks are flat **front**
photos, so the wearer's left is on the **image's right** (`x_center_ratio >
0.5`) and the wearer's right is on the image's left. The bundled rules follow
this; `compose_mockup.py` mirrors (and warns about) any rule that doesn't, and
`edit_placement_rule.py` refuses to save one. `--offset-x-pct` is always in
image coordinates: positive moves toward the image's right. Plain `sleeve` is
rejected as ambiguous.

## Editing the rules catalog

Show the current catalog:

```bash
python3 scripts/edit_placement_rule.py show [--category hoodie] [--placement full_front]
```

Add a new category/placement when one is missing:

```bash
python3 scripts/edit_placement_rule.py add tote front \
    --width-ratio 0.45 --x-center-ratio 0.50 --y-top-ratio 0.30
```

Refine an existing default (e.g. after the user approves a tuned result):

```bash
python3 scripts/edit_placement_rule.py update hoodie full_front --width-ratio 0.58
```

Edits are validated and written atomically to the editable copy in the data dir
(seeded from the bundled starter on first edit) — the shipped asset is never
mutated.

## Background removal: flat art vs photos

There are **two** background removers here because they solve different problems.
Pick by what the source *is*, not by habit:

| The source is… | Use | Why |
|---|---|---|
| **Flat art** on a solid color — a logo, line art, a decal, a DTF thumbnail on a white plate | `knockout_color.py` | Keys on the actual color, so edges stay crisp and there's no halo |
| **A photographic subject** — a real object/garment/person to isolate from a busy scene | `remove_background.py` (rembg) | U²-Net segmentation finds the salient subject a color key can't |

**Do not use rembg (`remove_background.py`) on a flat logo.** rembg is a
salient-object segmentation model built for photos; on flat art it produces a
soft matte that leaves a light **halo**, and it has no notion of "make *this*
color transparent," so it can't cleanly knock out a white plate.

### Knocking a color out of flat art

```bash
python3 scripts/knockout_color.py --input /tmp/logo.jpg --output /tmp/logo.png \
    [--mode color-to-alpha|flood] [--color auto|'#RRGGBB'] [--fuzz 0.10] [--feather 2]
```

The key color defaults to `auto` (median of the four corners). Two modes:

- **`color-to-alpha`** (default) — remove the key color **everywhere**, with
  clean anti-aliased edges. Each pixel's alpha becomes proportional to its
  distance from the key color and the foreground color is un-multiplied back
  out, so a gray edge pixel becomes *semi-transparent black* instead of an
  opaque gray rim. Best for one-color line art you want printed as ink on the
  garment (the garment shows through letter counters and open areas).
- **`flood`** — remove only the background **connected to the border** (a
  tolerant flood fill, feathered at the edge). Enclosed regions of the key color
  are **kept** — a white field inside an outline stays white. This is the
  "die-cut sticker" look.

#### Which mode? Decide it, don't guess it

The choice hinges on one thing: **is the key color an *ink* on this decoration,
or just background?** If it prints → `flood` (keep it). If it's background →
`color-to-alpha` (knock it out). Don't eyeball-guess, and don't blindly trust the
color list either — **run `--analyze` first** and reconcile the two:

```bash
python3 scripts/knockout_color.py --input /tmp/thumb.png --analyze \
    --expect-colors '#000000'      # the decoration's declared inks (colors[].rgb_hex)
```

Analyze writes nothing and reports:
- the auto-detected **key color**, and whether it matches a declared ink;
- **`enclosed_fraction`** — key-color pixels *inside* the art (letter counters, a
  field inside an outline). This is the number that decides whether the mode even
  matters: near-zero → both modes look the same; large → it's a real call;
- a **`recommended_mode`** derived from the inks (key color is a declared ink →
  `flood`; not → `color-to-alpha`), plus `warnings`.

**Use the color list as a guide, then verify.** The inks are operator-entered and
can be stale or wrong, so treat the recommendation as a strong prior, not a
verdict — when `decision_matters` is true, `Read` the actual cutout before
trusting it. Ask the user **only** when the signal is genuinely ambiguous
(a meaningful `enclosed_fraction` **and** the inks don't resolve it, or the inks
contradict what you see) — show both rendered options in the question. When the
inks clearly resolve it and the result looks right, just proceed.

> Example — decoration 2878 (Bacon & Co logo): declared inks `[Black]`, so white
> is *not* an ink → analyze recommends `color-to-alpha`, but flags that it removes
> ~38% of the image (the interior field). Correct call (a one-color black print
> where the garment shows through), but big enough to eyeball before uploading.

#### The thumbnail's background is not a print instruction

A decoration has two separate image artifacts — don't let one contaminate the
other:

| | `image` (thumbnail) | `dtf_production_png` (production file) |
|---|---|---|
| For | humans browsing the DB | the printer |
| Background | **keep one** — legibility wins | **none** — true cutout on transparency |
| Decides "does white print?" | never | its alpha, set from the color list |

So a thumbnail sitting on a white plate tells you **nothing** about whether that
white should print — that's what `--expect-colors` is for. **Do not assume
thumbnails have any particular background**; today they carry whatever was
supplied (a plate, a photo backdrop, or nothing), and migrating them is a slow,
separate effort. Point the knockout at the thumbnail regardless and let the color
list drive the cutout. If a thumbnail is itself hard to see (white art on a white
UI), fix the *thumbnail* with `thumbnail_card.py` (composite onto a neutral gray
or checker card) — never by baking a background into the art or the production
file.

Two failure modes this replaces — both from treating flat art as a photo or as a
hard threshold:

- *"Small halo, and white left inside the logo"* → rembg's soft matte + no
  interior handling. `color-to-alpha` removes all the white (interior included)
  with no halo; `flood` keeps the interior on purpose.
- *"The black border got all muddied up"* → a hard "make white transparent"
  threshold leaves the anti-aliased gray edge pixels fully opaque, so the smooth
  edge turns into a dirty jagged rim. `color-to-alpha` ramps those edge pixels'
  alpha instead, keeping the border crisp.

### Segmenting a photographic subject (rembg)

```bash
python3 scripts/remove_background.py --input /tmp/photo.jpg --output /tmp/cut.png
```

If the input already has meaningful transparency it is copied through unchanged
(`{"skipped": true}`); pass `--force` to re-run rembg anyway.

## Rules to follow

- **No model-generated pixels** in the compositing *or* cleanup pipeline unless
  the user explicitly asks — and say so first. Cleaning up degraded art means
  restoring its existing inks deterministically, **not** regenerating it (a
  generative model would rewrite the letterforms/text). Reviewing your own output
  is fine and required — that's judgment, not generation.
- **Inspect art at production scale before a drop.** A thumbnail hides ghosting,
  haze, and faded/jagged outlines that wreck a 13″ print. If the art is degraded
  or AI-generated, clean it with `cleanup_art.py` and `Read` the proof before
  sizing — see [Cleaning up degraded art](#cleaning-up-degraded--ai-generated-art).
- **Always self-review before returning.** `Read` the rendered PNG and
  re-compose with deltas if the placement is off, up to 3 attempts. See
  [Self-review loop](#self-review-loop-required).
- **Respect aspect ratio.** `compose_mockup.py` locks it automatically; never
  hand it raw pixel dimensions that would squash the decoration.
- **Don't assume a file exists.** Verify input paths before composing.
- **Save every mockup** so you can diff between iterations.
- **Lead with the reviewed result** (the PNG), then one line on the placement
  (and any auto-adjustment you made), then ask what to tune next.
- When ambiguous ("put it on the chest"), ask one clarifying question
  ("full front or left chest?") rather than guessing.

## When NOT to use

- The user wants a brand-new logo/design *created* from a prompt → that's
  generative image work, out of scope here.
- The user wants vector/print-ready separations, embroidery **DST** digitizing,
  or color-by-color screen seps → out of scope. (Preparing a **DTF** production
  PNG at 300 DPI *is* in scope — see [Making art production-ready](#making-art-production-ready-dtf--dropping-the-art).)
- The user wants a photoreal render with lighting/wrinkle warping → this skill
  does flat ratio-based compositing, not 3D/displacement warping.
