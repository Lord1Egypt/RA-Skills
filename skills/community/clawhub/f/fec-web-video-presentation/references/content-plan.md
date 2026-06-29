# Content Plan

## Script

Use the same language as the source material unless the user asks otherwise. Convert written text into spoken wording, but keep the author's claims, order, names, and important numbers intact.

For every script:

- Keep one idea per beat.
- Remove footnote-like detours unless they are central to the story.
- Mark uncertain facts instead of smoothing them into confident claims.
- Keep technical names exact.
- Prefer short sentences that can be spoken without rereading.

## Outline

The outline is the implementation contract for the web presentation.

Include:

- Title and intended audience.
- Total target duration.
- Chapters with stable ids.
- Step count per chapter.
- One screen task per step.
- Content pool per chapter: facts, numbers, quotes, examples, media, diagrams, or UI states available for visuals.
- Asset list with owner, path, missing status, and replacement strategy.

Avoid:

- Naming concrete animations too early.
- Specifying CSS implementation details.
- Stuffing several list items into one step when they need separate attention.
- Adding unsupported claims just to make a scene feel full.

## Acceptance

A content plan is ready when another implementer can build the presentation without deciding what each chapter says, what each step reveals, or which source facts are available for visuals.
