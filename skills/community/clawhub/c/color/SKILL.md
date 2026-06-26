---
name: Color
slug: color
version: 1.0.0
homepage: https://clawic.com/skills/color
description: "Build, inspect, adapt, and validate color systems, palettes, tokens, contrast, color-space choices, and cross-surface color behavior for UI, branding, charts, images, and print."
changelog: "Initial release with practical guidance for palettes, contrast, tokens, color spaces, charts, branding, print, and implementation workflows."
metadata: {"clawdbot":{"emoji":"🎨","os":["linux","darwin","win32"]}}
---

## When to Use

Use when color is the real decision surface: palette building, semantic tokens, dark mode, chart colors, brand systems, accessibility, print handoff, or image/export consistency.

If the job is context-specific, load the matching file before locking the palette:
- `ui-systems.md` for product UI, design systems, semantic tokens, states, surfaces, and dark mode.
- `palettes.md` for palette construction, neutrals, accents, tonal ladders, and brandable combinations.
- `accessibility.md` for contrast, non-color cues, text legibility, and state signaling.
- `data-viz.md` for categorical vs sequential scales, heatmaps, dashboards, and chart-safe colors.
- `branding.md` for brand palettes, campaigns, logos, packaging, and cross-channel consistency.
- `print.md` for CMYK, spot colors, proofs, coated vs uncoated stock, and prepress handoff.
- `color-spaces.md` for RGB/HEX/HSL/HSV/LAB/OKLab/OKLCH decisions and conversion traps.
- `commands.md` when the user needs concrete code, CSS tokens, or command-line conversions.

Keep the system-level workflow in this file, then pull in the specialized file that matches the real output instead of solving every color problem with generic palette advice.

## Quick Reference

| Situation | Load | Why |
|-----------|------|-----|
| Product UI, theming, semantic states, dark mode | `ui-systems.md` | Prevent token drift, weak states, and inconsistent surfaces |
| Palette ideation, tonal ramps, neutrals, accent strategy | `palettes.md` | Build palettes that scale instead of isolated swatches |
| Text contrast, alerts, status chips, colorblind-safe design | `accessibility.md` | Keep color usable, legible, and compliant in context |
| Charts, maps, dashboards, categorical or sequential scales | `data-viz.md` | Avoid misleading charts and indistinguishable series |
| Brand systems, campaigns, packaging, logo environments | `branding.md` | Preserve brand recognition across surfaces and sizes |
| Print production, proofs, CMYK, spot inks, material shifts | `print.md` | Avoid screen-to-print surprises and prepress mistakes |
| RGB, CMYK, LAB, OKLCH, conversions, gamut, interpolation | `color-spaces.md` | Pick the right space for design, editing, and export |
| CSS, design tokens, JS helpers, conversion commands | `commands.md` | Use concrete implementations once the strategy is clear |

## Fast Workflow

1. Identify the job type: UI system, palette exploration, chart, brand surface, image treatment, or print handoff.
2. Identify the destination: app UI, marketing page, charting library, social graphic, packaging, PDF, or press output.
3. Decide what color must do: guide hierarchy, encode state, separate data, express brand, improve readability, or survive production.
4. Inspect existing constraints before changing anything: current palette, token names, contrast, background shifts, export format, gamut, and theme variants.
5. Load the destination-specific file if the work is product UI, palette design, accessibility, data viz, branding, print, or color-space heavy.
6. Make the minimum color decisions that keep the whole system coherent: neutrals, accent count, state mapping, tonal steps, and conversion/export rules.
7. Validate the result in the actual context: light and dark, disabled and hover, chart legend, image overlay, browser preview, and printed proof when relevant.

## Color-Job Defaults

| Job | Usually best starting point | Watch out for |
|-----|-----------------------------|---------------|
| Product UI theme | Neutral ladder + one primary + defined semantic states | Token drift, weak disabled states, dark-mode collapse |
| Marketing palette | Brand anchor + controlled accent pair + support neutrals | Too many accents, campaign colors overpowering brand |
| Dashboard or chart | Distinct categorical set or ordered sequential ramp | Color-only meaning, low-contrast lines, legend confusion |
| Image overlays or captions | Neutral text with overlay/backplate and one accent | Beautiful mockups that fail on real photos |
| Print piece or packaging | Approved print palette with proofed conversions | CMYK dulling, stock shift, out-of-gamut brand colors |
| Design-token refactor | Semantic roles mapped to stable primitives | Naming by hue instead of intent |
| Accessibility cleanup | Contrast-safe neutrals and state patterns first | Chasing AA numbers while meaning still depends on color |

## Core Rules

### 1. Choose colors by job, not by taste

- A background color, brand accent, error state, chart series, and print ink are different jobs.
- If the palette has to handle hierarchy, status, and data at once, separate those responsibilities before adding more colors.
- The best-looking swatch in isolation can still fail when it has to carry text, hover states, or category meaning.
- Start by defining what each color must do in the interface or asset, not what hue feels fashionable.
- If a color has no clear role, it is probably noise.

### 2. Build the system before polishing the palette

