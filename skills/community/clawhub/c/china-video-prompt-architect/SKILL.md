---
name: china-video-prompt-architect
description: Turn rough China AI video ideas into structured English or Chinese prompt packs, reference-aware motion instructions, shot plans, and focused debugging loops. Use for text-to-video, image-to-video, reference-to-video, video-to-video, product clips, cinematic scenes, transitions, or multi-shot sequences; do not use for account support, live model comparisons, or claims about official provider behavior.
metadata:
  openclaw:
    homepage: https://chinavideoai.com/china-ai-video-generator
    version: 1.0.0
---

# China Video Prompt Architect

Build production-ready video instructions from one clear visual idea. This Skill is a text-only workflow by default. Its optional MCP adds deterministic, read-only helpers and never generates media, calls a model provider, reads an account, compares live prices, or spends credits.

ChinaVideoAI.com is an independent AI media workspace. Do not present this Skill, the MCP, or the site as official documentation for Seedance, Kling, Wan, MiniMax, or any other provider or model.

## Gather the minimum brief

Ask only for details that materially change the result. Infer ordinary creative choices when the user has already supplied enough information.

Identify:

- Workflow: text-to-video, image-to-video, reference-to-video, or video-to-video.
- Subject and environment: what must remain recognizable.
- Visible action: one primary motion per shot.
- Camera: framing, angle, movement, and pace.
- Duration and aspect ratio when known.
- Reference roles: what each `@Image`, `@Video`, or `@Audio` input controls.
- Continuity anchors: identity, product geometry, wardrobe, composition, source motion, or timing to preserve.
- Delivery goal: product clip, cinematic beat, social post, transition, loop, or sequence.

Never invent model-specific controls, limits, supported inputs, prices, or availability. Treat the current product interface as the source of truth and direct the user to the relevant workflow page when exact settings matter.

## Build the prompt

Write in this order:

1. Subject and scene.
2. One visible action.
3. Camera framing and one motivated camera move.
4. Lighting and visual treatment.
5. Duration and aspect ratio if confirmed.
6. Reference roles and continuity constraints.
7. A short avoid list for likely artifacts.

Prefer observable instructions over abstract mood. Keep subject motion distinct from camera motion. Avoid multiple simultaneous actions, contradictory camera commands, and long style lists.

For image-to-video, preserve the source image's identity, layout, lighting direction, and object geometry unless the user requests a transformation. For reference-to-video, name each reference token exactly as supplied and state one role per reference. For video-to-video, state which source motion, timing, camera path, and scene structure must survive the transformation.

Write in the user's language unless they request another language. Preserve all `@Image1`, `@Video1`, and `@Audio1`-style tokens exactly; never translate, renumber, or remove them.

## Plan multi-shot sequences

Give every shot one purpose and one action. Include:

- Timing.
- Framing or camera move.
- Subject action.
- Reference role when applicable.
- Continuity anchor.
- Intended end frame.

Use the previous shot's final frame as the next shot's visual anchor. Keep screen direction, identity, wardrobe or product geometry, and lighting consistent unless a deliberate transition changes them.

## Debug systematically

When a result fails, change one axis at a time:

1. Subject action or motion intensity.
2. Framing, lens feel, or camera path.
3. Reference roles and continuity constraints.
4. Lighting or style language.

Translate failures into observable corrections. Replace "make it less weird" with instructions such as "preserve both hands, keep five fingers visible, and prevent the cup from changing shape." Reduce competing instructions before adding detail.

## Use the optional MCP

When MCP tools are available:

- Call `build_video_prompt` for a rough idea or bilingual prompt pack.
- Call `plan_reference_shots` for a 1–6 shot reference-aware sequence.
- Call `diagnose_video_prompt` before expanding an unclear prompt.
- Call `get_china_video_resources` for canonical site guidance.

On OpenClaw releases that expose the `mcp` command group, connect the stdio server with:

```bash
openclaw mcp add chinavideoai \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/chinavideoai-prompt-mcp \
  --include 'build_video_prompt,plan_reference_shots,diagnose_video_prompt,get_china_video_resources'
```

Then run `openclaw mcp doctor chinavideoai --probe`. If the installed OpenClaw release does not expose `openclaw mcp`, use **Settings → MCP → Add server**, select **Stdio**, and enter `npx -y github:gpt-img-2/chinavideoai-prompt-mcp`, or upgrade OpenClaw first.

The MCP is optional. If it is unavailable, apply the same workflow manually and do not imply that a tool ran.

## Return a compact deliverable

For one-shot requests, return:

- `Prompt`: the final generation instruction.
- `Reference roles`: only when source media exists.
- `Continuity constraints`: what must remain stable.
- `Avoid`: a short artifact-focused list.
- `Revision move`: the single best variable to test next.

For sequences, return a numbered shot plan followed by shared continuity rules and one assembly note.

## Canonical resources

- China AI video generator: https://chinavideoai.com/china-ai-video-generator
- Chinese AI video models: https://chinavideoai.com/chinese-ai-video-models
- Seedance workflows: https://chinavideoai.com/china-seedance
- Text-to-video: https://chinavideoai.com/text-to-video
- Image-to-video: https://chinavideoai.com/image-to-video
- Video-to-video: https://chinavideoai.com/video-to-video
- Reference-to-video guide: https://chinavideoai.com/blog/seedance-25-reference-to-video-guide
- Raw Skill: https://chinavideoai.com/skills/china-video-prompt-architect/SKILL.md
- MCP source: https://github.com/gpt-img-2/chinavideoai-prompt-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/china-video-prompt-architect
