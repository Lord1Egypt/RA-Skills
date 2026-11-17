---
name: edit-image
description: >
  Modify an image the user already has, by instruction or by mask. Use when the user says "remove
  the person/wires/watermark", "add a hat", "replace the sofa", "change the wall to blue", "make
  it sunset", "inpaint this region", "extend the background", "make it wider", or "outpaint /
  expand the canvas". This is changing the content of one existing image, not generating from
  scratch. For quality and resolution only (upscale, denoise, deblur, restore an old photo), use
  restore-and-upscale. To fuse several separate images into one, use composite-scene.
---

# Edit image

Take an image the user already has and change it: add, remove, or replace objects, recolor or relight, blend elements, restore, inpaint a masked region, or outpaint to extend the canvas. The work starts from their pixels and keeps everything they did not ask to change. To make a fresh image from a prompt instead, that is a generation task, not this one.

## Inputs to collect

- **The source image.** Required. URL, base64, data URI, or a UUID from a previous generation or the Image Upload API. (Ask only if none provided.)
- **The instruction:** what to add, remove, replace, recolor, relight, blend, or extend. One plain sentence is enough.
- **A region**, if the edit is local. For removal or inpaint, a binary mask (white = the area to act on, black = keep). For outpaint, the per-side pixel extension.
- **What must stay untouched** (the subject, the framing, the palette), so the edit stays surgical.

## Models

Route by the kind of edit. Confirm the live model and inspect its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale choice.

- **Instruction edit (general): Qwen-Image-Edit-2511** (`alibaba:qwen-image-edit@2511`). Applies a text instruction to add, remove, replace, recolor, or restyle while holding visual consistency. Strong default when the ask is phrased as a sentence and no mask is needed.
- **Unified recolor / relight / restore / blend: Bria FIBO Edit** (`bria:21@1`). Instruction-driven with optional mask support, tuned to preserve original lighting and structure. Reach for it on tone, light, and compositional edits.
- **Inpaint or outpaint a masked region: FLUX.1 Fill [pro]** (`bfl:1@2`). Prompt-guided fill inside a mask. Use when you want to describe what should appear in the region.
- **Extend the canvas (prompt-guided): FLUX Expand** (`bfl:1@3`, FLUX.1 Expand [pro]). Outpaint with a prompt steering the new regions.
- **Remove an object cleanly: FLUX Erase** (`bfl:flux@erase`). Mask-driven and prompt-less. You paint what disappears, the model reconstructs what was behind it. The only knob is `settings.dilatePixels`.
- **Extend the canvas (prompt-less): FLUX Outpainting** (`bfl:flux@outpainting`). No prompt, no mask, per-side pixel extension that continues whatever is already at the edge.

The key splits to remember: object removal is mask-driven and prompt-less (FLUX Erase). Outpainting is a per-side pixel extension, not a width/height. "Replace with something specific" is inpaint (prompt-guided), "make it gone" is erase.

Load `references/examples.md` for a worked, schema-verified recipe per edit mode (instruction edit, mask-driven removal, outpaint).

## Workflow

1. Resolve the chosen model's schema with `runware-run` and confirm the exact field names (`inputs.image`, `inputs.mask`, `outpaint.*`, `settings.*`). Never guess them.
2. Upload or reference the source into `inputs.image`. For a local edit, prepare the mask (see Technique) into `inputs.mask` at the **same resolution** as the source.
3. Run `imageInference` synchronously. Stills return inline, no polling needed.
4. Check the result against the Quality bar. Retry with a tighter mask, a clearer instruction, or an adjusted `dilatePixels` if the edit bled or under-covered.

## Technique

**Pick the tool from the verb.** If you can say it in one sentence ("remove the person"), erase. If you must describe a replacement ("put a park bench there"), inpaint. If the goal is "more of the same canvas", outpaint prompt-less. If it is "add a new element off the edge", outpaint prompt-guided. If it is tone, light, or blend, FIBO Edit. Anything else phrased as an instruction, Qwen.

**Object removal (FLUX Erase) is mask-driven and prompt-less.** Pass the image and a binary mask, nothing else. White (255) marks what to remove, black (0) marks what to keep, at the exact source resolution. The model reconstructs the background and also catches shadows and reflections the mask did not fully cover. The single lever is `settings.dilatePixels`, which expands the mask outward before processing:

- Default `10` suits clean segmentation masks.
- Soft edges (hair, fur, smoke, translucent fabric): `15` to `20`.
- Objects with visible shadows or reflections: `12` to `18`.
- Tight removals next to content you keep: lower it, or set `0` with a precise hand mask, to avoid eroding the neighbor.

A FLUX Erase request is small. The masked area is what disappears:

```json
{
  "taskType": "imageInference",
  "model": "bfl:flux@erase",
  "inputs": { "image": "https://...", "mask": "https://..." },
  "settings": { "dilatePixels": 10 }
}
```

For people, auto-generate the mask with the Image Masking API (`runware:35@4` full-body, `runware:35@2` face) and pipe its `maskImageURL` straight into `inputs.mask`. Remove one coherent region per pass for complex scenes rather than scattered islands across the frame. Common removal patterns and their dilation:

