# Canvas Schema Reference

## agent_capabilities.canvas

Uses the [JSON Canvas 1.0 spec](https://jsoncanvas.org/spec/1.0/).

### Structure

```json
{
  "nodes": [
    {
      "id": "group-shared-notes",
      "type": "group",
      "label": "Shared Notes",
      "x": -100, "y": -100,
      "width": 800, "height": 600,
      "color": "5"
    },
    {
      "id": "share-<note-id>",
      "type": "text",
      "text": "## Note Title\n\nContent excerpt…",
      "x": 0, "y": 0,
      "width": 400, "height": 200,
      "color": "4"
    }
  ],
  "edges": [
    {
      "id": "edge-share-<note-id>",
      "fromNode": "group-shared-notes",
      "fromSide": "bottom",
      "toNode": "share-<note-id>",
      "toSide": "top",
      "toEnd": "arrow"
    }
  ]
}
```

### Node ID Convention

- Group: `group-shared-notes`
- Note nodes: `share-<bear-note-id>`
- Edges: `edge-share-<bear-note-id>`

### Color Codes

| Value | Color | Usage |
|-------|-------|-------|
| `"4"` | Green | Shared note nodes |
| `"5"` | Cyan | Group container |

### Layout

- New nodes stack vertically with 250px spacing
- Group node auto-expands height to contain children
- X offset = 0, Y = max(existing Y) + 200
