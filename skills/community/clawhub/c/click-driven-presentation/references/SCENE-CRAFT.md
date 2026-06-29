# Scene Craft — read before building each scene

This is a video-like webpage, not slides.
A scene is right when a viewer feels they are watching something happen, not reading a deck.
Build every scene against the rules below, then run the completion self-check.

## This is a video, not slides

Plain tests for every step:

- **Not slides** — no header, footer, page number, or brand bar; the key visual dominates the frame.
- **Comfortable to watch** — large type, generous whitespace, restful color; no walls of small text.
- **Visually alive** — the screen demonstrates the idea; it does not just stack text, and it does not dump everything at once.

## Every scene must draw something

> This is the floor. Every scene needs at least one moving / drawn demonstration — CSS, SVG, Canvas, or JS. **A text-only scene fails review.**

The strongest "video feel" comes from the viewer *seeing* the explained thing happen:

- a number counting up, a bar growing, ranks swapping;
- flow nodes lighting in sequence, a connector drawing itself;
- a comparison split open, a spotlight sweeping, a shape morphing;
- a simulated terminal, chat window, or file tree.

Combine them however the content wants — but every scene must demonstrate, never narrate only.

## Reveal step by step — never all at once

The page is driven by a **global step counter**; a click (or arrow/space) advances one step. The scene is a pure function of `step`.

> When the narration lists items ("first X, then Y, then Z"), **never** stagger X / Y / Z onto one step.

Do this instead:

- one item = one step;
- X lights up alone on its step;
- on Y's step, X dims to context and Y lights up;
- on Z's step, X / Y are dimmed and Z lights up.

Test: will the speaker say them one at a time? If yes, reveal them one at a time.

## Keep the essential 1–3 things per step

Video is sound + picture: speech carries the line, the picture enlarges the beat.
Each step puts only the 1–3 things worth enlarging on screen — a hero line, a number, a comparison — plus the demonstration.
Do not move the whole paragraph onto the screen.

## Dual-source rule

> **Rhythm and order** follow the **script** — the beat order must not be shuffled.
> **On-screen detail** (numbers, quotes, cases) comes from the **source article** when one was given.

When the user provided a source article alongside the script, go back to it for the on-screen detail — it holds more specifics than the spoken line.
Let the screen's information density exceed the narration's.
If you only ever use the spoken line, the screen is just the script retyped — that is a slide.

## Aesthetics: type, color, motion, whitespace

Viewers sit back and their attention floats, so:

- **Type large** — hero text reads from across a room.
- **Whitespace generous** — keep a wide safe margin on all four sides; do not fill the frame.
- **Color restful** — pull colors and font families from theme tokens (so a theme swap never breaks the scene); sizes, spacing, and timing are free per scene.
- **Motion clean** — entrances land crisply and settle without stealing focus; impact comes from *design ideas* (content-driven demonstration), not from speed or flashing.

## Content-driven animation, not entrance animation

Find the idea's *inherent motion* first (a value rising, a path completing, a split opening). Only fall back to a generic entrance when there is genuinely no inherent motion.
Do not give every step the same entrance, and do not run perpetual micro-motion (endless pulsing/floating) on everything.

## Avoid the AI-generated look

These visual fingerprints all read as machine-made — avoid all of them:

- purple/pink or blue-violet diagonal gradient backgrounds;
- rounded cards with a colored left border;
- gradient buttons and big rounded pills;
- emoji used as icons;
- fake data, fake logos, fake "N users" numbers;
- the same entrance animation on every step of the scene;
- ken-burns / glow-breathing / constant flicker on every shot;
- a mono tag or index number stuck in a corner of every frame.

When an asset is missing, **admit it**: use a placeholder card (a box labeled with the description at the real aspect ratio). Never pad with emoji, unrelated stock, or invented numbers. An honest placeholder beats a fake every time.

## Code red-lines

The scaffold already provides the fixed 16:9 stage, the global step counter, the hidden progress bar, and token theming — understand them, do not rewrite them. Then:

### Must use tokens (so a theme swap never breaks)

- **Colors** via CSS variables (`--shell` / `--surface` / `--text` / `--text-2` / `--accent` / `--rule`, …) — no hardcoded hex / rgb / color names.
- **Font families** via variables (`--font-display` / `--font-body` / `--font-mono`) — no hardcoded font names.
- Theme personality comes through the primitive classes (`.hero-num`, `.card`, `.rule`, `.stage-frame`) — do not redefine them in scene CSS.

### Free per scene (this is where scenes design themselves)

- font sizes, spacing/padding/margin, gaps, grid sizes — write concrete values for the composition;
- animation durations, easings, keyframes — write to the motion's intent.

### Other engineering red-lines

- Drive animation with CSS keyframes, **not** `setTimeout` / `setInterval`.
- An interactive element inside a scene (a button, a custom control) must carry `data-no-advance`, or clicking it will advance the stage step.
- Physically isolate scenes: each scene gets its own folder and its own CSS class prefix (`.hk-`, `.pr-`, …); never import across scenes; never edit shared files beyond the scene's own registry entry.
- Every scene must have a `steps` array (see `STEPS-SPEC.md`); its length must equal the max step the code uses, plus one.

## Completion self-check (run after every scene)

> Mandatory: after building a scene and clicking through it once, verify each item, fix what fails, **then** report. Reporting "done" without fixing a failed item is not allowed.

- [ ] At least one CSS / SVG / Canvas / JS demonstration — none means go back.
- [ ] Different steps have different dominant motion — one animation for the whole scene means go back.
- [ ] Large type, generous whitespace, restful color; no small-type text walls.
- [ ] Lists revealed one item per step (1 item = 1 step).
- [ ] On-screen detail richer than the spoken line (pulled from the source when given).
- [ ] No purple/pink gradient, colored-border cards, emoji-as-icon, fake data, or fake logos.
- [ ] Missing assets are placeholders, not fakes; the scene reports what is still missing.
- [ ] No header / footer / page number — only the key content.
- [ ] Colors and font families all go through tokens; primitives carry theme personality.
- [ ] Scene is physically isolated (own CSS prefix, no cross-scene import, no edits to shared files beyond its registry entry).
- [ ] `steps` array exists and `steps.length` equals the max step used, plus one.
- [ ] `npx tsc --noEmit` passes — do not report "done" otherwise.

Any item fails → fix it now. Do not "leave it for later."
