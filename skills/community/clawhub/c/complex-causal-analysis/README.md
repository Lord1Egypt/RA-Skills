# Complex Causal Analysis

Visualize cause-and-effect relationships with interactive D3.js causal network diagrams.

![Preview](preview.png)

## What It Does

Transforms lists of causal factors into beautiful, interactive network visualizations. Perfect for analyzing historical events, business systems, or any complex cause-and-effect relationships.

## Features

- 🎯 **Hierarchical Layout** - Root causes at top, outcomes at bottom
- 🖱️ **Draggable Nodes** - Rearrange elements freely; connections follow
- 🎨 **Color-coded Strength** - Green (strong) / Yellow (medium) relationships
- ➡️ **Directional Arrows** - Arrows in middle of each link show direction
- 📋 **Click for Details** - See causes, results, and evidence for each node
- 🔍 **Zoom & Pan** - Explore large networks easily
- 📱 **Fixed Sidebar** - Node list stays visible while navigating

## Quick Example

Input:
```json
{
  "title": "Roman Empire Fall",
  "nodes": [
    { "id": "Economic Crisis", "layer": 3, "type": "Economic", "desc": "Hyperinflation, trade collapse" },
    { "id": "Military Overextension", "layer": 2, "type": "Military", "desc": "Too many frontiers to defend" },
    { "id": "Rome Falls", "layer": 0, "type": "Outcome", "desc": "Western Empire ends 476 AD" }
  ],
  "links": [
    { "source": "Economic Crisis", "target": "Military Overextension", "strength": 8 },
    { "source": "Military Overextension", "target": "Rome Falls", "strength": 9 }
  ]
}
```

Output: Interactive HTML visualization you can open in any browser!

## Usage

1. Activate the skill
2. Provide your topic and causal factors
3. Receive a downloadable HTML file
4. Open in browser to explore interactively

## Use Cases

- Historical analysis (why did empires fall?)
- Business root cause analysis
- Scientific cause-effect chains
- Problem diagnosis
- Decision mapping

---

**Author**: 得志 ( Dezhi )  
**Tags**: visualization, d3, causal-network, history, analysis  
**Version**: 1.1.0