# Controlled generation - worked recipes

Three end-to-end ControlNet recipes, one per control type (Canny edges, OpenPose, depth). Each runs the same two-call pipeline: a `controlNetPreprocess` task builds the control map, then an `imageInference` task conditions generation on that map. Confirm every AIR is `live` and every field and range against the live schema with `runware-run` before calling, since the catalog moves.

## The two-call shape

**Call 1 - extract the map.** `controlNetPreprocess` takes the preprocessor AIR in `model` and the source in `inputs.image`. It returns a guide image:

```json
{
  "data": [
    {
      "taskType": "controlNetPreprocess",
      "taskUUID": "<echoes your request>",
      "inputImageUUID": "<uuid of the source>",
      "guideImageUUID": "<uuid of the guide>",
      "guideImageURL": "https://im.runware.ai/image/.../<guideImageUUID>.jpg"
    }
  ]
}
```

**Call 2 - condition generation.** `imageInference` takes a base model in `model` and a `controlNet` array whose entry carries the matching ControlNet AIR plus the `guideImageURL` (or `guideImageUUID`) from call 1. It returns the image inline:

```json
{
  "data": [
    {
      "taskType": "imageInference",
      "taskUUID": "<echoes your request>",
      "imageUUID": "<uuid of the result>",
      "imageURL": "https://im.runware.ai/image/.../<imageUUID>.jpg",
      "seed": 123456789
    }
  ]
}
```

Pass `guideImageURL` from call 1 straight into `controlNet[].guideImage` in call 2. Both calls return synchronously, no polling. The base model and the ControlNet must share an architecture: a FLUX.1 [dev] ControlNet (`runware:25@1`, `runware:27@1`, `runware:29@1`) needs the FLUX.1 [dev] base (`runware:101@1`), an SDXL ControlNet (`runware:20@1`, `runware:3@1`) needs an SDXL base.

## 1. Canny edge-locked restyle

**Scenario.** The user has a render of a leather armchair and asks to keep the exact silhouette and seams but make it a glossy chrome sci-fi chair. Outlines must hold, the material changes completely. Canny is the right map for a hard silhouette.

**Call 1 - Canny edge map.** Tune the thresholds to set how much structure survives. Defaults (`lowThresholdCanny: 100`, `highThresholdCanny: 200`) suit most inputs. Push `highThresholdCanny` up to keep only strong edges on a busy source, push `lowThresholdCanny` down to catch soft transitions.

```json
{
  "taskType": "controlNetPreprocess",
  "model": "runware:controlnet-preprocess@canny",
  "inputs": {
    "image": "https://example.com/leather-armchair.jpg"
  },
  "settings": {
    "lowThresholdCanny": 100,
    "highThresholdCanny": 200
  }
}
```

**Call 2 - restyle on the edge map.** FLUX.1 [dev] base (`runware:101@1`) with the FLUX Union Pro Canny ControlNet (`runware:25@1`). `startStep: 1, endStep: 10` on a 30-step run is the balanced window: edges shape the early layout, then the model is free to invent the new material.

```json
{
  "taskType": "imageInference",
  "model": "runware:101@1",
  "positivePrompt": "a glossy chrome sci-fi armchair, polished reflective metal, studio lighting, clean background",
  "width": 1024,
  "height": 1024,
  "steps": 30,
  "controlNet": [
    {
      "model": "runware:25@1",
      "guideImage": "<guideImageURL from call 1>",
      "weight": 1,
      "startStep": 1,
      "endStep": 10
    }
  ]
}
```

Field notes (verified against the live schema):

- `controlNet[]` items require `model` and `guideImage`. `weight` defaults to `1` (range `-4` to `4`). `controlMode` is `balanced` (default), `controlnet`, or `prompt`.
- `startStep`/`endStep` are absolute step numbers. Do not also send `startStepPercentage`/`endStepPercentage` in the same entry, the two pairs are mutually exclusive.
- Raise `endStep` toward `steps` to hold the silhouette harder (good for a pure restyle that keeps the subject), lower it to let the new material dominate. A higher `startStep` weakens structure adherence because guidance arrives after the early layout is set.
- For FLUX.1 [dev], `positivePrompt`, `width`, and `height` are all required. `width`/`height` are `128`-`2048`, multiple of `64`. `steps` max `50`.

