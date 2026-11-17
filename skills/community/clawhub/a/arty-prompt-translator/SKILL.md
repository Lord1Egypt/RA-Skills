---
name: "arty-prompt-translator"
description: "Translate rough visual ideas into structured prompts for image, video, NFT, sprite, and campaign work."
license: "MIT-0"
---

# Arty Prompt Translator

Use this skill when the user gives a rough, vague, emotional, partial, or mixed visual idea and needs it turned into a clear prompt for image generation, image editing, video generation, NFT assets, sprites, thumbnails, ads, posters, pitch visuals, or creative campaigns.

This skill is especially useful before using image/video generation tools such as Nano Banana Pro, Gemini image generation, Kling, Sora-style video prompting, Midjourney, Stable Diffusion, Flux, or similar systems.

## Core Rule

Do not jump straight from a vague idea to generation unless the user explicitly asks for speed over quality. First translate the idea into a production-ready visual brief and prompt.

When information is missing, infer sensible defaults and ask only the questions that materially affect the output.

## Prompt Translation Workflow

1. Identify the output type:
   - still image
   - image edit
   - video shot
   - NFT trait/character/collection asset
   - sprite or game asset
   - thumbnail/social post/banner
   - product/campaign visual
   - presentation or pitch visual

2. Extract the visual intent:
   - subject
   - setting or background
   - mood
   - style family
   - composition
   - color palette
   - lighting
   - camera or viewpoint
   - level of realism
   - constraints
   - intended platform or use

3. Convert emotional language into visual language:
   - "epic" -> large scale, heroic pose, dramatic rim light, low-angle framing, high contrast
   - "dark" -> low-key lighting, deep shadows, muted palette, controlled highlights
   - "premium" -> clean composition, refined materials, deliberate negative space, polished lighting
   - "viral" -> simple readable subject, strong silhouette, high contrast, recognizable hook
   - "cute" -> rounded forms, soft palette, gentle expression, friendly proportions
   - "aggressive" -> sharp angles, tense pose, harsh lighting, dynamic diagonals

4. Preserve identity and continuity when relevant:
   - Keep character traits stable across outputs.
   - Call out untouchable details such as face, silhouette, color scheme, costume, logo, species, object shape, or brand markers.
   - For iterative edits, specify what must change and what must remain unchanged.

5. Produce a structured prompt with sections:
   - Objective
   - Subject
   - Scene
   - Style
   - Composition
   - Lighting and color
   - Technical constraints
   - Negative constraints
   - Final prompt

6. If the target is video, add:
   - duration
   - camera movement
   - subject motion
   - scene transition
   - pacing
   - first frame and last frame intent
   - audio/dialogue notes only if requested

7. If the target is NFT or collection work, add:
   - collection role
   - trait layer or rarity role
   - consistency rules
   - background rules
   - metadata-relevant descriptors
   - forbidden changes that would break collection identity

8. If the target is a sprite/game asset, add:
   - view angle
   - frame count or pose
   - silhouette readability
   - transparent background requirement
   - pixel/2D/3D style
   - animation loop notes if needed

9. If the target is an ad/campaign visual, add:
   - message hierarchy
   - focal hook
   - audience
   - platform crop/aspect ratio
   - text/no-text constraint
   - safe area and readability rules

## Clarifying Questions

Ask at most three questions before producing the prompt. Prefer default assumptions unless a missing detail would likely waste a generation.

High-value questions:

- What is the final use: NFT, post, banner, thumbnail, video, sprite, or concept art?
- Should the style be realistic, cinematic, anime, 3D, pixel art, illustration, or brand/editorial?
- What must stay unchanged from an existing character, product, logo, or scene?

Avoid asking about details the model can safely infer, such as minor background props, exact camera lens, or exact color names, unless the user cares about them.

## Output Format

When the user asks for help improving a prompt, respond with:

```markdown
**Brief understood**
- Output:
- Final use:
- Subject:
- Style:
- Key constraints:

**Optimized prompt**
[production-ready prompt]

**Negatives / avoid**
[negative constraints]

**Operational notes**
[short operational notes: tool/model, aspect ratio, consistency risks, or open questions]
```

When the user asks for a direct generation and the prompt is already clear, keep the translation short and proceed according to the relevant generation workflow.

## Quality Checklist

Before using or handing off the prompt, verify:

- The subject is visually specific.
- The final use is clear.
- The composition is not ambiguous.
- The style is describable without relying only on taste words.
- Important constraints are explicit.
- Negative constraints prevent common failure modes.
- The prompt avoids contradictory instructions.
- If editing an existing image, unchanged elements are named clearly.
- If video, motion and camera behavior are described.
- If NFT or game asset, consistency and background rules are explicit.

## Common Fixes

If the user's prompt is too vague, add visual specifics.

If it is too long, compress it into production-relevant details and remove story exposition that will not appear visually.

If it mixes styles, choose one dominant style and one secondary influence.

If it asks for text inside images, warn that generated text may fail and suggest adding text later in a design tool unless exact typography is required.

If the user wants a character to stay consistent, recommend using a reference image or a saved character sheet.

If the request is for public posting, recommend fact-checking text claims and avoiding logos, trademarks, or living-person likenesses unless the user has rights or approval.

## Tone

Be direct and practical. The goal is to make visual generation less random, not to sound like a prompt-engineering textbook.
