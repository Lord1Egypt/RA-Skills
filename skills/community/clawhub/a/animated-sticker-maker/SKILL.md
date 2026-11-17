---
name: animated-sticker-maker
description: Make one transparent animated sticker package from one static reference image and one natural-language motion prompt. Use only when the user explicitly names or invokes animated-sticker-maker (for example, $animated-sticker-maker on hosts with dollar-sign invocation); do not trigger for ordinary image, GIF, animation, or multi-sticker pack requests.
license: Apache-2.0
---

# Animated Sticker Maker

Turn one reference image and one motion prompt into a short, transparent animated sticker. Derive the identity lock, motion plan, working background, frame timing, validation plan, and export settings internally; do not require the user to supply them.

Resolve every script and reference path against the directory containing this `SKILL.md`.

## Inputs and boundaries

Require only:

1. `reference_image`: one static image containing a clear primary subject.
2. `prompt`: natural language describing the intended expression, action, text, loop, or target platform.

Support people, pets, mascots, illustrations, objects, and logos. If the image has multiple plausible subjects and the prompt does not identify one, ask once before generating. Do not promise stable multi-subject acting, scene animation, or camera motion in v1.

Produce one sticker per invocation. For a multi-sticker series, keep the shared identity specification, pack ordering, naming, and release-level brand assets in the owning project, then invoke this Skill separately for each sticker that needs its workflow. Do not turn project-specific pack orchestration into a generic Skill feature.

