# Prompt, Canvas, and Character Consistency

## Canvas contract

Lock these before shot design:

| Item | Default for vertical AI drama |
|---|---|
| aspect ratio | `9:16` |
| delivery resolution | `1080×1920` |
| test resolution | `720p` |
| frame rate | `24 fps` |
| episode duration | 90–120 seconds |
| shots per episode | 12–18 |
| subtitle safe area | keep faces/actions out of bottom 10–12% |
| title safe area | top 8–10% |
| text policy | all final text in post |
| dialogue policy | clean video plus separate voice track |

## Character bible fields

For every principal character record:

- character ID and display name;
- face shape, eyes, ears, hair/forehead mark, silhouette, body ratio;
- hand/foot structure, tail/accessory shape, material, palette;
- outfit IDs, prop IDs, expression range, scale chart;
- front/side/back/expression references;
- voice ID, pitch, pace, accent, catchphrase;
- forbidden changes.

Consistency is not one prompt. It is reference assets + written anchor + per-shot QC + rework rules.

## Reference hierarchy

- one primary full-body reference for silhouette, costume, and scale;
- one face close-up for eyes, muzzle, ears, forehead mark;
- optional expression, side, back, and prop references;
- one scene key art per recurring location;
- one prop sheet per recurring story object.

Do not mix references with different body proportions or costume versions in one shot.

## Prompt formula

`character anchor + scene + first-frame composition + action sequence + camera movement + lighting/color + emotion + end state + technical constraints`

For a multi-shot generation, specify ordered beats in 4–8 second phrases. Do not overpack more than 4 major actions into a 30-second task.

## Prompt hierarchy

Build each prompt in this order:

1. identity anchor and outfit/prop IDs;
2. scene, time, weather, and geography;
3. first-frame composition and subject placement;
4. playable action in cause-and-effect order;
5. camera intention;
6. lighting, palette, texture, and lens;
7. emotion and performance beat;
8. VFX or environmental motion;
9. continuity constraints;
10. end state;
11. technical format.

Do not mix a new action with an unexplained cut, a new costume, and a new camera axis in the same 5-second beat.

## Multi-shot generation blocks

For a 15–30 second task:

- give each internal shot a clear purpose;
- state the order and approximate duration;
- keep the same character/scene IDs;
- preserve prop hand, eyeline, screen direction, and light direction;
- specify the transition: cut on action, match cut, whip pan, sound bridge, or hard cut;
- define the final frame needed for the next task.

If the model cannot hold multiple shot boundaries, split the block into single-shot tasks rather than accepting a drifting montage.

## Coverage prompt checklist

Every shot prompt should answer:

- whose POV or story function is this?
- what changes in the shot?
- what is the dominant action?
- what is the camera doing and why?
- where is the subject in frame?
- where did the subject come from and where are they going?
- which hand holds the prop?
- which direction is the light coming from?
- what must remain identical to the neighboring shot?

## Camera error negatives

Add only when observed:

`unmotivated camera, camera through wall, axis jump, reversed screen direction, eyeline mismatch, teleporting subject, floating feet, prop switching hands, background morphing, crowd duplication, light direction flip, sudden lens change`

## Keyframe and endpoint discipline

- Generate or select a keyframe for complex staging.
- Record the intended start state and end state.
- Use the last frame of the prior task when continuous motion matters.
- For dialogue coverage, keyframe the listening reaction as well as the speaker.
- For action, keyframe the moment before impact, the impact, and the reaction.

## Seedance 2.5 parameters

- model: `doubao-seedance-2-5-260628`
- create task: `POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks`
- duration: 4–30 seconds
- ratio: `9:16`, `16:9`, `1:1`, `3:4`, `4:3`, `21:9`, `adaptive`
- resolution: `480p`, `720p`, `1080p`
- audio: `generate_audio: true` for test ambience; `false` for dialogue-first production
- watermark: keep `false` for clean edit; add company watermark in post
- continuity: `return_last_frame: true` or explicit first/last-frame conditioning
- reference image payload: public URL, asset ID, or Base64 data URI; never a local filesystem path
- text rendering: do not ask the model to render final Chinese text

## Cross-shot continuity methods

1. Generate a clean keyframe per shot with the same character references.
2. Use image-to-video first-frame conditioning where exact staging matters.
3. Use the previous shot's returned last frame as the next first frame for continuous action.
4. Keep outfit IDs and scene IDs explicit in the shot manifest.
5. Review face, ears, tail, hands, costume, and scale before accepting a take.
6. If three takes fail the same invariant, revise the reference or prompt rather than continuing blind retries.

## Negative prompt baseline

`different character, redesigned face, changed ears, changed tail, changed body ratio, wrong outfit, extra fingers, extra limbs, deformed hands, morphing, flicker, melting, plastic skin, text, captions, watermark, logo, gibberish writing, horizontal frame, low resolution`

Add project-specific negatives only when they address a repeated observed failure.

## Text-in-post rules

- Signs, phone UI, contracts, newspapers, labels, captions, and legal notices are vector overlays.
- Generate blank surfaces and abstract glyphs in video.
- Use one modern sans font and one period serif font per project.
- Keep subtitles to 1–2 lines and 10–18 Chinese characters per line.
- Keep all final text inside platform-safe areas.
