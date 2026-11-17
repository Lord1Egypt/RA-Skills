# Editorial Design System

This rule translates useful design lessons from magazine-style and Swiss-style slide systems into WeChat cover production. It is an inspiration protocol, not a template import.

Source inspiration should remain generic and portable. Treat external magazine-style or Swiss-style slide systems as design references only; do not depend on a local installation path, repository checkout, or runtime file from another skill.

## Non-Copy Boundary

- Do not copy HTML templates, CSS class names, shader code, slide layout IDs, or assets from the source project.
- Do not include source attribution text inside generated covers, images, or user-facing visual artifacts.
- Use only abstracted principles: grid discipline, theme presets, type scale, image-slot discipline, and quality checks.

## Cover Style Families

### editorial-ink

Use for cultural essays, reflective articles, bookish topics, personal columns, and slow media.

Principles:

- serif or editorial headline mood
- warm paper background or low-noise photographic background
- restrained ink palette
- strong negative space
- one clear visual metaphor
- title block aligned to a stable axis

### swiss-grid

Use for AI, technology, product, design, data, research, business analysis, and explainer covers.

Principles:

- sans-serif headline mood
- strict grid and axis
- high contrast between paper, ink, and one accent color
- hairline dividers instead of decorative frames
- large number or short phrase only when it is source-grounded
- no gradients, shadows, rounded decorative cards, or arbitrary color mixing

## Theme Presets

These are cover-level style tokens, not copied CSS variables.

### editorial-ink presets

| preset | ink | paper | use case |
|---|---|---|---|
| ink-classic | deep black | warm off-white | default editorial covers |
| indigo-porcelain | deep indigo | cool porcelain | tech, research, data |
| forest-ink | forest green | ivory | nature, culture, non-fiction |
| kraft-paper | dark brown | kraft beige | history, books, nostalgia |
| dune-gallery | charcoal | sand | art, design, brand essays |

### swiss-grid presets

| preset | base | accent | use case |
|---|---|---|---|
| ikb-blue | warm white + black | International Klein Blue | AI, technology, design |
| lemon-yellow | warm white + black | lemon yellow | youth, retail, energy |
| highlighter-green | warm white + black | highlighter green | future, sustainability, emerging tech |
| safety-orange | warm white + black | safety orange | industrial, warning, decision points |

## Layout Discipline

For cover prompts and typography specs, always declare:

- `cover_design_family`: `editorial-ink` or `swiss-grid`
- `theme_preset`
- `grid_axis`: left, right, center-top, or split
- `title_safe_zone`: percentage box, normally 35%-45% width or a clean central block
- `image_role`: evidence, atmosphere, metaphor, product, portrait, or abstract system
- `text_weight_plan`: headline, subtitle, metadata if any

## Typography Rules

- Bigger text should be lighter in weight; smaller labels should be heavier for legibility.
- Chinese cover titles longer than 16 characters should be rewritten into title + subtitle.
- Do not solve overcrowding by shrinking text below mobile readability.
- Keep kicker / metadata above or near the title block; do not split kicker and title into unrelated axes.
- Avoid more than two type moods in one cover.

## Image-Slot Rules

- Images serve a function: evidence, real subject, atmosphere, metaphor, or product context.
- Do not use images as random decoration.
- Product, screenshot, and diagram covers should keep the subject inspectable.
- Avoid rounded frames, heavy shadows, and ornamental borders for swiss-grid.
- Editorial-ink can use photographic atmosphere, but the title area must remain clean.

## Quality Checks

- Is the design family declared and appropriate to the article?
- Is there exactly one accent strategy?
- Does the title safe zone survive mobile thumbnail viewing?
- Is the image role clear and source-aligned?
- Are there any copied source templates, class names, visual signatures, or layout IDs?
- Does the result look like a publishable WeChat cover rather than a slide screenshot?
