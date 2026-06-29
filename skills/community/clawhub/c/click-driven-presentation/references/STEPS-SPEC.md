# Steps Spec — the single source of truth

A presentation is a list of **scenes**; each scene is a list of **steps**.
One step = one beat = one focused idea the speaker lands with one click.
The `steps` data for a scene is the single source of truth: the engine, the on-screen beats, and any later narration all read from it.

## What a step is

Slice the narration script into steps by this test: **would the speaker pause here before saying the next thing?**
If yes, it is a step boundary.

- A claim and its evidence are usually two steps.
- A list of N items is **N steps**, never one — reveal them one at a time.
- A transition with nothing spoken is still a step if the screen changes; give it an empty narration string.

## The `steps` array

Each scene module exports a `steps` array. Each entry describes one step:

```ts
export const steps = [
  { say: "The first line the speaker says here.", show: "hero claim, large" },
  { say: "The second beat.",                       show: "reveal data point 1" },
  { say: "",                                       show: "diagram completes (no narration)" },
];
```

Field rules:

- `say` — the narration text for this step, kept semantically faithful to the script (you may adjust punctuation for natural speech, but never drop a key phrase, number, or quote). Use `""` for a silent beat.
- `show` — a short note on what the screen does this step (on-screen intent). This guides the scene's visual; it is not rendered verbatim.
- The array order is the click order.

## The anti-drift rule (do not break this)

The largest step index the scene's code uses (`if (step === N)` / `step >= N`) **must equal `steps.length - 1`**.

- More code steps than array entries → the speaker runs out of script before the visuals finish.
- More array entries than code steps → a beat the speaker says has nothing on screen.

Check this in the completion self-check for every scene.
This holds even though this skill synthesizes no audio — it keeps the spoken script and the on-screen beats aligned, and it is exactly what a downstream audio/render pipeline would consume if the user later adds narration.

## Naming

- Scene folders: `NN-id` (`01-hook`, `02-problem`, …), two-digit ordinal + short kebab id.
- The ordinal is the deck order; the id is a stable handle that travels through the build.

## On-screen text ≠ the whole script

`show` is a curated subset of what is spoken.
The screen carries the 1–3 things worth enlarging this beat (a hero line, a number, a comparison) plus the visual that demonstrates the idea.
Do not type the full narration onto the screen — that is a slide, not a video.
Pull extra on-screen detail (specific numbers, quotes, cases) from the source article when one was provided (see the dual-source rule in `SCENE-CRAFT.md`).
