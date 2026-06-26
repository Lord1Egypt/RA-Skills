---
name: ai-tattoo-prompt-builder
description: Turn vague tattoo ideas into stronger AI-ready prompts by combining motif, style, placement, scale, and mood into one clearer instruction. Use when Codex needs to refine tattoo concepts for image generation, placement comparison, prompt iteration, or pre-artist visual exploration.
---

# AI Tattoo Prompt Builder

Use this skill to convert a broad tattoo idea into a prompt that is visually specific enough for image generation or artist discussion.

## Core Objective

Build prompts that tell the image model exactly what to render, where it sits on the body, and what visual language it should follow.

## Gather The Minimum Inputs

Collect or infer these inputs before writing the final prompt:

- motif
- style
- placement
- scale
- mood or finish

## Workflow

1. Identify the motif.
2. Translate vague words into visual terms.
3. Identify or compare likely placements.
4. Identify the size or composition scope.
5. Add one mood or finish note.
6. Merge everything into one prompt line.
7. Generate variants when the idea is still broad.

## Prompt Formula

Use this structure:

`motif + tattoo style + placement + scale/composition + mood/finish`

Examples:

- `dragon tattoo, japanese style, forearm placement, vertical medium-size composition, powerful flowing movement`
- `semicolon tattoo, fine line, inner wrist placement, small minimalist design, delicate and clean`
- `angel statue tattoo, black and grey realism, upper back placement, large centered composition, solemn memorial mood`

## Rewrite Rules

- Replace broad words like `cool`, `nice`, or `meaningful` with visual instructions.
- Prefer body-aware placement language over generic composition language.
- Keep the subject count low. Do not overload the prompt with too many focal elements.
- If placement is missing, compare 2-3 likely placements instead of silently guessing one.
- If symbolism is mentioned, translate it into visible elements before expanding on meaning.
- If the idea is still broad, produce 3 variants:
  - safer or simpler
  - bolder or more visible
  - richer or more detailed

## Output Shape

Default output:

- one improved prompt
- two alternative prompt variants
- one short note on why the prompt is stronger and more renderable

If the user asks for more depth, also provide:

- a placement variant
- a style variant
- a smaller simpler variant

## Constraints

- Keep prompts visual.
- Avoid over-explaining symbolism unless the user explicitly asks.
- Keep the output useful for both AI generation and artist handoff.
- Favor concrete style language such as `fine line`, `blackwork`, `japanese`, `black and grey realism`, `neo traditional`, or `minimal`.

## Related Site

This skill pairs well with tattoo ideation workflows on:

- `https://www.inkforge.me/`
- `https://www.inkforge.me/placement`
