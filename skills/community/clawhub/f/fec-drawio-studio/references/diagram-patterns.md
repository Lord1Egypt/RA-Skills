# Diagram Patterns

Use these conventions when a user asks for a named technical diagram.

## Architecture

- Group nodes by tier: client, edge, service, data, external.
- Use swimlanes or grouped containers when boundaries matter.
- For layered block architecture, prefer horizontal tiers with left-side tier labels, content-driven containers, and optional cross-cutting sidebars for security, monitoring or governance.
- Put bus or event-stream nodes near the center of publisher/subscriber rows.
- Use cylinders for databases, rounded rectangles for services, dashed outlines for external systems.
- Use arrows only when data flow or dependency direction matters; use spatial grouping for pure capability stacks.

## ERD

- Model tables as containers with rows for columns.
- Mark primary keys and foreign keys in labels.
- Use dashed relationship edges when cardinality is not fully known.
- Prefer top-to-bottom layout for schemas with multiple relation clusters.
- Use stable table widths and row heights so long column names wrap instead of resizing neighboring tables.

## UML Class

- Use a class box split into name, fields and methods.
- Use hollow triangle arrows for inheritance, dashed hollow triangle for interface implementation.
- Keep interfaces or abstract bases above concrete classes.
- Keep associations orthogonal and label multiplicity near the edge segment it describes.

## Sequence

- Lay participants left-to-right and time top-to-bottom.
- Keep request, response and async message styles visually distinct.
- Add activation boxes only when they clarify nested work.
- Leave enough horizontal spacing for message labels; if labels collide, wrap text or split the interaction into phases.

## ML / Deep Learning

- Show tensor shape on a second line when it matters.
- Group encoder, decoder, embedding, attention and output stages.
- Route skip connections around the primary flow.

## Flowchart

- Use ovals for start/end, rectangles for process, diamonds for decisions.
- Label decision branches.
- Merge branches back to a central path when possible.
- Keep the primary path vertical. Route alternate or error branches sideways and back to the main path with orthogonal edges.
- For editable draw.io flowcharts, follow [flowchart-quality.md](flowchart-quality.md) before final delivery.

## Mindmap

- Put the central concept in the middle and distribute first-level branches across quadrants.
- Use curved edges without arrowheads and keep each branch color consistent from parent to leaves.
- Fan leaves away from the center; do not let branches cross through the central label.

## Network Topology

- Use hierarchical rows such as internet, edge, switching/routing and devices.
- Distinguish wired and wireless links visually, usually solid for wired and dashed for wireless.
- Keep endpoint devices aligned in rows or columns so connection paths remain scannable.