- A color system needs primitives, semantic roles, and component-level usage, not only named swatches.
- Neutrals usually carry more of the product than the accent color does, so define the neutral ladder early.
- A palette that looks balanced on a moodboard can still fail when applied to buttons, borders, tables, banners, and empty states.
- Use accents deliberately; more accent colors usually create weaker hierarchy, not richer design.
- If the job spans multiple products or channels, define reuse rules before designing edge-case surfaces.

### 3. Use perceptual spaces for ramps and interpolation

- RGB and HSL are convenient, but they do not always create visually even steps.
- OKLCH or OKLab are better starting points when the task needs predictable lightness steps, tonal ramps, and theme derivations.
- HSL remains useful for fast exploration, but do not assume equal HSL steps look equally bright.
- Conversion is not neutral: a color that looks stable in one space can shift when moved into another gamut or output format.
- If a system needs scalable ramps, trust perceptual spacing more than eyeballing random hex values.

### 4. Contrast is contextual, not just a ratio

- Contrast checks for text, UI boundaries, icons, charts, and overlays are related but not identical jobs.
- Passing AA on one background does not mean the same foreground works on tinted cards, photos, hover states, or dark surfaces.
- A state color that "reads fine" in a mockup can disappear inside disabled, pressed, or selected variants.
- Thin type, small labels, chart lines, and over-photo text fail faster than large blocks of text.
- Measure contrast, but also validate the real composition where the color will be used.

### 5. Never let meaning depend on color alone

- Status, validation, category, and priority should still work in grayscale, low vision, and low-quality displays.
- Pair color with text, shape, iconography, pattern, position, or motion when the distinction matters.
- Sequential and diverging chart scales need labels and legends that remain understandable without perfect hue perception.
- Red and green can coexist, but they cannot be the only signal.
- If the user would lose the meaning when the color is removed, the system is underspecified.

### 6. Validate the whole state matrix, not the hero screen

- Palettes break in edges: disabled buttons, hover backgrounds, table striping, empty charts, skeletons, and on-image captions.
- Dark mode needs a deliberate surface strategy; simply inverting colors usually destroys hierarchy.
- Brand colors that work for headlines can fail for body text, borders, or small icons.
- Charts need validation at line thickness, marker size, and dashboard density, not only in a polished presentation slide.
- If the system ships across web, mobile, image exports, and PDF, validate each medium before calling it stable.

### 7. Treat color management as a real production constraint

- Display RGB, exported PNG, social upload, PDF, and press sheet can all move the same color differently.
- sRGB is still the safest default for most digital delivery, but not every workflow ends there.
- Print introduces CMYK conversion, ink limits, substrate shift, and proofing requirements that a screen mockup hides.
- Image assets, CSS colors, and chart libraries can each interpret the same value differently when profiles or rendering assumptions diverge.
- If the job crosses digital and print, define the handoff rules explicitly instead of trusting one set of hex codes to survive everything.

### 8. Make tokens semantic and naming durable

- Name colors by role or outcome, not by the hue of the moment.
- `text-primary`, `surface-muted`, and `status-danger` age better than `blue-700-button`.
- Keep primitives stable underneath semantics so a rebrand does not require renaming the entire component layer.
- One-off overrides multiply quickly; if a component needs a special token, document why it exists.
- Durable naming matters more than any single hex choice when the system will evolve.

## Specialized Cases Worth Loading

- Load `ui-systems.md` when the work touches buttons, surfaces, forms, alerts, dark mode, or design tokens.
- Load `data-viz.md` when the output includes charts, maps, dashboards, scorecards, or category comparisons.
- Load `print.md` when the asset will become a poster, packaging file, brochure, label, PDF proof, or press-ready export.
- Load `branding.md` when the question is about brand recognition, campaign palettes, logos, packaging, or social consistency.

## What Good Looks Like

- Every important color has a clear role and survives the surfaces where it is used.
- The neutral system, accent strategy, and semantic states feel related instead of assembled from disconnected swatches.
- Text, icons, charts, and overlays stay legible in the real preview, not only in the ideal mockup.
- Token names express function, so future changes can swap values without rewriting the whole system.
- Color ramps look visually even instead of randomly jumping in brightness.
- The design still works in grayscale, dark mode, tinted surfaces, and after export or print conversion.
- The agent has not confused pleasing colors with a complete color system.

## Common Traps

- Starting with an accent color and improvising everything else afterward.
- Naming tokens by hue and locking the design system to this quarter's palette.
- Treating contrast as solved because one text/background pair passes a checker.
- Designing categorical charts with hues that collapse for colorblind users or at small line widths.
- Using brand colors for body copy when they were only safe for display-sized headlines.
- Building ramps in RGB or HSL and assuming equal code steps mean equal perceived steps.
- Solving state communication with red and green alone.
- Forgetting that tinted cards, overlays, and dark mode change contrast math and perception.
- Assuming screen colors will print faithfully without proofing or conversion decisions.
- Exporting gorgeous color palettes that have no neutral strategy, state mapping, or component rules behind them.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `image` — Image processing, exports, and color-sensitive visual asset workflows.
- `image-generation` — AI image creation where palette, art direction, and color consistency matter.
- `branding` — Brand-system decisions beyond color alone.
- `photography` — Capture, grading, and print-aware image workflows where color intent matters.
- `svg` — Vector graphics workflows where palette discipline and contrast affect brand delivery.

## Feedback

- If useful: `clawhub star color`
- Stay updated: `clawhub sync`
