# Component Registry

Component Registry is the system capability catalog. It answers which components the skill recognizes, what each component can preserve as editable PowerPoint, and which delivery routes are allowed before a builder draws anything.

The machine-readable source of truth is `references/component-registry.json`, validated by `schemas/component-registry.schema.json`.

## Required Workflow

Before building a non-trivial deck:

1. Resolve each PPT IR object to a `component_type`.
2. Load `references/component-registry.json`.
3. Run `scripts/resolve_component_delivery.py`.
4. Produce `.ppt-work/contracts/delivery-plan.json`.
5. Validate the delivery plan.
6. Build according to the selected routes.
7. Record actual route deviations in Build Manifest.

## Route Meaning

- `native_ppt`: editable PowerPoint text/shapes/cards.
- `native_chart`: editable chart data and labels.
- `native_table`: editable table cells.
- `native_diagram`: editable nodes/connectors/labels.
- `svg_component`: bounded SVG component, not whole-slide replacement.
- `raster_component`: bounded raster component with disclosure.
- `generated_image`: generated illustration or concept scene with native title/caption.
- `background_image`: background only; title/body remain native.
- `hybrid_overlay`: SVG/raster base plus native editable overlays.
- `unsupported`: no valid route; builder must stop or choose another builder.

## Non-Negotiables

- Ordinary text, cards, KPI cards, simple charts, and tables do not rasterize.
- `native_required` objects never silently fall back to SVG or image.
- Premium profile forbids unknown builder support and whole-slide raster.
- Complex diagrams prefer `native_diagram -> hybrid_overlay -> svg_component`.
- Conceptual scenes use generated/background visuals with native title, caption, and source note.

## Diagram Components

Relationship-heavy components must be backed by Diagram IR before route selection. Component Registry only says which implementation routes are allowed; Diagram IR says what the diagram means.

Stage 5 diagram component types include:

```text
process_flow
process_lane
swimlane
timeline
layered_architecture
issue_tree
decision_tree
causal_chain
flywheel
hub_spoke
zoned_ecosystem
capability_landscape
dependency_graph
data_flow
state_transition
```

`ecosystem_map` remains as a compatibility component name, but new Diagram IR should prefer `zoned_ecosystem` when the diagram is explicitly zone-based.

Delivery Resolver may attach `diagram_analysis` to an object-level Delivery Plan entry: node count, edge count, connector-web risk, layout recommendation, recommended delivery route, and split recommendation.
