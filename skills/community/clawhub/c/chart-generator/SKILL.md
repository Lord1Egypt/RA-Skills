---
name: chart-generator
description: "Chart Generator: Create many types of charts and graphs from data with built in styling and theme - including bar, line, pie, scatter, doughnut, radar. Use when an agent needs chart generator, create business dashboards with professional charts, generate marketing reports with colorful visualizations, build presentation slides with modern dark themed graphs, produce academic papers with publication quality figures, generate chart, chart type, data through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/chart-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/chart-generator"}}
---
# Chart Generator

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Generate modern, professional charts and graphs from data. Supports multiple chart types including bar, line, pie, scatter, doughnut, radar, and more. Features five preset themes for different use cases: Corporate (professional blues and grays), Modern Dark (presentation-ready with vibrant accents), Minimal (publication-quality with subtle colors), Colorful (marketing-friendly with distinct hues), and Academic (colorblind-accessible). Charts can be exported in multiple formats including PNG, SVG, PDF, and WebP. The tool handles custom styling, responsive sizing, gradient fills, data labels, and complex configurations. Perfect for creating data visualizations for reports, presentations, dashboards, social media, and documentation. Returns chart images as signed URLs with configurable expiration or as base64-encoded data for immediate embedding.

## Product Instructions
### Chart Generator - Tool Instructions

#### Overview
Generate modern, professional charts and graphs from data. Supports 9 chart types (bar, line, pie, doughnut, scatter, bubble, radar, polar area, horizontal bar), 5 preset themes plus custom styling, and 4 export formats (PNG, SVG, PDF, WebP). Charts can be returned as cloud-stored file URLs or base64-encoded data for immediate embedding. Powered by QuickChart API (Chart.js compatible).

---

#### Actions

##### generate_chart
Generate a chart image from structured data with theme and format options.

**Required Parameters:**
- `chart_type` (string): Type of chart. One of: `"bar"`, `"line"`, `"pie"`, `"doughnut"`, `"scatter"`, `"bubble"`, `"radar"`, `"polarArea"`, `"horizontalBar"`
- `data` (object): Chart.js compatible data object. Must contain `labels` (array of strings) and/or `datasets` (array of dataset objects). Each dataset has `label` (string), `data` (array of numbers or point objects), and optional color overrides (`backgroundColor`, `borderColor`, `borderWidth`).

