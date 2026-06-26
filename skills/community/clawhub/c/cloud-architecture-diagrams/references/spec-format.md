# Spec Format & Layout Cookbook

The spec is a single JSON object. `build_diagram.py` turns it into both a
`.excalidraw` and a `.drawio` file with icons embedded.

## Top-level keys

| Key      | Required | Notes |
|----------|----------|-------|
| `title`  | no  | Drawn top-left as a big heading. |
| `provider` | no | Icon set: `"aws"`, `"azure"` (official, bundled), `"gcp"` (Google, bundled), or `"microsoft"` (msicons.com, default; has Power Platform/Dynamics/Copilot). |
| `providers` | no | List form, e.g. `["azure","microsoft"]`, to allow several. |
| `drawio_shapes` | no | `true` → the `.drawio` uses draw.io's native vector stencils (AWS/GCP/Azure) instead of embedded SVG. Excalidraw always embeds SVG. |
| `canvas` | no  | `{"width":..,"height":..}` — informational; sizing is automatic. |
| `zones`  | no  | Dashed grouping containers, drawn behind everything. |
| `nodes`  | yes | The components (cards or icon-only). |
| `edges`  | no  | Arrows between nodes. |
| `badges` | no  | Numbered step circles (the black ① ② ③ markers). |

A node may carry its own `"provider"` to override the spec default for that one
icon (e.g. an AWS diagram that also shows an Entra ID logo).

## Zones

A dashed rounded rectangle with a title in the top-left corner — use one per
logical boundary (a cloud, a platform, a data tier).

```json
{"id":"az","label":"Azure","x":400,"y":70,"width":880,"height":740}
```
Optional: `"color":"#9aa0a6"`, `"style":"solid"` (default `"dashed"`),
`"fill":"#f5f7fa"` (default none), `"opacity":100`.

## Nodes

Two flavors:

**Card** (default) — white rounded box, icon top-left, bold title, optional
description. This is the standard architecture box.
```json
{"id":"app","title":"App Service","desc":"Hosts the APIs",
 "icon":"App Service","x":430,"y":360,"width":230,"height":84}
```

**Icon-only** (`"card": false`) — just the icon with a centered label beneath.
Use for actors (Users), portals, or standalone product logos.
```json
{"id":"user","title":"Users","icon":"User","x":30,"y":400,
 "width":64,"height":64,"card":false}
```

Node fields:
| Field | Meaning |
|-------|---------|
| `id` | unique string, referenced by edges |
| `title` | bold label |
| `desc` | small gray sub-label (cards only) |
| `icon` | service name to match (see finding icons) |
| `icon_url` | exact msicons URL; bypasses matching |
| `drawio_shape` | exact draw.io stencil key (e.g. `mxgraph.aws4.lambda`) to pin the native shape when `drawio_shapes` is on; bypasses shape matching |
| `x`,`y`,`width`,`height` | position & size |
| `card` | `true` (default) or `false` |

If `icon` matches nothing good (and no `icon_url`), the node renders as a clean
labeled box — no broken image.

## Edges

```json
{"from":"classifier","to":"mcp","label":"Retrieve & classify",
 "dir":"both","color":"#1565c0"}
```
| Field | Meaning |
|-------|---------|
| `from`,`to` | node ids |
| `label` | optional text on the arrow |
| `dir` | `"to"` (default), `"both"`, or `"from"` |
| `color` | hex; default gray `#5f6368`. Use a brand blue like `#1565c0` to highlight a key flow. |
| `style` | `"dashed"` for dashed line |
| `waypoints` | `[[x,y],...]` to force routing around obstacles |

Routing is automatic: the script picks exit/entry sides from the relative
positions of the two nodes and draws a straight or single-elbow line. If an
arrow cuts through a card, add `waypoints` to steer it.

## Badges (numbered steps)

```json
{"n":1,"x":150,"y":120}
```
A black circle with a white number — matches the ① ② ③ flow markers in
Microsoft sequence diagrams. Place them next to the relevant arrow or node.

