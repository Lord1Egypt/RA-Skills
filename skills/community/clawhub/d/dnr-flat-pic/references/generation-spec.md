# Canonical Rendering Contract

Apply this contract to every generation and edit. Treat the flat-color rules as hard constraints, not stylistic preferences.

## Contents

- Hard Flat-Color Specification
- HSB Palette and Fill Budget
- Source Cleanup
- Canonical Generation Specification

## Hard Flat-Color Specification

### Core General Rule (Highest Priority)

All output consists exclusively of closed shapes with solid, uniform flat color fills and crisp, vector-like contours. No region, at any scale, contains gradients, continuous tonal transitions, or soft effects of any kind. Disregard all continuous photographic lighting from the reference; do not retain realistic atmosphere, soft illumination, or continuous tonal depth.

### Implementation Rules by Category

#### 1. Light & Shadow

##### Correct implementation

Represent all lighting and shadow effects using discrete, solid color shapes only:

- Highlights: lighter solid polygons, hard-edged planes, strips, or bands
- Shadows: darker solid polygons, hard-edged planes, strips, or bands formed by overlap, occlusion, or directional lighting
- Bright source shapes (light sources and lit elements, including light strips, point lights, lit windows, lamps, and signs): bright solid highlight geometries with clean, closed contours; keep brightness inside the source shape and prohibit glow, spill, expanded illumination, and continuous falloff on surrounding surfaces
- Point/directional lights: render the source as a solid shape, and illuminated surfaces as one or more adjacent hard-edged color planes; use a limited number of discrete value steps for brightness changes

##### Strictly prohibited

- All gradients (linear, radial, mesh, atmospheric) and continuous tonal transitions
- Glow, bloom, halo, neon spill, luminous fog, rim light, and optical diffusion around light sources
- Radial falloff, reflected spill, penumbra, soft transitions, and continuous illumination fields
- Soft shadows and ambient occlusion shading
- Glossy reflections, specular shine, photographic highlights, and translucent glare

#### 2. Depth & Form

##### Correct implementation

Convey depth and form only through:

- Shape overlap and occlusion
- Scale variation
- Vertical positioning
- A small set of discrete solid tone steps

##### Strictly prohibited

- Depth-of-field effects, blur, haze, and vignette
- Any continuous shading used to imply volume or distance

#### 3. Surface & Detail

##### Correct implementation

Simplify all surface details to uniform solid fills. Handle repeated elements in two tiers:

- **Texture-tier repeats** (micro surface patterns): remove entirely
- **Entity-tier repeats** (macro semantic objects): do not delete; group and simplify per the repeated-element grouping and internal-detail rules in `semantic-complexity.md`

Reference examples:

- Texture-tier: brick grain, fabric weave, wallpaper patterns, dotted texture, paving tile grain
- Entity-tier: window rows, street lamp arrays, tree lines, shelf goods

Text, logos, and interface marks are handled per the Source Cleanup rules below.

##### Strictly prohibited

- All texture, grain, fabric weave, skin pores, food texture, and painterly noise
- Feathering, soft edges, and deliberately blurred boundaries

### General Supplementary Rules

1. **No Exemption Principle**: All color regions have crisp, sharp boundaries. No region is exempt from the no-gradient rule, regardless of its size, brightness, darkness, distance, luminous property, atmospheric role, or visual priority.
2. **Contour Requirement**: All closed shapes maintain clean, vector-like contours. This refers to the inherent edge of each filled region, not an added stroke or outline layer.

## HSB Palette and Fill Budget

### Fixed HSB Palette

Use the following HSB palette as the complete color basis for the final PNG:

| Role | HSB base value |
|---|---|
| Main blue | `(218, 75, 75)` |
| Main yellow | `(28, 67, 92)` |
| Secondary blue | `(235, 75, 55)` |
| Secondary orange | `(5, 67, 90)` |
| Brightest | `(50, 8, 99)` |
| Darkest | `(220, 100, 5)` |
| Accent green | `(140, 42, 45)` |
| Accent purple | `(300, 75, 50)` |

### Allowed HSB Variation

- Main blue and main yellow: hue ±3°, saturation ±3 percentage points, brightness ±3 percentage points.
- Secondary blue, secondary orange, and accent green: hue ±8°, saturation ±8 percentage points, brightness ±8 percentage points.
- Accent purple: hue ±3°, saturation ±3 percentage points, brightness ±3 percentage points.
- Brightest and darkest: fixed values only; no variation is allowed.

### Palette Role Assignment (Not Color Matching)

The fixed HSB palette is the sole authoritative color source for the final output. Do not match, reproduce, or approximate the source photograph's native hues, white balance, or local colors.

Use the source photograph only to determine composition, object structure, discrete light-dark value tiers, and warm-cool regional contrast. Use those structural attributes to assign palette roles, not to calculate matching hues.

Assign palette roles in this priority order:

1. **Fixed semantic category**
   - Assign accent green to plant, foliage, tree, and grass regions by default. Use allowed green variants for highlights and shadows.
   - Exception: when the foliage itself is clearly yellow or orange, or is semantically autumnal rather than merely warm-lit, assign main yellow and secondary orange variants instead; do not force green.
   - Assign the brightest source regions directly to the fixed brightest value.
   - Assign the darkest source regions directly to the fixed darkest value.
2. **Dominant area role**
   - Fill the largest background or dominant surface with either main blue for a cool-dominant scene or main yellow for a warm-dominant scene.
   - Choose the dominant role from the scene's overall warm-cool tendency, not its exact source hue. The goal is stylized unity, not photographic color accuracy.
3. **Structure and shadow role**
   - Use secondary blue and secondary orange for structural shadows, intermediate tones, subordinate surfaces, and depth layering.
   - Align secondary-role placement to the source image's discrete light-dark value hierarchy; do not use secondary colors for large dominant areas.
4. **Accent role**
   - Use accent purple only for small, localized decorative highlights. Never use it for large surfaces, backgrounds, or primary subjects.

#### Key style rule

It is required and expected that the final color scheme differs from the source photograph. Prioritize consistent stylized palette identity over color realism. All filled regions must stay within the fixed palette and its permitted variation ranges; no free colors are allowed.

### Fill Construction

- Retain one dominant background field, filled with either main blue or main yellow.
- Default to fill-only construction; no additional strokes or outline layers by default.

## Source Cleanup

Remove all non-image elements by default: subtitles, social media controls, interaction counters (like, comment, share), watermarks, app chrome, labels, captions, explanatory text, decorative frames, complexity scores, and infographic panels.

This rule applies to all text, logos, numbers, signs, and interface-style marks.

- Delete the element entirely if removal does not impair composition, scale, spatial structure, or recognizability.
- Replace the entire element with a small number of regular solid rectangles aligned to the original region only if it is visually dominant and its removal would create a noticeable structural void. Use the assigned HSB palette role for the original region when reliable; otherwise use the adjacent region's assigned palette role. Do not introduce a free or unrelated color.

Never retain readable glyphs, pseudo-text, letter/digit-like strokes, logo contours, or recognizable brand marks.

## Canonical Generation Specification

(Internal execution template, adapted to the reference image. Not displayed unless requested.)

1. Apply the complete Hard Flat-Color Specification above as the highest-priority rendering contract.
2. Apply Source Cleanup as defined above.
3. Build and apply the semantic brief using `semantic-complexity.md`.
4. Apply the HSB Palette Role Assignment above to every filled region.
5. Apply `aspect-ratio-adaptation.md` only when the user requests a ratio different from the reference.
6. Generate one clean final illustration using only the fixed palette and permitted variants.
