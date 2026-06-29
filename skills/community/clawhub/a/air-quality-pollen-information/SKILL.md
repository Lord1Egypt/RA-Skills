---
name: air-quality-pollen-information
description: "Air Quality & Pollen Information: Get air quality indices, pollutant levels, pollen forecasts, and historical data worldwide. Use when an agent needs air quality & pollen information, air quality pollen information, health and safety monitoring for outdoor activities, allergy management and pollen level tracking, travel planning and destination air quality assessment, environmental monitoring and pollution trend analysis, create map, locations through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/air-quality-pollen-information
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/air-quality-pollen-information"}}
---
# Air Quality & Pollen Information

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Comprehensive environmental data tool that provides real-time air quality indices, pollutant concentrations, pollen forecasts, and historical data for any location worldwide. The tool enables AI agents to retrieve current air quality conditions with AQI values and health recommendations, forecast data for both pollen types and pollutant levels, historical air quality trends up to 30 days, and generate visual maps with environmental overlays. Agents can flexibly select which data items to include by specifying any combination of pollutants including CO, NO2, O3, SO2, PM2.5, PM10 and pollen types including tree, grass, and weed allergens. The tool processes up to 10 locations simultaneously and provides additional computations such as health recommendations for different population groups, dominant pollutant concentrations, and detailed pollutant information. All responses are in English and include universal AQI scaling for consistent global comparisons. Map generation capabilities include satellite and road views with various environmental data overlays saved to cloud storage for 7 days.

## Product Instructions
### Air Quality & Pollen Information

Real-time air quality indices, pollutant concentrations, pollen forecasts, historical data, and map visualizations for any location worldwide. Supports up to 10 locations per request with both coordinate and address-based input.

---

#### Actions

##### get_current_conditions

Get current Air Quality Index (AQI), pollutant concentrations, and health recommendations.

**Required fields:**
- `action`: `"get_current_conditions"`
- `locations`: Array of 1-10 location objects (each with `latitude`/`longitude` OR `address`)

**Optional fields:**
- `include_items`: Filter specific pollutants — `"co"`, `"no2"`, `"o3"`, `"so2"`, `"pm25"`, `"pm10"`. Omit to receive all pollutants.
- `universal_aqi`: Use universal AQI scale (boolean, default `true`)
- `extra_computations`: Array of additional data to include — `"HEALTH_RECOMMENDATIONS"`, `"DOMINANT_POLLUTANT_CONCENTRATION"`, `"POLLUTANT_ADDITIONAL_INFO"`

**Example:**
```json
{
  "action": "get_current_conditions",
  "locations": [{"address": "San Francisco, CA"}],
  "universal_aqi": true,
  "extra_computations": ["HEALTH_RECOMMENDATIONS"]
}
```

**Example (multiple locations, mixed input):**
```json
{
  "action": "get_current_conditions",
  "locations": [
    {"latitude": 40.7128, "longitude": -74.0060, "name": "NYC"},
    {"address": "Los Angeles, CA"},
    {"address": "London, UK", "name": "London City Center"}
  ],
  "include_items": ["pm25", "no2", "o3"]
}
```

---

##### get_forecast

Get pollen forecast data for up to 5 days. Includes tree, grass, and weed pollen types with seasonal status and health recommendations.

**Required fields:**
- `action`: `"get_forecast"`
- `locations`: Array of 1-10 location objects

**Optional fields:**
- `include_items`: Filter specific pollen types — `"tree pollen"`, `"grass pollen"`, `"weed pollen"`. Omit to receive all three. Note: pollutant items (co, no2, etc.) are not available for forecasts.
- `forecast_days`: Number of days (1-5, default `5`)

**Example:**
```json
{
  "action": "get_forecast",
  "locations": [{"address": "Portland, OR"}],
  "include_items": ["tree pollen", "grass pollen"],
  "forecast_days": 3
}
```

---

##### get_history

Get historical air quality data with hourly AQI values and pollutant concentrations, up to 30 days back.

**Required fields:**
- `action`: `"get_history"`
- `locations`: Array of 1-10 location objects

**Optional fields:**
- `hours_history`: Number of hours to retrieve (1-720, default `24`)
- `include_items`: Filter specific pollutants — `"co"`, `"no2"`, `"o3"`, `"so2"`, `"pm25"`, `"pm10"`. Omit to receive all.
- `universal_aqi`: Use universal AQI scale (boolean, default `true`)

**Example:**
```json
{
  "action": "get_history",
  "locations": [{"latitude": 35.6762, "longitude": 139.6503, "name": "Tokyo"}],
  "hours_history": 48,
  "universal_aqi": true
}
```

---

##### create_map

Generate a map image with air quality or pollen data overlays. The map is stored in cloud storage for 7 days and a download URL is returned.

**Required fields:**
- `action`: `"create_map"`
- `locations`: Array of 1-10 location objects

**Optional fields:**
- `map_config`: Object with map settings:
  - `width`: Width in pixels (100-2048, default `640`)
  - `height`: Height in pixels (100-2048, default `640`)
  - `zoom`: Zoom level (1-20, default `10`)
  - `map_type`: Base map — `"roadmap"`, `"satellite"`, `"terrain"`, `"hybrid"` (default `"roadmap"`)
  - `overlay_type`: Data layer — `"aqi"`, `"aqi_red_green"`, `"pm25"`, `"pollen_tree"`, `"pollen_grass"`, `"pollen_weed"`
  - `include_legend`: Show color scale legend (boolean, default `true`)

