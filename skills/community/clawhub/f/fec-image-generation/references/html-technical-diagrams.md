# HTML Technical Diagrams

Use this route when a technical diagram should be easy to open in a browser, share as one file, switch dark/light themes, and export from the browser after visual QA.

This route complements, but does not replace, other diagram sources:

| Need | Prefer |
| ---- | ------ |
| Small markdown-maintained diagram | Mermaid, Graphviz, or SVG |
| Editable source for future manual changes | `fec-drawio-studio` and `.drawio` |
| Browser-ready themed technical diagram | HTML technical diagram route |
| Raster-first visual, poster, concept art, or image edit | Image generation or editing route |

## Supported Diagram Intents

- `architecture`: system topology, system blueprints, deployment topology, cloud regions, trust boundaries, clients, gateways, services, data stores, event buses, auth flows, agent runtime maps, memory or recall overview diagrams, before/after architecture comparisons, and infrastructure overview diagrams.
- `workflow`: ownership lanes, process maps, approval gates, automation runs, exception paths, cyclical loops, runbooks, CI/CD, incident response, tool calls, and request lifecycles.
- `sequence`: participants over time, API call chains, cache fallback, auth checks, async traces, and return messages.
- `dataflow`: sources, ingest, processing, storage, consumers, PII boundaries, governance, analytics, and lineage.
- `lifecycle`: object states, terminal states, retries, waits, cancellation, timeout, deployment or order status transitions.

Use the `architecture` mode for browser-ready overview diagrams with explicit coordinates. Use `fec-drawio-studio` instead when the priority is `.drawio` source, official vendor icons, diagrams.net manual editing, or complex auto-layout.

## Themed Semantic Diagrams

Use `visual.style` when the same JSON source needs a clearer delivery tone without changing its model: `default`, `terminal`, `blueprint`, `minimal`, `glass`, `warm`, `openai`, or `editorial-dark`.

For agent, memory, and AI workflow maps, prefer architecture nodes with semantic `type` values:

- Actors and entry points: `user`, `browser`, `gateway`.
- Intelligence and orchestration: `agent`, `model`, `tool`.
- Memory and knowledge: `memory`, `vectorstore`, `graphdb`, `document`.
- Runtime movement: `queue`, `messagebus`, `backend`, `external`.

Use connection `flow` values when arrows need meaning beyond visual direction:

- `control`: orchestration, policy, trigger, or command.
- `data`: request payloads, documents, embeddings, facts, or responses.
- `read`: retrieval from memory or stores.
- `write`: persistence, indexing, notes, or memory updates.
- `async`: evented or queued work.
- `feedback`: loops, retries, refinement, or reasoning cycles.

When two or more flow types are present, the renderer emits a flow legend automatically. Keep arrow labels short and use `waypoints` to route around dense groups, title labels, and node interiors.

## System Blueprint Workflow

Use the architecture route for presentation-ready system blueprints, deployment topology, integration maps, agent runtime views, memory or recall maps, and before/after architecture comparisons. First extract a compact system model, then draw:

- Entry surfaces: browsers, mobile clients, CLIs, webhooks, schedulers, or agent/session entry points.
- Application layer: gateways, frontend apps, backend services, workers, orchestration, runtime hosts, and tool adapters.
- Data layer: databases, object stores, caches, vector stores, queues, event buses, logs, and analytics stores.
- External dependencies: identity providers, AI models, payment/email services, SaaS APIs, cloud services, design tools, or runtime connectors.
- Identity and trust boundaries: auth, permissions, PII zones, tenant boundaries, private networks, secret stores, and policy checks.
- Key flows: request/control flow, data flow, event flow, deployment flow, recall/memory flow, or before/after migration flow.

Keep the first blueprint readable:

- Show 4-10 primary nodes and collapse low-value files, classes, or endpoints into grouped nodes.
- Use 1-3 group boundaries for layers, trust zones, runtime environments, or ownership domains.
- Include a short title and subtitle that work when the file is shared outside the original conversation.
- Use a legend or up to three summary cards for runtime, data, trust, risks, inputs, or outcomes.
- Prefer semantic color roles over decorative styling, and split into multiple diagrams when connectors or labels become dense.

