---
name: ai-video-camera-work
description: "Design and prompt AI video using named camera work. Use for Veo, Sora, Kling, Runway, or any text/image-to-video model when a shot needs a specific camera move, shot size, angle, lens, focus, composition, or time effect. Includes a 100-term bilingual camera index, a 60-second blueprint workflow, and ready-to-use shot prompts derived from CodeX 実践塾's four infographic sheets."
category: creative
---

# AI Video Camera Work

The source post's lesson in one line:

> **Name the camera move, then the subject, then the direction and speed. “More impactful” is not a camera instruction.**

This skill turns vague video ideas into a shot list and a prompt that a video model can follow.

## When to use

- A prompt like “make it more cinematic / powerful / dynamic” did not work.
- The model substitutes a zoom for a dolly, ignores an orbit, or changes the shot size.
- You need a 60-second AI video with a real blueprint instead of a one-shot prompt.
- You need to describe a shot to Veo, Sora, Kling, Runway, Pika, or a local video model.
- You need consistent camera language across several scenes.

## The method

```text
1. Define the shot's job.
2. Choose ONE camera move from the 100-term index.
3. Add shot size + angle + lens/DOF + composition.
4. Add subject + action + start/end position.
5. Add direction + speed + duration.
6. Add light + continuity + negative constraints.
7. Generate, inspect, repair one variable at a time.
```

The source sheet's own formula:

> **技法名 + 被写体 + 方向・速さを指定**  
> technique + subject + direction/speed

## Prompt formula

```text
[Shot size], [angle], [lens / depth of field], [composition].
Camera: [one movement] [direction] at [speed] over [duration].
Subject: [who/what], [action], [start position] → [end position].
Environment: [place, time, weather, era].
Light: [source, direction, contrast, palette].
Continuity: [wardrobe, props, screen direction, identity anchors].
Negative: no cuts, no text artifacts, no morphing, no extra limbs, no camera shake unless requested.
```

### Four ready prompts

**Dolly in**

```text
Medium shot, eye level, 50mm, shallow depth of field, centered composition.
Camera: slow dolly in toward the subject over 5 seconds, constant speed, no zoom.
Subject: a lone courier in a rain-soaked alley, walking toward camera, start mid-frame, end chest-up.
Light: cool practical neon from screen-left, soft rim light.
Continuity: same coat, same bag, screen direction toward camera.
Negative: no cuts, no text, no morphing, no extra people.
```

**Orbit**

```text
Medium wide shot, chest height, 35mm, rule of thirds.
Camera: 360-degree orbit around the subject at constant radius over 8 seconds, smooth gimbal.
Subject: a warrior standing still in a ruined courtyard, centered, cloak moving in wind.
Light: low sun from screen-right, long shadows.
Continuity: same armor, same sword, horizon level.
Negative: no cuts, no zoom, no camera shake, no text.
```

**Rack focus**

```text
Close-up, eye level, 85mm, shallow depth of field, locked-off camera.
Camera: rack focus from the foreground hand to the background doorway over 2 seconds.
Subject: a hand holding a key in the foreground; a silhouette appears in the doorway behind.
Light: warm practical lamp on the hand, cold blue background.
Negative: no camera movement, no cuts, no text, no morphing.
```

**Whip pan**

```text
Wide shot, eye level, 24mm.
Camera: fast whip pan from screen-left to screen-right over 0.6 seconds, strong motion blur, then settle.
Subject: empty street on the left; a speeding car enters from the right.
Light: dusk, wet asphalt reflections.
Negative: no cuts, no text, no warped car shape, no extra vehicles.
```

## The 100-term index

Full bilingual table with prompt cues:

`references/100-camera-movements.md`

Four groups:

| Group | Numbers | Covers |
|---|---|---|
| Movement basics | 001–025 | pan, tilt, dolly, truck, crane, orbit, rack focus, zoom, roll |
| Shot size / angle | 026–050 | extreme wide → extreme close, POV, Dutch, aerial, profile |
| Focus / lens / composition | 051–075 | DOF, split diopter, macro, anamorphic, thirds, negative space |
| Time / advanced | 076–100 | speed ramp, hyperlapse, freeze, reverse, loop, fly-through, bullet time |

## 60-second blueprint workflow

Full workflow and templates:

`references/60-second-ai-video-workflow.md`

Short version:

1. **Blueprint** — 10 scenes, second-by-second; 20 subtitle lines with display windows; factual rules; visual rules.
2. **Approve** — do not render before the blueprint is checked.
3. **Voice** — direction separate from body; generate the whole script at once; keep narration shorter than subtitles.
4. **Picture** — one camera move per shot; use the formula above.
5. **Assemble** — narration at scene heads; duck music; consistent screen direction.
6. **QA** — run the same blueprint twice; compare structure and inspect text frame by frame.
7. **Package** — blueprint, shot prompts, voice script, QA notes, sources.

## Repair table

| Symptom | Repair |
|---|---|
| “Cinematic” ignored | replace with a named movement + subject + direction/speed |
| Zoom instead of dolly | “camera physically moves toward the subject; lens does not zoom” |
| Orbit wobbles | “constant radius, chest height, subject centered, smooth speed” |
| Rack focus invisible | “near focus on hand → far focus on door; locked camera; shallow DOF” |
| Too busy | one move, one action, one lighting change |
| Identity drift | reference image + wardrobe/face anchors every shot |
| Text corrupt | generate no text; add subtitles in the edit |
| Wrong duration | fix in edit; do not rely on “make it 55 seconds” |
| Voice too long | shorten script; speed up ≤1.2×; tighten pauses |
| Model varies each run | repair by time range + quantity, not a new style prompt |

## Guardrails

- **One dominant camera move per shot.** Split complex moves.
- **Do not stack dolly + zoom + orbit + handheld** unless the model is known to handle it.
- **Use English camera terms** for most models, with a plain-language restatement.
- **Do not use “more powerful”** as the only direction.
- **Do not claim a shot succeeded** without inspecting frames.
- **Label source claims**: the linked article's model versions, timings, and free-tier numbers are the author's claims, not independently verified.
- **Do not claim the LINE-gated PDF** was read; it is GATED.

## Source and assets

- Post: https://x.com/Codex_jisen/status/2110505177245777955
- Article: https://x.com/i/article/2103440981387587742
- Follow-up: https://x.com/Codex_jisen/status/2110636237405188466
- PDF post (gated): https://x.com/Codex_jisen/status/2111262714144379348
- Notes: `references/codex-post-notes.md`
- Source links: `references/source-links.md`
- Four original infographics: `assets/images/camera-work-1.jpg` … `camera-work-4.jpg`

The images were copied at full resolution (2048×1638). The 100 terms and section labels were transcribed by direct visual reading of those images; no OCR engine was available. Hashes are in `references/source-links.md`.

## Completion checklist

- [ ] shot size chosen
- [ ] angle chosen
- [ ] one camera movement chosen
- [ ] subject + action + start/end position
- [ ] direction + speed + duration
- [ ] lens/DOF + composition
- [ ] light + continuity
- [ ] negative constraints
- [ ] generated and inspected
- [ ] one variable repaired, not five
- [ ] source/caveats recorded
