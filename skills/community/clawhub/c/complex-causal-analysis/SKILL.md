# Complex Causal Analysis

An interactive causal network visualization skill for analyzing cause-and-effect relationships in complex systems. Creates beautiful D3.js-based Sankey-style diagrams showing how factors connect and propagate through systems.

## Features

- **Hierarchical Layout**: Top-to-bottom flow from root causes to final outcomes
- **Interactive Nodes**: Click nodes to see details (causes, results, evidence)
- **Draggable Elements**: Drag any node to reposition; connections follow automatically
- **Color-coded Strength**: Green = strong (8-10), Yellow = medium (5-7) causal relationships
- **Directional Arrows**: Small arrows in the middle of each link showing causation direction
- **Evidence Support**: Each node can include historical or factual evidence
- **Fixed Sidebar**: Stays on screen while zooming/panning the graph
- **Zoom & Pan**: Mouse wheel to zoom, drag canvas to pan

## Use Cases

- Historical event analysis (dynasty collapses, wars, revolutions)
- Business cause-and-effect mapping
- Scientific phenomenon chains
- Problem root cause analysis
- Decision tree visualization

## Input Format

Provide JSON with this structure:

```json
{
  "title": "Topic Name",
  "nodes": [
    { "id": "Node Name", "layer": 3, "type": "Category", "desc": "Description", "color": "#hex" }
  ],
  "links": [
    { "source": "Cause", "target": "Effect", "strength": 8 }
  ]
}
```

## Layer Conventions

- **Layer 3**: Root causes / Deep factors
- **Layer 2**: Intermediate factors
- **Layer 1**: Direct causes
- **Layer 0**: Final outcomes

## Strength Guidelines

- **8-10**: Strong causal relationship
- **5-7**: Medium causal relationship  
- **1-4**: Weak (exclude)

## Example Prompt

```
Create a causal network visualization for [TOPIC].

Nodes:
- [list with id, layer, type, description]

Links:
- [list source → target with strength 1-10]

Requirements:
- Top-to-bottom layout
- Only medium (5-7) and strong (8-10) relationships
- Add small arrow in middle of each link
- Node details show causes and results
- Include evidence/support for each node
```

## Output

Generates a standalone HTML file with:
- Embedded D3.js (via CDN)
- No external dependencies
- Works in any modern browser
- Mobile-responsive

## Skill Activation

When you activate this skill, provide:
1. Your topic/theme
2. List of causal factors (nodes)
3. Relationships between factors (links)

The skill will generate the JSON and produce a clickable HTML file you can open in your browser.

## Technical Details

- Built with D3.js v7
- Bezier curves for smooth link paths
- Force-directed initial positioning with manual adjustment
- SVG-based rendering for crisp graphics
- Dark theme with gradient background

---

**Tags**: visualization, d3, causal-network, history, analysis, interactive