# Genre: live-scene-doodle

## Status

Reference-only

## Fit

Use this when the return wants:

- a real photographed or filmed scene as the emotional base
- simple hand-drawn 2D doodles, text, stars, particles, clouds, fireworks, seeds, or icons layered on top
- a strong contrast between high-fidelity reality and naive, childlike, magical motion
- one quiet real-world anchor made more alive through a small impossible event

## Core Quality

What makes this genre good is not simply adding doodles to footage.

It is good when the doodles feel emotionally and physically attached to the scene: a cup can receive rain, a flower can orbit text, a page can emit stars, a foam top can bloom into fireworks.

The best versions feel like `reality with one illustrated secret`.

## Motion Strategy

- start from one visually strong real-world anchor: cup rim, flower center, book page, window edge, tabletop, foam surface, horizon line
- add only one doodle family or one main metaphor per clip
- keep the doodle motion loop short, light, and repeatable: drift, drip, orbit, burst, float, trail, scatter
- align doodle start and end points precisely to the real object's boundary
- use empty sky, wall, table, or dark negative space as breathing room for the doodle layer
- let the real footage stay calm; the doodle should animate the scene, not fight it

## Motion Logic References

When the motion grammar overlaps with an H5 pattern, read:

- `pattern-cards/tap-to-bloom.md` for local awakening and delight
- `pattern-cards/rainy-night.md` for atmospheric observation on real surfaces
- `pattern-cards/wind-scatter.md` for floating seeds, fragments, or doodled drift
- `pattern-cards/kinetic-collage.md` for visual layering and editorial taste
- `pattern-cards/light-gamification.md` when the doodle behaves like a tiny celebratory reward effect

Borrow the metaphor logic, attachment logic, and emotional pacing.

Do not borrow literal interaction mechanics or template composition.

## Prompt Strategy

- treat this as scene-first Mode A: describe the real frame before the doodle logic
- prefer `i2v-first` when the photographed scene, camera framing, or lighting treatment matters
- describe the real scene first with camera framing, material, light, and anchor object
- then describe the doodle layer in very simple visual language: white line cloud, pastel handwritten word, small glowing star, fluorescent line fireworks
- specify exactly where the doodle is attached to the scene
- describe the loop behavior in one short readable cycle
- state the emotional contrast through visible scene-plus-doodle contrast rather than abstract mood words
- keep the doodles minimal and stylized; avoid turning them into full 3D effects or highly rendered illustrations

Strong prompts in this genre usually answer:

- what the real-world anchor is
- what impossible doodle metaphor appears around it
- where the doodle is physically attached
- what tiny repeating motion carries the return

Also follow `{baseDir}/references/video-integration.md`, especially the MP4 sidecar rules and H5-vs-video guidance.

## Return Uses

- turning a quiet real-world shot into a tiny emotional fairytale
- making one object feel more alive, lonely, celebratory, or dreamlike through a simple overlay metaphor
- returning healing, wonder, or soft melancholy without building a full narrative sequence
- using real-scene texture plus minimal doodle motion to create a strong aesthetic identity quickly

## Aesthetic Principles

- realism plus childish doodle contrast is the point
- doodles should be simple enough that their emotional meaning lands instantly
- the real footage should still be beautiful without the doodle layer
- leave breathing room; clean backgrounds help the overlay feel precious
- match doodle brightness and palette to ambient light: pure white or soft neon in darker shots, brighter colored accents in clearer brighter shots

## Suitable Emotional Register

Strong fits:

- healing
- dreamy tenderness
- quiet loneliness
- micro-celebration
- gentle wonder
- poetic smallness

Usually weaker fits:

- dense exposition
- multi-step narrative comedy
- aggressive catharsis
- scenes that need heavy world-building rather than one elegant metaphor

## Example Motif Families

- handwritten orbit words around a flower or hand
- stars, sparks, or small celestial objects flying out of a book or window
- clouds, rain, tears, or tiny weather systems attached to a drink, lamp, or object
- fireworks, glow bursts, or celebratory line blooms from foam, fruit, lights, or rooftops
- seeds, petals, birds, or particles drifting across large real landscapes

## Reference Assets

- `assets/examples/video-examples/live-scene-doodle/`
  Fetch first if missing: `bash {baseDir}/scripts/fetch-asset-bundle.sh "video-examples/live-scene-doodle"`
- every `.mp4` example in this folder should have a sibling `.md` file with the same stem describing the real anchor, doodle attachment point, loop behavior, and what to borrow
