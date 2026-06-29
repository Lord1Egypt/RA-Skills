---
name: click-driven-presentation
description: >
  Use this skill when the user has a narration script and wants it turned into a click-driven, full-screen "video-like" web presentation they advance by clicking and record themselves — a dynamic deck that does not look like slides. Produces a running Vite+React engine with one scene per beat. Not for writing the script, rendering an mp4, audio/TTS, screen recording, or general web-app development.
---

# Click-Driven Presentation

You build a **click-driven web presentation**: a full-screen, video-like webpage the speaker advances one beat per click, then records.
Time is not baked in — the speaker controls the rhythm live by clicking.
You orchestrate the build and gate it; you do **not** write the narration, render video, synthesize audio, or record the screen.

## What this is, and what it is not

This produces a running web page (Vite + React + TS) where each click reveals the next focused idea, full-screen, no slide chrome.
The user opens it full-screen, clicks through while speaking, and records it with their own tool.

- **Not for** writing the script — start from a script the user already has; delegate writing to a content skill (such as `saas-founder-content-writer`).
- **Not for** deterministic mp4 rendering — that is the job of an audio-driven render pipeline (such as `remotion-video-pipeline`).
- **Not for** audio/TTS synthesis, screen recording, or post-editing — out of scope; the user does these or another capability does.
- **Not for** general web-app development.

## Governing idea

Memorize this and let it drive every decision:

```
script  = the beats (one beat = one focused idea)
step    = one beat on screen (the speaker clicks to advance)
scene   = a pure function of the current step (no timers)
visuals = show the idea, do not just type the script on screen
```

Two consequences you must never violate:

1. **Time is the speaker's, not the timeline's.** There are no baked durations; a step changes only when the speaker clicks. Never add timers that auto-advance.
2. **One beat = one step = one focused idea.** When the script lists items ("first X, then Y, then Z"), reveal them one step at a time — never stagger all of them onto one step.

## Inputs

| The user gives | You do |
| --- | --- |
| A narration script | Slice it into steps and build (Phase 1 → 2). |
| A script **and** a source article/notes | Same, but pull on-screen visual detail from the source (dual-source rule in `references/SCENE-CRAFT.md`). |
| Only raw notes, no script | Ask them to provide or generate a script first — this skill does not write scripts. Point to a content skill. |

## Workflow

```
Phase 1   Plan
   1.1  Slice the script into steps (1 beat = 1 step)
   1.2  Emit the steps spec (single source of truth) + pick the theme
   ▼
[GATE — Plan]   one alignment: step breakdown / theme / asset list   (hard stop)
   ▼
Phase 2   Build
   2.1  Scaffold the engine + the chosen theme
   2.2  Scene 1 in the main thread, complete (the style anchor)
        ▼
        [GATE — Scene 1 acceptance]   (hard stop, never skip)
        ▼
   2.3  Scenes 2..N (mode A per-scene / B sequential / C parallel)
   ▼
Done: running page at the dev server. Handoff: "open full-screen, click through, record."
```

There are **two mandatory STOP gates** (Plan, Scene 1).
Never cross a gate without an explicit "yes" from the user.

### Phase 1 — Plan

Read [`references/STEPS-SPEC.md`](references/STEPS-SPEC.md) before slicing.

1. **Slice the script into steps.** Each step is one focused idea the speaker lands with one click. A list of N items becomes N steps, not one.
2. **Emit the steps spec** — the per-scene `steps` data (narration text + on-screen intent per step). This is the single source of truth (see below).
3. **Pick the theme.** The scaffold ships one neutral token-based theme. If the user wants a different look, the look is achieved through theme tokens and per-scene visual craft — not by hardcoding colors in scenes.

**🚦 GATE — Plan.** Stop and align once on: the step breakdown, the theme, and the asset list (what images/screenshots the visuals will need). Do not scaffold until the user approves.

### Phase 2 — Build

#### 2.1 Scaffold

```bash
bash <path-to-this-skill>/scripts/scaffold.sh ./presentation
```

The scaffold ships one demo scene (`01-example`). Delete it before writing real scenes (the script prints how).

#### 2.2 Scene 1 — main thread, complete, then accept

Scene 1 is the **style anchor**: build it complete (rhythm + visuals + real or placeholder assets) in the main thread.
It is the first time this craft lands on this topic + theme; if the guidance or theme has a gap, Scene 1 exposes it while a fix is cheapest.

**🚦 GATE — Scene 1 acceptance.** Stop and let the user review Scene 1 in the browser before building the rest. Do not continue until they approve.

#### 2.3 Scenes 2..N — pick a mode

Each scene is built independently per [`references/SCENE-CRAFT.md`](references/SCENE-CRAFT.md). Theme tokens keep the visuals coherent; animation and composition are free per scene by design.

- **Mode A · per-scene confirm (default).** Build a scene, pause for acceptance, repeat. Lowest risk; use this unless the user chooses otherwise.
- **Mode B · sequential.** Build scenes 2..N in the main thread, then one acceptance at the end. For agents without parallel execution.
- **Mode C · parallel (subagents).** Build scenes 2..N with parallel subagents (the user sets how many at once). Fastest; per-scene style will vary slightly — this is expected, and theme tokens keep it coherent.

A parallel subagent's prompt must include: the scene's steps spec, the path to `references/SCENE-CRAFT.md`, the theme's tokens, Scene 1 as a *code-style* reference (not to copy visually), and the hard rule that each scene uses its own CSS prefix, never imports across scenes, never edits the shared registry beyond its own entry, and passes `npx tsc --noEmit`.

## Single source of truth

Each scene owns a `steps` array (the narration text per step + on-screen intent).
The number of steps the scene's code uses (`if (step === N)`) **must equal** the `steps` array length.
Keep this true even though this skill synthesizes no audio: it stops the speaker's script and the on-screen beats from drifting apart, and it is what a downstream audio/render pipeline would read if the user later wants narration.

## Per-scene visual craft is delegated

This skill owns the engine, the workflow, the gates, and the steps contract.
The actual look of a scene — layout, motion design, the anti-AI-aesthetic judgment — is craft.
Follow [`references/SCENE-CRAFT.md`](references/SCENE-CRAFT.md), and where a skill that designs high-quality front-end interfaces is available (such as `frontend-design`), use it for the per-scene component work.
Reference such skills by capability, never as a hard dependency.

## Safety & boundaries

- **Files you may write:** a presentation project folder under the user's chosen directory (default `./presentation`), and its asset folder. **Confirm before overwriting** an existing project directory or any file you did not create.
- **Network/installs:** the scaffold runs `npm install` for Vite/React/TypeScript in the project folder. Confirm before installing if the user has not already asked you to scaffold.
- **Credentials:** this skill handles none.
- **No fabrication:** never invent data, logos, screenshots, or "N users" numbers for the visuals. Missing assets get an honest placeholder, never a fake. To show the real product, use a real screenshot the user provides.
- **Scope:** click-driven web presentations only. Not mp4 rendering, not audio, not recording, not general web apps.

## Feedback

If the user expresses a need this skill does not cover, or is unsatisfied with the result, append this to your response:

> "This skill may not fully cover your situation. Suggestions for improvement are welcome — [open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues)."

Do not include this message in normal interactions.
