# 60-Second AI Video Workflow

Derived from the linked article **撮影ゼロ・録音ゼロ。ClaudeとGeminiで60秒動画を作る全手順** by @Codex_jisen (2026-09-25). This is the article's workflow, translated and normalized; timings and model versions are the author's claims, not independently verified.

## The shape

```text
Blueprint → Voice → Picture → Assemble → QA
   (design)   (TTS)   (code/AI)   (edit)   (two-run check)
```

The camera-work vocabulary is used inside the **blueprint** and **picture** stages: each scene gets a named shot size, angle, movement, lens, and duration.

## 1. Blueprint first

Ask for a design document before generation:

```text
Do not make the video yet. First produce a second-by-second blueprint for a 60-second video.

Output a table with:
- scene number
- start second / end second
- what is on screen
- camera shot size, angle, and movement
- subject action
- subtitle text and display seconds
- sound/music cue
- continuity constraints

Then produce:
1. 10 scenes that cover 0–60 seconds.
2. 20 subtitle lines, each with a display window.
3. A rules list: no unverified claims, no invented numbers, no anachronisms, no forbidden imagery.
4. Visual direction: palette, texture, era, references.

Wait for approval before rendering.
```

Blueprint checklist:

- [ ] every second is accounted for
- [ ] 10 scenes, 20 subtitle lines (or the requested counts)
- [ ] each scene has one dominant camera move
- [ ] no contradictory moves in the same shot
- [ ] factual rules are explicit
- [ ] visual rules are explicit
- [ ] the end state of every shot is described

## 2. Voice

The article uses Gemini 3.8 Flash TTS through Claude (author's claim). The transferable rule:

> **Direction and body are separate inputs.**

```text
Voice direction:
- historical-program narrator
- low, weighted, unhurried
- intimate, not announcer-loud

Read this script:
<11 lines>

Per-line direction:
Line 1: ...
Line 2: ...
Line 11: very low, chewing each word.
```

Operational rules:

- Generate the full script in one request if the provider has a daily cap.
- Keep narration shorter than the subtitle; heavy voices run long.
- Do not trust “fit it in 55 seconds”; measure and fix in the edit.
- Use a **secret input field**, not the chat, for an API key.

## 3. Picture

For each scene, send one camera-controlled prompt:

```text
[Shot size], [angle], [lens/DOF], [composition].
Camera: [movement] [direction] at [speed] over [duration].
Subject: [who/what], [action], [start position] → [end position].
Environment: [place, time, weather, era].
Light: [source, direction, contrast, palette].
Continuity: [wardrobe, props, screen direction, identity anchors].
Negative: no cuts, no text artifacts, no morphing, no extra limbs, no camera shake unless requested.
```

One movement per shot. If a scene needs a reveal plus an orbit, split it into two shots.

## 4. Assemble

- Place each narration line at the head of its scene.
- Duck music under voice.
- Keep a consistent screen direction.
- Check that subtitles do not cover the subject's face.
- Keep a safety margin at the start/end of each clip.

## 5. QA

The article's most useful finding: **run the same blueprint twice and compare**.

- Does the structure match?
- Do the subtitles match?
- Does any text render incorrectly at frame level?
- Does the voice match the script?
- Does the camera move actually happen, or did the model substitute a zoom?
- Is the subject identity stable?
- Is the screen direction consistent?

## Camera-controlled shot list

| # | Sec | Shot size | Angle/lens | Movement | Subject/action | Subtitle | Sound |
|---:|---|---|---|---|---|---|---|
| 1 | 0–6 | wide | eye level, 35mm | slow dolly in | ... | ... | ... |
| 2 | 6–12 | medium | low angle, 50mm | orbit 90° | ... | ... | ... |
| 3 | 12–18 | close | eye level, 85mm | locked-off | ... | ... | ... |
| ... | | | | | | | |

## Failure fixes

| Failure | Fix |
|---|---|
| “More impact” ignored | replace adjectives with technique + subject + direction/speed |
| Model substitutes zoom for dolly | say “camera physically moves toward the subject; lens does not zoom” |
| Orbit wobbles | specify constant radius, chest height, subject centered, smooth speed |
| Rack focus not visible | specify near focus → far focus, shallow DOF, locked camera |
| Shot too busy | one move, one subject action, one background change |
| Text corrupt | keep text out of the generated frame; add subtitles in the edit |
| Identity drifts | use a reference image and describe wardrobe/face anchors every shot |
| Timing wrong | fix in the edit; do not rely on “make it 55 seconds” |
| Voice too long | shorten narration; speed up ≤1.2×; tighten pauses |
| Same prompt gives different style | accept variation; repair by time range + quantity (“20–26s, triple the torches”) |

## Deliverables

A usable handoff contains:

1. `blueprint.md` — scene table, rules, visual direction
2. `shot-prompts.md` — one prompt per scene
3. `voice-script.md` — direction + lines
4. `qa.md` — two-run comparison and frame-level checks
5. `sources.md` — links and what was gated
