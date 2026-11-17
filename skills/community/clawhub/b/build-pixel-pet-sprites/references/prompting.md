# Pixel-pet prompt patterns

## Character master

Use the reference image as a strict identity and costume reference. Request a full-body
chibi pixel-art character before requesting animation frames.

```text
Use case: stylized-concept
Asset type: pixel-pet character master
Primary request: Convert the referenced character into a complete full-body chibi
pixel-art pet while preserving its recognizable identity, colors, costume, silhouette,
and signature details.
Input images: Image 1 is the strict identity/costume reference.
Style/medium: handcrafted pixel art, crisp square pixels, limited palette, hard edges,
consistent pixel density, no antialiasing.
Composition: one large front view plus only the views/details needed to lock the model.
Constraints: full body visible; readable at sprite size; no text; no watermark.
Avoid: cropped limbs, costume drift, smooth vector rendering, painterly blur, 3D.
```

## Animation atlas

Generate one action per row and one chronological frame per column. Use the largest
requested frame count as the column count; require unused cells to remain empty.

```text
Use case: stylized-concept
Asset type: production pixel-art animation atlas
Primary request: Use the approved character master as a strict model reference. Create
an exact <columns>-column x <rows>-row sprite grid. Rows follow the supplied action
order; frames progress left to right.
Layout: equal cells, identical character scale, stable bottom-center anchor, complete
sprite/effects inside every cell, no labels or grid lines.
Background: perfectly flat solid #FF00FF chroma key with no shadow, gradient, texture,
floor, or lighting variation. Never use #FF00FF in the subject.
Style: crisp handcrafted pixel art; no antialiasing, blur, vector smoothness, or 3D.
Constraints: exact frame counts and row order; adjacent frames must show incremental
motion; unused cells fully #FF00FF; no text, logo, or watermark.
```

For each action, specify frame-by-frame progression, whether it loops, and its intended
timing. Use anticipation, action, follow-through, and settle poses for one-shot actions.
Keep detached effects inside the cell but do not rely on them for character alignment.

## Visual QA

Check identity, costume, silhouette, frame progression, duplicate/missing frames,
effect containment, and model drift in the generating agent's own context. Do not reopen
the same `image_gen` result with `view_image`. Use scripts for size, alpha, edge,
frame-count, anchor, and jitter validation.
