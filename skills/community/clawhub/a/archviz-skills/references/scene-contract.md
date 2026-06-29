# Scene Contract

For complex diagrams, create a small intermediate scene contract before choosing a renderer.

This borrows the useful part of Visio-style reconstruction workflows: separate **diagram facts** from **rendering syntax**.

## When To Use

- More than 20 nodes.
- Multiple containers / layers / swimlanes.
- Mixed diagram types.
- User asks for both preview and editable handoff.
- Exact topology matters more than visual flourish.

## Minimal Schema

```json
{
  "metadata": {
    "title": "",
    "audience": "",
    "renderer_target": "mermaid|html|drawio|canvas|ascii",
    "palette": "warm-paper|editorial-parchment|host"
  },
  "nodes": [
    {"id": "n1", "label": "Short label", "role": "process", "group": "g1"}
  ],
  "groups": [
    {"id": "g1", "label": "Layer", "role": "container"}
  ],
  "edges": [
    {"id": "e1", "from": "n1", "to": "n2", "label": "", "style": "solid"}
  ],
  "constraints": {
    "max_accent": 1,
    "max_label_words": 6,
    "fallback_required": true
  }
}
```

## Render Mapping

| Target | Mapping |
|---|---|
| Mermaid | groups -> `subgraph`; nodes -> shape by role; edges -> arrows |
| HTML | groups -> grid/section; nodes -> cards; edges -> SVG overlay if needed |
| draw.io | groups -> containers; nodes -> editable shapes; edges -> orthogonal connectors |
| Canvas | groups -> group nodes; nodes -> text cards; edges -> JSON Canvas edges |
| ASCII | groups -> headings; nodes -> boxed lines; edges -> numbered references if dense |

## Gate

Before rendering:

- Every edge endpoint exists.
- Every group has a clear semantic role.
- Labels fit the target environment.
- If the scene has more than two relationship types, split the output.
- If the target fails, scene contract must still be usable for a fallback renderer.

