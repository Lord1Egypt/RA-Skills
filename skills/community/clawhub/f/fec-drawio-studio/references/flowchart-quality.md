# Flowchart Quality

Use this reference when a draw.io / diagrams.net deliverable is a process, workflow, approval path, release path, incident response path, onboarding flow or other flowchart that must remain readable after opening in diagrams.net.

## Readability Contract

- Keep manually authored flowcharts narrow. Prefer `pageWidth` between 600 and 800; do not exceed 800 unless the diagram is intentionally a wide cross-functional table.
- Set `dx` and `dy` close to the page dimensions so diagrams.net does not initially zoom the drawing until labels become tiny.
- Put the primary path top-to-bottom. Use side branches only for alternatives, failures, retries and exceptions, then return them to the main path with orthogonal connectors.
- Split more than five dense stages into multiple diagrams or pages instead of making one oversized canvas.

## Stage Grouping

- Use `swimlane` containers for real stages, actors, phases or bounded groups; avoid loose rectangles when a title and containment relationship matter.
- Keep stage containers on a 10px grid, normally with a 20px outer page margin and 30-40px vertical breathing room between stages.
- Give container headers a readable hierarchy: stage labels around 14-16px, bold, with a clear border color.
- Set stage containers to `connectable="0"` and `collapsible=0` so connectors target intentional nodes and the diagram does not gain collapse controls.
- Size containers to fit their children with 15px or more bottom padding. A container with large one-sided blank space usually needs a layout pass.

## Labels

- Keep node text centered for process boxes unless a table-like artifact genuinely needs aligned rows.
- Use `whiteSpace=wrap;html=1` on process nodes, and keep normal body text at 12px or larger.
- Put the node title first, visually stronger than the body. Use concise labels and move long implementation detail into notes or metadata.
- Use the same language as the user's request, and escape XML attribute content before saving.

## Connectors

- Use `edgeStyle=orthogonalEdgeStyle` for normal flowchart connectors.
- Make the main stage-to-stage path visually stronger than secondary edges, for example with a thicker stroke and a consistent accent color.
- Label decision branches and exception paths close to the edge segment they describe.
- For fan-out from one node to several peers, use explicit `entryX`, `entryY`, `exitX` and `exitY` anchors so branches do not cross.
- Route retry, rollback and loop connectors around the left or right margin with explicit waypoints instead of diagonal shortcuts through content.

## Visual System

- Use a small palette with one color per stage type or actor group. Keep process node fills neutral and let borders or headers carry the stage color.
- Reserve warning, failure, pending and future states for exceptional nodes; do not use status colors as decoration.
- Keep container corners square when the stage boundary is structural; rounded corners are fine for ordinary process nodes.

## Final Review

Before delivery, run:

```bash
node skills/fec-drawio-studio/scripts/diagram-lint.mjs diagram.drawio --format markdown --strict
```

Then manually check that the opened diagram has no crossed main-path connectors, no clipped labels, no collapsed-looking stages, and no unreadably small text at the default diagrams.net zoom.
