---
name: commerce-and-trade-competitiveness-data-hub
description: "Commerce and Trade Competitiveness Data Hub: Query World Bank TCdata360 trade and competitiveness data by country or region name. Use when an agent needs commerce and trade competitiveness data hub, trade competitiveness data, export market analysis, trade competitiveness benchmarking, tariff and logistics monitoring, cross border policy research, query trade data, country or region through AgentPMT-hosted remote tool calls. Discovery terms: commerce and trade competitiveness data hub."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/trade-competitiveness-data
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/trade-competitiveness-data"}}
---
# Commerce and Trade Competitiveness Data Hub

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Access World Bank trade and competitiveness data from TCdata360 (2,400+ indicators, 46 sources) for 200+ countries. Get merchandise exports/imports, trade balances, tariff rates, high-tech and ICT export shares, Logistics Performance Index rankings, Ease of Doing Business scores, and trade-to-GDP ratios. Includes CAGR trend analysis, regional comparisons, and SDG 17 alignment tracking.

## Product Instructions
### Commerce and Trade Competitiveness Data Hub

#### Overview
Natural language interface to World Bank trade and competitiveness data. Query exports, imports, trade balance, logistics performance, tariffs, and trade costs by country or region. Uses English country names only -- no indicator codes needed.

Data sourced from World Bank World Development Indicators (WDI) and TCdata360 (2,400+ indicators from 46 sources). Covers merchandise and service trade volumes, exports/imports as % of GDP, trade openness, Ease of Doing Business rankings, Logistics Performance Index (LPI), tariff rates, time and cost to trade, high-tech and ICT exports, and CAGR trend analysis. Includes regional/global comparisons, trade balance calculations, human-readable insights, and SDG 17 (Partnerships through Trade) alignment.

#### Actions

##### query_trade_data
Fetches trade and competitiveness data for a country or region from the World Bank.

**Required parameters:**
- `country_or_region` (string): Country or region name in English (e.g., "China", "Japan", "Vietnam", "Sub-Saharan Africa"). Also accepts partial matches and income groups ("High Income", "OECD"). Unicode names are not supported. Unrecognized names return an error with a suggestion.

**Optional parameters:**
- `trade_topic` (string): One of "exports", "imports", "competitiveness", "logistics", "tariffs", "trade_costs", or "all". Defaults to "all".
- `calculate_trade_balance` (boolean): Calculate trade balance (exports minus imports) if both merchandise export and import data are available. Defaults to true.
- `include_doing_business` (boolean): Include Doing Business rankings and ease of doing business scores. Defaults to true. Setting to false also filters out time-to-export/import and cost-to-export/import indicators.
- `include_lpi` (boolean): Include Logistics Performance Index scores. Defaults to true. Setting to false filters out the logistics_performance indicator.
- `time_period` (string): "latest" (most recent available), "last_5_years", "last_10_years", or a specific range "YYYY:YYYY" (e.g., "2015:2020"). Also accepts "YYYY-YYYY" format (converted to "YYYY:YYYY"). Defaults to "latest".
- `include_regional_comparison` (boolean): Include regional and global comparison data (World, High Income, Upper Middle Income, Lower Middle Income) for key indicators. Defaults to true.
- `include_trends` (boolean): Include trend analysis with absolute change, percent change, direction, and CAGR for indicators with multiple data points. Defaults to true.

**Example -- All trade data for Vietnam:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "Vietnam",
  "trade_topic": "all",
  "time_period": "latest"
}
```

**Example -- Export trends for China over the last 10 years:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "China",
  "trade_topic": "exports",
  "time_period": "last_10_years",
  "include_trends": true
}
```

**Example -- Competitiveness metrics for Singapore:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "Singapore",
  "trade_topic": "competitiveness",
  "include_doing_business": true,
  "include_lpi": true
}
```

**Example -- Tariff analysis for India:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "India",
  "trade_topic": "tariffs",
  "time_period": "latest"
}
```

**Example -- Trade costs with regional comparison:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "Rwanda",
  "trade_topic": "trade_costs",
  "include_regional_comparison": true
}
```

**Example -- Logistics performance for Netherlands:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "Netherlands",
  "trade_topic": "logistics"
}
```

**Example -- Imports data without Doing Business indicators:**
```json
{
  "action": "query_trade_data",
  "country_or_region": "Brazil",
  "trade_topic": "imports",
  "include_doing_business": false
}
```

#### Workflows

##### Country Trade Profile
1. Call `query_trade_data` with a country and `trade_topic: "all"` for a comprehensive trade overview.
2. Review the `insights` array for human-readable analysis of trade patterns.
3. Check `trade_balance` for surplus/deficit status.
4. Review `regional_comparison` to see how the country compares to World, High Income, Upper Middle Income, and Lower Middle Income averages.

##### Trade Balance Analysis
1. Call `query_trade_data` with `calculate_trade_balance: true` (default).
2. The response includes a `trade_balance` section with exports, imports, balance amount, and surplus/deficit classification for each year.
3. Currency values are formatted in human-readable units (millions, billions, trillions).

##### Competitiveness Benchmarking
1. Call `query_trade_data` with `trade_topic: "competitiveness"`.
2. Review Ease of Doing Business rank (1 = best, lower is better) and LPI score (1-5 scale, higher is better).
3. Trade openness (trade as % of GDP) indicates how integrated the economy is with global trade.

