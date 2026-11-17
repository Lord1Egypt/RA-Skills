# Animate an image: worked recipes

Three end-to-end recipes. Each shows the scenario, the async `videoInference` request, and the result shape. Confirm the AIR is `live` and the field names against the live schema before sending. Run async: the request returns a `taskUUID`, then poll `getResponse` until terminal. The finished clip is at `videoURL`.

All AIRs below are verified against the Runware catalog: `runway:1@2` (Runway Gen-4.5), `luma:ray@3.2` (Luma Ray 3.2), `prunaai:p-video@animate` (Pruna P-Video-Animate).

## 1. Subtle product motion (Runway Gen-4.5)

Scenario: a packshot of a watch on a stone surface. The client wants it to feel alive for a social post without re-staging the scene. Hold the camera, add a slow push-in, and layer one atmospheric element the still already implies (steam off a coffee cup beside it, or here, drifting dust motes in the light).

Source still goes in `inputs.frameImages` marked `first`. The prompt directs only what changes over time. State the holds.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "runway:1@2",
    "inputs": {
      "frameImages": [
        { "image": "https://example.com/watch-packshot.jpg", "frame": "first" }
      ]
    },
    "positivePrompt": "Slow continuous push-in toward the watch face. Fine dust motes drift gently through the warm side light. A faint specular highlight travels slowly across the polished bezel. The watch holds completely still. No other subject motion.",
    "width": 1280,
    "height": 720,
    "duration": 5
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
      "videoUUID": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/f1e2d3c4-b5a6-7890-1234-567890abcdef.mp4"
    }
  ]
}
```

Why it works: the subject channel is locked to zero ("holds completely still", "no other subject motion"), so the only motion is the camera push and the atmospheric dust. Both have visual evidence in the still. This is the cheapest "alive" effect for a product shot.

## 2. Character gesture with camera push-in (Luma Ray 3.2)

Scenario: a half-body portrait of a barista. The client wants a short "alive portrait" for an avatar: the subject breathes and gives a small gesture while the camera tightens. Both channels active, each on purpose.

Ray takes the still as the `first` frame via `inputs.frameImages`. Match the output aspect to the source so nothing crops. Ray returns a silent MP4, so plan audio separately if the client needs it.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "b7e8d9c0-1a2b-3c4d-5e6f-708192a3b4c5",
    "model": "luma:ray@3.2",
    "positivePrompt": "Slow steady push-in toward the barista. She breathes calmly, her chest rising and falling, and gives a small warm nod toward the camera. Steam curls upward continuously from the cup in her hands. The camera moves forward gradually across the clip.",
    "width": 832,
    "height": 1104,
    "duration": 5,
    "inputs": {
      "frameImages": [
        { "image": "https://example.com/barista-portrait.jpg", "frame": "first" }
      ]
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
      "taskUUID": "b7e8d9c0-1a2b-3c4d-5e6f-708192a3b4c5",
      "videoUUID": "c1d2e3f4-a5b6-7890-cdef-1234567890ab",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/c1d2e3f4-a5b6-7890-cdef-1234567890ab.mp4"
    }
  ]
}
```

Why it works: the gesture (nod, breath) stays inside the head-and-shoulders region the still supports, so nothing warps. The camera push and the subject motion reinforce each other. Set aspect through `width`/`height` here, not also through `resolution`. To pin a start and end pose instead, add a second `frameImages` entry with `frame: "last"`.

## 3. Motion transfer from a reference video (Pruna P-Video-Animate)

Scenario: a talking-head clip of a presenter exists, and the client wants the same delivery on a cartoon mascot. The image controls who is on screen, the video controls what happens. Route to P-Video-Animate.

The still is `inputs.referenceImages` (exactly one). The motion source is `inputs.referenceVideos` (exactly one). Match the image's framing and pose to the first frame of the source video or the motion is lost. Leave `positivePrompt` out to transfer the motion as-is.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "d4c5b6a7-8e9f-0a1b-2c3d-4e5f60718293",
    "model": "prunaai:p-video@animate",
    "inputs": {
      "referenceImages": ["https://example.com/mascot-portrait.jpg"],
      "referenceVideos": ["https://example.com/presenter-talking.mp4"]
    },
    "resolution": "720p",
    "settings": { "preserveAudio": true }
  }
]
```

Result:

```json
{
  "data": [
    {
      "taskType": "videoInference",
      "taskUUID": "d4c5b6a7-8e9f-0a1b-2c3d-4e5f60718293",
      "videoUUID": "ae78185a-4ca6-425e-aa85-1968de419142",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/ae78185a-4ca6-425e-aa85-1968de419142.mp4"
    }
  ]
}
```

Why it works: both the mascot still and the first frame of the presenter video are head-and-shoulders facing the camera, so the talking-head motion maps cleanly. The model is style-agnostic, so the cartoon look carries through. The output aspect is inferred from the source video. To override one behavior (add a wave at the end, change the lip-synced words), add a `positivePrompt` that names only that action and keep the source motion otherwise. Pair a full-body still with a full-body source if the motion needs a body to map onto.
