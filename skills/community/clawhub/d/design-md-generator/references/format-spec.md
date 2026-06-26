# DESIGN.md Format Specification

Based on the Google Stitch DESIGN.md format. Each section has a specific purpose and structure.

## Section 1: Visual Theme & Atmosphere

**Purpose:** Set the overall mood and design philosophy in rich, descriptive prose.

**Structure:**
- Opening paragraph: 3-5 sentences describing the overall feel, like an art director's brief
- Typography description: what fonts are used and why they create the intended feel
- Color philosophy: how color is used (sparingly? vibrantly? monochromatically?)
- Key Characteristics: bullet list of 7-10 specific technical traits

**Example opening:**
> Linear's website is a masterclass in dark-mode-first product design — a near-black canvas (#08090a) where content emerges from darkness like starlight.

**Tone:** Opinionated, descriptive, almost poetic. Not a spec sheet — a design critique.

## Section 2: Color Palette & Roles

**Purpose:** Document every color with context about WHERE and WHY it's used.

**Structure:** Group colors by function:
- Brand & Accent (1-3 colors)
- Background Surfaces (3-5 levels, darkest to lightest)
- Text & Content (3-4 levels, brightest to dimmest)
- Semantic (success, warning, danger, info)
- Border & Divider (2-4 variants)
- Overlay & Special

**Format per color:**
```markdown
- **Semantic Name** (`#hex`): Description of where and why this color is used. Be specific about context.
```

**Name colors evocatively:** "Deep Sea" not "Dark Background", "Lobster Coral" not "Red Accent".

## Section 3: Typography Rules

**Purpose:** Complete font family specification + hierarchy table.

**Must include:**
- Font Family section with full fallback stacks
- OpenType features if any
- Hierarchy table with columns: Role | Font | Size | Weight | Line Height | Letter Spacing | Notes

**Table should cover:** Display/Hero → H1 → H2 → H3 → Body Large → Body → Body Small → Label → Code

## Section 4: Component Stylings

**Purpose:** Document every reusable component with all visual states.

**Components to cover:**
- Buttons (Primary, Secondary, Ghost/Tertiary) with states: default, hover, active, focus, disabled
- Cards with border, shadow, padding, radius
- Code blocks with syntax color tokens
- Navigation (desktop + mobile)
- Inputs with focus states
- Badges/Pills with variants

**Include exact values:** background, text, border, radius, padding, shadow, transition duration.

## Section 5: Layout Principles

**Purpose:** Spacing system, grid, and whitespace philosophy.

**Must include:**
- Spacing scale table (token → px value → usage)
- Grid system (max-width, columns, gutter)
- Card grid pattern (CSS Grid auto-fill spec)
- Whitespace philosophy paragraph

## Section 6: Depth & Elevation

**Purpose:** Shadow system and surface layer hierarchy.

**Structure:**
- Shadow system table: Level → Shadow CSS → Usage
- Surface hierarchy: numbered list from deepest to highest, with hex + purpose
- Backdrop effects for modals and sticky nav

## Section 7: Do's and Don'ts

**Purpose:** Design guardrails — what makes this system unique and what breaks it.

**Format:** Two lists with ✅ Do's and ❌ Don'ts
- 5-8 items each
- Each item explains WHY, not just WHAT
- Focus on what's unique about THIS system

## Section 8: Responsive Behavior

**Purpose:** How the design adapts across screen sizes.

**Must include:**
- Breakpoints table: Name → Width → Behavior
- Touch target minimums (44px for WCAG)
- Collapsing strategy for: navigation, card grids, sidebars, hero text, code blocks

## Section 9: Agent Prompt Guide

**Purpose:** Make the DESIGN.md immediately actionable for AI agents.

**Must include:**
- Quick Color Reference: a compact code block with the 10-12 most important colors
- Ready-to-Use Prompts: 2-4 complete prompts for common page types (landing, dashboard, docs, etc.)

**Prompt format:** Each prompt should be a complete paragraph that an agent can copy-paste and get a matching result.
