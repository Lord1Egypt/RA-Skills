---
name: climate-environment-and-land-data-hub
description: "Climate, Environment, and Land Data Hub: Query World Bank climate and environmental data by country name or ISO code. Use when an agent needs climate, environment, and land data hub, climate environmental data, climate risk analysis, environmental compliance insights, pollution trend tracking, resource and land assessment, query climate data, country or region through AgentPMT-hosted remote tool calls. Discovery terms: climate, environment, and land data hub, climate environmental data."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/climate-environmental-data
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/climate-environmental-data"}}
---
# Climate, Environment, and Land Data Hub

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
See how any country's environmental footprint stacks up against the rest of the world. Look up CO2 and greenhouse gas emissions, track how forests and agricultural land are changing, check renewable energy adoption and fossil fuel dependence, and monitor air quality and freshwater use across 100+ countries. Every result includes trend analysis showing whether things are getting better or worse, side-by-side comparisons with global averages, and progress toward Paris Agreement and UN Sustainable Development Goals.

## Product Instructions
### Climate, Environment, and Land Data Hub

#### Overview
Natural language interface to World Bank climate and environmental data. Query CO2 emissions, forest coverage, water resources, energy consumption, and air quality by country or region. Supports 100+ countries by English name. No indicator codes needed -- just provide a country name and topic.

Data sourced from the World Bank API. Covers emissions (CO2, GHG, methane, nitrous oxide), forests and land use, energy access and renewables, water resources, and air quality (PM2.5 exposure). Includes Paris Agreement targets, SDG alignment (SDG 7, 13, 15), trend analysis, and global comparisons.

#### Actions

##### query_climate_data
Fetches climate and environmental data for a country or region from the World Bank.

**Required parameters:** None (all optional; defaults to World/all topics/latest).

**Optional parameters:**
- `country_or_region` (string): Country name in English (e.g., "Kenya", "United States", "China") or 3-letter ISO code (e.g., "KEN", "USA"). Defaults to "World" if omitted. Unrecognized names return an error with a suggestion.
- `environmental_topic` (string): One of "emissions", "forests", "water", "energy", "air_quality", or "all". Defaults to "all".
- `time_period` (string): "latest" for most recent data, or a year range like "2015:2020". Defaults to "latest".
- `include_paris_targets` (boolean): Include Paris Agreement targets and SDG alignment in the response. Defaults to true.
- `include_per_capita` (boolean): Include per capita calculations where applicable. Defaults to true. Set to false to exclude per-capita indicators (e.g., CO2 per capita).

**Example -- Get emissions data for Kenya:**
```json
{
  "action": "query_climate_data",
  "country_or_region": "Kenya",
  "environmental_topic": "emissions"
}
```

**Example -- Get all climate data for Brazil with a time range:**
```json
{
  "action": "query_climate_data",
  "country_or_region": "Brazil",
  "time_period": "2015:2020"
}
```

**Example -- Forest data for the world, no per-capita:**
```json
{
  "action": "query_climate_data",
  "environmental_topic": "forests",
  "include_per_capita": false
}
```

**Example -- Energy data for Sub-Saharan Africa without Paris targets:**
```json
{
  "action": "query_climate_data",
  "country_or_region": "Sub-Saharan Africa",
  "environmental_topic": "energy",
  "include_paris_targets": false
}
```

**Example -- Air quality for India:**
```json
{
  "action": "query_climate_data",
  "country_or_region": "India",
  "environmental_topic": "air_quality"
}
```

#### Workflows

##### Country Climate Profile
1. Call `query_climate_data` with a country and `environmental_topic: "all"` to get a full climate profile.
2. Review the `paris_agreement_targets` and `sdg_alignment` sections for policy context.
3. Check the `global_comparison` on each indicator to see how the country compares to the world average.

##### Emissions Tracking Over Time
1. Call `query_climate_data` with `environmental_topic: "emissions"` and a `time_period` range (e.g., "2010:2022").
2. Review the `trend` field on each indicator to see if emissions are increasing, decreasing, or stable.

##### Regional Comparison
1. Call `query_climate_data` for a region (e.g., "Sub-Saharan Africa", "Latin America", "South Asia").
2. Compare with a specific country by calling again with that country name.
3. Use the `global_comparison` data to contextualize results.

#### Notes
- **Supported countries:** 100+ countries by full English name (e.g., "Kenya", "Germany", "Brazil"), plus World Bank regions ("Sub-Saharan Africa", "Latin America", "East Asia and Pacific", "Europe and Central Asia", "Middle East and North Africa", "North America", "South Asia") and income groups ("Low Income", "Lower Middle Income", "Upper Middle Income", "High Income").
- **3-letter ISO codes** are also accepted (e.g., "KEN", "USA", "CHN"). 2-letter codes are accepted if uppercase.
- Country names must be in English. Native-language or Unicode names are not supported.
- Country name input longer than 100 characters is rejected.
- If `country_or_region` is omitted or empty, it defaults to "World" (WLD).
- If `environmental_topic` is omitted or not recognized, it defaults to "all" (returns all indicators).
- **Environmental topics and their indicators:**
  - `emissions`: CO2 total, CO2 per capita, total GHG, methane
  - `forests`: forest area %, forest area sq km, agricultural land %
  - `water`: freshwater withdrawal, clean fuel access
  - `energy`: renewable energy %, fossil fuel %, renewable electricity %, access to electricity %
  - `air_quality`: PM2.5 exposure, clean fuel access
- Setting `include_per_capita` to false filters out any indicator key containing "per_capita".
- **Response includes:** data values with year, trend analysis (increasing/decreasing/stable over ~10 years), global comparison (percentage above/below world average), Paris Agreement targets, SDG alignment, and a summary with data availability percentage.
- When no data is found for any indicator, success is false and a message is included.
- Data availability varies by country and indicator. Some indicators may return null values.

## When To Use
- Use this skill for `Climate, Environment, and Land Data Hub` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: climate, environment, and land data hub, climate environmental data, climate risk analysis, environmental compliance insights, pollution trend tracking, resource and land assessment, query climate data, country or region.
- Supported action names: `query_climate_data`.

## Use Cases
- Climate risk analysis
- Environmental compliance insights
- Pollution trend tracking
- Resource and land assessment
- Resilience planning

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_climate_data` (action slug: `query-climate-data`): Fetch climate and environmental data for a country or region from the World Bank. Returns CO2 emissions, greenhouse gas data, forest coverage, renewable energy percentages, air quality (PM2.5), water withdrawals, and electricity access. Includes trend analysis, global comparisons, and Paris Agreement/SDG progress tracking. Price: `10` credits. Parameters: `country_or_region`, `environmental_topic`, `include_paris_targets`, `include_per_capita`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "climate-environmental-data"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "climate-environmental-data"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "climate-environmental-data"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "climate-environmental-data"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "climate-environmental-data"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "climate-environmental-data"
  }
}
```

## Call This Tool
Product slug: `climate-environmental-data`

Marketplace page: https://www.agentpmt.com/marketplace/climate-environmental-data

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
    "name": "Climate-Environment-and-Land-Data-Hub",
    "arguments": {
      "action": "query_climate_data",
      "country_or_region": "example country or region",
      "environmental_topic": "all",
      "include_paris_targets": true,
      "include_per_capita": true,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "climate-environmental-data",
  "parameters": {
    "action": "query_climate_data",
    "country_or_region": "example country or region",
    "environmental_topic": "all",
    "include_paris_targets": true,
    "include_per_capita": true,
    "time_period": "latest"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `query_climate_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/climate-environmental-data
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
