---
name: elevation-data-point-path-charts-statistics
description: "Elevation Data - Point, Path, Charts & Statistics: Get elevation data for points or paths. Use when an agent needs elevation data point, path, charts & statistics, elevation data point path charts statistics, hiking trail elevation profile analysis, cycling route difficulty assessment, geographic surveying and flood risk mapping, real estate site elevation evaluation, get elevation, locations through AgentPMT-hosted remote tool calls. Discovery terms: elevation data point, path."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/elevation-data-point-path-charts-statistics
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/elevation-data-point-path-charts-statistics"}}
---
# Elevation Data - Point, Path, Charts & Statistics

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Comprehensive elevation data tool that provides elevation information for any location on Earth including ocean floor depths. The tool offers discrete location elevation lookups for up to 512 points, elevation sampling along defined paths with configurable resolution, automatic elevation profile generation with visualization charts, and detailed statistics including minimum maximum average elevation gain total ascent and descent. Features elevation data in both meters and feet with resolution accuracy indicators, elevation categorization from below sea level to very high elevation, distance calculations for path-based requests, and optional chart generation saved to cloud storage. Perfect for hiking and trail planning applications, geographic surveying and terrain analysis, cycling route optimization, real estate site assessment, and adventure sports planning.

## Product Instructions
### Elevation Data - Point, Path, Charts & Statistics

Get elevation data for any location on Earth. Look up elevations for individual points, sample elevations along a path, and generate visual elevation profile charts with statistics.

#### Actions

##### get_elevation

Get elevation data for one or more discrete locations. Returns elevation in meters and feet, resolution, and an elevation category for each point. When multiple locations are provided, includes aggregate statistics (min, max, average, gain, ascent, descent).

**Required fields:**
- `action` — `"get_elevation"`
- `locations` — Array of location objects (max 512), each with:
  - `latitude` (number, -90 to 90)
  - `longitude` (number, -180 to 180)

**Example — Single point:**
```json
{
  "action": "get_elevation",
  "locations": [
    {"latitude": 27.9881, "longitude": 86.9250}
  ]
}
```

**Example — Multiple points with statistics:**
```json
{
  "action": "get_elevation",
  "locations": [
    {"latitude": 37.7749, "longitude": -122.4194},
    {"latitude": 36.5785, "longitude": -118.2923},
    {"latitude": 36.2388, "longitude": -116.8318}
  ]
}
```

---

##### get_path_elevation

Sample elevation values at evenly-spaced points along a path defined by two or more waypoints. Returns elevation data for each sample point plus path statistics including total distance, ascent, and descent.

**Required fields:**
- `action` — `"get_path_elevation"`
- `path` — Array of at least 2 location objects, each with:
  - `latitude` (number, -90 to 90)
  - `longitude` (number, -180 to 180)

**Optional fields:**
- `samples` — Number of evenly-spaced sample points along the path (2–512, default 100)
- `generate_chart` — Set to `true` to also generate an elevation profile chart image (default false)
- `chart_width` — Chart width in inches (6–20, default 12). Only used when a chart is generated.
- `chart_height` — Chart height in inches (4–12, default 6). Only used when a chart is generated.

**Example — Path with 50 samples:**
```json
{
  "action": "get_path_elevation",
  "path": [
    {"latitude": 36.5785, "longitude": -118.2923},
    {"latitude": 36.2388, "longitude": -116.8318}
  ],
  "samples": 50
}
```

**Example — Path with chart generation:**
```json
{
  "action": "get_path_elevation",
  "path": [
    {"latitude": 46.8523, "longitude": -121.7603},
    {"latitude": 46.7867, "longitude": -121.7354}
  ],
  "samples": 200,
  "generate_chart": true,
  "chart_width": 14,
  "chart_height": 8
}
```

---

##### get_elevation_profile

Same as `get_path_elevation` but always generates an elevation profile chart image. The chart shows elevation vs. distance with min/max markers and dual axes (meters and feet). A signed URL to the chart image is included in the response.

**Required fields:**
- `action` — `"get_elevation_profile"`
- `path` — Array of at least 2 location objects, each with:
  - `latitude` (number, -90 to 90)
  - `longitude` (number, -180 to 180)

**Optional fields:**
- `samples` — Number of sample points along the path (2–512, default 100)
- `chart_width` — Chart width in inches (6–20, default 12)
- `chart_height` — Chart height in inches (4–12, default 6)

**Example — Elevation profile for a hiking trail:**
```json
{
  "action": "get_elevation_profile",
  "path": [
    {"latitude": 36.5785, "longitude": -118.2923},
    {"latitude": 36.4600, "longitude": -118.1700},
    {"latitude": 36.2388, "longitude": -116.8318}
  ],
  "samples": 100,
  "chart_width": 12,
  "chart_height": 6
}
```

