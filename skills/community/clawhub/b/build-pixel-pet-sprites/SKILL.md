---
name: build-pixel-pet-sprites
description: Create a production-ready chibi pixel-art virtual desktop pet based on a character reference image, including character design sheets, multi-action animation sprite sheets, transparent RGBA frame assets, action strips, asset inventories, GIF previews, automatic character alignment using alpha edges and connected-component analysis, jitter measurement, asset validation, ZIP packaging, and web integration delivery. Use this for creating virtual desktop pets, pixel mascots, animated sprites, frame-by-frame animations, character animation alignment, or fixing position drift between animation frames.
---

# Build Pixel Pet Sprites

Create a reusable, aligned sprite package from a character reference or repair an
existing package whose subject drifts between frames.

## Route the task

- For a new character/reference, run the complete workflow.
- For new actions on an existing pet, reuse the approved character master and the same
  dedicated image-generation subagent.
- For an existing transparent package with visible drift, skip generation and start at
  alignment.
- For web integration only, use the aligned atlas and `sprite-manifest.json`; do not
  request new images.

## Complete workflow

### 1. Define the animation specification

Collect:

- reference image paths and their roles;
- character invariants that must never drift;
- ordered action names;
- exact frame count, duration, and loop behavior for each action;
- target frame dimensions and final output directory;
- transparent output, preview, and web-delivery requirements.

Choose one row per action and chronological frames from left to right. Prefer equal frame
counts when the consuming application benefits from a rectangular atlas.

### 2. Generate through the imagegen skill

Read and follow the installed `imagegen` skill. Use its dedicated-subagent workflow so
the main thread receives no image bytes or Base64.

Generate in this order:

1. a full-body character master that locks identity, costume, palette, proportions, and
   pixel density;
2. an animation atlas using the approved master as a strict reference.

Pass local references with `referenced_image_paths`. Keep later revisions with the same
generating subagent. Use the prompt patterns in [references/prompting.md](references/prompting.md).

For transparent assets, generate on uniform `#FF00FF`, then use the imagegen skill's
installed `remove_chroma_key.py` helper. Do not modify `scripts/image_gen.py`.

### 3. Build the deterministic package

Create a package configuration using
[references/package-config.md](references/package-config.md), then run:

```powershell
python scripts/build_sprite_package.py <transparent-atlas.png> <config.json> <output-dir> --character-master <master.png>
```

The script normalizes the atlas with nearest-neighbor sampling and produces the atlas,
action strips, individual frames, previews, manifest, and ZIP.

### 4. Align the subject before delivery

Always align generated animation frames, even when visual inspection looks acceptable:

```powershell
python scripts/align_sprite_frames.py <package-dir> <aligned-output-dir>
```

The aligner:

- thresholds the Alpha channel;
- applies morphological closing;
- selects a central, body-like connected component with lower-frame presence;
- excludes detached effects from anchor detection;
- derives a body/support anchor and a per-action median target;
- translates the complete RGBA frame with integer offsets only;
- records offsets and before/after jitter without scaling or blurring pixels.

If the complete content cannot move without clipping, regenerate or package with more
transparent padding. Do not silently crop the main subject.

### 5. Validate the aligned package

Run:

```powershell
python scripts/validate_sprite_package.py <aligned-output-dir>
```

Require all checks to pass:

- expected actions and exact frame counts;
- consistent RGBA dimensions;
- non-empty frames and correct strip/atlas sizes;
- transparent corners and zero outer-edge contamination;
- no clipped main subject;
- materially reduced within-action X/Y anchor jitter.

Inspect generated visual content only in the generating subagent. Use script reports for
dimensions, alpha, edges, anchors, and jitter.

### 6. Deliver

Return:

- aligned output directory and ZIP;
- aligned atlas and manifest;
- preview GIF path;
- final prompt set and generation mode for generated work;
- brief QA with frame totals, dimensions, issues, and before/after jitter.

Keep the unaligned source package. Never overwrite existing assets; create a versioned
sibling. Do not return Base64, discarded variants, or high-volume image tool output.

## Web handoff

Recommend loading one atlas plus `sprite-manifest.json` rather than requesting every
frame separately. Render the atlas with Canvas or CSS background positioning, disable
image smoothing, and use the manifest's duration, loop, row, dimensions, and anchor data.
