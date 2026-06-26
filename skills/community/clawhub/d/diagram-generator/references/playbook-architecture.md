# Architecture Diagram Playbook

Use this playbook for system architecture, application architecture, platform architecture, deployment architecture, and component dependency diagrams.

## Default Choice

- Default format: Draw.io
- Default direction: vertical or automatic
- Use Mermaid only for high-level architecture summaries.
- Use Excalidraw only for informal whiteboard architecture sketches.

## Layer Model

Prefer `diagramType: "architecture"` with `layers` instead of manually creating containers.

Recommended layer order:
1. Users or external systems
2. Access or gateway
3. Services or applications
4. Data stores
5. External dependencies

Common layer names:
- Client Layer
- Access Layer
- Service Layer
- Data Layer
- External Dependency Layer

## Draw.io Rules

- Layers flow top to bottom.
- Components in the same layer can sit side by side.
- Keep layers equal width when possible.
- Use compact vertical spacing, but leave enough room for connector readability.
- Put databases, caches, and message queues in the data layer.
- Do not mix data stores with business services unless the prompt explicitly asks.
- Use one edge label per repeated relationship type; repeated labels reduce readability.
- Put cross-layer dependencies in top-level `elements` as edges.

## Device Type Presets

Use `deviceType` when possible:

| Component | `deviceType` |
| --- | --- |
| User or client | `user` |
| API gateway or ingress | `gateway` |
| Service or application | `service` |
| Server | `server` |
| Database | `database` |
| Cache | `cache` |
| Message queue | `messageQueue` |
| Cloud dependency | `cloud` |
| External system | `externalSystem` |

## Mermaid Rules

Use Mermaid for simple documentation-first architecture:
- Use flowchart layout.
- Keep labels short.
- Group major areas with subgraphs if supported by the generator.
- Avoid dense cross-links.

## Excalidraw Rules

Use Excalidraw for whiteboard architecture:
- Keep container backgrounds transparent.
- Bind and group labels with shapes.
- Bind connectors to element edges.
- Use explicit geometry for complex diagrams.
- Keep labels away from connector lines.

## Quality Gate

Before generation:
- Confirm whether the diagram is conceptual, logical, physical, or deployment-focused.
- Confirm format and usage context.
- Verify each component belongs to a layer.
- Verify data stores are separated from service components.
- Verify cross-layer edges are top-level elements.

After generation:
- Check top-to-bottom layer order.
- Check same-layer components are aligned.
- Check major layers have consistent width.
