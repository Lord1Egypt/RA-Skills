---
name: diagram-generator
description: Generate and edit diagrams with the mcp-diagram-generator MCP server. Use this skill for new diagrams, existing .drawio/.mmd/.excalidraw edits, network topology, architecture, flowchart, swimlane, sequence, class, ER, mind map, and Excalidraw whiteboard work. Always use this skill when the user asks to draw, generate, revise, or export any diagram.
version: 1.1.3
---

# Diagram Generator

## Purpose

Create and edit diagrams by converting user intent into a structured JSON specification, then delegating file generation to the `mcp-diagram-generator` MCP server.

Supported formats:
- Draw.io: `.drawio`
- Mermaid: `.mmd` or markdown Mermaid content
- Excalidraw: `.excalidraw`

Supported work:
- Natural-language diagram creation
- Existing `.drawio`, `.mmd`, and `.excalidraw` edits
- Default output paths under `diagrams/{format}/`
- Custom filenames and output paths

Contact: AlkaidY, `tccio2023@gmail.com`.

## Required MCP Tools

Before generating a diagram, verify that the MCP server tools are available:
- `mcp__mcp-diagram-generator__get_config`
- `mcp__mcp-diagram-generator__generate_diagram`
- `mcp__mcp-diagram-generator__init_config`

If the tools are missing, configure the MCP server.

Recommended remote configuration:

```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "npx",
      "args": ["-y", "mcp-diagram-generator"]
    }
  }
}
```

Local development configuration:

```json
{
  "mcpServers": {
    "mcp-diagram-generator": {
      "command": "node",
      "args": ["/absolute/path/to/mcp-diagram-generator/dist/index.js"]
    }
  }
}
```

After changing configuration, restart the agent environment. On first use, the server creates `.diagram-config.json` and default output directories.

## Main Workflow

### 1. Intake

For new diagrams, collect the basic options before accepting or processing the full diagram prompt:
- Diagram type
- Output format
- Layout direction
- Usage context
- Optional filename or output directory

Read `references/interaction-intake-guide.md` before asking intake questions.

Skip intake when the user already provided all required options and the full prompt. For existing-file edits, ask only for the target file and requested changes if missing.

### 2. Dispatch To A Playbook

Select exactly one primary playbook based on the diagram type:

| User Intent | Primary Playbook |
| --- | --- |
| Network topology, datacenter, zone, router, switch, firewall | `references/playbook-network-topology.md` |
| System architecture, application architecture, layered component diagram | `references/playbook-architecture.md` |
| Flowchart, process, decision tree | `references/playbook-flowchart.md` |
| Swimlane, cross-team handoff, approval workflow by department | `references/playbook-swimlane.md` |
| Sequence, class, ER, UML-style diagrams | `references/playbook-uml.md` |
| Whiteboard sketch, hand-drawn style, informal Excalidraw diagram | `references/playbook-excalidraw.md` |
| Unsure about format | `references/format-selection-guide.md` first, then the matching playbook |

Only read the playbook needed for the current diagram. If a playbook points to `json-schema-guide.md` or `network-topology-examples.md`, read only the relevant section.
For explicit geometry, also read `references/layout-quality-guide.md`.

### 3. Choose Format

Use these defaults unless the user explicitly chooses otherwise:

| Diagram Type | Default Format | Default Direction |
| --- | --- | --- |
| Network topology | Draw.io | Vertical |
| Architecture | Draw.io | Vertical or automatic |
| Flowchart | Mermaid | Vertical |
| Swimlane | Draw.io | Horizontal |
| Sequence | Mermaid | Automatic |
| Class | Mermaid | Automatic |
| ER | Mermaid | Automatic |
| Mind map | Mermaid | Automatic |
| Whiteboard sketch | Excalidraw | Automatic |

Usage context can override defaults:
- Word: prefer portrait-friendly vertical layouts.
- PPT: horizontal layouts are acceptable when readability improves.
- Code repositories and documentation: prefer Mermaid for simple flow, sequence, class, and ER diagrams.
- Whiteboard collaboration: prefer Excalidraw.
- Complex network or architecture diagrams: prefer Draw.io unless the user explicitly asks for Excalidraw.

