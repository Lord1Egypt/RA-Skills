# Pixel Retro — Design Brief

## Visual Identity

Pixel Retro transports users back to the golden age of 8-bit gaming. Hard pixel edges, bold solid shadows, and monospace fonts create an unmistakable retro aesthetic. It's nostalgic but functional — the visual language of classic video games applied to modern UI.

## Core Design Language

**Colors**: Warm orange (#FF6B35) is the hero — energetic, playful, impossible to ignore. Cyan (#00B4D8) provides cool contrast. Everything sits on a deep navy background (#1A1A2E) that evokes CRT screens in dark rooms. No gradients, no opacity tricks — solid, flat colors only.

**Shapes**: Absolutely no rounded corners. Every element has sharp 90-degree edges. Borders are thick (2-4px) and solid. This is the single most important visual rule — violate it and the pixel aesthetic collapses.

**Shadows**: Hard offset shadows with zero blur. The shadow is a solid block of color offset from the element — like sprites layered on a game screen. `4px 4px 0px rgba(0,0,0,0.5)` — no blur radius, ever.

**Typography**: 'Press Start 2P' for headings — the quintessential pixel font. 'Fira Code' for body text — monospace but highly readable. All text is monospace. Line height is tight; pixel fonts look wrong with generous spacing.

**Motion**: Step-based animation using CSS `steps()`. No smooth easing curves — everything snaps. Hover states shift instantly. Page transitions are near-instant (50-80ms). This creates the characteristic "frame-by-frame" feel of retro games.

## Key Visual Signatures

1. **Hard pixel shadows**: Every interactive element casts a solid, offset shadow block. On hover, the element shifts toward the shadow (translate -2px, -2px), creating a "button press" illusion.

2. **Thick borders**: 3px solid borders on all containers. Double borders on focus states. Borders are always a slightly lighter version of the background.

3. **Monospace everywhere**: No proportional fonts allowed. Headings in pixel display fonts, body in coding monospace. Numbers should be tabular.

4. **CRT scanlines overlay**: A subtle scanline pattern over the entire page (CSS repeating-linear-gradient with low opacity) adds authenticity without hurting readability.

5. **Pixelated decorations**: Decorative elements use pixel-art patterns — dot matrices, blocky dividers, 8-bit style icons.

## When to Adapt

- **Data dashboards**: Use the neon color palette for data viz — cyan for positive, orange for highlights, pink for alerts
- **Creative tools**: Lean into the playful side — more pixel decorations, game-like UI patterns
- **Developer tools**: Keep the monospace foundation but simplify decorations — let the code aesthetic speak
- **Dark mode**: Already dark by default, but can lighten to a gray CRT tone for accessibility

## Anti-Patterns (avoid these)

- Don't use ANY rounded corners — not even 1px
- Don't use smooth CSS transitions — always use steps()
- Don't use opacity-based shadows — shadows must be solid color blocks
- Don't use proportional/sans-serif fonts — monospace only
- Don't use gradients larger than 2 color stops — keep it pixel-flat
- Don't use blur effects — no backdrop-blur, no box-shadow blur
