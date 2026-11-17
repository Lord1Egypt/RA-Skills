---
name: fec-tailwind-design-system
description: Use when designing, implementing, or reviewing Tailwind CSS design systems, token mapping, theme extension, utility class governance, component variants, dark mode, responsive utilities, safelists, or maintainable class composition; Chinese triggers include Tailwind, design Token, component variants, dark mode, class management.
---

#Tailwind Design System

Suitable for front-end tasks hosting product design systems, component variations, and theme rules with Tailwind CSS. Load [references/tailwind-system-patterns.md](references/tailwind-system-patterns.md) when specific configuration, variant, class organization and migration details are needed.

## Purpose

Make the tokens, themes, component variations, and responsive styles in the Tailwind project maintainable instead of scattering one-off utility classes into business code.

## Procedure

1. Identify the current situation: Confirm Tailwind version, configuration location, dark mode strategy, component library, CSS variables, design token and class merging tool.
2. Establish token boundaries: color, spacing, rounded corners, shadow, font, z-index and breakpoints are first derived from the project token or `theme.extend`.
3. Design component variants: Basic components such as buttons, input boxes, cards, pop-up windows, and tables use centralized variant APIs to express size, semantics, status, and density.
4. Control class complexity: Repeated combinations are precipitated into components, slots, variants or local helpers; do not copy long class strings to multiple pages.
5. Handle themes and dark modes: Explicit `class`, `data-theme` or CSS variable schemes to avoid first render flickering and contrast regression.
6. Access responsiveness: mobile-first organization utility; leave complex layouts to responsive layout workflow, don’t just rely on stacked breakpoint prefixes to try your luck.
7. Verify style results: check hover, active, focus-visible, disabled, loading, selected, invalid, dark and different breakpoints.

## Constraints

- Don't think of the Tailwind class as the design system itself; the real system is the token, component API, state matrix, and usage constraints.
- Do not expand global tokens arbitrarily for a single page; new tokens must have semantic names and reuse scenarios.
- Do not use spliced dynamic classes to break build scans; use safelist, mapping table or variant tools when necessary.
- Do not override base component internals outside the component to implement variations.
- Don't let dark mode rely solely on inverse colors; status colors, borders, shadows, charts, and images are all re-examined.

## Expected Output

Output Tailwind token mapping, theme configuration boundaries, component variant design, class reuse strategy, dark mode and responsive validation results. After completion, the style should be reusable by project components, searchable, testable, and consistent with the design system rules.