### 4. Build The JSON Specification

Follow `references/json-schema-guide.md` for the schema. Core structure:

```json
{
  "format": "drawio",
  "diagramType": "architecture",
  "title": "Diagram title",
  "elements": [
    {
      "id": "unique-id",
      "type": "container",
      "name": "Display name",
      "level": "environment",
      "geometry": { "x": 0, "y": 0, "width": 800, "height": 600 },
      "children": []
    },
    {
      "type": "edge",
      "source": "source-id",
      "target": "target-id"
    }
  ]
}
```

Universal rules:
- `elements` must be an array.
- IDs must be unique.
- Edges must be top-level elements, never inside `children`.
- Edge `source` and `target` must resolve to an existing node or container.
- `style` must be an object.
- Colors should use `#RRGGBB`.
- Use `fillColor: "none"` for Draw.io no-fill nodes when needed.

### 5. Quality Gate

Before calling the MCP server, verify:
- The chosen format matches the intake answer and playbook.
- `diagramType` is explicit when supported.
- Layout direction is reflected in coordinates or generator-specific fields.
- Complex Draw.io and Excalidraw diagrams have explicit `geometry`.
- Container hierarchy is valid.
- Edges are top-level elements.
- Text and connector rules for the selected format are followed.

After generation, inspect the saved file enough to confirm the expected format-specific properties exist. For code changes to the MCP server, also run `npm run test:diagrams` from `mcp-diagram-generator/`.

### 6. Generate

Preferred call:

```json
{
  "diagram_spec": "<spec object>"
}
```

Optional filename:

```json
{
  "diagram_spec": "<spec object>",
  "filename": "my-diagram.drawio"
}
```

Optional explicit output path:

```json
{
  "diagram_spec": "<spec object>",
  "output_path": "custom/path/to/diagram.drawio"
}
```

The MCP server validates the schema, creates missing directories, and writes to the configured default directory when no output path is supplied.

## Configuration Helpers

Initialize defaults:

```text
init_config()
```

Set custom paths:

```json
{
  "paths": {
    "drawio": "output/diagrams/drawio",
    "mermaid": "output/diagrams/mermaid",
    "excalidraw": "output/diagrams/excalidraw"
  }
}
```

Inspect configuration:

```text
get_config()
```

Update one format path:

```json
{
  "format": "drawio",
  "path": "custom/drawio-path"
}
```

## Troubleshooting

Tool missing:
- Configure the MCP server and restart the agent environment.

Schema validation failed:
- Read `references/json-schema-guide.md`.
- Check required fields, unique IDs, edge source/target, and parent-child structure.

Directory error:
- Check write permissions.
- Run `get_config()`.
- Reinitialize with `init_config()` if needed.

Wrong extension:
- Draw.io uses `.drawio`.
- Mermaid uses `.mmd` or markdown output.
- Excalidraw uses `.excalidraw`.

Nested container issue:
- Child coordinates are relative to the direct parent.
- Container sizes must fit child bounds plus padding.
- Network topology must follow environment -> datacenter -> zone -> device.

## Reference Index

Read only what is needed:

- `references/interaction-intake-guide.md`: interactive intake defaults and question template.
- `references/format-selection-guide.md`: format selection matrix.
- `references/playbook-network-topology.md`: Draw.io and Excalidraw network topology rules.
- `references/playbook-architecture.md`: layered architecture rules.
- `references/playbook-flowchart.md`: process and decision flow rules.
- `references/playbook-swimlane.md`: swimlane and handoff rules.
- `references/playbook-uml.md`: sequence, class, and ER rules.
- `references/playbook-excalidraw.md`: Excalidraw whiteboard and binding rules.
- `references/layout-quality-guide.md`: explicit geometry, spacing, and connector readability rules.
- `references/json-schema-guide.md`: schema details and examples.
- `references/network-topology-examples.md`: network topology JSON patterns.

## Output Discipline

When responding to the user:
- Confirm the selected diagram type, format, direction, and output file.
- Do not paste the full JSON unless the user asks.
- Provide the saved file path.
- Mention any validation or regression command that was run.
