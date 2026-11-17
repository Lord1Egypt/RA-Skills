---
name: add-audio-to-video
description: >
  Add sound to a silent video - sound effects, narration, or a music bed. Use
  when the user says "this clip has no audio", "add sound effects to my video",
  "make it sound like footsteps / rain / an explosion", "give this a soundtrack",
  or "voice over this clip". Routes sound design to a dedicated SFX model and
  defers narration and music to their own skills.
---

# Add audio to a silent video

Take a silent clip and give it sound. Three different jobs hide behind that ask: synchronized **sound effects** (footsteps, rain, impacts that line up with the action), spoken **narration**, or a **music bed**. Each routes to a different model, and only one of them is a dedicated SFX model. This skill covers the SFX route directly and hands the other two to their sibling skills.

## Inputs to collect

- **The silent video** (URL or UUID). For SFX, max **10 seconds** per call.
- **What kind of audio**: sound effects synced to the action, narration/voiceover, or background music. This decides the route.
- For SFX: an optional **prompt** describing the sound to bias toward (e.g. "heavy rain on metal, distant thunder"). Leave it off to let the model read the video and design sound from what it sees.
- Whether the result must be the **video with sound muxed in** (SFX route returns this) or a standalone audio file to mix yourself.

## Models

- **Sound effects → Mirelo SFX 1.5** (`mirelo:1@1`) - the one dedicated SFX model. Feed it a video and it returns the **same video with synchronized sound effects** muxed in. Honest caveat: dedicated SFX coverage is thin (this single model), so set expectations and consider the native-audio route below.
- **Narration / spoken voiceover →** use the **`voiceover`** skill (text-to-speech). Not this model.
- **Music bed →** use the **`music`** skill (text-to-music). Not this model.
- **Often the better route: native audio at generation time.** Several video models emit incidental sound (ambient, foley, even speech) as part of the original generation. If you still control the generation step, turning that on usually beats bolting SFX on afterward. Check capabilities and the audio flag via `runware-models` + `runware-run` before regenerating.

Confirm the live model and its schema via `runware-models` + `runware-run` before calling - never hardcode a stale choice.

## Workflow

1. **Classify the ask** (SFX vs narration vs music) and route. For narration go to `voiceover`, for music go to `music`. The rest of this is the SFX route.
2. **Resolve the schema** (`runware-run`) and confirm the input field (`inputs.video`) and the output-format rule.
3. **Upload the silent clip** to `inputs.video` (URL or UUID). Keep it under **10 seconds**.
4. **Run `audioInference` asynchronously** and poll until terminal - audio/video tasks are time-based, do not block a sync call on them.
5. **Read the result** and review the sound against the picture (see Quality bar). Retry with a sharper prompt or a different `seed` if the sync or the sound choice is off.

## Technique

- **Two modes, pick one - they are mutually exclusive.** Supply **either** `inputs.video` (synced SFX over your clip, output is video) **or** `positivePrompt` alone (text-to-audio, output is a bare audio file). For adding sound to an existing video you want the video-input mode.
- **Let the picture drive the sound.** With a video in, the model watches the action and places effects on it. A prompt is optional and acts as a bias ("rain, thunder, no music"), not a full script. Over-describing fights what the model already sees.
- **Duration follows the video.** In video-input mode the result matches the clip length, so `duration` does not apply (the schema rejects it there). `duration` only exists for the prompt-only audio mode (1-10s).
- **Align a longer source with `settings.startOffset`.** If your clip's interesting moment starts late, set the offset (in seconds) to begin sound design from that point in the video.
- **Coverage is genuinely thin.** One SFX model means limited stylistic range. When the result is weak, the stronger fix is often upstream: regenerate the video on a model that produces **native audio**, rather than expecting deep SFX variety here.

## Parameters that matter

- `inputs.video` - the silent clip (URL/UUID), **max 10s**. Its presence forces video output (`MP4`/`MOV`/`WEBM`) and disables `duration`.
- `positivePrompt` - 2-3000 chars; optional in video mode (a sound bias), required in prompt-only mode.
- `duration` - 1-10s, default 10. **Prompt-only mode only**; not valid alongside a video input.
- `settings.startOffset` - 0-10s; where in the video sound design begins. Requires a video input.
- `outputFormat` - video (`MP4`/`MOV`/`WEBM`) with a video input, audio (`MP3`/`WAV`/`FLAC`/`OGG`) without one.
- `steps` (5-30, default 25), `seed` - quality/repeatability knobs. Confirm exact names against the live schema (`runware-run`); never guess.

## Quality bar

- Effects **land on the action** - footfalls hit feet down, impacts hit contact, no audible drift across the clip.
- The sound matches the scene (right material, right space) and the prompt bias if one was given.
- The returned file is the **video with audio**, playable, length unchanged from the source.
- If sync or sound choice is wrong, retry with a tighter prompt or new `seed`; if range is the limit, route to native-audio regeneration instead.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `voiceover` (spoken narration / TTS), `music` (background music bed), and the video-generation skills when native audio at generation time is the better route.
