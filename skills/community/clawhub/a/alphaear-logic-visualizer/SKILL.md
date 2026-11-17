---
name: alphaear-logic-visualizer
description: Use this skill to turn finance or investment logic into a visual diagram, especially transmission chains, thesis maps, causal loops, risk/benefit paths, and Draw.io-compatible mxGraph XML/HTML artifacts. Trigger when the user asks to visualize, draw, map, diagram, or explain complex finance logic visually. Do not use for raw data lookup, news search, stock screening, or signal tracking unless a diagram is the requested deliverable.
---

# AlphaEar Logic Visualizer

Create Draw.io-compatible finance logic diagrams from structured or semi-structured investment reasoning.

## Inputs

- Required: title or topic plus the logic chain to visualize.
- Preferred node shape: each node has `name`, `type` or `impact`, `logic`, and optional `evidence`.
- Ask a follow-up if the causal direction or main deliverable is unclear.

## Workflow

1. Extract nodes, causal edges, and impact polarity from the user's thesis.
2. Classify nodes as positive, negative, or neutral.
3. Use `references/PROMPTS.md` or `scripts/visualizer_prompt.py` to generate plain mxGraph XML.
4. Validate that the XML starts with `<mxGraphModel>` and ends with `</mxGraphModel>`.
5. Render to HTML with `VisualizerTools.render_drawio_to_html(xml_content, filename)` from `scripts/visualizer.py` when the user needs a file artifact.
6. Return the rendered HTML path and a concise explanation of the diagram structure.

## Output Contract

- Deliver Draw.io XML or an HTML file that embeds the diagram.
- Use left-to-right layout for transmission chains and top-to-bottom layout for hierarchies.
- Use green for positive, red for negative, and grey for neutral impacts.
- Avoid overlapping nodes and make edge labels short.

## Failure Handling

- If the thesis lacks enough structure, first produce a node/edge outline and ask for confirmation.
- If rendering fails, still return validated XML and explain how to open it in Draw.io.
- Do not invent unsupported financial relationships; mark uncertain links as assumptions.

## Validation

- Run or review `tests/test_visualizer.py` after changing scripts.
- Use `evals/evals.json` for routing and output-contract checks.
