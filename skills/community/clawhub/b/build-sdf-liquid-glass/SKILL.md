---
name: build-sdf-liquid-glass
description: Build lightweight SDF and canvas displacement glass surfaces with Vaso for React interfaces. Use when the user explicitly asks for WeFlow D, SDF glass, Canvas Map, Vaso, a no-WebGL liquid-glass fallback, or many compact refractive cards. Do not select this by default when the WebGL liquid-glass skill is available.
---

# Build SDF Liquid Glass

Create a bounded displacement lens with a sharp, accessible content layer.

## Workflow

1. Inspect the existing component framework, card dimensions, background, and browser targets.
2. Install `vaso` with the repository's package manager.
3. Adapt `assets/react/SDFLiquidGlass.tsx` and `sdf-liquid-glass.css` for React projects. Preserve the same layer separation elsewhere.
4. Render Vaso as an absolute background layer and place text and controls in a sibling overlay. Do not let the displacement filter process readable content.
5. Measure the host with `ResizeObserver` instead of hard-coding responsive width.
6. Keep a translucent CSS background under the effect so unsupported browsers still show a usable card.
7. Verify light, dark, and detailed backgrounds. Drag or resize the surface and check that the map follows its bounds.

## Default Tuning

Start with:

- `radius: 16`
- `depth: 0.58`
- `blur: 0.4`
- `dispersion: 0.32`
- Stable notification height: `86px`

Read `references/tuning.md` before increasing depth or dispersion.

## Quality Gates

- Keep foreground content crisp and outside the filtered layer.
- Reject doubled text, rainbow fringes across glyphs, stale canvas dimensions, and clipped rounded corners.
- Keep `depth` subtle for operational UI; use stronger distortion only for decorative surfaces.
- Test resize behavior, Chromium desktop, and a mobile viewport.
- Check the console and preserve readable CSS fallback colors.

## Default Preference

If the user asks only for an optimized glass material without naming D/SDF/Vaso, use `$build-webgl-liquid-glass` instead.
