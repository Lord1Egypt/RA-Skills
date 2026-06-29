---
name: drivethru-graphic-artist
description: Generate product mockups by compositing a decoration (logo/graphic) onto a blank product photo (t-shirt, hoodie, hat, mug, ...). Deterministic image manipulation only — detects the garment bounding box, scales and positions the decoration via a ratio-based placement-rules catalog, and writes a PNG. No generative AI. Use whenever the user wants to see how a logo or design looks on a garment/product, place artwork on a blank, remove an image background, or iteratively tune a print's size/position/rotation.
version: 0.1.0
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
composite **mockup**. Everything is deterministic image manipulation: Pillow
for transform/compose, [rembg](https://github.com/danielgatis/rembg) (U²-Net
segmentation — *not* generative) for background removal and garment bbox
detection.

**No generative AI is ever used in this pipeline.** Only fall back to an
image/LLM model if the user *explicitly* asks (e.g. "generate a new logo"),
and say so before you do.

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
and `rotation_deg`. Look-up order: `(category, placement)` →
`(_defaults, placement)` → error.

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

- **No generative AI in the mockup pipeline** unless the user explicitly asks —
  and say so first.
- **Respect aspect ratio.** `compose_mockup.py` locks it automatically; never
  hand it raw pixel dimensions that would squash the decoration.
- **Don't assume a file exists.** Verify input paths before composing.
- **Save every mockup** so you can diff between iterations.
- **Lead with the result** (the PNG), then one line on what changed, then ask
  what to tune next.
- When ambiguous ("put it on the chest"), ask one clarifying question
  ("full front or left chest?") rather than guessing.

## When NOT to use

- The user wants a brand-new logo/design *created* from a prompt → that's
  generative image work, out of scope here.
- The user wants vector/print-ready separations, DST/embroidery files, or
  color-by-color seps → out of scope.
- The user wants a photoreal render with lighting/wrinkle warping → this skill
  does flat ratio-based compositing, not 3D/displacement warping.
