# Prompt Architecture

Use this reference to convert vague requests into ERNIE-Image-ready prompts. It adapts public ERNIE Image prompt-guide patterns into this skill's API workflow. Preserve exact visible text unchanged.

## Core Prompt Formula

Use the five-part base formula for most prompts:

1. Subject: who or what appears.
2. Action or context: what is happening and where.
3. Style: photography, anime, poster, UI, vector, oil paint, concept art, etc.
4. Lighting: direction, intensity, color temperature, mood.
5. Quality: detail level, lens or medium, sharpness, depth, finish.

For structured design tasks, append:

6. Composition: grid, rule of thirds, split screen, centered symmetry, foreground/background, negative space.
7. Exact text: quoted strings only, preferably short phrases or labels.
8. Spatial placement: title location, label position, relative item size, margins, contrast.

## Style Categories

### Photorealistic

Use for product shots, portraits, architecture, food, interiors, and documentary scenes. Include camera/lens, lighting source, material texture, depth of field, subject placement, and realistic shadows.

Template: `Photorealistic [shot type] of [subject] in [environment], [camera/lens/framing], [light direction and color], [materials/textures], [background depth], sharp detail, realistic shadows, natural proportions.`

### Anime & Manga

Use for anime characters, manga panels, fantasy illustration, stylized scenes, and comic storytelling. Specify era or visual language, linework, color/grayscale, facial features, hair, outfit, and panel framing.

Template: `[anime/manga style] illustration of [character] [action/context], [hair/eyes/outfit/distinctive features], [background], [linework/color treatment], [lighting], consistent character design.`

### Text in Image

Use for posters, product banners, cards, covers, signage, infographic labels, and UI-like graphics. Keep text short where possible; long paragraphs should become a title plus labels or numbered lines. Put exact text in quotes.

Template: `[design type] with exact text "[text]" at [position], [font weight/style], [text color], [background contrast], [alignment], [surrounding whitespace], readable typography, clean layout.`

### Concept Art

Use for sci-fi, fantasy, game environments, creatures, vehicles, maps, and cinematic worldbuilding. Specify the main focal element, scale cues, foreground/midground/background, lighting effects, atmosphere, and production-design style.

Template: `Cinematic concept art of [subject/world], [foreground element], [midground], [background], [scale cues], [lighting effect], [atmosphere], detailed production design, coherent spatial layout.`

### Abstract & Artistic

Use for fine art, generative visuals, posters, album-art style images, geometric compositions, and expressive aesthetics. Specify movement, medium, dominant/accent colors, texture, temperature, and surface treatment.

Template: `[art movement/medium] composition of [theme], [dominant colors] with [accent colors], [texture/surface], [shape language], [mood], balanced negative space, high visual coherence.`

### Layout & Composition

Use for banners, ads, comparison graphics, editorial layouts, multi-product scenes, split-screen designs, and structured design mockups. Specify item count, relative size, alignment, spacing, and reading order.

Template: `[layout type] with [number] elements arranged in [grid/split/rule-of-thirds], [main subject] at [position], [secondary elements] at [position], [spacing], [negative space], [reading order], clean alignment.`

## `use_pe` Strategy

Use `--use-pe` for short creative ideas where added detail helps: simple animals, mood images, broad concept art, atmospheric scenes, style exploration, or prompts missing lighting/material/composition.

Use `--no-use-pe` for exact text, bilingual labels, signs, flowcharts, UI text, strict poster layout, multi-panel comics, character consistency, or long prompts that already specify composition and style.

## ERNIE-Image Quality Gates

- Exact text must be inside quotes.
- Keep visible text under 8-10 words when possible. Split long copy into short labels or numbered lines.
- Multi-panel images must describe every panel separately, in order.
- Multi-object scenes must specify object count, relative position, relative size, and spacing.
- Product shots must specify product shape, material, camera angle, background, shadow, and label placement.
- UI or poster prompts must name title area, content area, call-to-action area, margins, and contrast.
- Exact text tasks should not depend on prompt enhancement. Use `--no-use-pe`.
- If the prompt contains both exact text and rich style, keep text/layout clauses early and style clauses late.

## Failure Diagnosis

| Failure | Fix |
|---|---|
| Misspelled text | Shorten text, quote it once, specify location and high contrast, use `--no-use-pe`. |
| Missing text | Move exact text earlier in the prompt and remove competing labels. |
| Layout drift | Use grid, split-screen, top/bottom, left/right, foreground/background, and relative size terms. |
| Character inconsistency | Repeat hair, outfit, colors, accessories, and distinctive features in each panel or variant. |
| Product deformation | Simplify scene, describe material and silhouette, remove unrelated props. |
| Style conflict | Choose one primary style and make the other a minor texture or accent. |
| Cluttered result | Reduce object count, add negative space, and say "avoid cluttered background". |
| Weak cinematic quality | Add light direction, lens/camera, atmosphere, texture, and depth cues. |

## Common Mistakes and Fixes

- Too vague: add subject, context, style, lighting, and composition.
- Conflicting styles: choose one primary style; use the second style only as a texture or accent.
- Text overload: reduce paragraphs to short phrases, labels, or numbered lines.
- Missing spatial context: specify foreground, background, left/right/top/bottom, spacing, and relative scale.
- Weak text rendering: quote the exact text, place it explicitly, and specify high contrast.
- Overcrowded layout: reduce object count and add negative space.

## Task Templates

### Poster

Create a [poster type] for [topic/product/event]. Place [main subject] at [position]. Add the exact title "[title]" at [position] with [font style, weight, color, size, contrast]. Add exact supporting text "[subtitle]" at [position]. Use [style], [palette], [lighting], clear hierarchy, readable typography, generous margins, and a balanced poster layout.

### Ecommerce Image

Create a product hero image for [product]. Put the product at [center/left/right] with [camera angle]. Show [features] as clean callouts with exact labels: "[label 1]", "[label 2]", "[label 3]". Use uncluttered background, accurate product shape, realistic materials, sharp edges, controlled shadows, and high-end commercial lighting.

### Infographic or Flowchart

Create a clean infographic titled "[exact title]" at the top. Arrange [number] steps [left-to-right/top-to-bottom/radial]. Each step contains a simple icon, a numbered marker, and exact label text: "[step 1]", "[step 2]", "[step 3]". Use aligned connectors, consistent spacing, high contrast, and readable bilingual or single-language typography.

### Comic or Storyboard

Create a [number]-panel comic/storyboard in a clear grid. For each panel, specify scene, character action, facial expression, camera framing, and exact dialogue. Keep character design, clothing, colors, scale, and panel order consistent. Use readable speech bubbles and clean panel borders.

### UI Screenshot Style

Create a high-fidelity UI screenshot style image of [app/page]. Use [device/window/frame], [navigation], [main content], [controls], and exact UI text: "[text]". Keep crisp typography, realistic interface density, aligned components, clean spacing, and no decorative clutter.
