---
name: composite-scene
description: >
  Merge several real images into one coherent picture without manual cut-out or masking. Use when
  the user says "put this product into that scene", "combine these two photos", "place my subject
  on this background", "drop the watch onto the table", "make these into one image", or wants a
  product, a subject, and a backdrop fused with matching light and perspective. The inputs are
  multiple images. To edit a single image, use edit-image. To keep one character identical across
  new scenes, use character-consistency.
---

# Composite scene

Combine several real elements (a product, a subject, a backdrop, a style) into one coherent image, with lighting and perspective already reconciled, without cutting out, masking, or compositing by hand. Each element is a separate reference image and the prompt directs how the pieces fit. This is the reverse of `character-consistency`: instead of holding one subject across many images, it pulls many images into one.

## Inputs to collect

- **One clean reference per element.** The product shot, the subject, the backdrop, and/or the style reference. A subject on a plain background composites more predictably than one already buried in a busy scene. (Ask only if none provided.)
- **The relationship between elements:** placement, scale, and contact ("resting on", "leaning against", "walking beside"). The references can't convey this, so the prompt must.
- **The target scene:** setting, target lighting, camera angle/framing.
- **How many** outputs, and whether the same elements drop into several different scenes.

## Models

- **Default: Google Nano Banana 2** (`google:4@3`) accepts up to **14 reference images** in one call and reconciles lighting and perspective across all of them. Best general pick for composition.
- **Reference-guided alternatives:** any image model that accepts `referenceImages` (e.g. Nano Banana Pro, IP-Adapter on a FLUX/SDXL base). Smaller reference budgets and weaker cross-element relighting, so confirm support and the field via `runware-models` plus `runware-run` before calling.
- Confirm the model is `live` and current via `runware-models`. Never hardcode a stale choice.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the reference-image field and its max count.
2. Upload each element as its own entry in `inputs.referenceImages`. One entry per element, not one combined image.
3. Run `imageInference` synchronously with a `positivePrompt` that **names each reference by its array position** ("the watch from the first image", "the table from the second image") and **directs the relationship, placement, scale, and target lighting**.
4. For the same elements across several scenes, reuse the *same* references and change only the scene/relationship clause.
5. For a busy composite, build up in passes: get two or three elements right, feed that result back in as a new reference, then add the next element.
6. Review for placement, scale, and lighting coherence, then retry with a clearer reference or a more explicit relationship clause.

See `references/examples.md` for worked end-to-end recipes (product into a scene, two subjects merged, style-transfer composite) with concrete requests and result shapes.

## Technique

- **References supply the *what*, the prompt supplies the *where* and *how*.** The reference images carry each element's identity. `positivePrompt` carries placement, scale, lighting, and the relationship between elements. Both are needed.
- **Order matters.** The model maps "the first image" / "the second image" in the prompt to the array order, so naming the position is the most reliable way to say which element is which. Adding a description ("the watch", "the table") on top of the position helps once a scene has three or more references.
- **Direct the relationship explicitly.** State contact and arrangement: "resting on", "leaning against", "walking beside". The references cannot tell the model how the pieces relate, so the prompt has to.
- **Let the model handle lighting.** Don't match lighting between source references. Describe the target lighting once and the model relights every element to fit the final scene.
- **Prompt template.** List the elements by position, state the placement and contact, then name the one target lighting and angle all elements must reconcile to:
  - *Elements:* "the [thing] from the first image, the [thing] from the second image, ..."
  - *Placement:* the relationship and scale ("resting on", "leaning against", "walking beside", "scaled naturally to each other").
  - *Lighting to reconcile:* one target light and camera angle for the whole frame ("warm morning light, overhead flat-lay angle"), plus a hold clause naming the per-element details to keep.
- **Three common patterns:**
  - *Product into a scene:* shoot the product once on a plain background, then drop it into as many styled environments as needed without re-shooting.
  - *Merging subjects:* two subjects photographed apart, brought into one setting with both identities held. This is the bridge to `character-consistency`.
  - *Style transfer:* pair a content reference with a style reference, and the model repaints the first in the manner of the second. An actual example beats describing a style in words.
- **Build complex scenes in passes** rather than stacking all references at once. Iterating on a confirmed partial result is more reliable than asking for everything in one shot.

## Parameters that matter

- `inputs.referenceImages`, up to **14** on Nano Banana 2, one entry per element. Order is significant because the prompt refers to elements by position.
- `positivePrompt` does the directing: placement, scale, lighting, and inter-element relationships. This is where the composite is actually controlled.
- `seed`, fix it to reproduce or iterate on a given composite, vary it for alternates.
- `width` / `height` (or `resolution`) set the target frame for the composed scene.
- Confirm exact field names and limits against the live schema (`runware-run`). Never guess.

## Quality bar

- Every element keeps its source identity (the product, the subject, the backdrop read as themselves, not redrawn).
- Placement, scale, and contact match the prompt's stated relationship.
- Lighting and perspective are consistent across elements, not pasted-on. No floating subjects or mismatched shadows.
- Only honest composites: no invented logos, fake badges, or on-image copy the user didn't supply. Retry incoherent results with a clearer reference or a more explicit relationship clause.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `character-consistency` (hold one subject across many images, the reverse move), `product-photography` (same product across shots, then composite the result here).