##### Historical Trend Analysis
1. Call `query_trade_data` with `time_period: "last_10_years"` and `include_trends: true`.
2. Review the `trends` section for each indicator showing oldest/newest values, absolute and percent change, direction (improving/declining/stable), and CAGR.
3. For exports and competitiveness indicators, positive change means "improving". For tariffs, time, and cost indicators, negative change means "improving" (lower is better).

#### Notes
- **Supported countries:** 100+ countries by full English name (e.g., "Vietnam", "Japan", "Germany"), plus partial name matching. Also supports 2-3 letter ISO codes if they match known World Bank codes.
- **Regions:** "Sub-Saharan Africa", "Latin America", "Middle East", "South Asia", "East Asia", "Europe", "North America", "Arab World".
- **Income groups:** "Low Income", "Lower Middle Income", "Upper Middle Income", "High Income", "OECD".
- **Special values:** "World" or "Global" for worldwide data.
- Country name input longer than 100 characters is rejected.
- If country_or_region is empty, defaults to "World" (WLD).
- **Trade topics and their indicators:**
  - `exports`: merchandise exports, exports % of GDP, high-tech exports, ICT exports, service exports, time to export, cost to export
  - `imports`: merchandise imports, imports % of GDP, service imports, time to import, cost to import
  - `competitiveness`: Ease of Doing Business rank, LPI, trade % of GDP, exports/imports % of GDP
  - `logistics`: LPI score, time to export/import
  - `tariffs`: simple mean tariff rate, weighted mean tariff rate
  - `trade_costs`: time to export/import, cost to export/import, simple and weighted mean tariff rates
  - `all`: all available trade indicators
- **Trade balance calculation:** Exports minus imports. Positive = surplus, negative = deficit, zero = balanced. Calculated by matching merchandise export and import data by year.
- **Currency formatting:** Large values displayed in millions, billions, or trillions (e.g., "$1.23 trillion").
- **CAGR (Compound Annual Growth Rate):** Calculated when multi-year data is available and both start and end values are positive.
- **Trend direction interpretation:** For exports/competitiveness/logistics, positive change = "improving". For tariffs/time/cost/ease of doing business, negative change = "improving" (lower is better).
- **Insights generated automatically:** Trade surplus/deficit, export orientation (% of GDP), trade openness, LPI interpretation (world-class/strong/moderate/developing/challenges), Doing Business rank tier, tariff level, export process efficiency, ICT export strength, export growth trends, and comparison to global averages.
- **LPI score interpretation:** 4.0+ = world-class, 3.5-4.0 = strong, 3.0-3.5 = moderate, 2.5-3.0 = developing, below 2.5 = significant challenges.
- **Ease of Doing Business interpretation:** Rank 1-30 = top-tier, 31-100 = competitive, 100+ = challenges present. Note: Doing Business project was discontinued in 2021; latest data from 2020.
- **Regional comparison:** Compares key indicators (exports % of GDP, imports % of GDP, trade % of GDP, LPI, Ease of Doing Business) against World, High Income, Upper Middle Income, and Lower Middle Income averages.
- Data availability varies by country and indicator. Most recent data is typically 1-2 years behind the current year.
- SDG alignment: SDG 17 (Partnerships for the Goals), SDG 17.10 (universal trading system), SDG 17.11 (increase developing country exports).

## When To Use
- Use this skill for `Commerce and Trade Competitiveness Data Hub` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: commerce and trade competitiveness data hub, trade competitiveness data, export market analysis, trade competitiveness benchmarking, tariff and logistics monitoring, cross border policy research, query trade data, country or region.
- Supported action names: `query_trade_data`.

## Use Cases
- Export market analysis
- Trade competitiveness benchmarking
- Tariff and logistics monitoring
- Cross-border policy research
- Country trade profile comparisons

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_trade_data` (action slug: `query-trade-data`): Fetch trade and competitiveness data for a country or region from the World Bank. Returns merchandise exports/imports, trade balance, tariff rates, high-tech/ICT export shares, Logistics Performance Index, Ease of Doing Business scores, trade openness ratios, CAGR trend analysis, and regional comparisons. Price: `5` credits. Parameters: `calculate_trade_balance`, `country_or_region`, `include_doing_business`, `include_lpi`, `include_regional_comparison`, `include_trends`, `time_period`, `trade_topic`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "trade-competitiveness-data"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "trade-competitiveness-data"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "trade-competitiveness-data"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "trade-competitiveness-data"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "trade-competitiveness-data"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "trade-competitiveness-data"
  }
}
```

## Call This Tool
Product slug: `trade-competitiveness-data`

Marketplace page: https://www.agentpmt.com/marketplace/trade-competitiveness-data

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
    "name": "Commerce-and-Trade-Competitiveness-Data-Hub",
    "arguments": {
      "action": "query_trade_data",
      "calculate_trade_balance": true,
      "country_or_region": "example country or region",
      "include_doing_business": true,
      "include_lpi": true,
      "include_regional_comparison": true,
      "include_trends": true,
      "time_period": "latest",
      "trade_topic": "all"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "trade-competitiveness-data",
  "parameters": {
    "action": "query_trade_data",
    "calculate_trade_balance": true,
    "country_or_region": "example country or region",
    "include_doing_business": true,
    "include_lpi": true,
    "include_regional_comparison": true,
    "include_trends": true,
    "time_period": "latest",
    "trade_topic": "all"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `query_trade_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/trade-competitiveness-data
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
