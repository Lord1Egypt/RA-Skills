---
name: cdance-seedance-video-prompt-architect
description: Turn rough Seedance and AI video ideas into structured prompt packs, tighter variants, and debugging loops. Use when the user wants better text-to-video, image-to-video, or reference-driven video prompts for creator content, product clips, and short-form video testing.
version: 1.0.0
homepage: https://cdance.net/docs/cdance-seedance-video-prompt-architect
metadata:
  openclaw:
    homepage: https://cdance.net/docs/cdance-seedance-video-prompt-architect
---

# C Dance Seedance Video Prompt Architect

This skill turns rough Seedance-style video ideas into cleaner prompt packs, stronger motion structure, and faster revision loops.

## Canonical links

- Docs: https://cdance.net/docs/cdance-seedance-video-prompt-architect
- Demo: https://cdance.net/ai-video-generator
- Create: https://cdance.net/create
- Raw SKILL.md: https://cdance.net/skills/cdance-seedance-video-prompt-architect/SKILL.md
- Seedance FAQ: https://cdance.net/blog/seedance-2-0-faq-guide
- Prompt workflow guide: https://cdance.net/blog/seedance-comfyui-workflow-guide

## Provenance and safety

- Maintained around the public C Dance workflow and documentation on `cdance.net`.
- Text-only skill pack.
- No helper scripts, no local binaries, and no required environment variables.
- It guides prompt design and references public pages only.

## When to use

- The user has a rough Seedance, SeaDance, or AI video idea and wants a stronger prompt
- The user wants text-to-video, image-to-video, or reference-driven video prompt rewrites
- The user needs 2 to 3 focused prompt variants for testing hooks, motion, or camera behavior
- The user has unstable outputs and needs a diagnosis plus a revision plan

## Workflow

1. Classify the request as text-to-video, image-to-video, or reference-driven video.
2. Extract the essentials:
   - subject
   - action
   - camera behavior
   - environment
   - style and lighting
   - duration and aspect ratio
   - hard constraints
3. Keep the first draft simple:
   - one primary subject
   - one dominant action beat
   - one camera rule
   - one short constraint block
4. Return:
   - one primary prompt
   - 2 or 3 tighter variants
   - a short avoid list
   - 3 concrete revision moves

## Prompt construction rules

- Prefer concrete visual language over vague adjectives.
- Use beat-based structure when motion matters.
- Avoid stacking multiple subjects and camera changes into one short clip.
- If identity or composition must stay stable, prefer image-to-video or reference-driven generation over pure text-to-video.
- Keep the constraint block focused on likely failure modes such as flicker, unstable faces, drifting composition, or chaotic movement.
- Do not invent unsupported model settings.

## Output formats

### Text-to-video

```md
Goal:
Subject:
Action:
Camera:
Environment:
Style and lighting:
Constraints:
Suggested settings: duration=?, aspect_ratio=?
Prompt:
```

### Image-to-video

```md
Reference anchor:
What must stay stable:
Allowed motion:
Camera move:
Style and lighting:
Constraints:
Prompt:
```

### Reference-driven video

```md
Source value:
What to preserve:
What to transform:
Style direction:
Constraints:
Prompt:
```

## Response style

- Be structured and concise.
- Prefer prompt packs over long theory.
- Point users to the canonical C Dance pages listed above when examples help.
