# Asset consistency rules

## Core rule

For character-driven comic drama, consistency comes from the asset chain, not from text prompting alone.

Use this order:

1. Character turnarounds
2. Keyframes based on turnaround URLs
3. Image-to-video based on keyframe URLs

## URL handoff rule

Use **public URLs** when passing assets between API-driven steps.

Apply this rule to:
- turnaround generation output → keyframe generation input
- keyframe generation output → video generation input

Do not rely on local file paths for these handoffs.

## Character turnarounds

Generate before any shot work.

Minimum set:
- protagonist(s)
- recurring antagonist(s)
- recurring support characters
- recurring non-human entities with recognizable forms

Treat the final turnaround set as the canonical source of identity.

## Keyframes

- Generate at least one keyframe per shot.
- Use all relevant character turnaround URLs as references.
- Keep keyframes strongly composed and readable.
- Prefer clean staging over overly dynamic layouts.
- Lock costume, palette, prop placement, and emotional framing whenever possible.

## Video generation

For `sora-2-generate`:
- prefer `imageToVideo`
- use the keyframe URL as the shot anchor
- default to 15-second single-shot clips unless production constraints require another supported duration
- keep the prompt focused on motion, mood, and camera evolution
- do not rewrite character identity in ways that contradict the keyframe

## If results drift

Fix in this order:
1. turnaround quality
2. keyframe quality
3. video prompt motion language

Do not skip directly to regenerating many videos without checking the upstream asset chain.