For README or stakeholder handoff, keep the JSON IR and HTML as the editable source, then export SVG/PNG/JPG artifacts:

```bash
node skills/fec-image-generation/scripts/export-diagram.mjs --input docs/architecture/system-blueprint.html --format svg
node skills/fec-image-generation/scripts/export-diagram.mjs --input docs/architecture/system-blueprint.html --format png --scale 2
```

Raster export uses an existing Chromium-family browser when available. If the environment cannot rasterize SVG, deliver the generated HTML/SVG and state that PNG/JPG export needs a local browser.

## JSON IR

All modes require:

```json
{
  "schema_version": 1,
  "diagram_type": "workflow",
  "meta": {
    "title": "Release Workflow",
    "subtitle": "PR to production"
  }
}
```

Mode-specific minimum fields:

- `architecture`: `nodes`, `connections`; optional `groups`, `legend`, and `summary`.
- `workflow`: `lanes`, `nodes`, `edges`; optional `summary`.
- `sequence`: `participants`, `messages`.
- `dataflow`: `stages`, `nodes`, `flows`.
- `lifecycle`: `lanes`, `states`, `transitions`.

IDs must start with a letter and use only letters, numbers, `_`, and `-`. Keep labels short enough to read inside nodes; put long explanation in surrounding prose instead of the diagram.

## Process Workflow IR

Workflow mode is for ordered processes where ownership, decisions, branches, and loop-backs matter more than exact infrastructure topology. Use lanes for actors or systems, nodes for steps, and edges for outcomes. Nodes still support explicit `col` placement so authors can control reading order without relying on a hidden auto-layout engine.

```json
{
  "schema_version": 1,
  "diagram_type": "workflow",
  "meta": {
    "title": "Procurement Approval",
    "subtitle": "Request to payment"
  },
  "lanes": [
    { "id": "requester", "label": "Requester" },
    { "id": "system", "label": "System" },
    { "id": "manager", "label": "Manager" }
  ],
  "nodes": [
    { "id": "start", "lane": "requester", "col": 0, "type": "start", "label": "Submit Request", "actor": "Employee" },
    { "id": "classify", "lane": "system", "col": 1, "type": "active", "label": "Classify Spend", "actor": "Policy Engine", "sublabel": "auto rules" },
    { "id": "review", "lane": "manager", "col": 2, "type": "decision", "label": "Approved?", "step": "A" },
    { "id": "pay", "lane": "system", "col": 3, "type": "success", "label": "Issue Payment" },
    { "id": "reject", "lane": "requester", "col": 3, "type": "failure", "label": "Return Request" }
  ],
  "edges": [
    { "from": "start", "to": "classify", "label": "intake", "variant": "emphasis" },
    { "from": "classify", "to": "review", "label": "policy result" },
    { "from": "review", "to": "pay", "label": "yes", "variant": "emphasis" },
    { "from": "review", "to": "reject", "label": "no", "variant": "return", "waypoints": [[650, 396], [520, 396]] }
  ],
  "summary": [
    { "title": "Inputs", "type": "active", "items": ["Purchase request", "Policy threshold"] },
    { "title": "Outcomes", "type": "success", "items": ["Payment issued", "Requester notified"] }
  ]
}
```

Workflow node fields:

- `type`: use `start`, `active`, `waiting`, `decision`, `success`, `failure`, or `external` for process semantics.
- `actor`: optional short owner or system label above the node.
- `step`: optional displayed step marker. If omitted, workflow nodes receive sequential markers automatically.
- `sublabel`, `width`, `height`, and `yOffset`: optional readability adjustments for dense lanes.

Workflow edge fields:

- `variant`: use `emphasis` for happy paths, `return` or `dashed` for loop-backs and rework, and `security` only for trust or policy checks.
- `waypoints`: optional `[x, y]` points for exception paths, cross-row links, or loops that should avoid labels and nodes.

