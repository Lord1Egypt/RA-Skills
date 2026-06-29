# Diagram Workflows

## Source selection

| Diagram type | Preferred source | QA focus |
| ------------ | ---------------- | -------- |
| ER diagram | Mermaid ER, DBML, Graphviz, SVG | Cardinality labels, table names, key fields, crossing relations. |
| UML class | Mermaid class, PlantUML, Graphviz | Inheritance direction, method/property wrapping, package grouping. |
| Sequence | Mermaid sequence, PlantUML | Lifeline order, activation spans, async/return arrows, message text. |
| Technical architecture | HTML `architecture` IR, Mermaid flowchart, C4/Structurizr, SVG/HTML, draw.io | Layer grouping, trust boundaries, data flow direction, legends. |
| Agent / memory architecture | HTML `architecture` IR with semantic node types and flow arrows, SVG/HTML, draw.io | Read/write path separation, tool-call loops, memory tiers, retrieval labels, flow legend. |
| ML / deep learning | SVG/HTML/canvas | Tensor shapes, layer order, branch joins, repeated blocks, annotations. |
| Flowchart / process workflow | HTML `workflow` IR, Mermaid flowchart, SVG, draw.io | Decision labels, terminal states, loop-back readability, connector spacing, exception path clarity. |
| Live session sketch | Interactive local browser server | Incremental reveal, session isolation, readable labels after manual dragging, export handoff. |

## Interactive live diagrams

Use the live route when the diagram is part of the conversation and the user benefits from seeing structure appear as it is generated. It is best for flow sketches, architecture drafts, short mind-map-like decompositions, and quick walkthroughs that may be dragged or relabeled before export.

Run the local server with:

```bash
node skills/fec-image-generation/scripts/interactive-diagram-server.mjs --port 6100
```

Open `http://127.0.0.1:6100/?s=meaningful-session-id`, then send commands to `/cmd?s=meaningful-session-id`. Always use a unique session id for each diagram. Start with `init`, add nodes before edges, and keep each command small enough that the browser can update incrementally.

Supported commands are `init`, `node`, `edge`, `container`, `remove`, `clear`, `layout`, `title`, and `export`. Supported node types are `terminal`, `terminal-end`, `process`, `decision`, `service`, `database`, `success`, `error`, and `container`.

Use `/export?s=session-id&format=json`, `svg`, or `drawio` for server-side source handoff. Use the browser toolbar for PNG export. If the local server cannot start, use Mermaid, SVG, or HTML technical diagrams instead of blocking the user.

## Minimum source manifest

When the rendering path allows it, save a layout manifest next to the PNG:

```json
{
  "canvas": { "width": 1280, "height": 720 },
  "boxes": [
    { "id": "api", "x": 80, "y": 120, "width": 220, "height": 96, "label": "API Gateway" }
  ],
  "connectors": [
    { "id": "api-db", "from": "api", "to": "db", "points": [[300, 168], [560, 168]] }
  ]
}
```

Coordinates are PNG pixel coordinates after export. Boxes should cover visible label/node bounds, not just the center point.

## Diagram repair playbook

- **Overlapping nodes:** increase rank/column spacing, split clusters, or move low-priority annotations into a legend.
- **Truncated labels:** widen the node, add manual line breaks, reduce label length, or increase export scale.
- **Connector through labels:** add waypoints, route orthogonally around boxes, or move labels above the segment.
- **Connector stacking:** separate parallel edges with different waypoints or bundle them with a shared labeled bus.
- **Edge clipping:** increase outer padding or export viewBox/canvas size.
- **Unreadable dense graph:** split into overview plus detail diagrams instead of shrinking everything.
- **Ambiguous arrow meaning:** add `flow` and a concise label rather than relying on color alone.

## Architecture diagrams

Use HTML `architecture` IR when the user wants a browser-ready single file with explicit system topology, groups, trust boundaries, data flows, and PNG QA. Use draw.io when the diagram must preserve official vendor shapes, diagrams.net editing, or long-term manual ownership. Use Mermaid/C4 when the diagram should live primarily in Markdown or text documentation.

For agent, memory, RAG, tool-call, or multi-agent diagrams, use semantic architecture node types (`agent`, `model`, `memory`, `vectorstore`, `graphdb`, `tool`, `document`, `queue`, `browser`, `user`, `gateway`) instead of generic boxes when the shape helps explain the system. Use `flow` values (`control`, `data`, `read`, `write`, `async`, `feedback`) so read paths, write paths, events, and reasoning loops are visually distinct. Add `visual.style` only after the structure is clear.

For UML coverage, route class, ER, state-machine, activity, and sequence needs to deterministic sources first: Mermaid, PlantUML, HTML technical diagrams, SVG, or draw.io. Prefer draw.io when future manual editing or official notation libraries matter; prefer HTML/SVG when browser-ready handoff and PNG QA matter.

## Process workflows

Use HTML `workflow` IR when the user wants a browser-ready process map, approval flow, automation runbook, incident workflow, or cyclical operating loop with lanes, numbered steps, actors, decisions, exception paths, and summary cards. Use `fec-drawio-studio` instead when the workflow must remain a `.drawio` file for diagrams.net editing, official shape libraries, manual swimlane maintenance, or stakeholder edits after handoff.

## Export guidance

Prefer exporting at 2x scale for raster PNGs, then downsample only if text remains crisp. Keep the editable source committed or attached wherever future diagram changes are expected.
