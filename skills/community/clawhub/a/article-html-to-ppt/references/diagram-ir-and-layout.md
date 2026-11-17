# Diagram IR And Layout

Use this reference whenever `primary_expression=relationship_visual`. Do not draw relationship diagrams directly from prose. Create or reference a valid Diagram IR first, validate it, analyze complexity, then choose a delivery route.

## Required Flow

1. Decide whether the slide truly needs a relationship visual.
2. Write the audience question and the one-sentence message.
3. Identify nodes and assign `node_type`, role, priority, status, shape, and short labels.
4. Identify groups: layer, lane, phase, domain, organization, system, capability cluster, data zone, or external zone.
5. Identify edges by relation semantics, not by decorative line style.
6. Identify main path(s); keep one dominant primary path unless the diagram is a landscape/ecosystem.
7. Identify boundaries: trust, ownership, security, failure, data, stage, network, or permission.
8. Select a `diagram_type`.
9. Set `layout_constraints` and `delivery_contract`.
10. Validate Diagram IR.
11. Analyze complexity and connector-web risk.
12. Simplify, cluster, or split before choosing raster fallback.

## Diagram Types

- `process_flow`: one main sequence with limited branches.
- `process_lane`: phased process without full role handoff.
- `swimlane`: multiple roles or systems handing work across lanes.
- `timeline`: milestones or roadmap.
- `layered_architecture`: layers, responsibilities, upstream/downstream calls.
- `issue_tree`: structured problem decomposition.
- `decision_tree`: branching decision paths.
- `causal_chain`: cause, mechanism, and outcome.
- `flywheel`: reinforcing loop.
- `hub_spoke`: one hub and several spokes.
- `zoned_ecosystem`: multi-party system with zones and cross-zone relations.
- `capability_landscape`: grouped coverage map, not a process.
- `dependency_graph`: dependency, blockers, and prerequisites.
- `data_flow`: source, processing, and consumption.
- `state_transition`: state changes and triggers.

## Relation Semantics

Store relationship meaning in `relation`: `sequence`, `request`, `response`, `data_flow`, `control`, `dependency`, `approval`, `handoff`, `feedback`, `influence`, `ownership`, `fallback`, `monitoring`, `validation`, `trigger`, `produce`, `consume`, `contain`, or `transition`.

Line style is secondary and should normally come from Style Contract `diagram_tokens.relation_styles`. Use:

- primary sequence/request/control: orthogonal + solid;
- response/dependency/monitoring/fallback: dashed or muted;
- feedback/influence: curved;
- optional or async edges: dashed/dotted/muted.

## Simplification Rules

- Merge duplicate same-direction relationships.
- Promote repeated node-level edges into a group-level relationship when possible.
- Move weak influence or monitoring edges into annotations.
- Keep node labels short; move explanations into annotations or speaker notes.
- Split when total nodes exceed 18, edges exceed 24, groups exceed 6, boundaries exceed 3, or two independent stories compete.

## Delivery Guidance

- `native_diagram`: nodes <= 8, edges <= 10, groups <= 4, boundaries <= 2, labels fit in two lines.
- `hybrid_overlay`: 9-16 nodes or complex zones; SVG base with native labels/legend/annotations.
- `svg_component`: complex ecosystem, capability landscape, architecture mural, or dense non-primary edit object.
- `raster_component`: only with explicit approval or renderer constraints; relationship diagrams default away from raster.

Run:

```bash
python3 scripts/validate_diagram_ir.py --diagram examples/contracts/valid/diagram-ir.json --strict
python3 scripts/analyze_diagram_complexity.py --diagram examples/contracts/valid/diagram-ir.json --json-output
python3 scripts/recommend_diagram_layout.py --diagram examples/contracts/valid/diagram-ir.json
```
