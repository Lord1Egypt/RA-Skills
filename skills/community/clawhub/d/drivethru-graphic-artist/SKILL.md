---
name: drivethru-graphic-artist
description: Generate product mockups by compositing a decoration (logo/graphic) onto a blank product photo (t-shirt, hoodie, hat, mug, ...). Deterministic compositing — detects the garment bounding box, scales and positions the decoration via a ratio-based placement-rules catalog, and writes a PNG (no model-generated pixels). Then self-reviews the rendered mockup by eye and auto-corrects placement (up to 3 passes) before returning it. Use whenever the user wants to see how a logo or design looks on a garment/product, place artwork on a blank, remove an image background, or iteratively tune a print's size/position/rotation.
version: 0.3.0
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
    install:
      uv:
        - Pillow>=10.3,<12
        - rembg>=2.0.56,<3
        - onnxruntime>=1.18,<2
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
2. **Decoration** — the logo/graphic to place. PNG with transparency is ideal;
   for a JPG/opaque image pass `--auto-remove-bg` to strip the background.
3. **Placement** — where it goes: `full_front`, `left_chest`, `right_chest`,
   `full_back`, `back_yoke`, `sleeve`, `front`, …

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

- `python3` with `Pillow`, `rembg`, and `onnxruntime` installed (see frontmatter
  `install.uv`).
- On first run, rembg downloads the `u2net` model (~170 MB) to its cache. This
  needs outbound network access once; subsequent runs are offline. If the
  download is blocked, bbox detection falls back to the full image frame and
  `--auto-remove-bg` will error.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/compose_mockup.py` | The workhorse: detect bbox, look up rule, scale/rotate/paste, write PNG, print a JSON receipt. |
| `scripts/detect_garment_bbox.py` | Standalone: print the garment bbox JSON for a blank. |
| `scripts/remove_background.py` | Standalone: run rembg on an image → RGBA PNG. |
| `scripts/edit_placement_rule.py` | Schema-validated, atomic mutator for `placement_rules.json` (`show` / `add` / `update` / `remove`). |

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

## Standalone background removal

```bash
python3 scripts/remove_background.py --input /tmp/logo.jpg --output /tmp/logo.png
```

If the input already has meaningful transparency it is copied through unchanged
(`{"skipped": true}`); pass `--force` to re-run rembg anyway.

## Rules to follow

- **No model-generated pixels in the compositing pipeline** unless the user
  explicitly asks — and say so first. (Reviewing your own output is fine and
  required — that's judgment, not generation.)
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
- The user wants vector/print-ready separations, DST/embroidery files, or
  color-by-color seps → out of scope.
- The user wants a photoreal render with lighting/wrinkle warping → this skill
  does flat ratio-based compositing, not 3D/displacement warping.
