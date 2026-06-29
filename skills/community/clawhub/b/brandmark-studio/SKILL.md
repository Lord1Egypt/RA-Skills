---
name: brandmark-studio
version: "1.0.0"
description: "Professional brand identity designer for SVG logos, icons, brandmarks, and complete visual identity systems. Use when the user asks for logos, icons, app icons, favicons, monograms, emblems, badges, icon packs, or brand identity design."
---

# Brandmark Studio

Use when the user requests brand identity assets, logos, icons, favicons, app icons, monograms, emblems, badges, or icon packs. Combines brand strategy, visual identity design, and SVG engineering into a production-ready workflow.

## Triggers

- Logo, SVG logo, or "make me a logo"
- Icon, app icon, favicon, or avatar
- Brand mark, monogram, emblem, or badge
- Icon pack or icon system
- Brand identity or visual identity
- "Design a brandmark" or similar

## Workflow

### Step 1: Discovery

Collect or infer from the user request:

| Field | Source |
|-------|--------|
| Brand name | User request or infer from context |
| Industry | User request or infer |
| Description | User request or infer from name/industry |
| Target audience | User request or infer |
| Desired style | User request or default to Modern/Minimalist |
| Secondary style | User request or none |
| Archetype | User request or infer from brand personality |
| Asset type | User request or default to `logo` |

**Supported asset types:** `logo`, `icon`, `logo_and_icon`, `icon_pack`, `favicon`, `app_icon`, `avatar`, `badge`, `emblem`, `monogram`

If information is missing, infer reasonable defaults. Do not ask the user to fill out a form unless critical details are ambiguous.

### Step 2: Strategy

Generate an internal design brief. Load `references/design-principles.md` and `references/archetypes.md` to inform selections.

- **Brand goals**: What the mark must communicate
- **Emotional goals**: Feeling the audience should have
- **Audience**: Who will see this mark
- **Brand positioning**: Where the brand sits in its space
- **Visual metaphors**: Concrete symbols that map to abstract brand values
- **Style direction**: Primary + secondary style blend (load `references/styles.md`)
- **Archetype alignment**: How the chosen archetype shapes the design (load `references/archetypes.md`)

Select **2–4 design principles**. Explain why each principle supports this specific design.

### Step 3: Concept Generation

Load `references/concept-generation.md`, `references/archetypes.md`, and `references/design-principles.md`.

Generate **three significantly different concepts**. Do not generate cosmetic variations of the same idea.

Each concept includes:
- **Name**: Short, memorable concept title
- **Symbolism**: What the visual elements represent
- **Composition**: Layout and structure
- **Design principles used**: Which principles from Step 2 apply
- **Strengths**: Why this concept works
- **Risks**: Where it might fail
- **Recommended use cases**: Best fit scenarios

### Step 4: Asset Creation

Load `references/svg-rules.md` and `references/asset-types.md`.

Generate production-ready SVG assets for the chosen concept (or all three if the user wants options).

**Scalability check:** Asset must remain recognizable at 16×16, 32×32, 64×64, and 512×512.

**Possible deliverables:** Master SVG, Horizontal SVG, Stacked SVG, Icon SVG, Favicon SVG, App Icon SVG, Avatar SVG, Monochrome SVG, Reverse SVG. Generate only what the asset type requires.

### Step 5: Icon Simplification Engine

Load `references/icon-simplification.md` and `references/svg-rules.md`.

When a logo or brandmark is created, automatically generate simplified icon versions. Generate: Icon SVG, Favicon SVG, Avatar SVG, App Icon SVG. Each must be recognizable at favicon size (16×16).

### Step 6: Quality Review

Load `references/quality-review.md`.

Evaluate the final mark across seven dimensions. Score 1–10 for each. If overall score < 8.0, recommend refinement or regeneration with specific notes.

## Reference Loading Map

| Task | Load |
|------|------|
| Logo generation | `styles.md`, `archetypes.md`, `design-principles.md`, `svg-rules.md`, `asset-types.md` |
| Icon generation | `styles.md`, `svg-rules.md`, `icon-simplification.md`, `asset-types.md` |
| Quality review | `quality-review.md` |
| Concept generation | `concept-generation.md`, `archetypes.md`, `design-principles.md` |
| Icon pack | `styles.md`, `svg-rules.md`, `icon-packs.md`, `asset-types.md` |
| Favicon/app icon | `svg-rules.md`, `icon-simplification.md`, `asset-types.md` |

## Output Requirements

Always explain:
- Design rationale
- Symbolism
- Selected design principles
- Style choices
- Archetype influence

Focus on producing production-ready SVG output while teaching the user why the design works.

## Constraints

**Avoid:**
- Clipart aesthetics
- Photorealism
- Excessive path counts
- Excessive gradients
- Decorative complexity
- Details that fail at favicon size

**Prioritize:**
- Scalability
- Memorability
- Simplicity
- Strong silhouettes
- SVG compatibility
- Brand relevance
- Effective negative space
