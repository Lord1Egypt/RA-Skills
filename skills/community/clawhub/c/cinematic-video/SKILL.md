---
name: cinematic-video
description: >
  Make video that looks shot, not generated, with deliberate framing, lens, camera motion,
  lighting, and color grade. Use when the user says "cinematic clip", "make it feel filmic", "a
  slow push-in on the subject", "golden-hour establishing shot", "dolly zoom", "give it a film
  look", or wants directed shot language rather than a generic moving image. For plain motion from
  a still with no shot direction, use animate-image. For several cuts in one clip, use
  multi-shot-video.
---

# Cinematic video

Produce a short video with intentional shot language: a chosen framing and lens, a named camera move, lighting, location, and a color grade. The lever is a compact cinematic prompt that names the director's decisions in camera vocabulary the model reads directly, not a wall of adjectives.

## Inputs to collect

- **The shot brief.** What is in frame and what it should feel like. (Infer from the request when stated.)
- **Text-to-video or image-to-video.** If the user has a still that fixes the look, that is image-to-video and the prompt directs motion only. If not, it is text-to-video and the prompt builds the whole frame.
- **Aspect and length.** Landscape (16:9) or vertical (9:16), and roughly how long. Drives dimension pair and `duration`.
- Optional: a reference for a locked character or brand look, an explicit grade or era ("1950s", "teal-and-orange").

## Models

Confirm the live model and its schema via `runware-models` + `runware-run` before calling. Never hardcode a stale choice. All three below carry `io:text-to-video` and `io:image-to-video`.

- **Text-to-video with native audio: Google Veo 3.1** (`google:3@2`). Reads the five-element scaffold and camera vocabulary directly, fills scene detail from world knowledge, and generates synchronized audio natively. Best when the shot needs sound (ambience, foley) baked into the clip.
- **Premium text-or-image-to-video: Luma Ray 3.2** (`luma:ray@3.2`). Strong cinematic motion and grade. Supports HDR output on 5-second clips.
- **Image-to-video, locked look: Runway Gen-4.5** (`runway:1@2`). The source still fixes subject, composition, palette, and lighting, the prompt directs only the motion. Gen-4 Turbo is the cheaper draft tier in the same family.

## Workflow

This is a time-based task: run **async and poll**, never block a sync call on a minutes-long job.

1. Resolve the model + schema via `runware-run`. Confirm the allowed dimension pairs, the `duration` set, and whether it takes `inputs.frameImages` (image-to-video) or `inputs.referenceImages`.
2. For image-to-video, upload the source still and pass it under `inputs.frameImages` (Gen-4.5 takes exactly one, marked the `first` frame).
3. Write the prompt with the compact cinematic scaffold (below). Lead with the camera phrase.
4. Run `videoInference` asynchronously and poll `getResponse` until terminal.
5. Read `videoURL` from the result. Review against the quality bar, retry the shot if the move or grade missed.

## Technique

Lean on `runware-prompting` for phrasing. The craft for cinematic video:

- **Use the compact cinematic scaffold:** framing and camera motion, style, lighting, location, action. Three or four sentences naming each element beat a wall of adjectives. Drop an element when it does not matter for the shot (a flat-lit dialogue close-up needs no lighting clause). The scaffold is a checklist, not a template.
- **Lead with the camera phrase.** These models treat the first words as the load-bearing instruction for how to film it. "A dramatic dolly zoom centred on the vendor" at the open is parsed as a directive. The same phrase buried in sentence three reads as scene flavor.
- **Speak camera vocabulary, not synonyms.** The models read industry terms directly: push-in, pull-back, pan, tilt, dolly, crane, orbit, oner (one continuous shot), dolly zoom, rack focus, natural smartphone zoom. "Dolly zoom" beats "the camera moves in a strange way". "Golden-hour backlit" beats "warm yellow light from behind".
- **Pace the move.** Slow / gradual / steady reads deliberate and weighty. Rapid / sudden / dramatic reads urgent. A move without a pace word defaults to something average. Pacing is the second dial after the move name.
- **Trust world knowledge on text-to-video.** "Saturday morning at a 1950s diner" already implies chrome, vinyl booths, warm sunlight. Do not spend tokens spelling out the obvious read. The biggest quality lever is what you remove, not what you add.
- **For image-to-video, direct motion, not the scene.** The still already fixes the frame, so re-describing it gives the model nothing to do. Name what moves in two channels, the subject and the camera, and they are independent. State what holds still ("the camera holds completely still", "no subject motion") or the model animates both. Layer atmospheric motion on top (rain, smoke, steam, mist, neon flicker) for cheap perceived production value.
- **Bound motion to visual evidence.** A head-and-shoulders portrait cannot stand up and walk off, nothing below the shoulders exists to animate. When motion needs off-frame parts, start from a wider source still.

Fill in this scaffold, then write it out as three or four sentences. Lead with framing and camera motion. Drop any line that does not matter for the shot. Three or four sentences naming each element beat a wall of adjectives.

```
Framing + camera motion: [wide establishing / tight close-up] + [slow push-in / pan right / rack focus / dolly zoom / oner]
Style:                    [cinematic photorealism / shallow depth of field / 1970s film grain]
Lighting:                 [golden-hour backlit / cool window fill / single warm practical]
Location:                 [where, in a few words that carry the décor by world knowledge]
Action:                   [the one small thing the subject does, bounded by what is in frame]
```

Load `references/examples.md` for worked establishing, product, and character recipes with real requests and result shapes.

## Parameters that matter

- `positivePrompt` carries the whole shot. Required, kept to three or four sentences.
- `inputs.frameImages` for image-to-video (Gen-4.5: exactly one, `frame: "first"`). `inputs.referenceImages` to lock a character or brand look where the model supports it.
- `duration` is per-model: Veo 3.1 takes 4, 6, or 8 for text-to-video (default 4), Luma Ray 3.2 takes 5 or 10 only, Gen-4.5 takes 5, 8, or 10. Confirm against the live schema.
- `width` / `height` must be one of the model's allowed pairs (commonly `1280 × 720` landscape or `720 × 1280` vertical, Gen-4.5 adds `1104 × 832`, `832 × 1104`, `960 × 960`). Output dimensions are independent of the source still, so pick the pair that matches its aspect.
- `seed` for reproducible output across retries.
- Confirm exact field names against the live schema (`runware-run`). Never guess a parameter.

## Quality bar

- The named camera move actually happens at the pace asked, and only the channels intended (subject vs camera) moved.
- Framing, lighting, and grade read as a deliberate cinematographic choice, not a generic moving image.
- For image-to-video, the source look held, the model directed motion rather than inventing a new scene.
- Aspect and duration match the target use. Retry any shot where the move missed or the grade drifted.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `animate-image` (image-to-video from a still), `multi-shot-video` (several beats in one clip).
