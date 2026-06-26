---
name: design-md-generator
description: Generate DESIGN.md files from any website URL. Extracts the complete visual design system — colors, typography, spacing, components, shadows — into a structured markdown document that AI coding agents can read to produce pixel-perfect, visually consistent UI. Use when asked to "extract design system", "generate DESIGN.md", "capture the look of a website", "create a design spec from URL", or "reverse-engineer a site's visual language". Based on the Google Stitch DESIGN.md format.
---

# Design MD Generator

Generate structured DESIGN.md files from any website URL. The output follows the [Google Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/format/) with 9 standard sections.

## Workflow

### Step 1: Capture the site

Use the browser tool to load the target URL and take a screenshot:

```
browser action=navigate url="<TARGET_URL>"
browser action=screenshot
browser action=snapshot
```

### Step 2: Extract CSS tokens

Run the extraction script to pull all design tokens from the page's computed styles:

```bash
# From the skill directory
node {baseDir}/scripts/extract-tokens.js "<TARGET_URL>"
```

The script outputs a JSON file with:
- All unique colors (background, text, border, accent)
- Font families, sizes, weights, line-heights, letter-spacing
- Border radii, shadows, spacing values
- Component patterns (buttons, cards, inputs)

### Step 3: Generate DESIGN.md

Using the extracted tokens + screenshot for visual context, write a DESIGN.md with these 9 sections:

| # | Section | What to capture |
|---|---------|----------------|
| 1 | **Visual Theme & Atmosphere** | Mood, density, design philosophy. Write like an art director describing the aesthetic. |
| 2 | **Color Palette & Roles** | Every color with semantic name + hex + functional role. Group by: Brand, Background, Text, Semantic, Border. |
| 3 | **Typography Rules** | Font families with fallbacks. Full hierarchy table: role, font, size, weight, line-height, letter-spacing. |
| 4 | **Component Stylings** | Buttons (primary/secondary/ghost), Cards, Inputs, Navigation, Badges — with all states (default, hover, active, disabled). |
| 5 | **Layout Principles** | Spacing scale table, grid system, max-width, column count, whitespace philosophy. |
| 6 | **Depth & Elevation** | Shadow system table (flat → raised → floating → overlay). Surface hierarchy list. |
| 7 | **Do's and Don'ts** | Design guardrails. What makes this design system unique and what breaks it. |
| 8 | **Responsive Behavior** | Breakpoints table, touch targets, collapsing strategy for nav/grids/typography. |
| 9 | **Agent Prompt Guide** | Quick color reference block + 2-4 ready-to-use prompts for common page types. |

### Writing Guidelines

- **Be specific**: Use exact hex values, px sizes, font weights — not "dark blue" or "large text"
- **Be opinionated**: Describe the atmosphere like a design critic, not a spec sheet
- **Name colors semantically**: "Lobster Coral" not "Red 1", "Deep Sea" not "Background Dark"
- **Include states**: Every interactive component needs default + hover + active + focus states
- **Show hierarchy**: List surfaces from darkest to lightest, text from brightest to dimmest
- **Agent-ready prompts**: Write Section 9 prompts that another AI agent can copy-paste to build matching UI

### Output

Save the generated file as `DESIGN.md` in the target location specified by the user.

Optionally generate:
- `preview.html` — A visual catalog page showing color swatches, type scale, and component samples
- `preview-dark.html` — Same catalog on dark surface

## Reference

See `references/format-spec.md` for the complete section-by-section format specification with examples.

See `references/example-linear.md` for a high-quality example (Linear's DESIGN.md).
