---
name: edit-video
description: >
  Restyle or relight an existing video, changing the whole frame's look while the motion carries.
  Use when the user says "restyle this clip", "make this footage look like winter", "turn this
  into a cartoon", "relight this scene", "give the whole video a new look", or "edit this video
  without redoing it". This is a global look change across the frame. To swap one specific element
  such as an actor, a product, or a garment while everything else stays put, use replace-in-video.
  For aspect ratio, use reframe-video. For resolution, use video-upscale. For sound, use
  add-audio-to-video.
---

# Edit video

Take a clip the user already has and change it, without regenerating from scratch. There are two distinct jobs, and picking the wrong one wastes a run: a **whole-frame transform** that reimagines the entire shot in a new look while the original motion and timing carry through, or a **surgical edit** that changes one named region and holds the rest of the clip pixel-stable. This is video-to-video, so every run is async.

## Inputs to collect

- **The source clip.** A public URL or the UUID of a previous generation. (Ask only if none provided.)
- **What change** the user wants, and how far it should travel: a full restyle of the whole frame, or one specific localized edit (a color, a region, an environment, a wardrobe piece).
- **What must stay the same.** For a surgical edit this is load-bearing: the framing, the cuts, the lighting, the subject, the parts not being touched.
- Optional: a restyled or edited reference frame to pin the exact target look (anchoring).

## Models

- **Whole-frame transform / restyle: Luma Ray 3.2** (`luma:ray@3.2`). Pass `inputs.video` + a prompt describing the target look, and the model re-renders the entire frame guided by the source. The original motion carries through, but faces and backgrounds are reimagined along with the style, not held. Use it for bold restyles where the performance is the throughline and the new look is the point.
- **Surgical / localized edit: Runway Aleph 2.0** (`runway:aleph@2.0`). Pass `inputs.video` + a `positivePrompt` naming one change. It returns the same clip with that change applied and everything else preserved: framing, cuts, lighting math, the regions you did not name. Use it for a paint color, an environment swap, a wardrobe change, or a grade.
- Confirm both are `live` and inspect each schema via `runware-models` + `runware-run` before calling. Never hardcode a stale choice.

**Pick correctly, this is the whole skill.** Ask one question: should the whole frame be reimagined, or should only one named thing change while the rest stays identical? "Make this clip look like an anime" is a transform (Luma). "Change the red car to blue" is surgical (Aleph). When the source frame and the result differ everywhere, that is Luma. When they differ only inside one region, that is Aleph. To swap a specific character or object for a different one, that is its own job, see `replace-in-video`.

Route with: `Change <what> while keeping <what stays>.` A long "keeping" list against a small change is surgical (Aleph). A short or empty "keeping" list because the look should travel everywhere is a transform (Luma).

## Workflow

1. Resolve the chosen model's schema (`runware-run`) and confirm the input field names before calling.
2. Provide the source as `inputs.video` (URL or prior-generation UUID). For Aleph, plan around the 2 to 30 second, up-to-1080p source limits.
3. Run `taskType: videoInference` **asynchronously**: the task returns a `taskUUID`, then poll `getResponse` until terminal. Do not block a sync call on a minutes-long edit.
4. Read the result from `videoURL`.
5. Review against the quality bar below and retry with a tuned `strength` (Luma) or a tighter preserve-clause (Aleph) if it drifts.

See `references/examples.md` for worked async requests: a whole-frame Luma restyle and a surgical Aleph edit, by prompt and by anchor.

## Technique

- **Transform (Luma Ray 3.2): describe the look, let the motion carry.** Name the target style and trust the source for motion and composition. Do not expect faces or backgrounds to stay untouched, the model rebuilds the whole frame. `settings.edit.strength` is the preserve-versus-reinterpret dial across three bands (`adhere` close to source, `flex` moderate liberties, `reimagine` loose guidance), each with three levels. Start low. For people, the `face` control biases toward a recognizable face, though a heavy transform still reinterprets it. `settings.edit.autoControls: true` derives the conditioning from the source on the first pass and cannot be combined with `strength` or manual `controls`. Editing keeps the source aspect ratio, so changing format is a separate reframe step.
- **Surgical (Aleph 2.0): name only what changes.** The clip already holds the framing, cuts, lighting, subject, and motion. Describing any of those tells the model they are fair game and the part you wanted preserved drifts. Lead with a transformation verb the model honors cleanly (*change*, *replace*, *swap*, *add*, *remove*, *restyle*, *relight*), name the target attribute, then **end with a short clause pinning the rest in place** ("keep the chrome, the road, and the lighting exactly as in the source"). That closing clause is what stops a color change from also rebuilding the road. Art-direction phrasing beats caption phrasing.
- **Anchor when words are not enough.** Both models accept `inputs.frameImages`: a reference frame pinned to a position in the clip via `frame` (a name like `first`/`last` or a zero-based index) or, on Aleph, a `timestamp`. Pull a still from the source, edit it externally to the exact target look while keeping the source framing, then send it back. The model treats the anchor as the target appearance at that moment and carries it through. This is the way to lock a brand identity, exact typography, or a custom pattern that a prompt only approximates.
- **Aleph carries one edit across cuts.** A multi-shot source reel gets a single edit propagated through every cut, as long as the subject reads as continuous. Sharp identity jumps between shots can break propagation, edit those as separate clips.

## Parameters that matter

- `inputs.video` - the source, a URL or a prior-generation UUID. Aleph requires **2 to 30 seconds at up to 1080p**, output preserves the input aspect ratio.
- `settings.edit.strength` (Luma) - bands `adhere_1` … `reimagine_3`. Lower preserves shape and motion, higher reworks the subject. Start in `adhere`/`flex`.
- `settings.edit.controls` / `autoControls` (Luma) - per-signal conditioning (`poseStrength`, `depthBlur`, `face`, …), or let `autoControls` derive it. `autoControls` excludes `strength` and manual `controls`.
- `positivePrompt` (Aleph) - required, capped at 1000 characters. Name one change, then pin the rest.
- `inputs.frameImages` (both) - up to 5 anchors on Aleph; pin with `frame` or `timestamp`. Match the anchor's framing to its pinned moment.
- Confirm exact field names against the live schema (`runware-run`); never guess.

## Quality bar

- The right tool was chosen: a whole-frame restyle went to Luma, a one-region change went to Aleph. A surgical request that rebuilt the unnamed parts of the frame is a wrong-model failure, not a prompt tweak.
- For a surgical edit, only the named region changed. Framing, cuts, lighting, and untouched elements are pixel-stable against the source.
- For a transform, the original motion and timing carry through and the new look is coherent across the clip, not flickering frame to frame.
- The job was run async and read from `videoURL`, not blocked on a sync call. Retry drift with a tuned `strength` or a tighter preserve-clause before returning.

## Related skills

`runware-run`, `runware-models`, `runware-prompting`; `replace-in-video` (swap a specific character or object for a different one), `reframe-video` (change the clip's aspect ratio or format).
