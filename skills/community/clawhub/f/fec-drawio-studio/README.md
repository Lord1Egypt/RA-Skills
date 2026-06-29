# Editable technical diagram workflow

Editable draw.io / diagrams.net workflow for technical diagrams, official shape lookup, brand symbols, Graphviz layout, code structure maps, validation, and export fallback.

## Skill

- ID: `fec-drawio-studio`
- Category: `design-ui`
- Version: `2.8.0`
- Source: `skills/fec-drawio-studio/SKILL.md`

## Description

Use when creating editable technical diagrams with draw.io / diagrams.net sources, including architecture diagrams, ERD, UML, sequence diagrams, flowcharts, ML model diagrams, official shape lookup, brand symbols, Graphviz auto-layout, codebase structure maps, .drawio validation, or draw.io CLI export fallback. Do not use for ordinary raster image generation, freehand sketches, interactive canvas/Three.js scenes, or decorative SVG animation. Chinese triggers include draw.io, diagrams.net, editable architecture diagrams, .drawio, ER diagrams, UML, sequence diagrams, auto layout, shape retrieval, code structure diagrams.

## Usage

Install or import this package with any skill runtime that understands the standard `SKILL.md` layout. The canonical source remains the Frontend Craft repository.

## Packaged Files

- [data/THIRD_PARTY_NOTICES.md](data/THIRD_PARTY_NOTICES.md)
- [data/brand-icons.json](data/brand-icons.json)
- [data/shape-index.json](data/shape-index.json)
- [references/data-residency.md](references/data-residency.md)
- [references/diagram-patterns.md](references/diagram-patterns.md)
- [references/flowchart-quality.md](references/flowchart-quality.md)
- [references/xml-and-mermaid.md](references/xml-and-mermaid.md)
- [scripts/brand-symbols.mjs](scripts/brand-symbols.mjs)
- [scripts/diagram-url.mjs](scripts/diagram-url.mjs)
- [scripts/layout-graph.mjs](scripts/layout-graph.mjs)
- [scripts/scan-go-packages.mjs](scripts/scan-go-packages.mjs)
- [scripts/scan-js-modules.mjs](scripts/scan-js-modules.mjs)
- [scripts/scan-python-classes.mjs](scripts/scan-python-classes.mjs)
- [scripts/scan-python-modules.mjs](scripts/scan-python-modules.mjs)
- [scripts/scan-rust-modules.mjs](scripts/scan-rust-modules.mjs)
- [scripts/scan-ts-modules.mjs](scripts/scan-ts-modules.mjs)
- [scripts/shape-query.mjs](scripts/shape-query.mjs)
- [scripts/studio-core.mjs](scripts/studio-core.mjs)

## Optional Related Packages

- `@bovinphang/fec-image-generation`
- `@bovinphang/fec-canvas-threejs`
- `@bovinphang/fec-svg-animation`
- `@bovinphang/fec-ui-design`
- `@bovinphang/fec-source-driven-development`

## License

MIT