**Optional Parameters:**
- `theme` (string, default: `"corporate"`): Preset theme. One of:
  - `"corporate"` - Professional blues/grays, white background, top legend. Best for business reports.
  - `"modern_dark"` - Dark background (#1E1E1E) with vibrant accent colors, bottom legend. Best for presentations.
  - `"minimal"` - Black/white/gray tones, very subtle grid. Best for publications.
  - `"colorful"` - Vibrant pink/blue/yellow/teal/purple/orange. Best for marketing and social media.
  - `"academic"` - Colorblind-accessible palette (blue, orange, green, purple, brown, gray), black grid. Best for scientific publications.
  - `"custom"` - No preset applied; use `custom_options` to style from scratch.
- `width` (integer, default: 600, range: 100-2000): Chart width in pixels.
- `height` (integer, default: 400, range: 100-2000): Chart height in pixels.
- `title` (string): Chart title text displayed on the chart.
- `background_color` (string, default: `"white"`): Background color. Accepts named colors (`"white"`, `"transparent"`), HEX (`"#FFFFFF"`), RGB (`"rgb(255,255,255)"`), or HSL.
- `output_format` (string, default: `"png"`): Output format. One of: `"png"` (raster), `"svg"` (vector, scalable), `"pdf"` (document), `"webp"` (compressed).
- `device_pixel_ratio` (integer, default: 1): `1` for normal displays, `2` for retina/high-DPI displays.
- `custom_options` (object): Custom Chart.js options object to override theme defaults. Supports any Chart.js 3.x/4.x option (plugins, scales, etc.).
- `return_base64` (boolean, default: false): If true, returns base64-encoded image data instead of a file URL. Useful for embedding in emails or immediate display.
- `store_file` (boolean, default: true): If true, stores the chart in cloud storage and returns a signed download URL.
- `expiration_days` (integer, default: 7, range: 1-7): Number of days until the stored file expires and is automatically deleted.

**Example - Simple Bar Chart:**
```json
{
  "action": "generate_chart",
  "chart_type": "bar",
  "data": {
    "labels": ["Q1", "Q2", "Q3", "Q4"],
    "datasets": [{"label": "Revenue", "data": [45000, 52000, 48000, 61000]}]
  },
  "title": "Quarterly Revenue 2025",
  "theme": "corporate",
  "width": 800,
  "height": 500
}
```

**Example - Multi-Dataset Line Chart (Dark Theme, Retina):**
```json
{
  "action": "generate_chart",
  "chart_type": "line",
  "data": {
    "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "datasets": [
      {"label": "Product A", "data": [12, 19, 15, 22, 28, 25]},
      {"label": "Product B", "data": [8, 14, 18, 16, 20, 24]}
    ]
  },
  "title": "Product Sales Comparison",
  "theme": "modern_dark",
  "width": 1000,
  "height": 600,
  "output_format": "png",
  "device_pixel_ratio": 2
}
```

**Example - Pie Chart (Colorful):**
```json
{
  "action": "generate_chart",
  "chart_type": "pie",
  "data": {
    "labels": ["Desktop", "Mobile", "Tablet"],
    "datasets": [{"data": [55, 35, 10]}]
  },
  "title": "Traffic by Device",
  "theme": "colorful"
}
```

**Example - Scatter Plot (Academic, SVG):**
```json
{
  "action": "generate_chart",
  "chart_type": "scatter",
  "data": {
    "datasets": [{
      "label": "Sample Data",
      "data": [{"x": 10, "y": 20}, {"x": 15, "y": 25}, {"x": 20, "y": 22}, {"x": 25, "y": 30}]
    }]
  },
  "title": "Correlation Analysis",
  "theme": "academic",
  "width": 700,
  "height": 500,
  "output_format": "svg"
}
```

**Example - Custom Styled Chart:**
```json
{
  "action": "generate_chart",
  "chart_type": "bar",
  "data": {
    "labels": ["Mon", "Tue", "Wed", "Thu", "Fri"],
    "datasets": [{"label": "Tasks Completed", "data": [5, 8, 12, 7, 10]}]
  },
  "title": "Weekly Productivity",
  "theme": "custom",
  "background_color": "#F5F5F5",
  "custom_options": {
    "plugins": {"legend": {"display": false}},
    "scales": {"y": {"beginAtZero": true, "grid": {"color": "rgba(0, 0, 0, 0.1)"}}}
  }
}
```

**Example - Base64 Return (No File Storage):**
```json
{
  "action": "generate_chart",
  "chart_type": "line",
  "data": {
    "labels": ["1", "2", "3", "4", "5"],
    "datasets": [{"label": "Values", "data": [10, 20, 15, 25, 30]}]
  },
  "theme": "minimal",
  "return_base64": true,
  "store_file": false
}
```

**Example - PDF Export with Custom Expiration:**
```json
{
  "action": "generate_chart",
  "chart_type": "bar",
  "data": {
    "labels": ["Category A", "Category B", "Category C"],
    "datasets": [{"label": "Results", "data": [65, 85, 75]}]
  },
  "title": "Survey Results",
  "theme": "corporate",
  "output_format": "pdf",
  "width": 800,
  "height": 600,
  "expiration_days": 3
}
```

**Response fields:**
- `chart_type`: Chart type used
- `theme`: Theme applied
- `format`: Output format
- `width`, `height`: Dimensions
- `size_bytes`: File size in bytes
- When `return_base64` is true: `base64_data` (string), `content_type` (MIME type)
- When `store_file` is true: `file_id` (string), `signed_url` (temporary download URL), `expiration_date` (ISO date)

---

#### Data Format

Standard chart types (bar, line, pie, doughnut, radar, polarArea, horizontalBar):
```json
{
  "labels": ["Label 1", "Label 2", "Label 3"],
  "datasets": [{
    "label": "Dataset Name",
    "data": [10, 20, 30],
    "backgroundColor": "optional color override",
    "borderColor": "optional border color",
    "borderWidth": 1
  }]
}
```

Scatter and bubble charts use point objects instead of simple values:
```json
{
  "datasets": [{
    "label": "Points",
    "data": [{"x": 10, "y": 20}, {"x": 15, "y": 25}]
  }]
}
```

Multiple datasets are supported. Theme colors are auto-assigned to datasets that do not specify their own colors.

---

#### Workflows

1. **Business Dashboard Chart** - Use `generate_chart` with `theme: "corporate"`, a bar or line chart, and `store_file: true` to get a signed URL for embedding in reports.
2. **Email-Embedded Chart** - Use `generate_chart` with `return_base64: true` and `store_file: false` to get base64 data for inline embedding in emails.
3. **Scientific Publication Figure** - Use `generate_chart` with `theme: "academic"`, `output_format: "svg"` for scalable vector output suitable for print.
4. **Marketing Infographic** - Use `generate_chart` with `theme: "colorful"`, pie or doughnut chart, and `device_pixel_ratio: 2` for high-resolution social media images.
5. **Dark Mode Presentation Slide** - Use `generate_chart` with `theme: "modern_dark"`, large dimensions (1920x1080), and `device_pixel_ratio: 2`.
6. **Custom Branded Chart** - Use `theme: "custom"` with `custom_options` to apply your own colors, fonts, grid styles, and legend placement.

---

#### Notes

- Maximum chart dimensions are 2000x2000 pixels.
- Stored files expire after 1-7 days (configurable via `expiration_days`).
- The `data` object must contain at least a `datasets` array. The `labels` array is required for most chart types but not for scatter/bubble charts.
- When using `theme: "custom"`, no preset styling is applied. Combine with `custom_options` for full control.
- `custom_options` merges on top of theme defaults, so you can start with a theme and override specific options.
- The `device_pixel_ratio: 2` option doubles the rendered resolution (useful for retina displays) but also increases file size.
- If both `return_base64: true` and `store_file: true` are set, you get both the base64 data and a stored file URL.
- Validation: `chart_type` and `data` are required for `generate_chart`. Missing either returns a 400 error.
- Recommended sizes: social media 800x600, reports 1000x600, presentations 1920x1080.

## When To Use
- Use this skill for `Chart Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: chart generator, create business dashboards with professional charts, generate marketing reports with colorful visualizations, build presentation slides with modern dark themed graphs, produce academic papers with publication quality figures, generate chart, chart type, data.
- Supported action names: `generate_chart`.

## Use Cases
- Create business dashboards with professional charts
- Generate marketing reports with colorful visualizations
- Build presentation slides with modern dark-themed graphs
- Produce academic papers with publication-quality figures
- Design social media infographics with custom styling
- Automate report generation with data-driven charts
- Create real-time monitoring dashboards
- Generate email campaign analytics visualizations
- Build data analysis notebooks with embedded charts
- Produce financial reports with professional formatting

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `generate_chart` (action slug: `generate-chart`): Generate a modern, professional chart image from structured data. Supports 9 chart types (bar, line, pie, doughnut, scatter, bubble, radar, polarArea, horizontalBar), 5 preset themes plus custom styling, and 4 export formats (PNG, SVG, PDF, WebP). Returns chart as a cloud-stored file URL or base64-encoded data. Price: `2` credits. Parameters: `background_color`, `chart_type`, `custom_options`, `data`, `device_pixel_ratio`, `expiration_days`, `height`, `output_format`, plus 5 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "chart-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "chart-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "chart-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "chart-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "chart-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "chart-generator"
  }
}
```

## Call This Tool
Product slug: `chart-generator`

Marketplace page: https://www.agentpmt.com/marketplace/chart-generator

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Chart-Generator",
    "arguments": {
      "action": "generate_chart",
      "background_color": "white",
      "chart_type": "bar",
      "custom_options": {},
      "data": {
        "datasets": [
          {
            "backgroundColor": "example backgroundColor",
            "borderColor": "example borderColor",
            "borderWidth": 1,
            "data": [
              1
            ],
            "label": "example label"
          }
        ],
        "labels": [
          "example label"
        ]
      },
      "device_pixel_ratio": 1,
      "expiration_days": 7,
      "height": 400,
      "output_format": "png"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "chart-generator",
  "parameters": {
    "action": "generate_chart",
    "background_color": "white",
    "chart_type": "bar",
    "custom_options": {},
    "data": {
      "datasets": [
        {
          "backgroundColor": "example backgroundColor",
          "borderColor": "example borderColor",
          "borderWidth": 1,
          "data": [
            1
          ],
          "label": "example label"
        }
      ],
      "labels": [
        "example label"
      ]
    },
    "device_pixel_ratio": 1,
    "expiration_days": 7,
    "height": 400,
    "output_format": "png"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `generate_chart` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/chart-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
