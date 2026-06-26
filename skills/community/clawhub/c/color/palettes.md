# Palette Construction

## Core Rule

- Build palettes as relationships and roles, not as a pile of nice-looking swatches.

## Start With Neutrals

- Neutrals define most backgrounds, text, dividers, shadows, surfaces, and quiet UI.
- If the neutral ladder is weak, the accent color has to do too much work.
- Slightly tinted neutrals often feel more intentional than pure grayscale, but keep the tint subtle.
- Validate neutrals in both light and dark themes before choosing accents.

## Accent Strategy

- One primary accent plus one support accent is enough for many systems.
- Add more accents only when the product truly needs more semantic or brand range.
- Accents should differ in role, not only in hue.
- If every feature team gets its own accent, hierarchy collapses fast.

## Build From References Without Becoming Their Prisoner

- Extracting colors from a logo, screenshot, product photo, or moodboard is a strong starting move, not the final palette.
- Keep the anchor hues that carry recognition, then rebuild ramps and neutrals for usability.
- Reference extraction often over-represents loud colors and under-represents the muted support colors the system actually needs.
- If the source image has lighting or texture bias, correct for that before promoting the extracted colors into tokens.

## Tonal Ramps

- Build at least a usable light-to-dark ladder for the primary and neutral families.
- Use consistent lightness steps rather than random manual picks.
- A ramp should support backgrounds, borders, fills, text, and focus rings without jumping unpredictably.
- If a ramp only works at 500 and 600, it is not a real ramp yet.

## Common Palette Archetypes

| Pattern | Best for | Risk |
|---------|----------|------|
| Neutral + one accent | Most product UI | Can feel flat if neutrals are weak |
| Split complementary | Marketing and editorial work | Easy to over-accent |
| Analogous | Calm, cohesive systems | Categories blur together fast |
| Monochrome with value contrast | Premium or minimal systems | Needs strong typography and spacing |
| Neutral + semantic states | SaaS and dashboards | Brand expression may feel too quiet |

## 60-30-10 as a Sanity Check

- Use it as a balance check, not a law.
- Most of the interface should be carried by neutrals and surfaces.
- Secondary areas need enough distinction to organize layout without shouting.
- Small accents create focus precisely because they are scarce.

## Palette Review Questions

- Which colors are structural, and which are expressive?
- Which colors carry text, and are they safe for that role?
- Which colors need dark-mode variants?
- Which colors need print-safe versions?
- Which colors become confusing when disabled, tinted, or shown over images?

## Common Palette Traps

- Designing only the hero swatches and leaving ramps undefined.
- Adding accent colors because the palette "feels boring" instead of fixing hierarchy.
- Copying a trendy palette that does not match the domain or brand.
- Using the same accent for calls to action, info states, and chart categories.
- Forgetting that neutral quality determines whether a palette feels polished.
