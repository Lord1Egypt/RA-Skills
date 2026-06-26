---
name: aesthetic-copilot
description: Use when the user wants to generate high-fidelity PROMPTS for Text-to-Image models (Flux, Ideogram, Midjourney) based on vague layout/content descriptions.
---

# Aesthetic Copilot (v3.4 - Integrated)

## Overview
This skill acts as a **Meta-Prompt Generator**. It translates a user's vague idea into a **professional, commercial-grade image generation prompt** optimized for models like Flux, Ideogram, and Midjourney v6.

## File Map (MANDATORY READ ORDER)

| File | Role | When to Read |
|------|------|--------------|
| `SKILL.md` | This file — entry point | Always |
| `engine/README.md` | Content Classification Logic | Step 1 (Analyze) |
| `styles/premium/master-collection.md` | The Vault: Premium Styles | Step 2 (Style Selection) |
| `styles/apple-minimal.md` | Apple Minimal detail spec | When `apple-minimal` or `apple-pro` is selected |
| `styles/neo-brutalism.md` | Neo-Brutalism detail spec | When `neo-brutalism` is selected |
| `styles/warm-academia.md` | Warm Academia detail spec | When `warm-academia` is selected |
| `styles/cyber-glass.md` | Cyber Glassmorphism detail spec | When `cyber-glass` is selected |
| `styles/nature-organic.md` | Organic Nature detail spec | When `nature-organic` is selected |
| `engine/style-mixer.md` | Randomization & Conflict Logic | Step 3 (Dice Roll) |
| `engine/micro-innovation.md` | Artistic Twists | Step 4 (Innovation) |
| `layouts/README.md` | Layout Templates | Step 5 (Layout Selection) |
| `prompt-templates/*.md` | Output Skeletons | Step 6 (Generate) |

---

## The Workflow (Strict Execution Path)

### Step 1 — Analyze & Classify Intent
**Action**: Read `engine/README.md`.
Apply its classification logic to extract:
- **Keywords** from the user's input
- **Sentiment / Mood** (Warm, Playful, Serious, Futuristic…)
- **Industry** (Tech, Fashion, Education, Food…)
- **Attribute scores**: `formal_level`, `color_temp`, `contrast`, `complexity`

Use these attributes to drive all downstream decisions.

### Step 2 — Select Base Style
**Action**: Read `styles/premium/master-collection.md`.
Match the attributes from Step 1 to the closest style ID.

- If the matched style is `apple-minimal` or `apple-pro` → also read `styles/apple-minimal.md` for detail tokens.
- If the matched style is `neo-brutalism` → also read `styles/neo-brutalism.md` for detail tokens.
- If the matched style is `warm-academia` → also read `styles/warm-academia.md` for detail tokens.
- If the matched style is `cyber-glass` → also read `styles/cyber-glass.md` for detail tokens.
- If the matched style is `nature-organic` → also read `styles/nature-organic.md` for detail tokens.
- **Fallback**: If no confident match, default to `apple-pro`.

### Step 3 — Roll the Dice (Mixer)
**Action**: Read `engine/style-mixer.md`.
Randomly select (do NOT default to first item):
- ONE **Material Twist** from Pool A
- ONE **Lighting Modifier** from Pool B
- ONE **Composition Rule** from Pool C

Apply the **Harmony & Conflict Resolution** rules before proceeding.

### Step 4 — Inject Micro-Innovation
**Action**: Read `engine/micro-innovation.md`.
- Find the **Input Category** that matches the user's subject.
- Apply the corresponding **Twist** (not the standard depiction).
- Determine the **Text Integration** method (Embossed / Neon / Integrated / Masked).

### Step 5 — Select Layout
**Action**: Read `layouts/README.md`.
Match the user's description to a Layout ID:

| User Intent | Layout ID |
|-------------|-----------|
| "Top banner + columns", info layout | `hero-split` |
| "Left menu / sidebar" | `sidebar-fixed` |
| "Pinterest style", photo wall | `masonry-grid` |
| "Magazine cover", event poster | `poster-zine` |
| "Phone app", Instagram feed | `mobile-feed` |

Pass the selected Layout ID into the template as `[Layout]`.

### Step 6 — Route to Template
Select the correct template based on the classified intent from Step 1:

| Intent | Template |
|--------|----------|
| Magazine / Fashion / Editorial | `prompt-templates/editorial-spread.md` |
| Product / Object / Commercial | `prompt-templates/product-showcase.md` |
| Dream / Abstract / Surreal | `prompt-templates/surreal-concept.md` |
| Informational / Default | `prompt-templates/structural-poster.md` |

**Action**: Read the selected template file, then fill it with all values accumulated in Steps 1–5.

---

## Output Format

Return the final result wrapped in a single plaintext code block:

~~~markdown
**🎨 Aesthetic Copilot: Generated Prompt**

> **Template**: [Selected Template Name]
> **Style DNA**: [Base Style] + [Material Twist] + [Lighting Modifier]
> **Layout**: [Layout ID] — [Layout Name]
> **Concept**: [One sentence explaining the Micro-Innovation twist]

```
[Filled prompt content from the selected template]
```
~~~

---

## Anti-Patterns

- **Do not** use `structural-poster` for everything — route correctly in Step 6.
- **Do not** pick the first item in the Mixer pools — randomize.
- **Do not** skip Step 1 — content classification drives all downstream choices.
- **Do not** skip Step 5 — layout selection must be passed into the template.
- **Do not** use vague style guesses — always read `master-collection.md` first.