## Layout cookbook (match the Microsoft look)

- **Flow left → right.** Users/entry on the left, data sources on the right.
- **Zones** wrap related nodes. Leave ~30–40px padding inside a zone around its
  nodes, and start node `y` ~80px below the zone top so the zone title has room.
- **Card size:** ~`230×84` for a title+desc card; `64–72` square for icon-only.
- **Gaps:** keep ≥40px between cards horizontally and ≥26px vertically so arrows
  and labels have room.
- **Columns:** align nodes into columns/rows on a rough grid (e.g. x at 430,
  720, 1000, 1350). Aligned coordinates read as intentional.
- **Highlight** the 1–2 most important flows with a colored edge; leave the rest
  gray.
- **Titles** short; put detail in `desc`.

## Finding icons & synonyms

Run `python scripts/find_icon.py "<service>" --provider <aws|azure|microsoft> -n 4`
and pick from the candidates.

**AWS** — abbreviations resolve to the canonical service icon: `S3`, `EC2`,
`VPC`, `IAM`, `SNS`, `SQS`, `ECS`, `EKS`, `RDS`, `ELB`. Full names work too
("Elastic Load Balancing", "Amazon CloudFront"). Service icons are preferred
over the smaller resource icons automatically.

**GCP** — full names and short forms resolve: `BigQuery`/`BQ`, `Compute
Engine`/`GCE`, `Cloud Storage`/`GCS`, `GKE`, `Cloud Run`, `Vertex AI`, `Looker`.
The bundled Google set is curated (core products + category tiles); missing
services fall back to a labeled box until you import the full official pack.

**Microsoft** (`microsoft` provider) covers Azure services plus the full
Power Platform and Dynamics 365 families. Use natural product names: `Power
Apps`, `Power Automate`, `Power Pages`, `Copilot Studio`, `AI Builder`,
`Dataverse`, `Dynamics 365 Sales`, `Dynamics 365 Customer Service`, `Dynamics
365 Field Service`, `Dynamics 365 Finance`, `Dynamics 365 Business Central`,
`Dynamics 365 Supply Chain Management`, etc. Microsoft also renames products
often; if the current name misses, try the legacy name the icon set still uses:

| You want | Try this query |
|----------|----------------|
| Azure AI Search | `Cognitive Search` |
| Azure OpenAI / Azure AI Foundry model | `Azure OpenAI` (filed as "Open AI") |
| Azure AI Foundry / AI Studio | `AI Studio` |
| Microsoft Entra ID (formerly Azure AD) | `Entra ID` |
| Azure Functions (MCP / Function App) | `Function Apps` or `Power Automate` for a Flow |
| Microsoft Dataverse | `Dataverse` |
| Power Virtual Agents | `Copilot Studio` |
| Log Analytics / telemetry | `Application Insights` or `Monitor` |
| Blob/file storage | `Storage Accounts` |

If nothing scores well, fall back to a labeled box and note it to the user.
The full searchable index is `references/icon-index.json` (fields: `name`,
`category`, `path`, `url`, `search`).

## Minimal example

```json
{
  "title": "Tiny Flow",
  "zones": [{"id":"az","label":"Azure","x":200,"y":60,"width":520,"height":260}],
  "nodes": [
    {"id":"user","title":"User","icon":"User","x":60,"y":150,"width":64,"height":64,"card":false},
    {"id":"fn","title":"Function App","desc":"API","icon":"Function Apps","x":260,"y":140,"width":220,"height":84},
    {"id":"db","title":"Dataverse","desc":"Store","icon":"Dataverse","x":540,"y":140,"width":160,"height":84}
  ],
  "edges": [
    {"from":"user","to":"fn","label":"request","dir":"both"},
    {"from":"fn","to":"db","label":"query","dir":"both","color":"#1565c0"}
  ],
  "badges": [{"n":1,"x":150,"y":120}]
}
```