Use `summary` for compact process metadata such as prerequisites, inputs/outputs, or tools. Keep long explanations outside the SVG so labels remain readable.

## Architecture IR

Architecture mode uses explicit coordinates because system diagrams often need intentional placement, boundaries, and trust zones:

```json
{
  "schema_version": 1,
  "diagram_type": "architecture",
  "meta": {
    "title": "SaaS Architecture",
    "subtitle": "Browser-ready infrastructure overview"
  },
  "visual": {
    "style": "blueprint"
  },
  "groups": [
    { "id": "cloud", "label": "Cloud region", "type": "cloud", "x": 170, "y": 50, "width": 620, "height": 280 }
  ],
  "nodes": [
    { "id": "web", "label": "Web App", "type": "frontend", "x": 48, "y": 160, "sublabel": "React" },
    { "id": "api", "label": "API Gateway", "type": "cloud", "x": 230, "y": 160, "group": "cloud" },
    { "id": "svc", "label": "App Service", "type": "backend", "x": 420, "y": 160, "group": "cloud" },
    { "id": "db", "label": "PostgreSQL", "type": "database", "x": 620, "y": 160, "group": "cloud" }
  ],
  "connections": [
    { "from": "web", "to": "api", "label": "HTTPS", "variant": "emphasis" },
    { "from": "api", "to": "svc", "label": "REST" },
    { "from": "svc", "to": "db", "label": "SQL" }
  ],
  "summary": [
    { "title": "Runtime", "type": "backend", "items": ["API and worker services", "Managed relational data"] }
  ]
}
```

Supported node and group types include `frontend`, `backend`, `database`, `cloud`, `security`, `messagebus`, `external`, `agent`, `model`, `memory`, `vectorstore`, `graphdb`, `tool`, `document`, `queue`, `browser`, `user`, and `gateway`. Connections support the standard variants `default`, `emphasis`, `security`, `dashed`, and `return`; architecture connections may also include `flow`. Add `waypoints` as `[[x, y], ...]` when a connection needs to route around boundaries or labels.

Architecture output includes an automatic legend unless `legend` is set to `false`. A custom legend can be supplied as `{ "label": "...", "type": "..." }` items. `summary` renders up to three cards below the SVG and is not included in the layout manifest, so PNG QA focuses on the diagram itself.

## Architecture Layout Rules

- Draw groups as broad boundaries around components, not as decorative panels.
- Keep legends below or outside all boundaries; increase the coordinates and view area rather than squeezing content.
- Use `messagebus` nodes for event buses and place them in the gap between services.
- Use `security` connections for auth, token, policy, or trust-boundary flows.
- Prefer `waypoints` over dense crossing lines when gateways fan out to several services.
- Split the diagram when the overview needs more than one dense cluster or when label readability depends on shrinking text.

## Render Command

```bash
node skills/fec-image-generation/scripts/tech-diagram-render.mjs \
  --input diagram.json \
  --output diagram.html \
  --type architecture \
  --manifest diagram.layout.json
```

The generated HTML is self-contained and includes:

- Inline SVG.
- CSS-variable dark/light theme.
- Browser controls for theme toggle, SVG download, and print/PDF.
- Optional layout manifest for PNG QA.

## QA and Repair

After exporting a PNG from the browser, run:

```bash
node skills/fec-image-generation/scripts/png-qa.mjs \
  --png diagram.png \
  --manifest diagram.layout.json \
  --format markdown
```

Repair the source JSON or rendering dimensions rather than editing pixels:

- Overlap: split dense lanes or add rows/lanes/stages.
- Truncated label: shorten labels, add `sublabel`, or widen nodes.
- Connector through label: reduce edge labels or separate nearby nodes.
- Dense flow: split into overview and detail diagrams.
- Edge clipping: increase output space or simplify the path.

## Delivery Notes

Deliver the `.html` source together with any exported SVG/PNG/JPG requested by the user. Report the route used, source file, exported file, QA result, and any naming or domain assumptions that still need human confirmation.
