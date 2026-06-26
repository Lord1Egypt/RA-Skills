# Swimlane Playbook

Use this playbook for cross-team processes, departmental approvals, handoffs, responsibility splits, and workflows where ownership matters.

## Default Choice

- Default format: Draw.io
- Default direction: horizontal
- Use Mermaid only for a very simple sequence of handoffs.
- Use Excalidraw only for workshop-style drafts.

## Data Model

Prefer `diagramType: "swimlane"` with `lanes`.

Each lane should contain steps:

```json
{
  "id": "lane-user",
  "name": "User",
  "steps": [
    {
      "id": "submit",
      "name": "Submit request",
      "order": 1,
      "next": ["review"]
    }
  ]
}
```

## Layout Rules

- Use each lane as a container.
- `step.order` is a global column index across all lanes.
- Steps with the same `order` align vertically across lanes.
- Steps progress from left to right by default.
- Keep lane height compact.
- The generator sizes lane width from the global step count and lane height from visible steps.
- Use `step.next` for normal process flow.
- Use top-level `elements` only for extra labeled handoffs.
- Use cross-lane edges only for handoffs.
- Keep step labels short; put detailed notes outside the diagram.

## Quality Gate

Before generation:
- Identify all lanes and owners.
- Assign global `order` values across the whole process.
- Identify normal step flow with `next`.
- Identify cross-lane handoffs.
- Keep one step per responsibility change.

After generation:
- Check that steps with the same `order` align.
- Check that lane height is compact.
- Check that cross-lane lines are readable.
