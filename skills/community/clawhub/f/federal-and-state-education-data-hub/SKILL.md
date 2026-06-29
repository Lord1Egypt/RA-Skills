---
name: federal-and-state-education-data-hub
description: "Federal and State Education Data Hub: Natural language interface to World Bank education statistics. Query by country and education level, get enrollment rates, literacy, gender parity indices. Use when an agent needs federal and state education data hub, education statistics literacy, education policy analysis, school performance benchmarking, literacy and enrollment trends, regional equity reporting, query education data, country or region through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/education-statistics-literacy
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/education-statistics-literacy"}}
---
# Federal and State Education Data Hub

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Unified education analytics tool for public datasets covering literacy, enrollment, completion, equity, accountability, and school performance. Supports natural-language queries and routes requests across education-focused sources to return usable comparisons by country, state, and region.

## Product Instructions
### Federal and State Education Data Hub

Access education statistics for 200+ countries from the World Bank. Query enrollment rates, literacy rates, gender parity indices, pupil-teacher ratios, completion rates, and learning poverty data by country and education level.

#### Actions

##### query_education_data

Fetch education statistics for a country or region from the World Bank World Development Indicators database.

**Required fields:**
- `action` — `"query_education_data"`
- `country_or_region` (string) — Country or region name in plain English (e.g., `"Kenya"`, `"United States"`, `"India"`, `"South Africa"`, `"World"`). The tool first checks a built-in mapping of common country names, then falls back to fuzzy matching against the World Bank countries API for exact and partial matches.

**Optional fields:**
- `education_level` (string) — Education level to query. Default: `"all"`.
  - `"primary"` — Primary enrollment, completion, gender parity, pupil-teacher ratio, out-of-school rate, and learning poverty
  - `"secondary"` — Secondary enrollment, completion, gender parity, and pupil-teacher ratio
  - `"tertiary"` — Tertiary enrollment and gender parity
  - `"literacy"` — Adult literacy and youth literacy rates
  - `"all"` — All of the above combined
- `gender_disaggregation` (boolean) — Include male/female breakdowns for literacy, primary enrollment, and secondary enrollment. Default: `false`.
- `time_period` (string) — Time period for data. Default: `"latest"`.
  - `"latest"` — Most recent available data point
  - `"YYYY"` — Specific year (e.g., `"2020"`)
  - `"YYYY:YYYY"` — Year range (e.g., `"2015:2020"`)
- `include_gender_parity` (boolean) — Include gender parity indices (ratio of female to male enrollment/literacy) for each education level. Default: `true`.
- `include_teacher_ratios` (boolean) — Include pupil-teacher ratios for primary and secondary levels. Default: `false`.
- `include_completion_rates` (boolean) — Include primary and secondary completion rates where available. Default: `true`.
- `compare_to_region` (boolean) — Include regional averages for key indicators (primary enrollment, secondary enrollment, adult literacy) based on the country's World Bank region. Skipped when querying `"World"`. Default: `true`.

**Example — Primary education data for a country:**
```json
{
  "action": "query_education_data",
  "country_or_region": "Kenya",
  "education_level": "primary",
  "time_period": "latest"
}
```

**Example — All education data with gender breakdown:**
```json
{
  "action": "query_education_data",
  "country_or_region": "India",
  "education_level": "all",
  "gender_disaggregation": true,
  "include_gender_parity": true,
  "include_teacher_ratios": true
}
```

**Example — Literacy rates over a time range:**
```json
{
  "action": "query_education_data",
  "country_or_region": "Nigeria",
  "education_level": "literacy",
  "time_period": "2015:2020"
}
```

**Example — Tertiary enrollment without regional comparison:**
```json
{
  "action": "query_education_data",
  "country_or_region": "Brazil",
  "education_level": "tertiary",
  "compare_to_region": false
}
```

**Example — Secondary education with teacher ratios:**
```json
{
  "action": "query_education_data",
  "country_or_region": "South Africa",
  "education_level": "secondary",
  "include_teacher_ratios": true,
  "include_completion_rates": true
}
```

#### Response Format

Responses include:

- **data** — Per-indicator results. Each indicator contains:
  - `indicator` — World Bank indicator code
  - `values` — Array of data points with year, value, and country name
  - `available` — Whether data was found