- **People** in architecture or street shots: auto-mask, `dilatePixels` 15+ for loose clothing or hair.
- **Text, watermarks, signage**: tight mask, `dilatePixels` 5 to 8 since flat paint casts no real shadow.
- **Cables and wires** crossing the sky: thin strip masks, `dilatePixels` 15 to 20 so SAM-missed edges do not ghost.
- **Product clutter** in a flat-lay: mask only the stray items, keep `dilatePixels` moderate (8 to 12) so the hero's edge is not eroded.

**Outpainting is per-side pixel extension.** With FLUX Outpainting you do not pass `width`/`height`. You pass `outpaint.{top,right,bottom,left}` in pixels and the output is derived: `output_width = source_width + left + right`, same for height. Each side defaults to `0`.

```json
{
  "taskType": "imageInference",
  "model": "bfl:flux@outpainting",
  "inputs": { "image": "https://..." },
  "outpaint": { "top": 0, "right": 384, "bottom": 0, "left": 384 },
  "settings": { "autoCrop": true }
}
```

Plan the target canvas first, subtract the source dimensions, split the difference across the sides you want to grow. Extend the side with the most continuation cues (a horizon, a path, a wall), since asymmetric values are an explicit lever for that. For an aspect-ratio change, keep one axis fixed and grow only the other so the subject's framing is untouched. The three patterns that cover most work:

- **Widen a landscape**: grow `left` and `right` only, leave `top`/`bottom` at `0`. Natural scenes and textures continue cleanly.
- **Add breathing room around a subject**: symmetric extension on all four sides. The original pixels stay put, only the outer ring is new.
- **Reshape for a format**: asymmetric extension to hit a banner or hero ratio without re-framing the subject.

Prompt-less outpaint commits to continuing what is already at the edge. When the new region must introduce something new (a mountain range above a portrait) or redirect style (day to night), switch to FLUX Expand and steer it with a prompt.

**Watch the outpaint size ceiling.** Output is capped at 4 MP total with no side over 2048 px. A 1536 x 1024 source with 512 px on all four sides would compute to 2560 x 2048, which breaks the per-side limit and returns a 422 by default. Set `settings.autoCrop: true` and the model crops to fit instead of failing, so the effective extension on the overflowing axis shrinks but the request still succeeds. In automated pipelines prefer `autoCrop: true`, a smaller success beats a hard error. Extensions below roughly 64 px per side give little visible gain, so for micro-adjustments crop the source instead.

**Inpaint with FLUX.1 Fill** when you want to describe what fills the masked region. Same `inputs.image` plus `inputs.mask` shape as erase, with a `positivePrompt` describing the new content. The mask must match the source resolution exactly, and the prompt should describe only the region, not the whole image, so the fill blends rather than re-rendering the scene.

**Inpaint vs erase is replacement vs removal.** Both take an image and a mask. Inpaint (FLUX.1 Fill) needs a prompt and generates new content in the white region. Erase needs no prompt and restores what was behind. Use Fill to swap a sofa for a different sofa, use Erase to make the sofa gone. The practical test: if you can describe what you want in one sentence ("remove the person"), erase. If you need to describe what should replace it ("replace the person with a park bench"), inpaint. Erase also cleans the shadows and reflections a removed object leaves on surrounding surfaces, which inpainting, treating the mask boundary as absolute, does not.

**Instruction edits stay surgical.** With Qwen or FIBO Edit, name only what changes and, when it helps, name what must stay ("change the wall to navy, keep everything else"). Do not re-describe the whole scene, that invites drift in regions you did not want touched. FIBO Edit is the stronger pick when the edit is about tone, light, or blending two sources while preserving the original structure. Qwen is the stronger pick for add, remove, replace, and restyle phrased as a plain instruction. For either, a mask is optional and narrows the edit to a region when the model accepts one.

## Parameters that matter

- `inputs.image`: required source. URL, base64, data URI, or UUID.
- `inputs.mask`: binary PNG at the **exact** source resolution for masked edits. White = act, black = keep. Mismatched dimensions are a validation error.
- `settings.dilatePixels` (FLUX Erase): the only erase knob. Default `10`, range `0` to `25`. Raise for soft edges and shadows, lower near content you keep.
- `outpaint.{top,right,bottom,left}` (FLUX Outpainting / Expand): per-side extension in pixels, each defaulting to `0`. Asymmetric values are fine.
- `settings.autoCrop` (outpaint): when an extension would exceed the size ceiling, `true` crops the result so the request still succeeds instead of erroring. Use it in production pipelines.
- Outpaint sizing ceiling: output up to **4 MP** total, with neither side over **2048 px**. Quality is most consistent at or under 2 MP, upscale downstream if you need more.
- FLUX Erase trains near **1 MP**. Inputs close to that produce the best erasures, downscale a large source then upscale the result.
- Confirm every field against the live schema with `runware-run` before calling.

## Quality bar

- The edit did only what was asked. The subject, framing, and untouched regions are unchanged.
- Removals leave no ghost, halo, or stub. Shadows and reflections of the removed object are gone too. If a faint trace remains, raise `dilatePixels` and retry.
- Inpaint and instruction edits blend seamlessly into the surrounding pixels, no visible seam at the mask boundary.
- Outpaint continues lighting, texture, and depth without a seam at the join, and the output stays inside the 2048 / 4 MP limits.
- The mask matches the source resolution exactly. Any dimension mismatch is a hard failure, not a quality issue.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `product-photography` (clean and stage a product shot), `restore-and-upscale` (repair and enlarge), `controlled-generation` (structure-guided new images).
