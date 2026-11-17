---
name: animate-image
description: >
  Turn a still image into motion. Use when the user says "animate this photo", "make this picture
  move", "bring this illustration to life", "add motion to this image", "image to video", or wants
  a static still to become a short clip, including copying motion from another video onto your
  still. For a deliberately filmic look with lens, camera moves, and color grade, use
  cinematic-video. For a product spot, use product-ad-video. To make a face talk, use
  talking-avatar.
---

# Animate an image

Take one still image (a photo, a render, an illustration) and produce a short video where it moves. The image fixes the subject, composition, color, and lighting. Your job is to direct only what *changes over time*, not to re-describe what the image already shows.

## Inputs to collect

- **The source image.** One still that becomes the first frame of the clip. (Ask only if none provided.)
- **What should move:** the subject, the camera, atmospheric elements (rain, smoke, hair, water), or a combination.
- **For motion transfer:** a reference *video* whose motion you want applied to the still (talking-head, dance, gesture). This routes to a different model.
- **Length and aspect** if the user cares. Duration options vary per model, and output dimensions are independent from the source.
- Optional: a locked first-and-last frame (keyframes) when the shot must begin and end on specific images.

## Models

Confirm the live model and its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale AIR. The catalog moves weekly.

- **Default cinematic image-to-video: Runway Gen-4.5** (`runway:1@2`) - strong camera and subject control, reads cinematic move names directly. Gen-4 Turbo is the cheaper, faster tier for iteration.
- **Luma Ray 3.2** (`luma:ray@3.2`) - cinematic motion, first/last/intermediate keyframes, up to 1080p. Produces a **silent MP4** (no audio).
- **Seedance 2.0** (`bytedance:seedance@2.0`) - alternative image-to-video pick for high-motion shots.
- **Kling** family (`io:image-to-video`, e.g. Kling 2.5 Turbo Pro `klingai:6@1`) - another strong image-to-video option. Confirm the specific tier and its AIR via lookup.
- **Motion transfer: Pruna Video Animate** (`prunaai:p-video@animate`) - when you want another *video's* exact motion, timing, and camera move applied onto your still. The image is who, the video is what.

## Workflow

1. Resolve the model schema (`runware-run`) and confirm the input field for the source image and the allowed dimension/duration values. **This is async.**
2. Provide the still as the first frame. On Gen-4.5, Ray, and Seedance this is `inputs.frameImages` with `{ "image": ..., "frame": "first" }`. On Pruna Video Animate the still is `inputs.referenceImages` and the motion source is `inputs.referenceVideos`.
3. Run `videoInference` **asynchronously**: the task returns a `taskUUID`, then poll `getResponse` until terminal. Do not block a sync call on a minutes-long render.
4. Read the result: the finished clip is at `videoURL` (Ray's EXR sequence, when enabled, lands under `outputs.files[]`).
5. Review the motion against the source. Retry with a clearer motion prompt or a better-matched reference if it drifts or fights the image.

## Technique

- **The image is locked, the prompt directs time.** If a sentence describes something already visible in the source, delete it. Re-describing the scene gives the model nothing to do and tends toward a static loop with mild incidental motion.
- **Two channels: subject and camera.** They are independent. The subject is anything alive in the frame (breath, sway, gesture). The camera is how the frame itself moves. Direct each on purpose, and **state what holds still** ("the camera holds completely still", "no subject motion") or the model often animates both.
- **Name camera moves explicitly.** Push-in / pull-back, pan left/right, tilt up/down, dolly, orbit, crane. The explicit film term lands reliably. Vague direction gets interpreted.
- **Pace every move.** Slow / gradual / steady reads cinematic, rapid / sudden reads urgent, subtle / gentle reads as almost imperceptible drift, continuous means steady throughout. A move with no pacing word defaults to something average.
- **Layer atmospheric motion on top.** Rain, smoke, steam, mist, ripples, hair, fabric, neon flicker live in the scene itself and need no subject or camera channel. Naming each one makes the model commit rather than guess. This is often the cheapest "alive" effect.
- **Motion must have visual evidence in the source.** A head-and-shoulders portrait cannot stand up and walk away (nothing below the shoulders exists to animate). Don't add elements or actions the first frame can't support. For full-body motion, start from a wider source image.
- **Keyframes for timed shots (Ray).** Pin the same or a different image to the `first` and `last` frames and Ray interpolates between them. Intermediate frame indices choreograph beats across one clip (a 10s clip at 24fps is 240 frames, so `0`-`240`, or `-1` for last).
- **Motion transfer (Pruna Video Animate):** the largest quality lever is how well the still matches the **first frame** of the source video. Check framing, pose, and subject visibility. A head-and-shoulders still paired with a full-body dance has no body to map the choreography onto, so the motion is lost. Leave `positivePrompt` blank to transfer motion as-is, or add it to override one specific behavior (a gesture, an expression, lip-synced words). The model is style-agnostic: photoreal, cartoon, 3D, and mascots all carry through.

**Motion brief template.** Fill in the two channels for a prompt-directed clip. Leave a channel empty by stating its hold. Do not re-describe the scene: anything already in the source image does not belong here.

```
Subject motion: <what moves inside the frame, or "no subject motion">
Camera motion:  <named move + pace, or "the camera holds completely still">
Atmosphere:     <rain, smoke, steam, hair, ripples the still implies, optional>
```

Load `references/examples.md` for three worked recipes (subtle product motion, a character gesture with camera push-in, motion transfer via Pruna) with the full async request and result shape.

## Parameters that matter

- `inputs.frameImages` - exactly one image marked `first` for standard image-to-video; Ray also accepts `last` and numeric frame positions for keyframes.
- `inputs.referenceImages` + `inputs.referenceVideos` - the Pruna Video Animate motion-transfer pair (one each).
- `positivePrompt` - motion direction only (1 to 1000 chars on Gen-4.5). Optional on Pruna Video Animate.
- `width` / `height` - output dimensions, independent from the source. Match the source aspect to avoid crop/letterbox. Gen-4.5 allows `1280×720`, `720×1280`, `1104×832`, `832×1104`, `960×960`.
- `duration` - Gen-4.5: `5`, `8`, or `10` (default 10). Ray: `5` or `10`. Confirm per model, these differ.
- Ray `resolution` - `360p` / `540p` / `720p` / `1080p`. Set aspect via `resolution` **or** an explicit `width`/`height`, not both.
- Ray `settings.hdr` / `settings.loop` - HDR and loop both run at the 5s duration only and are **mutually exclusive**; `exrExport` requires `hdr`.
- Pruna `resolution` (`720p`/`1080p`), `fps` (`24`/`48`, omit to match source), `settings.preserveAudio` (default `true`).
- `seed` - fix for reproducibility. Confirm exact field names against the live schema; never guess.

## Quality bar

- The clip moves the way the prompt directed (right channel, right camera move, right pace), not a near-static loop.
- Only intended elements move. Channels meant to hold are still, because the hold was stated explicitly.
- No warping or hallucinated limbs from asking for motion the source frame can't support.
- For motion transfer, the still's identity and style are preserved and the source motion actually transferred (matched framing). Retry a mismatched pair with a re-framed still.
- For Luma Ray, the caller knows the output is silent and plans audio separately if needed.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `product-ad-video` (product still to ad clip), `multi-shot-video` (several beats in one generation), `cinematic-video` (text-to-video shot grammar).
