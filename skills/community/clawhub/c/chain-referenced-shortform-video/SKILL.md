---
name: chain-referenced-shortform-video
description: Use when generating AI films, short dramas, cinematic sequences, or storyboard-driven video scenes that need strong cross-shot continuity and real film-language control. Covers asset-driven preproduction, shot lists, storyboards, blocking, lensing, camera movement, five-dimension prompt control, subtractive prompting, staged keyframe gates, bridge-frame selection, shot cards, continuity ledgers, and chain-referenced video generation. Trigger for requests about AI movie generation, cinematic prompt engineering, short drama workflows, continuity pipelines, previsualization, scene packs, shot templates, bridge frames, or swapping scripts without rewriting the workflow.
---

# Chain-Referenced Shortform Video

Use this skill when the user wants to generate AI movies, short dramas, or cinematic scene sequences that hold character, scene, prop, and film-language continuity across multiple shots.

## What to load first

Read only these files first:

- `references/film-language.md`
- `references/review-rubric.md`
- `references/repo-mapping.md`

Load project-specific implementation files only if the user needs them.

For this repository, then load:

- `/Users/lebo/project/ai-video/src/ai_video_control/models.py`
- `/Users/lebo/project/ai-video/src/ai_video_control/shortform.py`
- `/Users/lebo/project/ai-video/src/ai_video_control/review.py`
- `/Users/lebo/project/ai-video/src/ai_video_control/cli.py`

## Operating stance

Act as:

- continuity supervisor
- storyboard artist
- cinematographer
- edit-minded prompt designer

Do not treat the task as `write a prettier prompt`. Treat it as `preproduction -> gated keyframes -> chained shots`.

## Core rules

1. Start with `single-scene micro-stories`.
2. Model each scene and shot with five dimensions:
   - `subject_motion`
   - `environment_light`
   - `medium_rendering`
   - `temporal_state`
   - `camera_optics`
3. Use subtractive prompting:
   - the master-scene prompt defines the locked facts
   - shot-delta prompts describe only the allowed change
   - never restate identity, wardrobe, room layout, or lighting if already locked
4. Do not render final sequence clips unless:
   - the master scene passes gate
   - the shot-delta keyframe passes gate
5. For `shot n > 1`, use chain reference:
   - select a bridge frame from the tail of video `n-1`
   - use that bridge frame as `first_frame`
   - use the approved shot `n` keyframe as `last_frame`
6. Every shot must also be readable as cinema:
   - clear dramatic beat
   - clear blocking
   - intentional framing
   - intentional camera movement
   - intentional edit relationship to the previous shot

## Production model

Design each shot as eight layers:

1. dramatic purpose
2. emotional state
3. subject blocking
4. screen geography
5. shot size / angle / lens intent
6. camera movement
7. light / atmosphere continuity
8. edit seam to previous and next shot

If these layers are not explicit, prompting will drift because the model will improvise them.

## Recommended asset model

Create reusable inputs before writing prompts:

1. character bible
2. scene pack
3. prop pack
4. shot template
5. beat sheet
6. continuity ledger
7. episode spec

Keep them loosely coupled so you can swap scripts or settings without rewriting the workflow.

## Production order

1. Build a character bible with only core identity anchors.
2. Build a scene pack that locks layout, lighting, and camera baseline.
3. Build a prop pack that separates:
   - fixed props
   - allowed temporal changes
   - forbidden drift
4. Build a beat sheet that states for each shot:
   - dramatic purpose
   - emotional change
   - what the viewer must learn or feel
   - what must be visible for the next cut to work
5. Build a shot template that locks:
   - framing
   - lens intent
   - camera side of line
   - floor marks
   - blocking rules
   - allowed changes
   - forbidden changes
6. For each shot, write a concise shot card with:
   - shot size
   - angle
   - movement
   - blocking
   - screen direction
   - bridge-frame preference
   - forbidden composition
7. Generate master-scene candidates.
8. Gate the master scene for:
   - clarity
   - identity
   - scene stability
   - prop stability
   - cinematic readability
9. Generate shot-delta candidates from the approved master scene.
10. Gate each shot-delta candidate for:
   - identity
   - scene
   - props
   - camera
   - staging readability
   - edit compatibility
11. Generate a short clip for the approved shot.
12. Extract tail frames and select the best bridge frame.
13. Use the bridge frame to condition the next shot.
14. Update the continuity ledger after every approved shot.

## Shot design rules

Each shot should usually change only one major thing:

