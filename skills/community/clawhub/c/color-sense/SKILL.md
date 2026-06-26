---
name: color-sense
description: Generate usable color systems for creative and design work. Use when the user asks for a palette, color direction, visual mood through color, brand/UI/poster/illustration/data-viz color planning, accessibility-aware color choices, or help translating an emotion or concept into specific HEX/RGB color recommendations.
---

# Color Sense

Generate a practical color system, not just a list of pretty colors.

## Ask for the minimum useful input

Accept a short request, but when needed clarify:
- use case: UI, brand, poster, illustration, photography grade, data visualization
- target mood: calm, premium, playful, energetic, trustworthy, nostalgic
- constraints: existing brand color, must-use or avoid colors, light/dark mode
- accessibility needs: WCAG contrast, color-blind friendliness, print concerns

If the user gives very little detail, make explicit assumptions instead of blocking.

## Output

### 1. Palette overview
- palette name
- intended use case
- emotional summary in 1-2 lines

### 2. Core palette
Provide 5-7 colors with a clear role for each:
- primary
- secondary
- accent
- neutral dark
- neutral light
- background
- optional status or data colors

For each color, provide:
- HEX
- RGB
- approximate CMYK when relevant
- role explanation

### 3. Usage system
Explain:
- suggested ratio such as 60/30/10
- where each color should appear
- hierarchy rules
- what should be rare vs dominant

### 4. Color logic
Explain the palette strategy in plain language:
- monochromatic, analogous, complementary, split complementary, triadic, etc.
- why it fits the requested mood and medium

If you need theory details or contrast reminders, read `references/color-harmony.md`.

### 5. Variants
When helpful, include:
- light version
- dark version
- muted version
- high-contrast version

### 6. Accessibility check
Include:
- estimated contrast notes for key pairs
- likely WCAG level when reasonably inferable
- color-blind friendliness risks
- safer alternatives if needed

Do not pretend to have exact computed contrast if you did not calculate it. Say “estimated” when needed.

### 7. Avoid list
Call out:
- combinations likely to fail in the requested context
- overused clichés
- readability or print risks

### 8. Implementation hints
Adapt to the medium:
- UI: buttons, surfaces, states, charts
- brand: hero color, support palette, usage boundaries
- illustration/poster: focal accents, shadow bias, atmosphere support
- photography: grading direction and highlight/shadow color bias

## Quality bar
Deliver palettes that are:
- specific
- explainable
- easy to apply
- not overly generic

Prefer one strong palette plus 1-2 alternates over many weak options.

## Boundaries

Do:
- translate mood into usable color systems
- provide concrete color values and roles
- discuss accessibility and practical tradeoffs

Do not:
- claim print-perfect accuracy
- pretend subjective taste is objective truth
- replace a full brand identity process
