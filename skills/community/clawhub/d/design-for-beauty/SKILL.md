---
name: design-for-beauty
description: Build or restyle interfaces with a curated library of bundled DESIGN.md references extracted from public websites. Use when the user asks for a landing page, dashboard, redesign, design system, UI polish, visual inspiration, or says things like "make it feel like Stripe/Apple/Linear/Notion", "参考某个品牌风格", "参考 DESIGN.md", or "give me 2-3 visual directions".
---

# Design For Beauty

Use this skill to turn real-world design references into implementation-ready UI direction.

The bundled references come from `awesome-design-md` and live under `references/design-md/`.
Do not read everything at once. Start from the catalog, shortlist, then load only the most relevant files.

## Start Here

1. Read `references/catalog.md`.
2. Pick 1-3 reference brands.
3. Open only the matching `references/design-md/<slug>/DESIGN.md` files.
4. Translate the chosen reference into project-specific decisions, not a blind clone.

## When To Use This Skill

- The user names a brand or product style: `Stripe`, `Apple`, `Linear`, `Notion`, `Airbnb`, `Tesla`.
- The user wants a visual direction without naming a brand: `premium minimal`, `editorial`, `developer-first`, `playful productivity`, `enterprise clean`.
- The user asks for a redesign, restyle, landing page, dashboard, design system, or front-end polish.
- The user wants multiple design directions and tradeoffs before implementation.

## Routing Rules

### If the user names a brand

- Treat that brand as the primary reference.
- Load its `DESIGN.md` directly.
- If the user names multiple brands, keep one primary reference for typography, spacing, and layout rhythm.
- Use at most one secondary reference for accent color, motion, or component mood unless the user explicitly asks for a broader blend.

### If the user gives only a vibe

- Search `references/catalog.md` first.
- Shortlist 2-4 references by category, tone, density, contrast, and interaction style.
- Then read only the 1-3 best matching `DESIGN.md` files.

### If the project already has a design system

- Preserve existing product patterns unless the user explicitly wants a rebrand.
- Borrow mood, spacing, contrast, or hierarchy instead of overwriting the whole system.

## Synthesis Workflow

### 1. Extract the reference system

Pull out the parts that actually matter for implementation:

- visual atmosphere
- color roles and contrast pattern
- typography hierarchy and font character
- spacing, radius, borders, and elevation
- component behavior
- layout density and page rhythm
- do/don't constraints

### 2. Adapt to the real project

- Keep the product's content model, IA, and accessibility requirements.
- If a reference uses proprietary fonts or art direction, emulate the rhythm with available substitutes and say so.
- Preserve focus states, semantic HTML, readable contrast, and reasonable touch targets.
- Favor project fit over pixel mimicry.

### 3. Produce implementation-ready output

Depending on the task, convert the reference into one or more of these:

- a concise design brief
- a shortlist of directions with tradeoffs
- CSS variables / design tokens
- component styling rules
- actual front-end code

## Conflict Resolution For Multi-Reference Blends

- Primary reference owns typography, spacing, and structural rhythm.
- Secondary reference may influence color, imagery, or motion.
- Tertiary influence should be minor and explicit.
- If the blend starts to feel incoherent, simplify back to one primary direction.

## Deliverable Checklist

Before you finish, make sure you:

- name which references you used
- identify the primary reference
- call out any font or asset substitutions
- keep the output accessible and product-appropriate
- preserve the strongest "do" and avoid the biggest "don't" from the reference

## File Map

- `references/catalog.md` - human-readable index of all references
- `references/catalog.json` - machine-readable index
- `references/design-md/<slug>/DESIGN.md` - full design reference files

## Search Tips

```bash
rg -n "monochrome|gradient|editorial|premium|dashboard|developer|playful" references/catalog.md
```

## Example Requests

- "Use Stripe as the base direction for this pricing page."
- "Give me 3 directions for an AI developer tool: one like Linear, one like Vercel, one like Apple."
- "参考 Notion 和 Airtable，做一个更温和的 B2B 数据产品首页。"
