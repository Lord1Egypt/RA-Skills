# Brand Aesthetic — Phosphor

<!--
  Monochrome CRT / low-bit computer graphics. Green phosphor default, with
  latitude for amber phosphor, duotone dither (yellow on blue), and teal
  monochrome. Pixels are visible, color count is low, the screen hums.
  Indie-game retro-computing register.
-->

## Palette

Default: **green phosphor** — deep black background (#0A0F08), phosphor green
foreground (#35E06B to #68FF9C), a quieter green shadow (#1E7A3A) for depth.
One, maybe two shades. Hard steps, no gradients inside shapes.

Sanctioned alternates, one per image:
- **Amber phosphor** — near-black brown ground, warm amber (#FFB000) glyphs
- **Duotone dither** — Game Boy yellow (#F0E060) on deep navy (#1A2456), or
  sea-green on teal, with visible Bayer/ordered dithering in the mid-tones
- **Teal monochrome** — muted teal (#3A8A8A) on bone (#F0EAD6), print-era

Two-to-three colors total per image. No photographic color ranges.

## Composition

Screen-native framing. The image sits inside a terminal, a game interface,
a desktop window, or a full-bleed CRT face. Status bars, menu chrome, ASCII
borders, cursor blocks, scan lines — all welcome as compositional elements.

Low resolution is the grammar. Objects are blocks of pixels. Type is
monospace (but never rendered as text — implied through shape alone).
Interfaces suggest the kind of HUD you'd see in an old dungeon crawler,
a BBS login, a Commodore 64 loader screen.

Scan lines and CRT curvature (barrel-mild) frame the composition when the
whole screen is shown. Otherwise, pixel-perfect flat.

## Rendering

**Sharp pixels.** Every edge steps. Anti-aliasing minimal or absent. The
viewer should be able to count the pixels along a diagonal.

**CRT bloom and bleed.** Bright pixels glow softly into their neighbors
(green on black especially). Color fringes at edges — red-blue chromatic
shift. Phosphor has mass; it's not a sharp projection.

**Dither everywhere.** Ordered Bayer dither, crosshatch dither, or noise
dither fills gradients and mid-tones. Never a smooth gradient — always
the pattern.

**Scan lines.** Horizontal dark lines running across the image at low
opacity. Optional VHS-like vertical tracking jitter at frame edges.

**Low color count.** 4, 8, or 16 colors maximum. Indexed palette. If more
than 16 colors are present, something has gone wrong.

## Tone

Late, quiet, alone with the machine. The after-hours register of someone
still logged in after midnight, reading a wiki on a CRT. Memory of
childhood computing, slightly haunted. Not nostalgic as decoration —
nostalgic as weight.

Melancholy curiosity. Monastic attention. The machine as companion, not
tool.

## Constraints

- **No high-bit-depth color.** The image should read as 4-bit or 8-bit
  indexed, not 24-bit truecolor.
- **No photorealistic textures.** Surfaces are flat-shaded pixel blocks,
  not rendered materials.
- **No modern UI.** No rounded corners, no soft shadows, no blur. If a
  UI element appears, it's hard-edged pixel furniture.
- **No typography rendered into the image.** Glyph-shaped blocks and
  monospace rhythm are fine; actual text is set by the CMS.

## Reference anchors

- **Videoverse** (2023, indie game) — yellow-on-blue duotone PC-98 world
- **Patboy Burger** (fan art) — deep green phosphor PC terminal
- **BRIKOYT** (indie horror) — teal/desaturated Soviet CRT desktop
- **Oregon Trail** (Apple II / MECC) — monochrome dithered landscapes
- **Apple II / Commodore 64 / PC-98** era interfaces
- **Classic Mac System 1–6** — 1-bit UI chrome, hatched shadows
- **Faith: The Unholy Trinity**, **Lunacid**, **Anodyne 2** — indie
  low-bit horror/adventure palettes
