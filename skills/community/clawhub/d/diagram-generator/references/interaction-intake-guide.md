# Interactive Intake Guide

Use this guide before creating a new diagram from natural language.

## Goal

Collect the few decisions that strongly affect layout quality before asking for the full diagram prompt.

Do not generate a diagram until both are clear:
- Basic options: diagram type, output format, layout direction, usage context.
- Full prompt: the user's actual diagram content.

## When To Ask

Ask intake questions when the user only says things like:
- "Draw a diagram for me."
- "Generate a network topology."
- "Use diagram-generator to create a diagram."
- "I want an architecture diagram."

Do not ask again when the user already provided:
- Diagram type
- Format or permission for the agent to recommend the format
- Layout direction or enough usage context to infer it
- Full diagram content

For editing an existing diagram, skip this intake. Ask only for the target file and requested change if they are missing.

## Intake Template

Ask in one concise message:

```text
Please confirm a few basics first:
1. Diagram type: network topology / architecture / flowchart / swimlane / sequence / class / ER / mind map / whiteboard sketch
2. Output format: Draw.io / Mermaid / Excalidraw / let me recommend
3. Layout direction: vertical / horizontal / automatic; network topology defaults to vertical
4. Usage context: Word / PPT / documentation / whiteboard collaboration / code repository
5. Filename or output directory: optional

After confirming these options, please provide the full diagram prompt.
```

## Defaults

Use these defaults only when the user selects "let me recommend" or "automatic", or when the usage context makes the choice obvious.

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

## Usage Context Rules

- Word: prefer portrait-friendly vertical layout.
- PPT: horizontal layout is acceptable when it improves first-slide readability.
- Documentation or code repository: prefer Mermaid for simple flow, sequence, class, and ER diagrams.
- Whiteboard collaboration: prefer Excalidraw.
- Complex network or architecture diagram: prefer Draw.io unless the user explicitly asks for Excalidraw.

## Prompt Handling

After the intake answers are clear, ask for the full prompt if the user has not provided it yet.

If the user provides the intake answers and prompt together, proceed directly.

Before generation, restate only the selected options in one short sentence, then generate the diagram. Do not restate the full prompt unless the user asks.

## Quality Gate

Before calling `generate_diagram`, check:
- `format` matches the selected or recommended format.
- `diagramType` is explicit when supported.
- Layout direction is reflected in coordinates or generator-specific fields.
- Complex Draw.io and Excalidraw diagrams have explicit `geometry`.
- Edges are top-level `elements`.
- For Excalidraw, labels are bound/grouped with shapes and connectors bind to element edges.
- For network topology, containers follow environment -> datacenter -> zone -> device.