To lock a consistent art style across a set, add a `lora` entry alongside `controlNet` and reuse one guide image across calls, varying only the prompt. For the SDXL tier, swap the base for an SDXL checkpoint and the ControlNet for `runware:20@1` (SDXL Canny).

## 2. Pose-driven generation (OpenPose)

**Scenario.** The user has a reference photo of a person mid-stride and wants a totally different character (a knight in armor) holding that exact body pose. Pose is the map: it carries limb placement and gesture, not the appearance.

**Call 1 - pose skeleton.** Set `includeHandsAndFaceOpenPose: true` when hands or facial orientation matter (it adds finger and face landmarks), leave it `false` for body-only pose.

```json
{
  "taskType": "controlNetPreprocess",
  "model": "runware:controlnet-preprocess@openpose",
  "inputs": {
    "image": "https://example.com/runner-reference.jpg"
  },
  "settings": {
    "includeHandsAndFaceOpenPose": true
  }
}
```

**Call 2 - new character on the skeleton.** FLUX.1 [dev] base (`runware:101@1`) with the FLUX Union Pro Pose ControlNet (`runware:29@1`). Describe only the new character and scene, the skeleton already encodes the pose.

```json
{
  "taskType": "imageInference",
  "model": "runware:101@1",
  "positivePrompt": "a knight in ornate steel plate armor, mid-stride, dramatic cinematic lighting, castle courtyard",
  "width": 832,
  "height": 1216,
  "steps": 30,
  "controlNet": [
    {
      "model": "runware:29@1",
      "guideImage": "<guideImageURL from call 1>",
      "weight": 1,
      "startStep": 1,
      "endStep": 10
    }
  ]
}
```

Field notes:

- Pose only constrains the figure's posture. The model is free on appearance, clothing, and background, so the prompt does all of that work.
- Match the canvas aspect ratio to the source pose. A standing figure wants a portrait frame (here `832x1216`) so the skeleton is not squashed.
- If the new character drifts off the pose, raise `weight` toward `1.5`-`2` or push `endStep` later. If the pose looks rigid and the character cannot emerge, lower `endStep`.

## 3. Depth-guided interior restyle

**Scenario.** The user has a photo of a plain living room and wants it redesigned as a warm Scandinavian interior, same room layout, windows, and camera perspective. Depth is the map for rooms and scenes: it holds 3D layout and perspective while every surface and object restyles.

**Call 1 - depth map.** The depth preprocessor takes no extra settings, just the source.

```json
{
  "taskType": "controlNetPreprocess",
  "model": "runware:controlnet-preprocess@depth",
  "inputs": {
    "image": "https://example.com/plain-living-room.jpg"
  }
}
```

**Call 2 - redesign on the depth map.** FLUX.1 [dev] base (`runware:101@1`) with the FLUX Union Pro Depth ControlNet (`runware:27@1`). Depth restyle usually wants a longer guide window than a Canny restyle so the room geometry stays put while the look changes hard.

```json
{
  "taskType": "imageInference",
  "model": "runware:101@1",
  "positivePrompt": "a warm Scandinavian living room, light oak floors, linen sofa, soft natural daylight, minimalist decor",
  "width": 1216,
  "height": 832,
  "steps": 30,
  "controlNet": [
    {
      "model": "runware:27@1",
      "guideImage": "<guideImageURL from call 1>",
      "weight": 1,
      "startStep": 1,
      "endStep": 15
    }
  ]
}
```

Field notes:

- Depth preserves layout, foreground-background separation, and camera perspective, not edges. Furniture can change shape as long as it sits at the same depth, which is what makes a redesign read as the same room.
- `endStep: 15` (half of 30) holds the geometry through more of the run than the Canny default. Raise it further to keep the layout near-identical, lower it to let the redesign reshape the space.
- For the SDXL tier, swap to an SDXL base and `runware:3@1` (SDXL Depth).
- For a redesign series of the same room, reuse the one depth map across calls and change only the style clause in the prompt so every variant shares the layout.