---

#### Response Details

##### Elevation data per point
Each result includes:
- `elevation_meters` / `elevation_feet` — Elevation in both units
- `resolution_meters` — Data resolution (distance between data points used for interpolation)
- `category` — One of: `below_sea_level`, `low_elevation`, `moderate_elevation`, `high_elevation`, `very_high_elevation`
- `description` — Human-readable elevation description
- `location` — Coordinates of the point

##### Statistics (returned for multi-point and path queries)
- Min, max, and average elevation (meters and feet)
- Elevation gain, total ascent, and total descent (meters and feet)
- Total distance in km and miles (path queries only)

##### Chart output (path actions with chart enabled)
- `elevation_chart.signed_url` — Direct link to the PNG chart image. Always present this URL to the user.
- `elevation_chart.file_id` — Storage reference ID
- `elevation_chart.filename` — File name
- The chart expires after 7 days.

#### Common Workflows

1. **Check elevation of a city** — Use `get_elevation` with a single location.
2. **Compare elevations of multiple places** — Use `get_elevation` with several locations to get comparative statistics.
3. **Analyze a hiking route** — Use `get_elevation_profile` with waypoints along the trail to see total ascent/descent and a visual chart.
4. **Assess road grade between two points** — Use `get_path_elevation` with start/end points and a high sample count for detailed elevation changes.

#### Important Notes

- Coordinates must be in decimal degrees (not DMS format). Convert addresses to coordinates before calling this tool.
- The `locations` parameter is for `get_elevation` only; the `path` parameter is for `get_path_elevation` and `get_elevation_profile`.
- Higher `samples` values give more detailed path data but use more API quota. Use 50–100 for overview, 200+ for detailed analysis.
- Chart images are stored for 7 days and accessible via the signed URL in the response.
- Maximum of 512 locations per `get_elevation` call or 512 samples per path call.

## When To Use
- Use this skill for `Elevation Data - Point, Path, Charts & Statistics` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: elevation data   point, path, charts & statistics, elevation data point path charts statistics, hiking trail elevation profile analysis, cycling route difficulty assessment, geographic surveying and flood risk mapping, real estate site elevation evaluation, get elevation, locations.
- Supported action names: `get_elevation`, `get_elevation_profile`, `get_path_elevation`.

## Use Cases
- Hiking trail elevation profile analysis
- Cycling route difficulty assessment
- Geographic surveying and flood risk mapping
- Real estate site elevation evaluation
- Mountain climbing route planning
- Paragliding launch site analysis
- Watershed and drainage studies
- Construction site planning
- Adventure sports terrain analysis
- Topographical data visualization

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `get_elevation` (action slug: `get-elevation`): Get elevation data for one or more discrete locations. Returns elevation in meters and feet, resolution, category, and aggregate statistics when multiple points are provided. Price: `10` credits. Parameters: `locations`.
- `get_elevation_profile` (action slug: `get-elevation-profile`): Same as get_path_elevation but always generates an elevation profile chart image. The chart shows elevation vs. distance with min/max markers and dual axes (meters and feet). A signed URL to the chart image is included in the response. Price: `10` credits. Parameters: `chart_height`, `chart_width`, `path`, `samples`.
- `get_path_elevation` (action slug: `get-path-elevation`): Sample elevation values at evenly-spaced points along a path defined by two or more waypoints. Returns elevation data for each sample point plus path statistics including total distance, ascent, and descent. Price: `10` credits. Parameters: `chart_height`, `chart_width`, `generate_chart`, `path`, `samples`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "elevation-data-point-path-charts-statistics"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "elevation-data-point-path-charts-statistics"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "elevation-data-point-path-charts-statistics"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "elevation-data-point-path-charts-statistics"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "elevation-data-point-path-charts-statistics"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "elevation-data-point-path-charts-statistics"
  }
}
```

## Call This Tool
Product slug: `elevation-data-point-path-charts-statistics`

Marketplace page: https://www.agentpmt.com/marketplace/elevation-data-point-path-charts-statistics

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
    "name": "Elevation-Data---Point-Path-Charts--Statistics",
    "arguments": {
      "action": "get_elevation",
      "locations": [
        {
          "latitude": 1,
          "longitude": 1
        }
      ]
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "elevation-data-point-path-charts-statistics",
  "parameters": {
    "action": "get_elevation",
    "locations": [
      {
        "latitude": 1,
        "longitude": 1
      }
    ]
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_elevation` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/elevation-data-point-path-charts-statistics
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
