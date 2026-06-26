# Browser Three.js Fast Path (No Build)

Use this path when users want a playable 3D game quickly from static files.

## Minimal Delivery Model

- `index.html` bootstraps canvas and UI overlay
- `styles.css` handles HUD and responsive layout
- `main.js` initializes scene, camera, renderer, and loop
- optional `assets/` for textures, models, and audio

## Recommended Development Sequence

1. Scene and camera calibration
2. Player movement and input handling
3. Basic collision proxies and fail condition
4. Score/progress logic
5. Restart flow and HUD readability
6. Performance pass for desktop and mobile

## Performance Guardrails

- Cap pixel ratio to avoid mobile GPU overload.
- Keep draw calls bounded with instancing and merged static meshes.
- Dispose geometries, materials, and textures on scene transitions.
- Avoid expensive post-processing until core loop is validated.

## Game Feel Checklist

- Input delay under one frame for movement and actions
- Clear camera framing during high-action moments
- High-contrast feedback for hit, damage, and success
- Restart and retry path under three interactions

## Upgrade Path to Structured Builds

Move to bundled workflow only when needed:
- codebase exceeds manageable single-file complexity
- shared systems require module boundaries
- automated tests and content pipeline justify tooling overhead

For most prototype-to-playable browser games, no-build remains the fastest delivery path.
