# Flowchart Playbook

Use this playbook for process flows, approval flows, decision trees, retry flows, error handling, and operational procedures.

## Default Choice

- Default format: Mermaid
- Default direction: vertical
- Use Draw.io for complex multi-branch layouts that need manual placement.
- Use Excalidraw only for informal whiteboard process sketches.

## Mermaid Rules

- Use `diagramType: "flowchart"`.
- Use `flowchart TD` for vertical flow.
- Use rounded nodes for start and end.
- Use diamond nodes for decisions.
- Decision edges must have clear labels such as `yes/no`, `approved/rejected`, or `success/failure`.
- Keep the main path vertical.
- Place exception, retry, rejected, or fallback paths as side branches.
- Keep node labels short.
- Put long explanations outside the diagram.

## Draw.io Rules

Use Draw.io when the process is too complex for Mermaid:
- Main path flows top to bottom.
- Side branches go left or right.
- Retry, return, reject, and fallback edges should not push the main flow downward.
- Decision nodes use diamond shape.
- Start and end nodes use rounded shape.
- Decision branches must have labels.

## Excalidraw Rules

Use Excalidraw for whiteboard process diagrams:
- Use explicit geometry for more than a few nodes.
- Bind and group text with shapes.
- Bind connectors to element edges.
- Put edge labels away from connector lines.

## Quality Gate

Before generation:
- Identify start and end nodes.
- Identify decisions and required branch labels.
- Identify the main success path.
- Identify side branches and loops.
- Confirm whether the output is documentation-grade or whiteboard-grade.

After generation:
- Check that decision nodes have at least two outgoing edges.
- Check that decision outgoing edges have labels.
- Check that the main path remains readable.
