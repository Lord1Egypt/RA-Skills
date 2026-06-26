# Brutalist Minimal — Design Brief

## Visual Identity

Brutalist Minimal rejects decorative design entirely. It's raw, honest, and functional — the visual equivalent of exposed concrete and steel beams. Black and white with zero compromise. No gradients, no rounded corners, no subtle shadows. Every design decision is made with the question: "Does this serve the content?" If not, it's removed.

## Core Design Language

**Colors**: Black. White. That's it. A single accent color (typically red #FF3366) is the only allowed deviation — used exclusively for links, buttons, or critical highlights. Black text on white backgrounds, white text on black sections. No grays between 333 and 666. The high contrast is deliberately aggressive.

**Shapes**: Everything is rectangular with sharp 90-degree corners. No rounded corners anywhere — not on buttons, not on cards, not on inputs. This is brutalist architecture applied to UI: honest materials, exposed structure.

**Shadows**: Hard black offset shadows with zero blur. `4px 4px 0px #000000`. The shadow is a solid shape — like a second layer of material behind the element. On hover, the element shifts rather than the shadow changing.

**Typography**: Monospace. Everything is monospace — headings, body, labels, buttons. IBM Plex Mono is the preferred typeface for its blend of technical precision and personality. The heading scale is extreme — heroes can go to 4rem (64px). Bold weights dominate; light/thin weights don't exist in brutalist design.

**Motion**: Zero. No transitions, no animations, no hover effects that involve smooth changes. Hover states are binary — on or off. If something needs to move, it jumps to its new position instantly. The only exception is a hard underline appearing on links.

## Key Visual Signatures

1. **Hard black shadows**: Like pixel retro, but more aggressive and minimal. Every elevated element gets a solid black shadow block. The shadow offset is larger (6-12px) and the contrast is maximum — black on white.

2. **Thick visible borders**: 2-3px solid black borders on inputs, cards, and separators. Borders are structural — they delineate space honestly. No subtle 1px borders; if there's a boundary, make it visible.

3. **Extreme typography**: Headings in massive bold monospace. Body text in readable monospace with high contrast. The type does all the heavy lifting since there are no decorative elements. Underlines replace color changes for links.

4. **No decoration**: No gradients, no patterns, no icons unless functionally necessary. When icons are used, they're simple feather icons — thin strokes, no fills, black only.

5. **Whitespace as structure**: Generous spacing (8px base unit, 128px max) creates breathing room. When you remove all decoration, spacing becomes the primary tool for creating hierarchy and grouping.

## When to Adapt

- **Documentation sites**: Brutalism shines here. Monospace body text is natural for code documentation. Add a sticky sidebar with section links. Keep the structure rigid.
- **Portfolio sites**: Allow ONE accent color (the designer's/developer's brand color). Keep everything else black and white. The accent should be used on 3-5 elements max.
- **Dark mode**: Invert — black background, white text, white borders. The hard shadow effect doesn't work on dark backgrounds, so elements use a thick white border instead of a shadow.
- **Blogs**: Add a subtle gray (#FAFAFA) background for article cards to differentiate from the page background. This is the gentlest concession to readability — but keep the borders sharp.

## Anti-Patterns (avoid these)

- Don't use rounded corners — not a single one, anywhere
- Don't use smooth transitions or animations — everything is instant or it doesn't move
- Don't use more than one accent color — brutalist color palettes are binary
- Don't add decorative elements — if it's not content, remove it
- Don't use thin fonts — brutalist typography has weight and presence
- Don't use subtle shadows — if there's a shadow, it should be hard and obvious
- Don't center text unnecessarily — left-aligned raw text is the brutalist default
- Don't use blur or transparency effects — brutalist is honest about materials
