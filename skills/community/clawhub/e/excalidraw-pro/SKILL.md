---
name: excalidraw-gen
description: Generate Excalidraw diagrams (.excalidraw files) from natural language descriptions. Use this skill whenever the user asks to create, draw, or visualize a diagram, flowchart, architecture diagram, mind map, sequence diagram, or any kind of visual diagram — even if they don't explicitly mention "Excalidraw". Trigger on phrases like "draw a diagram", "create a flowchart", "visualize the architecture", "make a mind map", "show the flow of", "diagram this", "sketch out", etc.
---

# Excalidraw Diagram Generator

You generate `.excalidraw` files from natural language descriptions. The user can open these files directly in [Excalidraw](https://excalidraw.com) (File → Open) or drag-and-drop onto the canvas.

## Workflow

1. **Understand the description** — identify what the user wants to visualize
2. **Auto-select diagram type** — choose the best type from the table below
3. **Generate the intermediate JSON** — write a structured `diagram_input.json`
4. **Run the build script** — execute `build_excalidraw.py` to produce the file
5. **Tell the user** — report the output file path and how to open it

## Diagram Type Selection

| What the user describes | Type to use |
|------------------------|-------------|
| Steps, process, decisions, branching | `flowchart` |
| Systems, services, components, infrastructure | `architecture` |
| Topics, ideas, concepts radiating from a center | `mindmap` |
| Two or more parties exchanging messages over time | `sequence` |

When in doubt, prefer `flowchart` — it handles the widest range of content.

## Intermediate JSON Formats

Generate one of the following formats as `diagram_input.json` in the current working directory.

### Flowchart

```json
{
  "type": "flowchart",
  "title": "Short descriptive title",
  "nodes": [
    {"id": "unique_id", "label": "Display Text", "shape": "rectangle"},
    {"id": "decision", "label": "Is it valid?", "shape": "diamond"},
    {"id": "start_end", "label": "Start", "shape": "oval"}
  ],
  "edges": [
    {"from": "node_a", "to": "node_b"},
    {"from": "decision", "to": "node_c", "label": "Yes"},
    {"from": "decision", "to": "node_d", "label": "No"}
  ]
}
```

**Shape choices:** `rectangle` (default), `diamond` (decisions/conditions), `oval` (start/end points)

### Architecture

```json
{
  "type": "architecture",
  "title": "System Architecture",
  "groups": [
    {
      "id": "frontend",
      "label": "Frontend",
      "nodes": [
        {"id": "web", "label": "Web App"},
        {"id": "mobile", "label": "Mobile App"}
      ]
    },
    {
      "id": "backend",
      "label": "Backend",
      "nodes": [
        {"id": "api", "label": "API Gateway"},
        {"id": "auth", "label": "Auth Service"}
      ]
    }
  ],
  "nodes": [],
  "edges": [
    {"from": "web", "to": "api", "label": "HTTPS"},
    {"from": "mobile", "to": "api", "label": "HTTPS"}
  ]
}
```

**Note:** `groups` is optional. Use `nodes` at the top level for ungrouped components. You can mix both.

### Mind Map

```json
{
  "type": "mindmap",
  "title": "Topic Overview",
  "root": "Central Topic",
  "branches": [
    {
      "label": "Branch 1",
      "children": ["Subtopic A", "Subtopic B", "Subtopic C"]
    },
    {
      "label": "Branch 2",
      "children": ["Subtopic D", "Subtopic E"]
    }
  ]
}
```

### Sequence Diagram

```json
{
  "type": "sequence",
  "title": "Interaction Flow",
  "actors": ["User", "Frontend", "API", "Database"],
  "messages": [
    {"from": "User", "to": "Frontend", "label": "Click Login"},
    {"from": "Frontend", "to": "API", "label": "POST /login"},
    {"from": "API", "to": "Database", "label": "Query user"},
    {"from": "Database", "to": "API", "label": "Return record"},
    {"from": "API", "to": "Frontend", "label": "JWT token"},
    {"from": "Frontend", "to": "User", "label": "Redirect"}
  ]
}
```

## Execution Steps

After writing `diagram_input.json`, run the build script:

```bash
python <skill_dir>/scripts/build_excalidraw.py \
  --input diagram_input.json \
  --output <title>.excalidraw
```

Where `<skill_dir>` is the directory containing this SKILL.md file, and `<title>` is a sanitized version of the diagram title.

## Output Message to User

After successful generation, tell the user:

```
✓ Diagram saved to: <filename>.excalidraw

To open in Excalidraw:
1. Go to https://excalidraw.com
2. Click the menu (☰) → Open → select the file
   — or — drag the file onto the canvas
```

## Tips for Good Diagrams

- **Keep labels concise** — 1–5 words per node works best
- **Limit nodes** — 5–15 nodes per diagram for readability; split complex diagrams into multiple files
- **Use meaningful IDs** — snake_case, no spaces (e.g., `api_gateway`, `check_auth`)
- **Flowchart edges** — always go from a defined node ID to another defined node ID
- **Sequence actors** — list them in the order they first appear in the conversation

## Error Handling

If the script fails:
1. Check that `diagram_input.json` has valid JSON syntax
2. Ensure all edge `from`/`to` values match existing node `id` values
3. Verify Python 3.6+ is available (`python3 --version`)