This is one [Agent Skills](https://agentskills.io/specification) package for hosts that support the standard; do not maintain a second host-specific instruction format. The host must provide a reference-conditioned raster generation or editing capability that can preserve the subject's identity. Use the host-native capability and fail before generation with a clear capability message when none is available. `agents/openai.yaml` is optional OpenAI UI and invocation metadata, not part of the workflow contract.

Use Python 3.10 or newer plus the packages in `requirements.txt` for deterministic processing. Do not make OpenCV a required dependency.

## Default package

Create this structure unless the prompt explicitly overrides it:

```text
output/<name>/
├── sticker.webp
├── source/
│   ├── frames/
│   │   ├── 000.png
│   │   └── ...
│   ├── rendered-frames/      # optional validated high-frame track
│   ├── reference.json        # basename, hash, and image metadata
│   └── motion.json
├── validation/
│   ├── contact-sheet.png
│   └── report.json
└── exports/                  # only when a platform or extra format is requested
    └── <platform>/
```

Use `1024×1024` RGBA for continuous-tone, illustrated, or generated raster sources. For native pixel art or another strict low-resolution grid, preserve the logical source canvas and set `motion.resampling` to `nearest`; do not force it through a non-integer `1024×1024` redraw. Use 4–8 unique frames, per-frame durations, a total duration of about 1.2–2.0 seconds, and a 400–700 ms hold on the clearest semantic frame. Loop by default. Do not create `preview.gif` unless requested or required by the target platform.

## Steps

### 1. Derive the identity lock

Inspect the reference at full size and small-icon size. Record the subject, signature silhouette, palette, material, facial or functional anchors, fixed marks, and forbidden drift. Separate identity features from incidental background details.

Complete this step only when every visible feature that makes the subject recognizable is classified as fixed, flexible, or removable.

### 2. Write the motion plan

Read [references/motion-plan.md](references/motion-plan.md). Convert the prompt into one primary semantic beat, a small set of anchor poses, deterministic transitions, exact text layers, frame durations, and loop behavior. Write the plan before producing final frames.

Use generation only for genuinely new poses, occlusion, or organic deformation. Use deterministic transforms for translation, scale, opacity, brightness, exact text, simple effects, timing, and packaging.

Complete this step only when each frame has one purpose and every requested semantic element appears in the plan.

Choose `motion.resampling` deliberately: `lanczos` for continuous-tone or illustrated raster work, and `nearest` for native pixel art and other hard grid-bound artwork.

### 3. Produce and validate anchors

Read the host's raster generation or editing instructions before generating. Always include the original reference when asking for a new anchor. Ask for a front-facing, isolated subject on either transparency or a flat high-distance work color. Generate the fewest anchors needed.

Inspect every anchor immediately against the identity lock. Reject identity drift before building temporal frames; do not hope that animation will hide it. Pause for user confirmation only when a choice changes the subject's identity or the requested meaning, not for routine numeric tuning.

If a generated anchor preserves one clean local expression or prop but drifts as a whole, reject it as a full anchor. You may salvage only that isolated component onto an approved identity-stable anchor when its boundary can be extracted without seams or duplicate features. Record the rejected source as a component source, the extraction rule, and the approved base anchor in the motion plan; never relabel the rejected full image as approved.

Complete this step only when all full-frame anchors are individually usable and every salvaged component has an approved base, a bounded role, and a deterministic extraction method.

### 4. Build clean RGBA assets

If an anchor already has correct alpha, preserve it. Otherwise read [references/transparency.md](references/transparency.md), choose a work color far from the subject palette, and run `scripts/chroma_key.py`. Keep shadows separate when the prompt or platform needs independent shadow control.

Complete this step only when the subject has no opaque background, color spill, bright fringe, clipped protrusion, or canvas-edge contact.

### 5. Compose the animation

Create one RGBA PNG per unique frame. Preserve the subject's aspect ratio unless the motion explicitly calls for deformation. Keep exact text in deterministic layers so spelling, placement, and timing remain controlled. Favor anticipation, one clear semantic hold, and a short recovery over evenly timed motion.

When a companion object presses, sits on, or touches the subject, align it against the local silhouette beneath its footprint. Do not infer contact from the subject's global bounding-box edge when the surface is curved, notched, or deformed.

Complete this step only when the sequence reads correctly without filenames or explanation and the loop has no unintended jump.

### 6. Package and run technical validation

Run:

```bash
python <skill-dir>/scripts/package_sticker.py \
  --frames-dir <working-frames> \
  --motion <motion.json> \
  --reference-image <reference-image> \
  --output <output/name>
```

Pass `--expected-size <WIDTHxHEIGHT>` when the internally derived source canvas differs from `1024x1024`. Use `--include-reference` only when the user wants the original image embedded; the default package records its basename, hash, dimensions, mode, format, and byte size without copying it. Use the nonstandard timing or frame-count flags only when the user's prompt explicitly overrides the defaults. Do not continue to platform export when technical validation fails.

Complete this step only when `sticker.webp`, copied source frames, `motion.json`, `reference.json`, the contact sheet, and the technical report all exist and technical validation passes.

Packaging validates the core motion schema, rewrites copied keyframes as real PNG files at canonical `frames/000.png`, `frames/001.png`, and so on, and rewrites matching semantic-hold references with them. Treat the packaged `source/motion.json` as the self-contained source of truth; do not retain paths that only resolve in the working directory.

The packager re-opens `sticker.webp` to verify its format, canvas, frame count, loop setting, and transparency. Native pixel-art packages use lossless WebP encoding. The generated report binds the normalized motion, reference metadata, source frames, and encoded WebP with an artifact fingerprint; any later change invalidates the recorded visual validation.

Packaging is transactional. It builds and validates a candidate in a sibling staging directory, replaces the existing usable package only after technical validation succeeds, and writes the latest technically failed candidate to `<output>.failed/`. A successful replacement removes that failed candidate. A declared `semantic_hold_frame` must name exactly one authored keyframe.

When `motion.render` is present, the packager reads its relative working `frame_dir`, validates its numeric `target_fps`, frame count, durations, canvas, Alpha, and visibility, then normalizes the track into `source/rendered-frames/` with its own `validation/render-report.json`. `rendered-frames/` is an internal artifact directory, not a public CLI parameter.

Every successful repack creates new validation reports with visual validation pending. Re-run visual validation after every repack; never preserve a prior pass across changed artifacts.

### 7. Perform visual validation and deliver

Read [references/validation.md](references/validation.md). Inspect the animation, contact sheet, semantic hold, Alpha edges on light and dark backgrounds, and the subject at small-icon size. This is maker-side validation, not an approval workflow or separate reviewer role. Record the result in `validation/report.json`; scripted checks do not replace visual inspection.

Record the decision with:

```bash
python <skill-dir>/scripts/record_visual_validation.py <output/name/validation/report.json> \
  --status pass \
  --identity "..." --meaning "..." --loop "..." --alpha "..." --small-size "..."
```

If a platform is requested, read [references/platform-exports.md](references/platform-exports.md), verify current official constraints, and write only derived files beneath `exports/<platform>/`. Do not resize or recompress the platform-neutral sources.

For a platform that accepts animated GIF, export from the validated package instead of the WebP:

```bash
python <skill-dir>/scripts/export_platform_gif.py \
  --package <output/name> \
  --platform <platform> \
  --size <WIDTHxHEIGHT> \
  --max-bytes <limit> \
  --preview-output <derived-preview.png> \
  --preview-max-bytes <preview-limit> \
  --spec-url <official-url> \
  --verified-on <YYYY-MM-DD>
```

The exporter requires `technical_validation`, `visual_validation`, and `deliverable_ready` to pass. A top-level `status: pass` alone is insufficient. It preserves source timing, applies the resampling policy recorded in `motion.json`, uses one shared GIF palette to reduce frame-to-frame color shimmer, chooses the highest tested color count that meets the byte limit, and records source validation, export parameters, and hashes. Omit preview arguments when the platform does not require one. `--spec-url` and `--verified-on` are mandatory provenance. Use `--allow-unvalidated` only for explicit diagnostics; its report is marked `diagnostic_unvalidated` and cannot become deliverable. If no palette candidate fits, change size, timing, or frame count only through an explicit validated decision; do not silently degrade the semantic hold.

Every normal export starts at `pending_visual_validation`, even when its source package and technical constraints pass. Inspect the actual GIF and preview, then record visual validation against the generated report with the same `record_visual_validation.py` command. The report sets `deliverable_ready: true` only while its fingerprint still matches those export files.

Keep authored keyframes as the default export track. When a platform benefits materially from smoother motion and the package contains a deterministic high-frame track declared by `motion.render`, export that track explicitly:

```bash
python <skill-dir>/scripts/export_platform_gif.py \
  --package <output/name> \
  --platform <platform> \
  --size <WIDTHxHEIGHT> \
  --max-bytes <limit> \
  --frame-track render \
  --track-report <output/name/validation/render-report.json> \
  --fps-candidates 30,24,20,15 \
  --min-colors 64
```

The render track needs its own passed technical and visual validation because it is a separate temporal artifact. `motion.render.target_fps` is the user-facing numeric generation target. `--fps-candidates` is an export fallback policy: the exporter searches palette sizes down to `--min-colors` at the preferred frame rate, then tries the next candidate. Do not create or select this track silently, and do not put subject-specific frame rates, palette floors, or platform limits into the generic Skill.

Complete the task only when the package and every requested export have passed both validation types and report `deliverable_ready: true`.

## Escalation rule

Ask the user only when a missing choice changes the intended subject, meaning, or irreversible public output. Make safe project-level adjustments to timing, position, scale, color-key thresholds, and compression without interrupting the run.