- subject pose or performance beat
- camera distance
- camera movement
- temporal state
- prop interaction

Do not change all of them at once.

Prefer this progression:

- `establish`
- `orient`
- `develop`
- `payoff`
- `exit or bridge`

If a scene feels flat, vary shot size or movement. If a scene feels unstable, reduce simultaneous changes.

## How to write prompts

### Master scene prompt

Include:

- core protagonist identity
- scene layout and lighting
- fixed props
- framing and floor marks
- camera side of line
- baseline lens feeling
- baseline temporal state

Do not include:

- later shot deltas
- multiple unrelated actions
- optional accessories unless they are essential continuity anchors

### Shot-delta prompt

Include only:

- the allowed action change
- the allowed temporal change
- the blocking delta
- the camera delta if and only if it is allowed
- the intended audience read of the shot
- explicit continuity constraints such as:
  - same framing
  - same side of line
  - same floor marks
  - no new props
  - no room changes

Do not include:

- full face or wardrobe re-description
- full scene re-description
- multiple new props
- camera reinvention unless camera change is explicitly allowed

## Camera and blocking heuristics

- If the emotional beat is intimate, bias toward `CU / MCU`, restrained blocking, and minimal movement.
- If the beat is spatial or tactical, bias toward `MS / LS / WS` and clear geography.
- Use `push-in` for realization, pressure, or dread.
- Use `pull-back` for alienation, aftermath, or loss.
- Use `lateral track` when the subject is moving through space.
- Use `handheld` only when instability is part of the intended feeling.
- Preserve screen direction unless the cut is motivated.
- Do not cross the 180-degree line by accident.
- When in doubt, simplify the move before simplifying the art direction.

## What to gate

### Master scene gate

Fail if:

- the image is soft or artifacted
- the subject identity is unstable
- the room layout drifts
- fixed props are missing
- lighting is inconsistent with the pack
- the frame does not establish usable geography
- the shot feels compositionally dead or confusing

### Shot-delta gate

Fail if:

- the character changes outside the allowed delta
- layout drifts
- props move outside the whitelist
- framing changes without permission
- the shot spec contradicts itself
- blocking becomes unclear
- screen direction breaks without a motivated transition
- camera movement conflicts with the beat
- the shot cannot cut cleanly from the previous shot

### Bridge-frame gate

Select from the tail of the previous clip based on:

- face visibility
- pose stability
- prop completeness
- low motion blur
- continuity usefulness
- edit seam quality
- pose that can plausibly launch the next action

Do not use the literal last frame by default.

## Good defaults

- shot length: `3-5s`
- master scene candidates: `4`
- shot-delta candidates per shot: `3`
- bridge-frame tail window: final `20%`
- bridge-frame candidates: `6`
- frame gate should prefer passing candidates over merely high scores

## Review loop

After every approved shot, record:

- what changed
- what remained locked
- what made the shot pass
- what phrase or move caused drift
- which bridge frame is canonical for the next shot

This ledger is more important than preserving every old prompt.

## Fallback strategy

If image-to-image editing is unavailable:

1. use text-to-image for the master scene
2. use image-to-video draft clips for shot-delta search
3. extract candidate frames
4. gate those frames as shot-delta keyframes

This is slower, but often more reliable than returning to freeform text-only keyframe generation.

## Borrow and adapt, do not copy blindly

Useful patterns from other ecosystems:

- storyboard skills: shot vocabulary, 180-degree rule, panel annotations
- cinematic writing skills: lighting, lens, and color language
- video production skills: feedback loops, approval ledgers, revision discipline
- Seedance-specific skills: explicit reference roles and time segmentation

Do not import one common bad habit from generic cinematic skills:

- repeating the full identity and set description in every shot prompt

For this workflow, that causes prompt pollution and continuity drift.

## Repo mapping

When applying this skill to this repository, map film-language concepts into the current episode YAML through `references/repo-mapping.md`.

## What to fix first when continuity fails

- If identity drifts: reduce identity anchors to the most visible features.
- If layout drifts: strengthen the scene pack and reduce motion.
- If props drift: move them into `allowed_changes` or remove them from the shot text.
- If framing drifts: add explicit `same framing / same floor mark` constraints to the video prompt.
- If eyelines or geography fail: fix the shot card and side-of-line rule before touching model settings.
- If the shot feels uncinematic: fix shot size, movement, and blocking before adding more adjectives.
- If a cut feels bad: change the bridge frame, not the character description.
- If the spec is self-contradictory: fix the spec first, not the prompt.
