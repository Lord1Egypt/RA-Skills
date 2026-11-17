# Editing workflow for Darktable advice

## Contents

- Diagnose before prescribing
- Build a non-destructive plan
- Choose one tone mapper
- Suggested editing sequence
- Judge at the right scale
- Response format

## Diagnose before prescribing

Describe only what the supplied rendering supports:

- composition and subject hierarchy;
- global brightness and contrast;
- apparent color cast and color relationships;
- highlight/shadow appearance;
- local distractions;
- apparent noise, softness, halos, or chromatic fringes;
- output-specific risks such as clipped saturated colors.

Mark recoverability, sensor clipping, focus failure, and color-channel clipping as uncertain until RAW data, scopes, or a Darktable screenshot supports them.

State the intended image direction in concrete terms: e.g. reduce sky prominence, separate subject from background, keep skin neutral, preserve dusk color, or match a series. Avoid style labels that do not specify a visible change.

## Build a non-destructive plan

Preserve the current edit by recommending one of these before a divergent treatment:

- create a duplicate in lighttable;
- take a darkroom snapshot for comparison;
- create a named history point or style when reuse is intended.

Do not recommend discarding history merely because the manual's beginner tutorial starts from defaults. Existing history may contain deliberate work.

Write the plan in the order the user should evaluate changes. This order is not a command to reorder the pixelpipe.

## Choose one tone mapper

First inspect the active history or Preferences > processing > auto-apply pixel workflow defaults.

### `sigmoid`

Use when the current edit already uses it, when a compact and predictable tone mapping is suitable, or when the user is on the current default scene-referred workflow. It is the default identified by the current processing-preferences page. Adjust contrast and skew before reaching for additional tone curves. Use its primaries controls only when color behavior in highlights needs intervention.

### `AgX`

Use when the current edit uses AgX or the user wants more explicit control over highlight color handling, the tone curve, and before/after-tone-mapping primaries. AgX maps the scene-referred range to the display while managing color through configurable primaries. Start from a suitable preset, set input exposure range, then tune curve/contrast and only then primaries. Avoid aggressive primaries changes without a color-specific reason.

### `filmic rgb`

Use when continuing an existing filmic edit, reproducing the filmic tutorial, or when its scene/look/reconstruct controls are specifically needed. Set exposure/mid-gray first, then black and white relative exposure, then contrast and shoulder/toe balance. Do not add filmic merely because the introductory manual teaches it.

### Guardrail

Keep one principal display transform active. Multiple active tone mappers can be intentional but make attribution difficult and often compress contrast twice. Explain the reason before recommending such a stack.

## Suggested editing sequence

Adapt or omit steps based on the diagnosis.

### 1. Establish technical integrity

- Confirm orientation and crop intent.
- Enable `lens correction` early if needed; vignetting correction can change overall brightness.
- Check `raw chromatic aberrations` and `chromatic aberrations` for color fringes.
- Check `hot pixels` for long exposures.
- Inspect raw clipping with the raw-overexposure warning before claiming highlight recovery.

### 2. Control noise before amplifying detail

- Start with `denoise (profiled)` for ordinary sensor noise when a camera profile is available.
- Use classical `raw denoise` only when its raw-stage behavior is useful.
- Consider the `neural restore` utility's raw-denoise task before darkroom editing for difficult captures; it creates a new DNG and does not modify the source.
- Judge noise at 100%, then zoom out. Do not erase useful texture to make a 100% crop perfectly smooth.

### 3. Set global brightness and adaptation

- Use `exposure` for overall scene brightness/mid-gray.
- In a scene-referred workflow, leave `white balance` active in Camera Reference mode and perform illuminant correction in the CAT tab of `color calibration`.
- Revisit exposure after lens correction and white balance because both can change perceived brightness.

### 4. Map scene range to display

- Adjust the already-active `sigmoid`, `AgX`, or `filmic rgb`.
- Use `tone equalizer` for broad luminance zones when the sky, subject, or shadows need independent tonal adjustment without changing module order.
- Check clipping and the scope; do not equate a bright display value with unrecoverable raw clipping.

### 5. Establish color relationships

- Use `color calibration` for illuminant and primary color correction.
- Use `color balance rgb` for global colorfulness/vibrance and shadow–midtone–highlight grading.
- Use `color equalizer` for hue-dependent hue, saturation, or brightness; watch for transitions and chroma noise.
- Use `color harmonizer` only when a palette-level shift serves the visual intent. Protect neutrals and keep pull strength/width conservative.
- Use `rgb primaries` for deliberate gamut/primary adjustments, not as a generic saturation slider.

### 6. Make local corrections

- Create a new instance of `exposure` with a mask for object-specific dodge/burn.
- Use `tone equalizer` for broad brightness-class adjustments.
- Use drawn masks for geometry, parametric masks for pixel properties, and combine them when both location and tone/color must be constrained.
- Inspect the mask overlay, edge feathering, blur radius, mask contrast, and opacity at normal view and 100%.

### 7. Shape detail and atmosphere

- Use `diffuse or sharpen` presets for lens deblur, capture sharpening, local contrast, or dehaze, then tune carefully.
- Use `contrast equalizer` when control by feature size is needed.
- Use `local contrast` for a simpler global effect.
- Avoid stacking several local-contrast tools until halos and noise amplification have been checked.
- Use `haze removal` for a simpler dehaze operation; compare with a diffuse-or-sharpen dehaze preset.

### 8. Retouch and finish

- Use `retouch` for dust, blemishes, and unwanted objects; inspect repeated texture and source/target transitions.
- Use `crop`, `rotate and perspective`, and `framing` according to delivery constraints.
- Add `grain`, `vignetting`, or other effects only when they support the image; keep them separable from corrective edits.

### 9. Verify output

- Fit view: composition, overall hierarchy, color balance, and contrast.
- 100%: focus, noise, halos, demosaic artifacts, retouch joins, and mask edges.
- Color assessment: tonal/color judgment against controlled surrounds.
- Clipping warning and scopes: output clipping and channel behavior.
- Soft proof and gamut check: print or constrained output gamut.
- Export: dimensions, format, bit depth, output profile, rendering intent, and metadata.

## Response format

Use the Round 00/01/02 loop in `collaboration-workflow.md`. Within a confirmed Round 02 plan, use this compact structure:

1. **Main diagnosis** — two to four concrete observations and the main risk.
2. **Editing direction** — the intended visible change.
3. **Steps** — ordered module instructions with control, direction, stopping criterion, and side effect.
4. **Checks** — what to inspect at fit view, 100%, and in scopes/soft proof.
5. **Uncertainty** — what requires the RAW, history stack, or screenshot to verify.

Give the complete restrained plan in one response. After the user reports a result or supplies a screenshot, revise only the steps affected by that evidence.
