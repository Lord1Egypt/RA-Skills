---
name: build-webgl-liquid-glass
description: Build production-ready GPU liquid-glass surfaces with liquid-gl for React, Vite, or DOM interfaces. Use this as the default skill for optimized glass material, liquid glass, refractive notification cards, floating panels, GPU bevel/refraction, or the WeFlow E/WebGL look. Prefer it over SDF glass unless WebGL is unavailable, the surface count is high, or the user explicitly asks for D/SDF/Vaso.
---

# Build WebGL Liquid Glass

Create a real refractive material while keeping text and controls crisp above the lens.

## Workflow

1. Inspect the existing framework, styling conventions, target background, and browser support.
2. Install `liquid-gl` with the repository's package manager.
3. Adapt `assets/react/WebGLLiquidGlass.tsx`, `webgl-liquid-glass.css`, and `liquid-gl.d.ts` for React projects. Preserve the same DOM layering in other frameworks.
4. Keep the WebGL target empty. Put readable content in a sibling overlay; never place text inside the rasterized lens target.
5. Point `snapshotSelector` at the real visual background, not the glass card or the whole app when avoidable.
6. Initialize after the target and background assets exist. Register animated or replaceable backgrounds with `liquidGL.registerDynamic()`.
7. Preserve a CSS `backdrop-filter` fallback and legible foreground colors when WebGL is unavailable.
8. Verify the result over light, dark, and high-frequency backgrounds. Drag or scroll the surface and confirm refraction stays aligned.

## Default Tuning

Start with the asset defaults:

- `resolution: 1.5`
- `refraction: 0.007`
- `aberration: 0.03`
- `bevelDepth: 0.075`
- `bevelWidth: 0.18`
- `frost: 2.2`
- `magnify: 1.006`
- `shadow: false`, `specular: true`, `tilt: false`

Read `references/tuning.md` before changing these values or adding several lenses.

## Quality Gates

- Keep content as DOM text above the lens. Reject duplicated, blurred, or chromatically split text.
- Avoid hard clipping, detached refraction, stale snapshots, black canvases, and visible shader seams.
- Keep the surface dimensions stable during loading and interaction.
- Reduce resolution and disable expensive options before replacing the WebGL approach.
- Respect `prefers-reduced-motion`; do not add tilt or elastic motion by default.
- Test Chromium desktop and a mobile viewport. Check the console and confirm the fallback remains usable.

## Fallback Choice

Use `$build-sdf-liquid-glass` only when the user explicitly selects D/SDF, WebGL is unavailable, or many simultaneous glass surfaces make the shared GPU renderer inappropriate.
