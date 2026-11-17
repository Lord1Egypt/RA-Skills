# Cinematic video: worked recipes

Three end-to-end recipes. Each shows the scenario, the cinematic prompt with real camera language, the async `videoInference` request, and the result shape. Confirm the AIR is `live` and the field names against the live schema before sending. Run async: the request returns a `taskUUID`, then poll `getResponse` until terminal. The finished clip is at `videoURL`.

All AIRs below are verified against the Runware catalog: `google:3@2` (Veo 3.1), `luma:ray@3.2` (Luma Ray 3.2), `runway:1@2` (Runway Gen-4.5).

Each prompt is built on the compact scaffold: lead with framing and camera motion, then style, lighting, location, action. Three or four sentences naming each element beat a wall of adjectives.

## 1. Moody establishing shot (text-to-video, Veo 3.1)

Scenario: the opening frame of a short film. No source still exists, so this is text-to-video and the prompt builds the whole frame. Lead with the wide framing and the slow push-in, name the style and the dramatic light, then let world knowledge fill the storm detail.

Veo 3.1 reads the five-element scaffold directly and generates synchronized audio natively (on by default via `providerSettings.google.generateAudio`). For text-to-video, `width` and `height` are required and must be one allowed pair, here `1280 × 720`. `duration` is 4, 6, or 8.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "model": "google:3@2",
    "positivePrompt": "A wide cinematic establishing shot with a slow push-in. Cinematic photorealism. Dramatic backlit golden-hour light breaking through heavy stormy clouds. A weathered white lighthouse stands on a Cornish coastal cliff, lashed by heavy rain and crashing sea spray against the black rocks below. The lighthouse beam rotates slowly through the dusk light, cutting through the rain in a single bright sweep.",
    "width": 1280,
    "height": 720,
    "duration": 8
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

Why it works: the camera phrase leads, so the model parses "wide establishing shot with a slow push-in" as a directive, not scene flavor. "Cornish coastal cliff" plus "stormy clouds" carries the geography and weather without spelling out that storm light is dramatic or that rain catches the beam. Four sentences cover all five elements. Eight seconds, the longest Veo allows, suits a single beat with an unhurried move, and the native audio carries the storm ambience without a second pass.

## 2. Product beauty shot with a slow push-in (image-to-video, Runway Gen-4.5)

Scenario: a packshot of a perfume bottle on polished stone. The client wants it to feel premium for a launch reel without re-staging. The still fixes subject, composition, palette, and lighting, so the prompt directs only the motion. Lock the subject to zero and let the camera and one atmospheric element carry the shot.

Source still goes in `inputs.frameImages` marked `first` (Gen-4.5 takes exactly one). `width` and `height` are required and must be one of the allowed pairs. Pick the pair that matches the still's aspect. `duration` is 5, 8, or 10.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "b7e8d9c0-1a2b-3c4d-5e6f-708192a3b4c5",
    "model": "runway:1@2",
    "inputs": {
      "frameImages": [
        { "image": "https://example.com/perfume-packshot.jpg", "frame": "first" }
      ]
    },
    "positivePrompt": "Slow continuous push-in toward the perfume bottle. A soft specular highlight travels gradually across the polished glass and the chrome cap. Fine atmospheric haze drifts slowly through the warm side light. The bottle holds completely still. No other subject motion.",
    "width": 960,
    "height": 960,
    "duration": 5,
    "seed": 42
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
      "videoUUID": "f1e2d3c4-b5a6-7890-1234-567890abcdef",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/f1e2d3c4-b5a6-7890-1234-567890abcdef.mp4"
    }
  ]
}
```

Why it works: the subject channel is named to zero ("holds completely still", "no other subject motion"), so the only motion is the slow push and the traveling highlight, both with visual evidence in the still. The pace word "slow" reads deliberate and weighty, the register a beauty shot wants. `seed` pins the take so a retry of the grade reproduces the same move. Setting aspect through the `960 × 960` pair keeps the square packshot from cropping.

## 3. Character close-up with rack focus (text-to-video, Luma Ray 3.2)

Scenario: an intimate character beat for a trailer. No locked still, so this is text-to-video and the prompt builds the frame and the focus move together. Lead with the close framing and the rack focus, name the shallow-depth style and the practical light, then give the subject one small action.

Ray reads cinematic motion and grade well. `duration` is 5 or 10 only. The dimension set is broad, so match the pair to the target aspect (here `1280 × 720`). Ray returns a silent MP4, so plan audio separately if the trailer needs it.

```json
[
  {
    "taskType": "videoInference",
    "taskUUID": "c2d3e4f5-6a7b-8c9d-0e1f-2a3b4c5d6e7f",
    "model": "luma:ray@3.2",
    "positivePrompt": "A tight character close-up with a slow rack focus. Cinematic shallow depth of field, the background falling into soft bokeh. Warm practical lamplight from one side, cool window light filling the shadows. A woman by a rain-streaked window, the focus pulling gradually from the foreground raindrops on the glass to her eyes. She breathes calmly and her gaze settles.",
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
      "taskUUID": "c2d3e4f5-6a7b-8c9d-0e1f-2a3b4c5d6e7f",
      "videoUUID": "ae78185a-4ca6-425e-aa85-1968de419142",
      "videoURL": "https://vm.runware.ai/video/os/a14d18/ws/2/vi/ae78185a-4ca6-425e-aa85-1968de419142.mp4"
    }
  ]
}
```

Why it works: "rack focus" is read as the industry term, so the shift lands as a focus pull from the raindrops to the eyes rather than a guess. The pace word "slow" and "gradually" set the unhurried register a character beat wants. The action stays small (a breath, a settling gaze) and inside the close framing, so nothing warps. Style and lighting are named once each, and "rain-streaked window" carries its own atmospheric motion for free.
