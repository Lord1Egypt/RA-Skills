---
name: drawio-skill
description: Create and edit draw.io diagrams through the configured drawio MCP server, including flowcharts, architecture diagrams, ML model diagrams, Chinese labels, animated connectors, and svg export.
---

# Draw.io Skill

Use this skill for all draw.io and diagrams.net work. This skill wraps the configured `drawio` MCP server; it does not replace the server.

## Required workflow

1. Start the draw.io session first.
- Call `start_session` before creating a new diagram or before inspecting or editing a diagram in a fresh session.

2. Create new diagrams from complete XML.
- Use `create_new_diagram` with a full `mxGraphModel`.
- Keep the diagram within a single viewport when practical.

3. Read before editing.
- Always call `get_diagram` before `edit_diagram`.
- Do not guess cell IDs.
- Preserve user changes already present in the live session.

4. Export deliverables.
- Export `.drawio` for editable source.
- Export `.svg` when the user needs a shareable artifact or when the diagram uses animated connectors.

5. Report outputs clearly.
- Tell the user which files were exported and where they were written.

## Export naming convention

- Write exports to the current workspace unless the user specifies a path.
- Derive a short kebab-case basename from the main topic when possible, such as `user-login-flow`, `payment-architecture`, or `event-pipeline`.
- If the topic is unclear, use `diagram`.
- For Chinese-language outputs, prefer an ASCII basename with a `-zh` suffix, such as `order-flow-zh`.
- For architecture diagrams, prefer `-architecture`, `-topology`, or `-flow` suffixes when they improve clarity.
- For machine-learning diagrams, prefer model-aware basenames such as `lstm-architecture`, `transformer-blocks`, or `cnn-pipeline`.
- When exporting both editable and shareable artifacts, keep the same basename for both, such as `diagram.drawio` and `diagram.svg`.
- Avoid spaces and non-ASCII characters in filenames unless the user explicitly requests them.

## Language and labeling rules

- If the request is primarily in Simplified Chinese, reply in Simplified Chinese.
- If the user wants Chinese labels, legends, or summaries, keep the diagram wording in Simplified Chinese.
- Keep standard abbreviations and proper nouns in their common form, such as API, Kafka, Redis, Kubernetes, LSTM, CNN, and Transformer.
- Keep node text short enough to fit inside shapes.

## General diagram rules

- Prefer clear left-to-right or top-to-bottom flow.
- Use explicit edge routing and waypoints when edges would otherwise overlap.
- Use titles, legends, and note boxes sparingly.
- Use color intentionally to separate data flow, control flow, or state.

## Architecture-specific rules

- Identify the major layers first, such as clients, edge, services, data, and external systems.
- Draw boundaries for environments or trust zones when relevant, such as browser, VPC, cluster, region, or third-party systems.
- Keep arrows directional and semantically consistent.
- Label protocols, topics, or data contracts only when they matter to the reader.
- Use containers for service groups, domains, or infrastructure groups instead of loose boxes.

## ML-diagram rules

- Show the main flow clearly from input to output.
- Use repeated blocks, grouped containers, and stage labels for model structure.
- Label tensor shape, sequence length, channel count, or embedding size only when it helps understanding.
- Use consistent color semantics for inputs, hidden states, attention paths, residual paths, and outputs.
- For recurrent or temporal models, make state flow visually distinct from data flow.
- For LSTM and RNN diagrams, separate cell state and hidden state.
- For Transformer diagrams, distinguish embeddings, attention, feed-forward blocks, residual paths, and normalization.
- For CNN diagrams, emphasize feature-map progression, pooling, skip paths, and classifier head.

## Animated connectors

When the user asks for animated connectors, flowing lines, or moving dashed lines:

- Add edge styling such as `dashed=1;dashPattern=8 4;flowAnimation=1;`.
- Keep arrowheads explicit with `endArrow=classic` unless the requested style suggests otherwise.
- Export to `.svg` because the animation is preserved there.

## Setup and recovery

This skill expects the `drawio` MCP server to already be configured and available.

- If the server is unavailable, tell the user that the drawio MCP connection needs to be configured or reconnected before continuing.
- After the connection is restored, restart the Codex session or reload the IDE window if the tools still do not appear.

## Good triggers

- "Create a system diagram in draw.io"
- "Create a Chinese-labeled draw.io diagram"
- "Edit this flowchart"
- "Export the current diagram as draw.io and svg"
- "Create a diagram with animated connectors"
- "Turn this process into a draw.io diagram"
- "Create a cloud architecture diagram"
- "Map a deployment topology"
- "Draw a business process flowchart"
- "Create an animated LSTM diagram"
- "Draw a Transformer architecture"
- "Create a CNN block diagram"
- "Update the existing draw.io layout and keep the same structure"
- "Generate a box-and-arrow diagram for this workflow"

## Limitations

- This skill depends on a working `drawio` MCP server.
- The editing workflow operates on the live draw.io session state exposed by the MCP tools.
- This skill does not bundle or install the MCP server by itself.
