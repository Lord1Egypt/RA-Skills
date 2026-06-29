# Click-Driven Presentation

**Platforms:** Claude · Openclaw · Codex
**Domain:** Video

## Purpose

A playbook + minimal engine for turning a narration script into a **click-driven, full-screen web presentation** — a video-like webpage the speaker advances one beat per click and records.
Unlike a baked-timeline render, the rhythm is the speaker's: a step changes only on click, so the script stays easy to revise and the deck can be presented live.

The governing idea:

```
script  = the beats (one beat = one focused idea)
step    = one beat on screen (the speaker clicks to advance)
scene   = a pure function of the current step (no timers)
visuals = show the idea, do not just type the script on screen
```

## When to Use

- When you have a narration script and want a "dynamic deck that does not look like slides" to record
- When you want the speaker to control pacing live (talk-driven), instead of locking timing into a render
- When you want fast iteration (edit, refresh, click through) and the option to present the deck live
- When you want a small, reproducible click-stepper engine instead of hand-rolling one each time

## What It Produces

A running Vite + React + TS project where:

- the stage is a fixed 16:9 canvas, scaled to the viewport, with black letterbox and no slide chrome (no header/footer/page numbers);
- a single global step counter drives everything — each scene is a pure function of the current step, advanced by click / arrow keys / space;
- a progress bar stays hidden and appears only on hover, so it never shows on the recording;
- colors and fonts come from theme tokens, so the look is consistent and swappable.

## Workflow

```
Input: a narration script (+ optional source article for visual detail)
Phase 1  Plan: slice into steps → emit the steps spec → pick the theme
   🚦 GATE — Plan (step breakdown / theme / asset list)
Phase 2  Build: scaffold → Scene 1 (main thread)
   🚦 GATE — Scene 1 acceptance (the style anchor)
   → Scenes 2..N (mode A per-scene / B sequential / C parallel subagents)
Done: running page — open full-screen, click through, record.
```

Two mandatory STOP gates (Plan, Scene 1) protect the most expensive rework points.

## Scope & Boundaries

- Click-driven web presentations only — **not** mp4 rendering (see `remotion-video-pipeline`), audio/TTS, screen recording, or post-editing.
- Does **not** write the script — start from one the user has; delegate writing to a content skill such as `saas-founder-content-writer`.
- Ships one neutral token-based theme; a different look comes from theme tokens and per-scene craft, not hardcoded colors.
- Delegates per-scene visual craft to a front-end design capability (such as `frontend-design`), referenced by capability, not as a hard dependency.
- Writes only a presentation project folder under the user's chosen directory; confirms before overwriting. Handles no credentials.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/open-skill-hub/issues) — improvements are welcome.
