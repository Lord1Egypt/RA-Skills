# Changelog

All notable changes to the `beauty-diagram` skill are documented here.

## [1.6.1] - 2026-06-16

### Changed: `bd:bg` now documents the full `white` / `dark` / `transparent` set

- The `bg` directive previously documented `transparent` as the only honoured value. It now documents the full set the CLI and API accept — `theme` (default), `white`, `dark` (the diagram's ink is hue-lifted so edges and labels stay legible), and `transparent` — so the skill suggests the right value. Unknown values fall back to `theme`.
