# Modern Clean — Design Brief

## Visual Identity

Modern Clean is the design equivalent of a well-organized desk — fresh, approachable, and quietly competent. It uses a vibrant indigo-to-pink gradient as its signature accent while keeping surfaces clean and uncrowded. The style prioritizes content clarity and ease of use over decorative flair.

## Core Design Language

**Colors**: The palette centers on cool indigo (#6366F1) as the primary action color, with a vibrant pink (#EC4899) as a secondary accent for emphasis and delight. Backgrounds use near-white slate tones rather than pure white — this subtle warmth prevents the "sterile hospital" feeling. Text is high-contrast slate-900 on light surfaces.

**Shapes**: Rounded corners are a defining characteristic. Cards use 8px radius, buttons use 8px, and larger containers use 12-16px. Nothing has sharp corners except code blocks and tables. This softness makes the interface feel approachable and modern.

**Shadows**: Subtle and layered. Shadows should be barely perceptible — suggest depth without shouting about it. The largest shadow is used only for modals and dropdowns. Cards use a gentle 4px Y-offset with low opacity (7-8%).

**Typography**: Inter is the primary typeface — it's the most versatile sans-serif for UI work, with excellent readability at small sizes and strong personality at display sizes. Headings use semibold weight (600), body text uses regular (400). The scale is tight — skip sizes are minimal, creating a harmonious rhythm.

**Motion**: Quick and purposeful. Hover states transition in 150ms, page transitions in 200-300ms. Use ease-in-out for most interactions. Buttons can have a subtle spring effect on hover (scale 1.02). Nothing should feel sluggish.

## Key Visual Signatures

1. **Gradient accent**: The primary button and key decorative elements use the indigo-to-purple-to-pink gradient. This is the most recognizable visual signature.

2. **Card hover lift**: Cards should lift slightly on hover (translateY -2px) with an increased shadow. This micro-interaction makes the interface feel responsive and alive.

3. **Soft focus rings**: Input focus states use a soft indigo ring (2px, opacity 40%) rather than the browser default. This feels modern and intentional.

4. **Badge and pill design**: Badges use fully rounded corners (9999px) with subtle background tints — success badges are a light green, not full saturation green.

## When to Adapt

- **Data-heavy dashboards**: Tighten the spacing scale, reduce card padding
- **Marketing pages**: Open up the spacing, use larger heading sizes, add more gradient decorative elements
- **Mobile-first**: Maintain the same color and radius tokens but simplify shadows (fewer layered shadows on mobile)
- **Dark mode pending**: If the user asks for dark mode, invert the background/text scale while keeping the primary gradient intact

## Anti-Patterns (avoid these)

- Don't use sharp corners anywhere except code blocks
- Don't use bright pure-white (#FFFFFF) backgrounds — always shift to slate-50 or similar
- Don't add strong/bright shadows — modern style uses subtle elevation
- Don't use serif fonts — this style is distinctly sans-serif
- Don't over-animate — motion is subtle and functional, never decorative
