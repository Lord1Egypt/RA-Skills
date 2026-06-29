# Image generation and chart workflow

Image and diagram generation workflow for deterministic diagrams, themed HTML/SVG technical diagrams, raster visual assets, image edits, and bounded PNG QA repair loops.

## Skill

- ID: `fec-image-generation`
- Category: `design-ui`
- Version: `2.8.0`
- Source: `skills/fec-image-generation/SKILL.md`

## Description

Use when generating or editing diagrams, charts, visual assets, posters, UI mockups, product images, infographics, academic figures, comics, avatars, storyboards, brand boards, or image-edit workflows, especially when exported PNGs need visual QA and bounded self-repair. Prefer deterministic Mermaid/SVG/HTML/canvas sources for text-heavy diagrams; use HTML technical diagrams for browser-ready system blueprints, architecture, deployment topology, agent runtime, memory flow, before-after architecture, workflow, sequence, data-flow, lifecycle, runbook, PII/data-lineage, and state-machine diagrams. Do not use for ordinary UI polish without generated imagery.

## Usage

Install or import this package with any skill runtime that understands the standard `SKILL.md` layout. The canonical source remains the Frontend Craft repository.

## Packaged Files

- [assets/interactive-diagram.html](assets/interactive-diagram.html)
- [references/artifact-routing.md](references/artifact-routing.md)
- [references/diagram-workflows.md](references/diagram-workflows.md)
- [references/html-technical-diagrams.md](references/html-technical-diagrams.md)
- [references/png-qa-autofix.md](references/png-qa-autofix.md)
- [scripts/export-diagram.mjs](scripts/export-diagram.mjs)
- [scripts/interactive-diagram-server.mjs](scripts/interactive-diagram-server.mjs)
- [scripts/tech-diagram-render.mjs](scripts/tech-diagram-render.mjs)

## Optional Related Packages

- `@bovinphang/fec-ui-design`
- `@bovinphang/fec-implement-from-design`
- `@bovinphang/fec-canvas-threejs`
- `@bovinphang/fec-svg-animation`
- `@bovinphang/fec-responsive-layout`
- `@bovinphang/fec-accessibility-check`
- `@bovinphang/fec-web-video-presentation`

## License

MIT
