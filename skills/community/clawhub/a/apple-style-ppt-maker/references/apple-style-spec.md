# Apple Minimal Presentation Spec

## Core Direction

Use a restrained keynote-like visual language:
- generous whitespace
- strict typographic hierarchy
- balanced alignment and margins
- low-noise surfaces with minimal decoration
- one accent color family per deck

Keep the design premium through consistency, not effects.

## Global Tokens (Deck Level)

Define once and reuse on every slide:
- `aesthetic`
- `palette.background`
- `palette.surface`
- `palette.text_primary`
- `palette.text_secondary`
- `palette.accent`
- `type_scale.h1`
- `type_scale.h2`
- `type_scale.body`
- `type_scale.caption`
- `spacing_scale`
- `layout_system`
- `motion_rule`

Do not drift these tokens between slides.

## Slide Composition Rules

- Keep one primary message per slide.
- Keep title and body blocks clearly separated.
- Use 2-column or 3-zone structures only when content justifies it.
- Keep visual focal point singular and obvious.
- Keep margins consistent and intentionally wide.

## Typography Rules

- Use short titles.
- Use concise bullets.
- Avoid dense paragraphs whenever possible.
- Keep line length readable.
- Maintain strong contrast between text and background.

## Visual Prohibitions

- avoid neon glow and cyberpunk gradients
- avoid dense texture overlays
- avoid multiple competing visual anchors
- avoid low-contrast text
- avoid decorative 3D clutter

## Data Slide Rules

- Prefer one key chart per slide.
- Keep chart labels minimal and legible.
- Keep annotation count low.
- Highlight only one key metric with accent color.

## Regeneration Rules

When regenerating one slide:
- preserve all deck-level tokens
- apply only the requested change
- do not modify other slide files
- snapshot old assets before overwrite
