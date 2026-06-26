# Tech Cyberpunk — Design Brief

## Visual Identity

Tech Cyberpunk plunges users into a neon-drenched digital future. Glowing cyan accents cut through deep darkness like city lights reflecting off rain-slicked streets. This is the visual language of hackers, synthwave, and cyberpunk fiction — high tech, low life, maximum atmosphere.

## Core Design Language

**Colors**: Neon cyan (#00F0FF) is the primary signature — it appears on buttons, links, focus rings, and key UI elements. Magenta (#FF00E5) provides dramatic contrast for secondary actions and highlights. Everything floats on a near-black void (#0A0A0F). The color palette is deliberately limited — 3 neon colors + functional colors. Overusing color destroys the cyberpunk contrast.

**Shapes**: Slightly rounded corners (4-8px) — not perfectly sharp like pixel style, but not soft either. Think "industrial precision." Cards have subtle borders that glow on hover. Corners shouldn't draw attention; neon glows should.

**Shadows**: This style redefines shadows. Instead of dark drop shadows, elements cast colored glows. Cards glow cyan on hover. Buttons have a magenta glow underneath. The glow intensity scales with elevation — modals cast the brightest glow, cards cast a subtle one.

**Typography**: 'Space Grotesk' for headings — a geometric sans-serif with a forward-looking feel. 'JetBrains Mono' for body and code — because in cyberpunk, even body text could be someone's terminal output. The type scale is dramatic — headings can be very large (3.5rem heroes), creating impact on dark backgrounds.

**Motion**: Fast and responsive — this is high-performance tech. But with a twist: occasional glitch effects. Buttons might flicker on hover (brief opacity shift). Page transitions are quick (100-200ms). Use spring easing for expandable elements — they should burst open.

## Key Visual Signatures

1. **Neon glow borders**: Card and input borders glow on focus/hover. Use box-shadow with the primary neon color at 15-30% opacity. The glow should be subtle on static elements and intensify on interaction.

2. **Grid background**: The page background has a subtle tech grid pattern — think Tron/cyberspace. CSS: `repeating-linear-gradient` with 1px lines at very low opacity (5-8%) creating a 40-60px grid.

3. **Glitch text effects**: Headings can have a subtle glitch effect on hover — a brief color split (cyan/magenta offset) using CSS pseudo-elements with clip-path. Use sparingly — once or twice per page.

4. **Scanline overlay**: A subtle horizontal scanline pattern over dark surfaces — reminiscent of CRT monitors. Very low opacity (3-5%) so it doesn't hurt readability.

5. **Duotone icons**: Icons should use the duotone style — a colorful fill with a distinct outline. Phosphor duotone icons match perfectly. The icon color should echo the nearest neon accent.

## When to Adapt

- **Data dashboards**: The dark background is perfect for data viz — use neon colors for chart lines/points, cyan for primary metrics, magenta for secondary
- **Developer tools**: Lean into the terminal aesthetic — monospace body text, code-like UI patterns, inline code styling
- **Marketing pages**: Add extra glow effects, larger typography, more dramatic grid backgrounds — this is where cyberpunk can be most expressive
- **Light mode**: Not recommended. If required, invert to a "white void" cyberpunk — white background with neon cyan/magenta accents, lighter grid. This is an advanced adaptation.

## Anti-Patterns (avoid these)

- Don't use light backgrounds — the dark void is fundamental
- Don't use muted/earth tones — cyberpunk colors are synthetic and vibrant
- Don't use serif fonts — this is distinctly futuristic
- Don't add too many different neon colors — stick to cyan + magenta + purple
- Don't overuse glitch effects — one is cool, three is a broken page
- Don't use opacity-only shadows — colored glow shadows are the signature
- Don't use round/bubble shapes — keep it angular and industrial
