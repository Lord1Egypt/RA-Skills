# Diagram quality examples

The JSON fixtures cover sequence self calls, workflow decisions and loops, and architecture groups with reverse/data/async edges. The Mermaid sources are equivalent text-first examples for standard sequence/workflow rendering. Preserve their labels and relationships when changing layout.

```sh
node skills/fec-image-generation/scripts/tech-diagram-render.mjs --input skills/fec-image-generation/assets/quality-examples/workflow.json --type workflow --output workflow.html --manifest workflow.layout.json
node skills/fec-image-generation/scripts/export-diagram.mjs --input workflow.html --format png --output workflow.png --theme light --scale 2 --manifest workflow.layout.json --output-manifest workflow.actual.json
node skills/fec-image-generation/scripts/png-qa.mjs --png workflow.png --manifest workflow.actual.json --format json
node skills/fec-image-generation/scripts/mermaid-render.mjs --input skills/fec-image-generation/assets/quality-examples/sequence.mmd --output sequence.svg --report sequence.render.json
```

Use a local Chromium browser for PNG; set FEC_BROWSER_PATH to its executable when detection fails. Mermaid needs an already installed mmdc; no automatic install or CDN is used. Missing Mermaid must be recorded as unavailable and the HTML route selected. Architecture editing uses the existing fec-drawio-studio skill when available, otherwise the JSON/HTML fixture. Graphviz is optional for dense topology and is not installed automatically.

Inspect final PNGs at intended reading size. Check node text against shape interiors, edge labels against arrowheads, branch/return directions, loop visibility, group boundaries and light/dark contrast. Run at 1x and 2x and inspect both. Geometry QA is evidence, not a substitute for visual review. Small explicit node sizes, overlapping explicit coordinates or obstructed explicit waypoints are reported; change the source with user intent preserved. Limit automatic source repairs to two rounds (five only when requested), and report partial acceptance if unresolved.
