---
name: controlled-generation
description: >
  Lock the composition of a generated image to a structural guide while you change everything
  else. Use when the user says "same pose, new character", "keep this layout, restyle it", "match
  this sketch", "turn my floor plan into a render", "same product silhouette, different finish",
  or wants interior redesign, sketch-to-render, or controlled asset variations. A control map
  (pose, edges, depth, segmentation) holds the structure, the prompt brings the new look. To keep
  a character's identity consistent rather than just its structure, use character-consistency.
---

# Controlled generation (ControlNet)

Generate a new image whose composition matches a source image while its style, subject, or finish changes freely. You extract a structural map (pose, Canny edges, depth, or segmentation) from the source, then condition generation on that map. This is the "same composition, new look" lever: interior redesign, sketch-to-render, and repeatable product or game-asset variations.

## Inputs to collect

- **The source image** to take structure from (a photo, sketch, render, or existing asset). Required.
- **Which structure to preserve:** silhouette/outlines (Canny), human pose (pose), 3D layout/perspective (depth), or scene regions (segmentation). If unstated, infer from the goal: outlines for objects/assets, pose for people, depth for rooms/scenes.
- **What changes:** the new style, subject, material, or palette described as a prompt.
- **How tightly** to hold the structure (loose restyle vs strict trace) and how many outputs.

## Models

Two pieces, both confirmed live via `runware-models` before calling, never hardcoded:

1. **A ControlNet preprocessor** (`form:controlnet` consumers depend on it) to build the control map:
   - Canny / edges: `runware:controlnet-preprocess@canny` (`op:edge-detection`)
   - Depth: `runware:controlnet-preprocess@depth` (`op:depth-estimation`)
   - Pose: `runware:controlnet-preprocess@openpose` (`op:pose-estimation`)
   - Segmentation: `runware:controlnet-preprocess@seg` (`op:segmentation`)
   - Soft edges: `runware:controlnet-preprocess@softedge` (`op:edge-detection`)
2. **A base model + a matching ControlNet** (`form:controlnet`) for inference. The ControlNet must match both the base family and the map type:
   - FLUX.1 [dev] base `runware:101@1` with FLUX Union Pro ControlNets: Canny `runware:25@1`, Depth `runware:27@1`, Pose `runware:29@1`.
   - SDXL alternatives: Canny `runware:20@1`, Depth `runware:3@1`.

Confirm each AIR is `live` and the ControlNet is built for the base you chose. A LoRA can ride alongside to lock a style (see the game-assets-canny guide). Offer SDXL as the faster/cheaper tier and FLUX dev as the quality tier.

## Workflow

Specializes the `runware-run` contract for a two-call control pipeline.

1. **Resolve schemas.** Inspect the preprocessor and the inference-model schemas via `runware-run`. Use only schema-valid fields.
2. **Extract the control map.** Run `taskType: "controlNetPreprocess"` with `inputImage` (URL or base64) and `preProcessorType` set to the map you want (`canny`, `depth`, `openpose`, `seg`). Keep the returned guide image.
3. **Generate conditioned on the map.** Run `taskType: "imageInference"` synchronously with your `model` (base), the prompt, and a `controlNet` array whose entry carries the matching ControlNet `model`, the `guideImage` from step 2, and `weight` / `startStep` / `endStep`.
4. **Read the result.** Images return synchronously as image URLs. Inspect for structure adherence vs creative freedom and adjust.
5. **For a set,** reuse the same guide image across calls and vary only the prompt so every output shares one composition.

Load `references/examples.md` for three worked, schema-verified recipes (Canny edge-locked restyle, OpenPose pose-driven generation, depth-guided interior restyle) with both calls and the result shape.

## Technique

Grounded in the FLUX dev game-assets-canny guide.

- **Extract, then condition.** The map carries the structure so the prompt no longer has to. Describe the new look in the prompt, not the geometry the guide already encodes.
- **Tune Canny thresholds to set how much structure survives.** `lowThresholdCanny` catches subtle edges (more detail, more constraint), `highThresholdCanny` keeps only strong edges (cleaner, looser). Defaults work for most inputs. Push low for soft-transition art, push high to drop noise.
- **Control the structure-vs-creativity balance with steps.** `startStep: 1, endStep: 10` (on a ~30-step run) is the balanced default: guidance shapes the early layout, then the model is free to invent detail. A higher `startStep` lets guidance kick in too late and structure adherence weakens. A higher `endStep` clamps the model to the source so hard that the new subject can barely emerge (good for pure restyle, bad for transformation).
- **Control mode trades guide against prompt.** Use `balanced` for a mix, `controlnet` to prioritize structure over the prompt, `prompt` to let text lead with the guide as a loose reference.
- **Match map to intent.** Canny for silhouettes and assets, pose for redirecting people, depth for rooms and perspective (interior redesign, sketch-to-render), segmentation to keep scene regions while restyling each.

  Pick the pipeline by filling this routing template, then send the two calls:

  ```
  control type: <canny | openpose | depth | seg>
  source image: <the URL or base64 to take structure from>
  preprocessor:  <runware:controlnet-preprocess@<type>>
  base + controlnet: <runware:101@1 + runware:25@1 (canny) | 29@1 (pose) | 27@1 (depth)>  (FLUX dev)
  steps / endStep: <~30 steps, endStep 10 for transform, 15+ for restyle>
  ```

  The control type drives every other line: it picks the preprocessor and the matching ControlNet, and how hard you hold structure (`endStep`) follows the intent (transform vs restyle).
- **Prep the source for clean edges** when using Canny: clear outlines, distinct features, decent contrast, minimal noise. Simplify a busy source before extracting.

## Parameters that matter

- `preProcessorType`: `canny`, `depth`, `openpose`, `seg`, `softedge`. Must match the ControlNet you pair it with.
- `lowThresholdCanny` / `highThresholdCanny`: Canny sensitivity. Lower low = more edges, higher high = fewer edges.
- `controlNet[].guideImage`: the preprocessor output, not the raw source.
- `controlNet[].weight`: how strongly the map steers generation. 1.0 is a balanced start.
- `controlNet[].startStep` / `endStep`: the window the guide is active. `1`/`10` on ~30 steps is balanced. Raise `endStep` to hold structure harder, raise `startStep` to weaken it.
- Control mode: `balanced` / `controlnet` / `prompt`.
- Confirm every field name and range against the live schema (`runware-run`). Never guess.

## Quality bar

- The output's composition (pose / outline / layout) matches the source while the intended look changed.
- Structure is held to the right degree: recognizable, not a rigid trace that blocks the new subject (raise `endStep` if too loose, lower it if too rigid).
- The map type fits the goal (Canny silhouette vs depth layout vs pose).
- For a set, every image reads as the same composition. Retry outliers by adjusting thresholds, weight, or the step window, not by re-rolling blindly.

## Related skills

`runware-run` (call the two-step pipeline), `runware-models` (confirm the preprocessor + ControlNet are live), `runware-prompting` (write the new-look prompt). Sibling outcomes: `character-consistency` (hold a subject instead of a composition), `product-photography` (controlled product variations).
