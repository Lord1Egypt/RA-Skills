# Excalidraw Playbook

Use this playbook when the user explicitly wants Excalidraw, a hand-drawn style, a whiteboard sketch, or a diagram meant for collaborative dragging and editing.

## Default Choice

- Default format: Excalidraw
- Default direction: automatic
- Best use: whiteboard collaboration, informal exploration, workshop drafts
- Do not use Excalidraw by default for dense engineering-grade network topology unless the user explicitly asks.

## Layout Rules

- For small sketches, omitted geometry can use the generator's basic grid layout.
- For complex diagrams, provide explicit `geometry`.
- Keep shapes far enough apart that connectors and labels remain visible.
- Put edge labels away from connector lines.
- Avoid dense cross-links.

## Binding Rules

Excalidraw output must preserve drag behavior:
- Connectors must use `startBinding` and `endBinding`.
- Connector endpoints must attach to element edges, not element centers.
- Node labels must be bound and grouped with node shapes.
- Container labels must be bound and grouped with container shapes.
- Container backgrounds should stay transparent by default.

## Format-Specific Expectations

For generated `.excalidraw` files:
- Shape elements should carry `boundElements` entries for text labels and arrows.
- Text labels should use `containerId` pointing at the shape.
- Shape and label should share a `groupIds` value.
- Arrows should have valid `startBinding.elementId` and `endBinding.elementId`.
- Edge label text should not cover horizontal or vertical connector lines.

## When Excalidraw Represents Network Topology

Apply the network topology semantics from `playbook-network-topology.md`, but adapt visual strictness:
- Keep datacenters and zones as transparent containers.
- Use distinct device colors and shapes.
- Use edge-bound connectors.
- Prefer fewer labels on connectors.
- Keep the diagram editable rather than pixel-perfect.

## Quality Gate

Before generation:
- Confirm the user really wants Excalidraw.
- Confirm whether the diagram is a sketch or an engineering artifact.
- Add explicit geometry for complex diagrams.
- Keep container backgrounds transparent.

After generation:
- Check every arrow has source and target bindings.
- Check shape labels are grouped and bound.
- Check container labels are grouped and bound.
- Check large containers have transparent backgrounds.
- Check edge labels do not cover connector lines.
