# Edit image - worked recipes

Three end-to-end recipes, one per edit mode. Each shows the real request and the result shape. Confirm every field and range against the live schema with `runware-run` before calling, since the catalog moves.

All three are `imageInference` tasks and return the same image response inline:

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "<echoes your request>",
      "imageUUID": "<uuid of the result>",
      "imageURL": "https://im.runware.ai/image/.../<imageUUID>.jpg"
    }
  ]
}
```

Reference the `imageURL` (or `imageUUID`) downstream. No polling, stills come back on the same call.

## 1. Instruction edit - recolor or replace (Bria FIBO Edit)

**Scenario.** The user has a product photo of a sofa and asks "change the sofa to navy blue, keep the room as is." No mask. One plain instruction.

Use **Bria FIBO Edit** (`bria:21@1`). It takes `inputs.image` plus a `positivePrompt` and preserves the original lighting and structure while applying the edit. Name only what changes. Adding "keep everything else" holds the untouched regions steady.

```json
{
  "taskType": "imageInference",
  "model": "bria:21@1",
  "inputs": {
    "image": "https://example.com/living-room.jpg"
  },
  "positivePrompt": "change the sofa to navy blue, keep the rest of the room unchanged",
  "CFGScale": 5,
  "steps": 50
}
```

Field notes (verified against the live schema):

- `inputs.image` is required. `inputs.mask` is optional and narrows the edit to a painted region when you want a hard boundary.
- `positivePrompt` is required, 2 to 3000 characters.
- `CFGScale` is an enum, one of `3`, `4`, `5` (default `5`). `steps` ranges 20 to 50 (default `50`).

For a plain add, remove, replace, or restyle instruction you can also route to **Qwen-Image-Edit-2511** (`alibaba:qwen-image-edit@2511`). Its input shape differs: pass the source in `inputs.referenceImages` (an array, one image) rather than `inputs.image`, plus the same `positivePrompt`. Reach for FIBO Edit on tone, light, and blend edits, Qwen on instruction-phrased object edits.

## 2. Object removal - mask-driven, prompt-less (FLUX Erase)

**Scenario.** A street photo with a pedestrian the user wants gone. The ask is one sentence ("remove the person"), so this is removal, not replacement. No prompt.

Use **FLUX Erase** (`bfl:flux@erase`). Pass the source and a binary mask at the **exact same resolution**. White (255) marks what disappears, black (0) marks what to keep. The model reconstructs the background and also clears shadows and reflections the mask did not fully cover.

```json
{
  "taskType": "imageInference",
  "model": "bfl:flux@erase",
  "inputs": {
    "image": "https://example.com/street.jpg",
    "mask": "https://example.com/person-mask.png"
  },
  "settings": {
    "dilatePixels": 15
  }
}
```

Field notes (verified against the live schema):

- `inputs.image` and `inputs.mask` are both required. A dimension mismatch between them is a hard validation error.
- `settings.dilatePixels` is the only knob. Default `10`, range `0` to `25`. It expands the mask outward before erasing.
- Raise it to `15` to `20` for soft edges (hair, fur, smoke) or visible shadows. Lower it, or set `0` with a precise hand mask, for tight removals next to content you keep.

For people, auto-generate the mask first with the Image Masking API (`runware:35@4` full-body, `runware:35@2` face) as a separate `imageMasking` task, then pipe its `maskImageURL` straight into `inputs.mask`. FLUX Erase trains near 1 MP, so downscale a large source then upscale the result.

## 3. Outpaint - per-side pixel extension (FLUX Outpainting)

**Scenario.** A 1024 x 1024 coastal square that needs to become a 2048 x 1024 banner without re-framing the subject. The new regions should continue the existing scene, no new elements, so prompt-less is the right call.

Use **FLUX Outpainting** (`bfl:flux@outpainting`). You do not pass `width`/`height`. You pass `outpaint.{top,right,bottom,left}` in pixels and the output is derived: `output_width = source_width + left + right`, same for height. To go from 1024 wide to 2048 wide, add 512 on each horizontal side and leave top and bottom at `0`.

```json
{
  "taskType": "imageInference",
  "model": "bfl:flux@outpainting",
  "inputs": {
    "image": "https://example.com/coast-1024.jpg"
  },
  "outpaint": {
    "top": 0,
    "right": 512,
    "bottom": 0,
    "left": 512
  },
  "settings": {
    "autoCrop": true,
    "mode": "high"
  }
}
```

Field notes (verified against the live schema):

- `inputs.image` and `outpaint` are both required. At least one of the four `outpaint` sides must be set. Each side defaults to `0`. Asymmetric values are fine.
- Output is capped at 4 MP total with neither side over 2048 px. `settings.autoCrop` defaults to `false`, which returns a 422 when an extension would overflow. Set `true` and the model crops to fit so the request still succeeds. Use it in production pipelines.
- `settings.mode` is `high` (default, best fidelity) or `fast` (quicker, good for plain landscape and texture continuation).

Plan the target canvas first, subtract the source dimensions, then split the difference across the sides you want to grow. Extend the side with the most continuation cues (a horizon, a path, a wall). When the new region must introduce something new or redirect style, switch to FLUX Expand (`bfl:1@3`) and steer it with a prompt instead.
