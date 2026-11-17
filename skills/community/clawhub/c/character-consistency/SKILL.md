---
name: character-consistency
description: >
  Keep the same character, person, or product looking identical across new scenes, poses, outfits,
  and styles. Use when the user says "the same character again", "keep her face consistent", "my
  mascot in a different scene", "same product, new background", or wants a reference, expression,
  or outfit sheet. The number-one thing people struggle with in image generation, so reach for it
  whenever identity must persist across images. To hold a composition or pose fixed rather than
  identity, use controlled-generation. To fuse separate photos into one scene, use
  composite-scene.
---

# Character consistency

Produce new images of an established subject (a character, a real person, a mascot, a product) that stay recognizably the *same* across scenes, angles, and styles. The lever is reference images plus prompt phrasing that ties the new image back to them, not re-describing the subject from scratch.

## Inputs to collect

- **The subject's reference image(s).** One clear shot is enough; several angles/expressions improve fidelity. (Ask only if none provided.)
- **What changes** in the new image: scene, pose, outfit, style, or all of these.
- **How many** outputs and the target use (single hero, a reference sheet, a set of expressions/outfits).
- Optional: a locked style or palette to carry across the set.

## Models

- **Default: Google Nano Banana 2** (`google:4@3`) - accepts up to **14 reference images** and holds identity strongly across scenes and styles. Best general pick.
- **For a trained, reusable identity** (a recurring brand character used at scale): train a LoRA via `train-style-model`, then generate with it - more setup, maximum consistency.
- **Reference-guided alternatives:** IP-Adapter on a FLUX/SDXL base, or any image model that accepts `referenceImages`. Confirm support and the exact field via `runware-models` + `runware-run` before calling.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the reference-image field and its max count.
2. Upload the subject reference(s) into `inputs.referenceImages`.
3. Run `imageInference` synchronously with a prompt that **names the subject as "the same … from the reference"** and then describes only what's new.
4. For a set (reference sheet, expressions, outfits), reuse the *same* references across calls and vary only the scene/pose clause. Keep a fixed seed if you want tighter repeatability.
5. Review for identity drift; retry the outliers with an added or clearer reference.

## Technique

- **Anchor, then vary.** State the immutable identity once ("the same woman from the reference image, same face and hair") and let the rest of the prompt change freely (new pose, lighting, outfit, setting). Do not re-describe the face from imagination - that invites drift.

  Fill this character-anchor template, then send it as `positivePrompt`:

  ```
  The same <subject> from the reference image <new scene, pose, lighting, or medium>. Keep <the immutable identity features: face, hair, key details> identical.
  ```

  The first clause is the immutable anchor (do not vary it). The middle clause is the only part that changes per image. The closing clause names the features to hold hardest.

  Load `references/examples.md` for worked end-to-end recipes (single subject, hidden-detail reference set, two locked subjects).
- **More references = more stability.** A single front shot works; adding profile/expression shots locks identity harder across angles.
- **Composition is a sibling move:** to place the subject *with* other real elements (product, backdrop), give each as a separate reference and describe how they fit - see `composite-scene`.
- **For a whole set,** hold references and style constant and change only one variable per image. That's what makes a reference/expression/outfit sheet read as one character.

## Parameters that matter

- `inputs.referenceImages` - up to **14** on Nano Banana 2; order is not significant.
- Prompt phrasing carries the consistency, not a `strength` dial - lead with "the same … from the reference".
- `seed` - fix it for tighter repeatability across a set; vary it for alternates.
- Confirm exact field names against the live schema (`runware-run`); never guess.

## Quality bar

- Face/identity is recognizably the same across every output (no morphing between siblings).
- Only the intended variables changed (pose/scene/outfit), not the subject.
- For a set, the images read as one character, not cousins. Retry any that drift with a clearer or extra reference.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `composite-scene` (subject + other elements), `train-style-model` (reusable identity), `product-photography` (same-product across shots).
