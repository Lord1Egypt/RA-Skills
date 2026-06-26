---
name: ai-video-scene-director
description: Plan AI video scenes from a creator's concept into character sheets, scene plates, multi-shot prompt briefs, credit-aware run plans, and review checklists for tools such as Claude, Higgsfield, Seedance, Nano Banana Pro, and similar image/video generators. Use when the user wants to make an AI short, music video, UGC ad, avatar scene, cinematic sequence, or repeatable AI video production workflow.
metadata: {"openclaw":{"homepage":"https://www.youtube.com/watch?v=0YhhPQVXA7c","requires":{"anyBins":["python3","python"]}}}
---

# AI Video Scene Director

Use this skill to turn an AI video idea into a production-ready prompt brief without wasting generations. It does not generate media directly. It prepares the source material an image/video tool or MCP connector needs.

## Workflow

1. Clarify the output.
   - Format: music video, cinematic short, product ad, avatar clip, explainer, or test shot.
   - Length: total seconds and target shot count.
   - Tool path: Claude-only planning, Higgsfield, Seedance, Nano Banana Pro, or other generator.
   - Constraints: budget, credit limit, aspect ratio, realism level, platform, and deadline.

2. Define continuity.
   - Character identity: face, hair, wardrobe, age range, body language, recurring props.
   - World rules: location, time period, visual genre, lighting, color grade, camera language.
   - Negative constraints: what must not change between shots.

3. Build the reference plan.
   - Character sheet prompt.
   - Outfit or prop reference prompt.
   - Scene plate prompt.
   - Combined character-in-scene reference prompt.
   - Use a single reference image before moving to video whenever possible.

4. Build the shot plan.
   - One row per shot: purpose, duration, action, camera movement, lens feel, lighting, sound/dialogue note, required reference.
   - Mark each shot as one-take or multi-shot.
   - Estimate generation attempts before running.

5. Produce prompt packs.
   - Image prompt for reference generation.
   - Video prompt for each shot.
   - Continuity reminder appended to every prompt.
   - Failure repair prompt for common issues such as face drift, plastic skin, bad hands, broken lip sync, or inconsistent wardrobe.

6. Review before generation.
   - Check that every prompt has a subject, action, setting, camera, lighting, duration, and continuity anchor.
   - Flag expensive or vague requests before the user spends credits.
   - State which assumptions are inferred.

## Output Format

Start directly with the deliverable. Do not add a persona, greeting, or process preamble.

Return:

- `concept`: one paragraph.
- `continuity bible`: concise bullets.
- `reference prompts`: character sheet, wardrobe/props, scene plate, combined reference.
- `shot table`: compact markdown table.
- `generation order`: exact sequence to run.
- `credit risk`: low, medium, or high with reason.
- `repair prompts`: 3 to 5 targeted fixes.
- `done criteria`: what a usable result must satisfy.

## Guardrails

- Do not copy prompts or private workflows from a creator's paid material.
- Do not claim guaranteed views, income, virality, or ranking.
- Do not help impersonate a real person, create non-consensual sexualized imagery, or bypass platform moderation.
- For product ads or affiliate content, include a disclosure reminder and avoid unverifiable performance claims.
- If the user provides a source video, cite it as inspiration and produce original prompts.

## Reference

If source validation is needed, read `references/source-evidence.md`. It summarizes the public video/comment evidence behind this skill and the limits of the conversion.
