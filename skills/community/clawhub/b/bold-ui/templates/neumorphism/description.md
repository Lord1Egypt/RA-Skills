# Neumorphism — Design Brief

## Visual Identity

Neumorphism creates interfaces that feel physically extruded from the background — like soft clay or plastic that's been gently pressed into shape. Elements have no hard separation from their surroundings; instead, they emerge through the interplay of light and shadow. The result is tactile, calming, and almost therapeutic. It's UI design as sculpture.

## Core Design Language

**Colors**: The entire interface uses essentially one base color with subtle variations. The background, cards, and buttons all share the same base hue (#E8E5F0 — a soft lavender-gray). Color is used sparingly — purple for primary actions, mint for positive states. This monochromatic foundation is what makes the shadow-play work. Any strong color contrast breaks the illusion.

**Shapes**: Very large rounded corners (12-24px). The softness is essential — sharp corners create harsh shadow transitions that ruin the neumorphic effect. Corners should be so rounded that elements feel like organic blobs rather than geometric rectangles.

**Shadows**: The defining feature. Every element has TWO shadows: a dark shadow on one side (bottom-right, simulating shadow) and a light shadow on the other side (top-left, simulating light hitting a raised surface). The light source is consistently top-left. The shadows are soft (large blur, moderate opacity). Pressed elements invert the shadows to inset.

**Typography**: Clean sans-serif (Inter) in a soft dark tone (#4C3F6B — not pure black). Text shouldn't fight with the shadow play. Weights are moderate — headings in semibold, body in regular. Thin text lacks contrast against the soft background.

**Motion**: Slow and gentle. 300ms is the minimum transition time — nothing should snap. Press animations should smoothly transition from "raised" to "pressed" shadow states. The overall feel is meditative, like pressing into soft clay.

## Key Visual Signatures

1. **Dual shadows**: Every raised element has `box-shadow: Xpx Xpx Ypx dark-color, -Xpx -Xpx Ypx light-color`. The dark shadow is typically 30-40% opacity black/dark-gray, the light shadow is 70-80% opacity white. Maintaining this duality consistently is THE neumorphic signature.

2. **No borders**: Elements have no visible borders. The edge between an element and the background is defined purely by the shadow transition. Adding a border breaks the illusion of the element being part of the same material.

3. **Pressed states (inset)**: When a button is pressed/active, the dual shadows become inset. `box-shadow: inset Xpx Xpx Ypx dark, inset -Xpx -Xpx Ypx light`. This creates the impression of the element being pressed INTO the surface. Toggle switches and buttons feel incredibly satisfying with this effect.

4. **Monochrome depth**: Cards at different elevations use the same background color but different shadow intensities. Higher elevation = bigger shadow offset and blur. The card itself never changes color — only its shadows do.

5. **Concave inputs**: Text inputs are "carved into" the surface — they use inset shadows only (no outset shadow). This makes them look like depressions in the material, clearly distinguishable from raised buttons.

## When to Adapt

- **Dark mode neumorphism**: Use a dark base color (#1E1E2E) with lighter shadows. The light shadow becomes subtle (10-15% opacity white), the dark shadow becomes deeper (30-40% opacity black). Dark mode neumorphism is actually easier to pull off than light mode.
- **Color accents**: The primary action button can be a different color — but maintain the dual shadow principle. A purple button on a gray background uses purple-tinted shadows. This creates a beautiful "separate material" look.
- **Accessibility**: Add thin borders (1px, very low opacity) as a fallback for users who can't perceive shadow depth. WCAG doesn't count shadow contrast, so borders provide a safety net.
- **Data displays**: Neumorphism struggles with complex data viz. For charts and tables, use a flat section with minimal shadow — let the data be the focus, not the surface.

## Anti-Patterns (avoid these)

- Don't use high-contrast colors — the palette should whisper, not shout
- Don't use sharp corners — shadows need curves to flow smoothly
- Don't use a single shadow — the dual shadow (dark + light) is non-negotiable
- Don't add borders — shadows define edges, borders ruin the illusion
- Don't mix light sources — all shadows must agree on the light direction (top-left)
- Don't use pure white or pure black for shadows — always tinted to the base color
- Don't use transparency/blur effects — neumorphism is about opaque surfaces and light physics
