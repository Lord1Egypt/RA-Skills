# Video prompting and input selection

Use the user's specified model, settings, facts and assets. Ask only for a missing
input that changes the deliverable or charge. Do not invent product claims or
promise exact logos, text, identity or motion fidelity.

| Intent                   | Prompt focus                                                     | MiniMax payload                                                            |
| ------------------------ | ---------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Text to video            | Subject, one clear action, setting, camera movement, light/style | `content`                                                                  |
| Animate a supplied image | Motion and camera changes; preserve the supplied subject         | `content`, `imageUrl`                                                      |
| Start/end transition     | Continuous action connecting the two supplied frames             | `content`, `imageUrl`, `lastFrameUrl`                                      |
| Reference-guided scene   | Assign each asset a role: product, person, movement or audio     | `content`, `referenceImageUrls`, `referenceVideoUrl`, `referenceAudioUrls` |

Frame inputs and reference assets are mutually exclusive. Confirm an ambiguous
photo's role before treating it as a character identity or style reference.
Images accept public URLs or image data URIs; video/audio require public URLs.
A local file path is not a public URL. `image` is not a MiniMax field.

For a five-second clip, start with one main action and a readable camera move.
Avoid conflicting camera directions or a long sequence that cannot fit. For
image-to-video, describe the motion rather than reinventing the subject.

Example image-animation prompt, to adapt to the user's actual product:

> Preserve the supplied lamp's shape and material. Slowly push the camera closer
> as the warm light turns on. Keep the background simple and focus on the light
> transition in one continuous shot.

For text-to-video, specify what must be created, for example a red bicycle moving
along a rainy city street, with a slow tracking shot and soft evening reflections.
Keep exact user wording when they request it; do not expand every prompt by default.

## Parameters by intent

Default to MiniMax H3 for a new ordinary request. This is a product default, not a
claim that it wins every quality comparison. Preserve an explicitly selected model
for follow-ups unless its contract cannot support the requested input or output.

- MiniMax H3: numeric duration 5–20; `resolution` is `720p` or `1080p`;
  `aspectRatio`; `content`; first-frame `imageUrl`.
- Seedance 2.0: numeric duration 4–15; numeric resolution `480` or `720`;
  `ratio`; `prompt`, `image`, `video`, optional reference `audio`.
- Wan 3.0: string duration `5`, `10` or `15`; uppercase `480P`/`720P`/`1080P`;
  `ratio`; `prompt`, optional `image`.
- HappyHorse 1.1: numeric duration 3–15; uppercase `720P`/`1080P`;
  `ratio`; `prompt`, optional `image` or image array.

Read [api-reference.md](api-reference.md) for full limits before using references
or another model. Account discovery returns model names, not a live parameter
schema. Do not guess new flags or change models just because a schema is unfamiliar.
Use 9:16 for an explicitly vertical social clip; preserve the user's other ratios.
Explain unsupported 4K, duration or editing requirements before spending.
