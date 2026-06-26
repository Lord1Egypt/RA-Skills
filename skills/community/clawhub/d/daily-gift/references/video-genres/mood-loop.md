# Genre: mood-loop

## Status

Reference-only

## Fit

Use this when the return wants:

- a short atmospheric loop
- subtle repetition with emotional weight
- motion such as wind, rain, glow, drifting dust, or breathing light
- a scene the user should linger inside rather than decode like a story

This is a broad fallback genre.

If a narrower genre such as `atmospheric-surface` or `object-micro-cinema` fits more precisely, prefer the narrower one first.

## Core Quality

What makes this genre good is not event density but atmospheric persistence.

The loop should feel intentional enough that the user wants to stay with it, not merely notice that it repeats.

## Motion Strategy

- keep the clip short and loop-friendly
- let one or two motions carry the feeling
- prefer mood evolution over narrative complexity
- make the loop seam hard to notice
- choose motions that can sustain emotional pressure through repetition: drifting curtain, rain on glass, breathing neon, slowly moving foliage, ash, glow, dust, water shimmer

## Motion Logic References

When the movement grammar overlaps with an H5 pattern, read that pattern card for emotional pacing and directional logic:

- `rainy-night.md`
- `wet-letter.md`
- `tear-stained-paper.md`
- `kinetic-collage.md`
- `memory-shelf.md`
- `extension.md`

Borrow the motion logic, not the interaction.

## Prompt Strategy

- describe the loop length clearly, usually `4` to `8` seconds
- lock the first frame first so the loop already feels complete before anything moves
- strongly prefer `i2v-first` when palette, texture, weather, or light behavior are central to the loop
- state what motion exists at the beginning so the first frame is not empty
- specify what tiny change happens over time and how the loop closes
- describe texture and light behavior, not just scene objects
- if using a symbol, make it emerge naturally from the atmosphere rather than as a pasted metaphor
- avoid overplotting; one breathing motion and one supporting motion are usually enough

Strong prompts in this genre usually answer:

- what the viewer is looking at
- what one or two motions keep the scene alive
- how the light, weather, or particles behave
- what emotional aftertaste the loop should leave

Also follow `{baseDir}/references/video-integration.md`, especially the genre bridge and MP4 sidecar rules.

## Return Uses

- returning a feeling that needs time rather than explanation
- giving the user a place to linger inside the mood
- turning atmosphere itself into the gift

## Reference Assets

- `assets/examples/video-examples/mood-loop/`
  Keep these lightweight local sidecars in the repo when available
- every `.mp4` example in this folder should have a sibling `.md` file with the same stem describing motion logic, pacing, loop behavior, and what to borrow