- **metadata** — Query context: country code, country name, education level, time period, and query timestamp.
- **regional_comparison** — When enabled, regional average data for key indicators from the country's World Bank region.
- **gender_parity_analysis** — When enabled, parity indices per education level with interpretation:
  - Index < 0.97 = female disadvantage
  - Index 0.97-1.03 = gender parity achieved
  - Index > 1.03 = female advantage
- **sdg_alignment** — SDG 4 (Quality Education) target analysis:
  - Target 4.1: Primary completion (on track if >= 90%)
  - Target 4.3: Tertiary access (expanding if > 30%)
  - Target 4.5: Gender equality in education
  - Target 4.6: Adult literacy progress (high >= 95%, moderate >= 80%, low < 80%)

If a country name cannot be resolved, the tool returns an error.

#### Education Indicators by Level

| Level | Indicators |
|---|---|
| literacy | Adult literacy rate, Youth literacy rate, Female literacy*, Male literacy* |
| primary | Primary enrollment, Primary completion, Gender parity (primary), Pupil-teacher ratio*, Out-of-school rate, Learning poverty, Female enrollment*, Male enrollment* |
| secondary | Secondary enrollment, Secondary completion, Gender parity (secondary), Pupil-teacher ratio*, Female enrollment*, Male enrollment* |
| tertiary | Tertiary enrollment, Gender parity (tertiary) |

*Included only when the corresponding optional flag is enabled.

#### Common Workflows

1. **Country education profile** — Call with `education_level: "all"` to get a comprehensive snapshot of a country's education system.
2. **Gender equity analysis** — Enable `gender_disaggregation: true` and `include_gender_parity: true` to get male/female breakdowns and parity indices.
3. **SDG 4 progress check** — Query with `education_level: "all"` and review the `sdg_alignment` section for target progress.
4. **Cross-country comparison** — Make separate calls for different countries with the same parameters, then compare results.
5. **Resource allocation review** — Enable `include_teacher_ratios: true` and `include_completion_rates: true` to assess education system capacity.

#### Important Notes

- Data is sourced from the World Bank World Development Indicators database.
- Boolean fields must be actual booleans (`true`/`false`), not strings like `"yes"` or `"no"`.
- Data availability varies by country and indicator; some countries may have gaps.
- Most recent data may be 1-3 years behind the current year.
- The `education_level` value is validated and must be one of: primary, secondary, tertiary, literacy, all.
- Regional comparison is automatically skipped when querying "World" data.

## When To Use
- Use this skill for `Federal and State Education Data Hub` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: federal and state education data hub, education statistics literacy, education policy analysis, school performance benchmarking, literacy and enrollment trends, regional equity reporting, query education data, country or region.
- Supported action names: `query_education_data`.

## Use Cases
- Education policy analysis
- School performance benchmarking
- Literacy and enrollment trends
- Regional equity reporting
- Program impact evaluation

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_education_data` (action slug: `query-education-data`): Fetch education statistics for a country or region from the World Bank World Development Indicators database. Price: `20` credits. Parameters: `compare_to_region`, `country_or_region`, `education_level`, `gender_disaggregation`, `include_completion_rates`, `include_gender_parity`, `include_teacher_ratios`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "education-statistics-literacy"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "education-statistics-literacy"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "education-statistics-literacy"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "education-statistics-literacy"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "education-statistics-literacy"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "education-statistics-literacy"
  }
}
```

## Call This Tool
Product slug: `education-statistics-literacy`

Marketplace page: https://www.agentpmt.com/marketplace/education-statistics-literacy

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
    "name": "Federal-and-State-Education-Data-Hub",
    "arguments": {
      "action": "query_education_data",
      "compare_to_region": true,
      "country_or_region": "example country or region",
      "education_level": "all",
      "gender_disaggregation": false,
      "include_completion_rates": true,
      "include_gender_parity": true,
      "include_teacher_ratios": false,
      "time_period": "latest"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "education-statistics-literacy",
  "parameters": {
    "action": "query_education_data",
    "compare_to_region": true,
    "country_or_region": "example country or region",
    "education_level": "all",
    "gender_disaggregation": false,
    "include_completion_rates": true,
    "include_gender_parity": true,
    "include_teacher_ratios": false,
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
- If `query_education_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/education-statistics-literacy
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
