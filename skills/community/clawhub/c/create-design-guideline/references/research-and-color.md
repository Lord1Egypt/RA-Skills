# Research and color

Read this for palette, theme, token, or color-accessibility decisions. Verify current pages before citing them. Keep standards, product policies, and aesthetic interpretation distinguishable.

## Evidence and method

Record each retained reference as `source → observed method → project decision`. Prefer a few relevant sources over a gallery of links. Check reuse terms when adopting code, fonts, or assets; studying a reference and reusing its implementation are different decisions.

Useful primary sources:

- [Radix Colors — Understanding the scale](https://www.radix-ui.com/colors/docs/palette-composition/understanding-the-scale): backgrounds, states, boundaries, solid fields, and text have separate jobs. A 12-step scale is a method, not a quota. Bright sky, mint, lime, yellow, and amber fields use dark foregrounds.
- [Radix Colors — Composing a palette](https://www.radix-ui.com/colors/docs/palette-composition/composing-a-palette) and [Aliasing](https://www.radix-ui.com/colors/docs/overview/aliasing): combine appropriate neutral, brand, and status families, then expose semantic roles.
- [Adobe Spectrum — Color fundamentals](https://spectrum.adobe.com/page/color-fundamentals/): account for perception, simultaneous contrast, adaptation, and gamut. HSL is not perceptually uniform.
- [CSS Color 4 — Oklab and OkLCh](https://www.w3.org/TR/css-color-4/#ok-lab): control lightness, chroma, and hue perceptually. For out-of-gamut values, use a documented mapping method and inspect the actual sRGB fallback.
- [IBM Carbon — Color](https://carbondesignsystem.com/elements/color/overview/) and [Color tokens](https://carbondesignsystem.com/elements/color/tokens/): separate role, token, theme, and value; study how surface hierarchy changes across themes.
- [Atlassian — Design tokens](https://atlassian.design/foundations/tokens/design-tokens/): semantic names preserve intent across products and themes.
- [Apple HIG — Color](https://developer.apple.com/design/human-interface-guidelines/color): adapt to appearance and the platform's semantic behavior.

For composition, use a reference that matches the product and explain its limits. [Linear's redesign](https://linear.app/now/how-we-redesigned-the-linear-ui) can inform quiet inactive UI and semantic relationships; [Vercel Geist](https://vercel.com/geist) can inform grid and typography. Their visual choices are examples, not requirements for another brand.

## Role and theme procedure

1. Inventory real backgrounds, foregrounds, states, alpha mixes, and fixed-theme exceptions.
2. Choose neutral temperature and brand expression from the brief, rather than tinting every surface by habit.
3. Split brand color into field, soft surface, boundary/focus, and accessible content roles when needed. Define status roles independently.
4. Establish lightness and chroma relationships, map supported themes, and record sRGB fallbacks and any gamut changes.
5. Measure critical pairs in each relevant state. For alpha, gradients, or imagery, inspect the actual composite and least-contrasting meaningful area.
6. Review in real layouts; record allowed use, forbidden pairs, and unresolved validation.

Use primitive → semantic → component layers. Name semantic roles by purpose, such as `surface-raised`, `text-primary`, or `brand-field`, and keep names stable as theme values change. Add a component token only for an exception that the semantic system cannot express.

## Accessibility requirements and exceptions

Use WCAG 2.2 as the default web accessibility target unless the project specifies another applicable standard. These checks cover selected criteria, not complete conformance:

- [1.4.3 Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html): ordinary text needs at least `4.5:1`; large text needs `3:1`. Large means at least 18 pt (24 CSS px), or 14 pt bold (approximately 18.67 CSS px), or the equivalent size for CJK fonts. Inactive controls, incidental text, and logotypes have defined exceptions. Do not treat supporting or muted text as exempt merely because it is secondary.
- [1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html): visual information needed to identify controls, states, or meaningful graphics needs `3:1` against adjacent colors. Decorative separators and inactive controls are not automatically subject to that gate. Customized focus indicators need the applicable non-text contrast; unmodified user-agent controls have an exception.
- [1.4.1 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html): essential information needs another cue, such as text, shape, or an icon.
- [2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html) and [2.4.11 Focus Not Obscured Minimum](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html): check visibility and author-created occlusion in the actual interface. A color pair alone cannot verify them.
- [2.4.13 Focus Appearance](https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html) is AAA. Its area and focused/unfocused contrast requirements are additional to AA; do not describe every focus check as this criterion.
- [2.5.8 Target Size Minimum](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) is AA: `24 × 24 CSS px`, with spacing, equivalent-control, inline, user-agent, and essential exceptions. [2.5.5 Target Size Enhanced](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html) uses `44 × 44 CSS px` at AAA. A team may choose 44 px as its touch policy, but label that policy separately.

Judge thresholds using the full computed ratio, not a rounded display value. APCA may provide supplementary typography evidence; it does not replace the project's WCAG gate unless a different evaluation has explicitly been adopted.

## Worked role example

Illustration only; these values do not prescribe a product palette:

| Foreground | Background | Measured contrast | Decision |
| --- | --- | ---: | --- |
| `#171717` | bright field `#C6FF4A` | approximately `15.20:1` | viable ordinary text on this field |
| `#FFFFFF` | bright field `#C6FF4A` | approximately `1.18:1` | reject for ordinary or large text |

Keep the bright field as one job. Select and test separate semantic values for text on the canvas, focus rings, and soft selected surfaces. Passing the field's foreground pair does not validate those other jobs.
