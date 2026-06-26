---
name: d2-diagram-creator
description: "Generate D2 diagram code supporting flowcharts, system architecture diagrams, organizational charts, service topology diagrams, state machine diagrams, swimlane diagrams, sequence diagrams, SQL table relationship diagrams, and grid diagrams. Use when users need to: (1) create or generate flowcharts and process diagrams, (2) design system architecture or infrastructure diagrams, (3) build state machine or sequence diagrams, (4) visualize relationships between components, entities or services, (5) create swimlane diagrams for cross-functional processes, (6) design database table structures and ER diagrams, (7) create grid layouts or dashboard designs, or any diagram that can be represented with nodes, connections, and containers in D2 syntax."
license: MIT
metadata:
  author: Fur1na
  version: "1.0.0"
---

# D2 Diagram Creator

Three-agent pipeline for high-quality diagram generation:

```
AskUserQuestion → Agent 1 (Analyzer) → Agent 2 (Generator) → Agent 3 (Validator)
```

Each agent is a `general-purpose` subagent with its own focused instructions. You (the main agent) orchestrate the pipeline — ask the user questions, then spawn agents in sequence, passing outputs forward.

---

## Step 1: Ask Requirements

Use AskUserQuestion to ask all questions at once. Do not split into multiple rounds, do not skip any.

### First round (always required)

```json
{
  "questions": [
    {
      "question": "How detailed should the diagram be?",
      "header": "Detail Level",
      "options": [
        { "label": "Core Flow", "description": "5-8 nodes" },
        { "label": "Moderate", "description": "10-15 nodes" },
        { "label": "Full Detail", "description": "Include all details and exception branches" }
      ]
    },
    {
      "question": "What is the layout direction of the diagram?",
      "header": "Layout Direction",
      "options": [
        { "label": "Horizontal", "description": "direction: right, left to right" },
        { "label": "Vertical", "description": "direction: down, top to bottom" }
      ]
    },
    {
      "question": "What format to export as?",
      "header": "Export Format",
      "options": [
        { "label": "D2 Code Only", "description": "No image export" },
        { "label": "SVG", "description": "Vector graphics (recommended)" },
        { "label": "PNG", "description": "Bitmap" },
        { "label": "Preview", "description": "ASCII text" }
      ]
    }
  ]
}
```

### Second round (only when SVG/PNG is selected)

```json
{
  "questions": [
    {
      "question": "Which theme to use?",
      "header": "Theme",
      "options": [
        { "label": "Light Theme", "description": "--theme 0, white background (default)" },
        { "label": "Dark Theme", "description": "--theme 200, dark background" }
      ]
    },
    {
      "question": "Enable hand-drawn sketch style?",
      "header": "Sketch",
      "options": [
        { "label": "No", "description": "Normal style (default)" },
        { "label": "Yes", "description": "--sketch, hand-drawn effect" }
      ]
    },
    {
      "question": "Choose layout engine?",
      "header": "Layout Engine",
      "options": [
        { "label": "dagre", "description": "Default, fast and efficient" },
        { "label": "elk", "description": "Complex diagrams, 100+ nodes" },
        { "label": "tala", "description": "Most powerful, SVG only, requires installation" }
      ]
    }
  ]
}
```

Only provide 2 theme options (Light/Dark). Do not add colorful, terminal, or other themes.

---

## Step 2: Spawn Analyzer Agent

Use the Agent tool to spawn the requirements analyzer. This agent deeply analyzes the user's request and produces a structured JSON document.

- **subagent_type**: `general-purpose`
- **description**: `Analyze diagram requirements`

The prompt should be:

```
Read the file at <skill-base-path>/agents/analyzer.md for your instructions.

Analyze this diagram request:

User request: <user's original description>

User preferences:
- Detail level: <answer>
- Layout direction: <answer>
- Export format: <answer>
- Theme: <answer, or "not selected">
- Sketch: <answer, or "not selected">
- Layout engine: <answer, or "not selected">

Return the structured requirements JSON.
```

Save the returned JSON — you will pass it to the generator agent.

---

## Step 3: Spawn Generator Agent

Use the Agent tool to spawn the D2 code generator.

- **subagent_type**: `general-purpose`
- **description**: `Generate D2 diagram code`

The prompt should be:

```
Read the file at <skill-base-path>/agents/generator.md for your instructions.

Generate D2 code based on these requirements:

<the requirements JSON from Step 2>

Read the diagram type guide at:
<skill-base-path>/references/diagram-types/<diagram_type>.md

Save the D2 code to a .d2 file (use a descriptive filename).
Return the file path.
```

Save the returned file path — you will pass it to the validator agent.

---

## Step 4: Spawn Validator Agent

Use the Agent tool to spawn the validator.

- **subagent_type**: `general-purpose`
- **description**: `Validate and export diagram`

The prompt should be:

```
Read the file at <skill-base-path>/agents/validator.md for your instructions.

Your skill base directory is: <skill-base-path>
The watermark removal script is at: <skill-base-path>/scripts/remove_watermark.py

Validate and export:

D2 file: <path from Step 3>
Requirements: <the requirements JSON>

Export preferences:
- Format: <export_format>
- Theme: <theme or "default">
- Sketch: <sketch or false>
- Layout engine: <engine or "dagre">

Fix any issues and export the final diagram.
```

Report the validator's summary to the user.

---

## Diagram Types Reference

| Type | Use Case |
|------|----------|
| **Flowchart** | Business processes, decision trees, algorithm flows |
| **System Architecture** | Component relationships, infrastructure, service interactions |
| **Organizational Chart** | Hierarchical structures, reporting relationships |
| **Service Topology** | Cloud architecture, network topology |
| **State Machine** | State transitions, workflow states, lifecycles |
| **Swimlane Diagram** | Cross-functional processes, multi-role workflows |
| **Sequence Diagram** | Time-based interactions, protocol flows |
| **SQL Table Diagram** | Database schemas, ER diagrams |
| **Grid Diagram** | Dashboard layouts, UI prototypes |

---

## Prohibitions

1. Do not skip requirement questions — always ask first
2. Do not add visual styles unless the user explicitly requests them
3. Do not add a diagram title unless the user explicitly requests one
4. Do not skip any of the three agents — the pipeline must run to completion
