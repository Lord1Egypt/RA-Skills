# Advanced Chart — Sub-Skill

## When to Use

User needs complex visualizations that go beyond basic charts:
- **Dashboards** with multiple charts in a layout
- **Gantt charts** for project timelines
- **Diagrams** (flowchart, sequence, ER, mind map)
- **PPT generation** with embedded visualizations
- **Advanced analysis** (YoY, cross-file joins, trend analysis)
- **Professional themes** and export options

## Implementation

This capability delegates to the **ChartGen** skill, which provides AI-powered visualization via the ChartGen API.

### Step 1 — Check ChartGen Availability

Verify that the `chartgen` skill is installed and configured. Look for the skill at:
- `../chartgen-skill/SKILL.md` (sibling directory)
- Or installed via OpenClaw's skill system

### Step 2 — If ChartGen is Available

Follow the ChartGen skill's workflow:

1. Read and follow the instructions in the ChartGen `SKILL.md`
2. The ChartGen skill handles:
   - Confirming the request with the user
   - Submitting to ChartGen API
   - Polling for results
   - Delivering artifacts (images, PPT, dashboards)

**Important**: ChartGen requires an API key. If not configured, it will provide setup instructions.

### Step 3 — If ChartGen is NOT Available

Inform the user and offer alternatives:

> The advanced chart capability requires **ChartGen AI** which is not currently installed.
>
> **Options:**
> 1. **Install ChartGen**: Tell me "install skill https://github.com/chartgen-ai/chartgen-skill.git"
> 2. **Use basic charts**: I can create bar, line, pie, scatter, and area charts locally (no API needed)
> 3. **Export data**: I can clean and export your data for use in other visualization tools

### Fallback to Basic Charts

If the user's request can be partially fulfilled with basic charts:

> Your request involves a dashboard layout, which needs ChartGen. However, I can create individual charts locally:
> - A line chart for the time-series data
> - A bar chart for the category comparison
>
> Want me to create these basic charts instead?

## ChartGen Capabilities Reference

When ChartGen is available, it supports:

| Type | Output | Description |
|------|--------|-------------|
| Charts | PNG | All ECharts types: bar, line, pie, scatter, heatmap, radar, treemap, etc. |
| Diagrams | PNG | Flowchart, sequence, class, state, ER, mind map, timeline |
| Dashboards | PNG/HTML | Multi-chart interactive layouts |
| Gantt | PNG | Project timelines with dependencies |
| PPT | PPTX | Presentation slides with visualizations |
| Reports | Text + Charts | Analysis reports with insights |
