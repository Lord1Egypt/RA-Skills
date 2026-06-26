# Genre: scene-animation

## Status

Reference-only

## Fit

Use this when the return wants:

- a short animated scene
- visible progression inside one location
- motion that changes the meaning of the scene
- a cinematic micro-arc rather than a pure ambient loop

This is a broad fallback genre.

If a narrower genre such as `touch-awakening`, `release-transform`, or `object-micro-cinema` fits more precisely, prefer the narrower one first.

## Core Quality

What makes this genre good is not just that something moves, but that the order of movement creates meaning.

The viewer should feel that the scene changes because of the motion, not that motion was added afterward for polish.

## Motion Strategy

- define what moves first, what follows, and what settles
- keep the action readable in a few seconds
- make sure the movement is carrying the return, not just adding polish
- prefer one readable progression over many simultaneous events
- if a reveal or bloom happens, stage it so the viewer can actually feel the before and after

## Motion Logic References

When the motion logic already exists in an H5 pattern, read the relevant card first:

- `tap-to-bloom.md`
- `rainy-night.md`
- `tension-release.md`
- `light-gamification.md`
- `inner-mirror.md`
- `gifted-data-viz.md`

Borrow the motion grammar and emotional sequence, not the interaction design.

## Prompt Strategy

- describe visible states and motion precisely rather than relying on abstract idea words
- lock the first frame before describing the scene progression
- prefer `i2v-first` when the scene layout, character treatment, or lighting setup matters to the arc
- specify duration and whether it should loop cleanly or end on a resolved final frame
- describe the initial state, the transition, and the settled or revealed state
- state what movement is emotionally central: bloom, pull, reveal, release, turn, glow shift, collapse, or environmental change
- if text appears, keep it secondary unless the whole video is fundamentally kinetic text

Strong prompts in this genre usually answer:

- what the viewer sees first
- what changes second
- what the emotional turn is
- what the final visual state should feel like

Also follow `{baseDir}/references/video-integration.md`, especially the H5-vs-video guidance and MP4 sidecar rules.

## Return Uses

- showing a small emotional arc
- giving the anchor a cinematic reveal
- making a setting feel alive enough to return a new perspective

## Reference Assets

- `assets/examples/video-examples/scene-animation/`
  Keep these lightweight local sidecars in the repo when available
- every `.mp4` example in this folder should have a sibling `.md` file with the same stem describing motion logic, progression beats, loop or non-loop behavior, and what to borrow
