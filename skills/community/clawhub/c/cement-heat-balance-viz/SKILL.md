---
name: cement-heat-balance-viz
description: Generate visualizations for cement production heat balance analysis including process flow diagrams, energy distribution charts, and temperature profiles. Use when users need to visualize cement plant thermal processes, heat balance data, or energy flow diagrams.
---

# Cement Heat Balance Visualization Skill

This skill creates visual representations of cement production heat balance data including process flow diagrams, Sankey diagrams for energy distribution, and temperature profiles along the production line.

## When to Use This Skill

Use this skill when users need to:
- Visualize cement plant thermal processes
- Show energy input/output distributions
- Create temperature profile diagrams along production stages
- Generate Sankey diagrams for heat balance analysis
- Produce professional technical diagrams for presentations or reports

## Core Concepts

The skill works with cement production data including:
- Temperature readings at different process stages
- Energy input sources (coal powder, alternative fuels)
- Energy output distribution (product heat, losses, etc.)
- Process flow visualization
- KPI metrics display

## Standard Workflow

1. **Analyze the heat balance data** - Understand the input parameters and output distributions
2. **Select visualization type** - Choose appropriate chart type based on data characteristics
3. **Generate the visualization** - Create HTML/CSS/JS visualization with proper styling
4. **Add annotations and labels** - Include units, descriptions, and key insights
5. **Provide the output** - Return the visualization as an HTML file that can be viewed in browsers

## Available Visualization Types

- **Process Flow Diagram** - Shows temperature progression through kiln stages
- **Energy Sankey Diagram** - Visualizes energy input/output flows
- **Temperature Profile Chart** - Line chart showing temperature vs. process length
- **KPI Dashboard** - Displays key performance indicators
- **Combined Report** - Integrates multiple visualizations in one report

## Implementation Details

The skill generates responsive HTML visualizations that:
- Work in modern browsers without external dependencies
- Use CSS gradients and animations for professional appearance
- Include proper Chinese/English labels as needed
- Are print-friendly and presentation-ready
- Follow the existing styling conventions from the cement-heat-balance.html template

## Customization Options

Users can specify:
- Color schemes (default: industrial theme with blues, reds, and yellows)
- Units (metric/imperial)
- Level of detail (overview vs. detailed)
- Output format (standalone HTML or embeddable component)
- Interactive elements (hover tooltips, clickable details)

## Example Usage

When a user provides cement heat balance data like:
```
Input: Coal powder - 100%
Output: 
- Product heat: 45%
- Kiln shell radiation: 15%
- Exhaust losses: 12%
- Mechanical stirring: 8%
- Raw material drying: 10%
- Preheater losses: 5%
- Other losses: 5%
```

The skill can generate:
1. A Sankey diagram showing these flows
2. A process flow diagram with temperature annotations
3. A KPI display showing efficiency metrics
4. A combined technical report

## Best Practices

- Maintain consistency with existing cement visualization styling
- Use appropriate units (°C, %, kcal/kg, etc.)
- Include clear legends and axis labels
- Highlight key efficiency metrics
- Ensure accessibility with proper color contrast
- Keep designs clean and professional for technical audiences