**Example:**
```json
{
  "action": "create_map",
  "locations": [{"address": "Paris, France"}],
  "map_config": {
    "width": 800,
    "height": 600,
    "zoom": 12,
    "map_type": "roadmap",
    "overlay_type": "aqi",
    "include_legend": true
  }
}
```

---

#### Location Input

Each location in the `locations` array accepts one of two formats:

- **Coordinates:** `{"latitude": 40.7128, "longitude": -74.0060}`
- **Address:** `{"address": "San Francisco, CA"}` — accepts street addresses, city/state, or city/country

Add an optional `name` field to any location for a custom display label: `{"address": "Paris, France", "name": "Eiffel Tower Area"}`

You can mix coordinates and addresses in the same request.

---

#### Common Workflows

1. **Check if outdoor exercise is safe:** Use `get_current_conditions` with `extra_computations: ["HEALTH_RECOMMENDATIONS"]` to get AQI and health advice for sensitive groups.

2. **Plan for allergy season:** Use `get_forecast` with `include_items: ["tree pollen", "grass pollen", "weed pollen"]` to see pollen levels for the coming days.

3. **Compare air quality across cities:** Use `get_current_conditions` with multiple locations and `include_items: ["pm25", "o3"]` to compare key pollutants side by side.

4. **Visualize pollution patterns:** Use `create_map` with `overlay_type: "pm25"` or `"aqi"` to generate a heatmap of air quality for a region.

5. **Analyze trends over time:** Use `get_history` with `hours_history: 168` (7 days) to review hourly AQI changes and identify pollution patterns.

---

#### AQI Categories

| Range | Category | Meaning |
|-------|----------|---------|
| 0-50 | Good | Air quality is satisfactory |
| 51-100 | Moderate | Acceptable for most people |
| 101-150 | Unhealthy for Sensitive Groups | Sensitive individuals may experience effects |
| 151-200 | Unhealthy | Everyone may begin to experience effects |
| 201-300 | Very Unhealthy | Health warnings of emergency conditions |
| 301+ | Hazardous | Emergency conditions for entire population |

---

#### Important Notes

- Addresses are automatically geocoded. If geocoding fails for one location, other locations in the batch still process successfully.
- Pollutant forecasts are not available; the `get_forecast` action provides pollen forecasts only. Use `get_current_conditions` for current pollutant levels.
- Historical data (`get_history`) covers air quality pollutants only, not pollen.
- Generated maps are stored for 7 days before expiring.
- Some regions may have limited air quality or pollen data availability.
- Each location result includes its own error field — always check for partial failures in multi-location requests.

## When To Use
- Use this skill for `Air Quality & Pollen Information` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: air quality & pollen information, air quality pollen information, health and safety monitoring for outdoor activities, allergy management and pollen level tracking, travel planning and destination air quality assessment, environmental monitoring and pollution trend analysis, create map, locations.
- Supported action names: `create_map`, `get_current_conditions`, `get_forecast`, `get_history`.

## Use Cases
- Health and safety monitoring for outdoor activities
- Allergy management and pollen level tracking
- Travel planning and destination air quality assessment
- Environmental monitoring and pollution trend analysis
- Public health reporting with visual maps
- Outdoor event planning
- Fitness app integration for workout recommendations
- Smart home automation for air purifiers and HVAC systems
- Environmental research and data analysis
- Emergency response during wildfires or industrial incidents
- School and workplace air quality monitoring
- Real estate location assessment
- Agricultural planning based on air conditions
- Tourism industry environmental reporting
- Healthcare provider patient advisories

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `create_map` (action slug: `create-map`): Generate a map image with air quality or pollen data overlays. The map is stored in cloud storage for 7 days and a download URL is returned. Price: `5` credits. Parameters: `locations`, `map_config`.
- `get_current_conditions` (action slug: `get-current-conditions`): Get current Air Quality Index (AQI), pollutant concentrations, and health recommendations for one or more locations. Price: `5` credits. Parameters: `extra_computations`, `include_items`, `locations`, `universal_aqi`.
- `get_forecast` (action slug: `get-forecast`): Get pollen forecast data for up to 5 days including tree, grass, and weed pollen types with seasonal status and health recommendations. Price: `5` credits. Parameters: `forecast_days`, `include_items`, `locations`.
- `get_history` (action slug: `get-history`): Get historical air quality data with hourly AQI values and pollutant concentrations, up to 30 days (720 hours) back. Price: `5` credits. Parameters: `hours_history`, `include_items`, `locations`, `universal_aqi`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "air-quality-pollen-information"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "air-quality-pollen-information"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "air-quality-pollen-information"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "air-quality-pollen-information"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "air-quality-pollen-information"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "air-quality-pollen-information"
  }
}
```

## Call This Tool
Product slug: `air-quality-pollen-information`

Marketplace page: https://www.agentpmt.com/marketplace/air-quality-pollen-information

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
    "name": "Air-Quality--Pollen-Information",
    "arguments": {
      "action": "create_map",
      "locations": [
        {
          "address": "example address",
          "latitude": -90,
          "longitude": -180,
          "name": "example name"
        }
      ],
      "map_config": {
        "height": 640,
        "include_legend": true,
        "map_type": "roadmap",
        "overlay_type": "aqi",
        "width": 640,
        "zoom": 10
      }
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "air-quality-pollen-information",
  "parameters": {
    "action": "create_map",
    "locations": [
      {
        "address": "example address",
        "latitude": -90,
        "longitude": -180,
        "name": "example name"
      }
    ],
    "map_config": {
      "height": 640,
      "include_legend": true,
      "map_type": "roadmap",
      "overlay_type": "aqi",
      "width": 640,
      "zoom": 10
    }
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_map` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/air-quality-pollen-information
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
