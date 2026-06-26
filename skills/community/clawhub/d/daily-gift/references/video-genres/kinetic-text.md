# Genre: kinetic-text

## Status

Reference-only

## Fit

Use this when the return wants:

- text itself to be the moving subject
- motion-graphics-like language instead of a physical scene
- readable words or glyph fragments to carry the emotional turn
- release, flow, lift, dissolve, reveal, or drift to happen through text motion

## Core Quality

What makes this genre good is not just that text moves.

It is good when the movement grammar itself expresses the return: release, continuation, accumulation, disturbance, disappearance, or reformation.

## Motion Strategy

- keep the clip short enough that the motion arc stays legible, often `4` to `8` seconds
- make the first frame compositionally strong before anything moves
- choose one dominant motion logic: scatter, flow, lift, reveal, dissolve, or erosion
- make text movement readable enough to feel intentional, even when full paragraph reading is not the point
- if the clip loops, ensure the end state can reconnect gracefully to the beginning

## Motion Logic References

When the motion matches an existing H5 pattern, read that pattern card for motion grammar and pacing:

- text scattering outward -> `pattern-cards/wind-scatter.md`
- text flowing like a current -> `pattern-cards/text-river.md`
- elements lifting away -> `pattern-cards/lift-away.md`
- surface burning or clearing to reveal a lower layer -> `pattern-cards/burn-reveal.md`
- wet or disturbed text surfaces -> `pattern-cards/wet-letter.md`
- fragile distressed text motion -> `pattern-cards/tear-stained-paper.md`

Borrow the motion logic, timing, direction, rhythm, and emotional arc of the movement.

Do not borrow the code or interaction design.

Video does not need interaction. The motion itself is the experience.

## Prompt Strategy

- treat this as Mode B by default: lock a strong first frame, then describe only the motion
- strongly prefer `i2v-first` so the text block, background texture, and composition are anchored before animation begins
- specify duration clearly
- describe the exact text form, size, position, color, and background in frame `0`
- describe exactly when and how the motion begins
- describe what happens in the middle beat
- describe what remains, dissolves, or resolves at the end
- keep the background and non-text elements restrained unless they truly support the motion

Strong prompts in this genre usually answer:

- what text or text-like form appears first
- what motion logic transforms it
- what the motion means emotionally
- what the final visual state should feel like

Also follow `{baseDir}/references/video-integration.md`, especially the prompt strategy and MP4 sidecar rules.

## Return Uses

- turning one line into a cinematic release
- making thought, memory, or language itself become the moving gift
- translating strong H5 text motion ideas into a watch-first format
- returning a line of language through pacing and motion rather than interaction

## Reference Assets

- `assets/examples/video-examples/kinetic-text/`
  Keep these lightweight local sidecars in the repo when available
- every `.mp4` example in this folder should have a sibling `.md` file with the same stem describing timing, motion grammar, pacing, loop behavior, and what to borrow
