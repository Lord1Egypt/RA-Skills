# Edit video: worked recipes

Three end-to-end recipes covering the load-bearing split: a whole-frame transform (Luma Ray 3.2) and a surgical edit (Runway Aleph 2.0), once by prompt and once anchored. Each shows the scenario, the async `videoInference` request, and the result shape. Confirm the AIR is `live` and the field names against the live schema before sending. Run async: the request returns a `taskUUID`, then poll `getResponse` until terminal. The finished clip is at `videoURL`.

Both AIRs below are verified `live` against the Runware catalog: `luma:ray@3.2` (Luma Ray 3.2), `runway:aleph@2.0` (Runway Aleph 2.0).

## 1. Whole-frame restyle (Luma Ray 3.2)

Scenario: a shot of a violinist performing exists, and the client wants the same performance reimagined as a figure of flowing golden light against a dark void. The bowing and motion are the throughline. Everything else is rebuilt from the prompt. This is a transform, so route to Luma.

The source goes in `inputs.video`. Describe the target look and let the motion carry. `settings.edit.strength` sets how far the result departs from the source, so start in `flex` and pull back to `adhere` if the performance drifts. On an edit, do not send `width`/`height`/`duration` or `resolution` with width/height: editing holds the source aspect ratio and runtime, and `settings.edit` is mutually exclusive with `width`/`height`.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "e5d6c7b8-9a0b-1c2d-3e4f-5a6b7c8d9e0f",
    "model": "luma:ray@3.2",
    "positivePrompt": "Transform the violinist into a luminous figure of flowing golden light against a dark void, ribbons of light streaming from the bow and tracing his body, following his exact bowing and motion.",
    "inputs": {
      "video": "https://example.com/violinist.mp4"
    },
    "settings": {
      "edit": { "strength": "flex_2" }
    }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "e5d6c7b8-9a0b-1c2d-3e4f-5a6b7c8d9e0f",
      "videoUUID": "f6e5d4c3-b2a1-0987-6543-21fedcba0987",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/f6e5d4c3-b2a1-0987-6543-21fedcba0987.mp4"
    }
  ]
}
```

Why it works: the prompt names the target look and ties it to the source motion ("following his exact bowing and motion"), so Ray carries the performance and rebuilds the frame around it. `flex_2` keeps the shape close while letting the light take over. For a bolder rework step up toward `reimagine`. To pin the exact target look instead of leaning on words, add a restyled `inputs.frameImages` entry (a frame pulled from the source and edited to the target look, framing held). For a clean first pass without tuning signals, set `settings.edit.autoControls: true`, which derives the conditioning from the source and cannot be combined with `strength` or manual `controls`.

## 2. Surgical color swap by prompt (Runway Aleph 2.0)

Scenario: a finished, color-graded clip of a black luxury sedan driving down an avenue exists, and the client signs off on one change: the paint goes deep crimson. The road, the lighting, the framing, and the camera move must stay pixel-stable. This is a one-region change, so route to Aleph.

The source goes in `inputs.video` (required). Name only what changes, then **end with a clause pinning the rest in place**. That closing clause is what stops a paint change from also rebuilding the road. `positivePrompt` is required and capped at 1000 characters. Aleph requires a 2 to 30 second source at up to 1080p and preserves the input aspect ratio.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "runway:aleph@2.0",
    "inputs": {
      "video": "https://example.com/sedan.mp4"
    },
    "positivePrompt": "Change the sedan's bodywork color to a deep glossy crimson red. Keep the chrome trim, glass, headlights, road, and surroundings exactly as in the source."
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "videoUUID": "9c1b2d3a-4e5f-6789-abcd-ef0123456789",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/9c1b2d3a-4e5f-6789-abcd-ef0123456789.mp4"
    }
  ]
}
```

Why it works: the prompt leads with a transformation verb the model honors (`change`), names one attribute (bodywork color), then pins the chrome, glass, road, and surroundings. Art-direction phrasing beats caption phrasing, so "change the bodywork to crimson, keep the chrome and surroundings" outperforms "a red sedan drives down an avenue". The same shape covers a wardrobe swap, an environment replacement (`replace the avenue with a coastal road, the car and framing stay exactly as in the source`), or a grade (`restyle as 1980s neon-noir, keep the motion and composition`). On a multi-shot reel inside one clip, Aleph propagates the single edit across every cut as long as the subject reads as continuous.

## 3. Surgical brand identity by anchor (Runway Aleph 2.0)

Scenario: a clip orbits a plain white sneaker, and the client needs an exact brand identity applied: a red side stripe, the wordmark "STRYDE" on the heel counter, contrast stitching. A prompt approximates the stripe geometry and the letterform drifts between frames, which a brand team rejects. Anchor the exact target look instead.

Pull the source's first frame, edit it externally to the precise design with the framing held, then send it back in `inputs.frameImages` pinned with `frame: "first"`. Aleph treats the anchor as the target appearance at that moment and carries it through the orbit. The prompt names the change, the anchor defines the truth. Aleph accepts up to 5 anchors, each pinned with `frame` (`first`/`last`/`0`/`-1`) or a `timestamp` in seconds, never both on one entry.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
    "model": "runway:aleph@2.0",
    "inputs": {
      "video": "https://example.com/sneaker.mp4",
      "frameImages": [
        { "image": "https://example.com/anchor-brand.jpg", "frame": "first" }
      ]
    },
    "positivePrompt": "Apply the brand identity shown in the reference image to the plain white sneaker. Keep the sneaker shape, the camera orbit, the matte surface, lighting, and framing exactly as in the source."
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "c3d4e5f6-7a8b-9c0d-1e2f-3a4b5c6d7e8f",
      "videoUUID": "7a8b9c0d-1e2f-3a4b-5c6d-7e8f90a1b2c3",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/7a8b9c0d-1e2f-3a4b-5c6d-7e8f90a1b2c3.mp4"
    }
  ]
}
```

Why it works: the design lives in the anchor frame, not the prompt string, so the stripe geometry and letterform stay locked through every angle of the orbit. The anchor matches the source's opening framing with only the brand added, which is what lets the model map it onto the rest of the clip. Reach for an anchor the moment the prompt feels vague: brand assets, exact typography, custom patterns, anything a designer signed off on. To evolve the look across the runtime instead of holding one identity, add a second anchor at `frame: "last"` and let the model interpolate between the two states.
