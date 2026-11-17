---
name: game-assets-2d
description: >
  Generate 2D game art that stays visually consistent across a whole set:
  sprites, die-cut stickers, item icons, parallax pieces, and asset sheets. Use
  when the user says "a set of game items in one style", "make me sprite icons",
  "die-cut stickers with a clean cutout", "variations of this asset that keep the
  same shape", "a pack of potions/chests/weapons", or wants transparent PNGs
  ready to drop into a game.
---

# 2D game assets

Produce cohesive 2D game art (sprites, stickers, item icons, parallax layers, full asset sheets) where every piece reads as part of one set. The levers are a style LoRA to lock the look across the set, ControlNet Canny to lock silhouette and structure while the look varies, and background removal to ship clean transparent cutouts.

## Inputs to collect

- **What asset(s)** and the set: a single sprite, a themed pack (potions, chests, weapons), an icon set, or parallax pieces. (Ask only if unclear.)
- **The target style** (pixel art, chibi sticker, hand-painted, neon) and whether a specific LoRA or trigger word should drive it.
- **A structure reference** when variations must keep the same shape (an existing asset to preserve via Canny). Optional for from-scratch sets.
- **Transparency**: whether outputs need transparent backgrounds (almost always yes for in-game use).
- **How many** outputs and the canvas size.

## Models

- **Base + style LoRA (default for a consistent look):** an SDXL-family base (e.g. `civitai:101055@128078`) plus a specialized style LoRA. The LoRA holds one aesthetic across the whole set. SDXL is the practical pick here because it supports CLIP Skip and has the deepest catalog of style LoRAs.
- **ControlNet Canny (preserve structure across variations):** SDXL Canny `runware:20@1`, or FLUX Canny `runware:25@1` on a FLUX base. Pair with the Canny preprocessor `runware:controlnet-preprocess@canny`.
- **Background removal (clean cutouts):** BiRefNet `runware:112@*` (General `runware:112@5` is a solid default, Matting `runware:112@9` for soft edges, Portrait `runware:112@10` for characters).
- Confirm each is live and inspect its schema via `runware-models` + `runware-run` before calling. Never hardcode a LoRA AIR from memory. Browse the catalog for the style you want.

## Workflow

1. Resolve the base model + LoRA schema (`runware-run`) and confirm the `lora` array shape and the LoRA's trigger word.
2. **(Structure path only)** Preprocess the reference asset with `controlNetPreprocess`, `preProcessorType: "canny"`, to get a guide image.
3. Run `imageInference` synchronously: base model + the style LoRA, plus the `controlNet` block with the Canny guide image when preserving structure. Use `numberResults` to batch the set in one call.
4. For each new asset in the set, keep the base + LoRA constant and vary only the subject clause in the prompt. Reuse the same Canny guide when shape must stay fixed.
5. Remove backgrounds with `removeBackground` (BiRefNet) to produce transparent PNGs.
6. Review the set for style and silhouette consistency, then retry any outliers.

## Technique

- **LoRA locks the style, the prompt names the asset.** Pick one specialized LoRA and reuse it across every call so the whole pack shares an aesthetic. Keep LoRA `weight` around `0.8` to `1.0`. Below `0.5` the style barely shows. Above `1.3` it dominates and adds artifacts. Include the LoRA's trigger word in the prompt.
- **Canny locks structure while the look varies.** To make variations of one asset (a chest in ten biomes, a sword reskinned), preprocess the original to a Canny edge map and feed it as the `controlNet` guide. The edges fix shape and proportions while the prompt and LoRA change the finish.
- **Tune the Canny step window.** `startStep: 1, endStep: 10` is the balanced default: edge guidance shapes the early structural steps, then the model gets creative freedom. Lowering `endStep` (e.g. 5) loosens structure and lets the subject change more. Raising it (e.g. 20) clamps so hard the subject can barely change, good only for restyles. A late `startStep` weakens adherence.
- **Prompt structure for assets:** describe the asset type and the style together. A reliable shape is `[style] game asset, [asset type], [specific details], clean lines, game-ready, [style] style, black background`. Generating on a flat black (or single-color) background makes the later cutout clean.
- **CLIP Skip refines sticker/sprite style.** On SDXL, `clipSkip: 2` skips the last two text-encoder layers and tends to produce the simpler, bolder look stickers and sprites want. SDXL already skips one layer by default, so this is two on top.
- **For a whole sheet,** hold base + LoRA (and the Canny guide, if used) constant and change only one variable per image. That single-variable discipline is what makes the set read as one coherent pack rather than loosely related pieces.
- **Then cut out.** Run background removal last to isolate each asset on transparency, ready to composite into different environments.

## Parameters that matter

- `lora[].weight`: `0.8` to `1.0` is the sweet spot, the single biggest driver of style consistency across the set.
- `controlNet[].guideImage`: the Canny edge map from the preprocess step. This is what holds silhouette and proportions.
- `controlNet[].startStep` / `endStep`: the structure-vs-creativity window. `1`/`10` is balanced, a lower `endStep` frees the subject, a higher one clamps it.
- `controlNet[].weight`: `1.0` is a balanced starting point for edge influence.
- `controlNet[].controlMode`: `balanced`, or `controlnet` to prioritize structure, or `prompt` to lead with the text and treat edges as a loose guide.
- `clipSkip`: `2` on SDXL for a cleaner sticker/sprite style.
- `lowThresholdCanny` / `highThresholdCanny`: on the preprocess step, lower thresholds catch more subtle edges, higher ones keep only prominent contours.
- `numberResults`: batch a set in one call.
- Confirm exact field names against the live schema (`runware-run`). Never guess.

## Quality bar

- Every asset in the set reads as one style (the LoRA held, so no piece looks like it came from a different pack).
- Where structure was meant to be preserved, the silhouette and proportions match the reference (Canny held). Where variation was wanted, only the intended details changed.
- Backgrounds are cleanly removed with no halo or leftover fringe, and the transparent PNG is genuinely transparent at the edges.
- Assets stay legible at small in-game sizes (simple composition, clean outlines). Retry any piece that drifts in style, breaks silhouette, or cuts out poorly.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `controlled-generation` (the ControlNet mechanics in depth), `character-consistency` (same subject across scenes), `train-style-model` (train your own reusable style LoRA for the set).
