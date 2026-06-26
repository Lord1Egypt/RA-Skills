---
name: ccdb
description: |
  CCDB Carbon Emission Factor Search Tool. Based on the Carbonstop CCDB database, it queries carbon emission factor data via the `carbonstop-ccdb` CLI.
  Supports keyword search for carbon emission factors, retrieving structured JSON data, and multi-keyword comparisons.

  **Use this Skill when**:
  (1) The user queries carbon emission factors (e.g., "electricity emission factor", "cement carbon emission", "natural gas emission coefficient", etc.)
  (2) The user needs to perform carbon emission calculations (needs to query the factor first, then multiply by activity data)
  (3) The user needs to compare the carbon emission factors of different energy sources/materials
  (4) The user mentions "CCDB", "carbon emission factor", "emission coefficient", "carbon footprint", "LCA", or "emission factor"
  (5) The user needs to query carbon emission factor data for a specific country/region or a specific year
---

# CCDB Carbon Emission Factor Search

Queries the Carbonstop CCDB emission factor database via directly calling the public HTTP API.

## Prerequisites

Requires Node.js ≥ 18 (for `npx`). No API Key is needed. The CLI uses built-in `crypto` and `fetch` with zero runtime dependencies.

## Security & Auditability

To ensure safe, deterministic execution and mitigate supply-chain risks, this skill pins the execution to `carbonstop-ccdb@1.0.1`.
- **Source Code**: [github.com/carbonstop/skills/tree/main/cli](https://github.com/carbonstop/skills/tree/main/cli)
- **NPM Package**: [npmjs.com/package/carbonstop-ccdb](https://www.npmjs.com/package/carbonstop-ccdb)
- **Engines**: Requires Node.js `>=18.0.0`
- **Dependencies**: 0 runtime dependencies.

Agents should run this CLI in a sandboxed environment if possible, or verify the exact version hash on the npm registry.

## Available Tools

This skill relies on the `carbonstop-ccdb` CLI. Because it is published to npm, you don't need to worry about absolute paths or local files.
You can execute it anywhere by running `npx carbonstop-ccdb@1.0.1 <command> [options]`.

### 1. Search Emission Factors (Formatted Output)

**Purpose**: Search for carbon emission factors by keyword and return human-readable formatted text.

```bash
npx carbonstop-ccdb@1.0.1 search "电力"
npx carbonstop-ccdb@1.0.1 search "electricity" --lang en
```

Parameters:
*   `keyword`: Search keyword, e.g., "electricity", "cement", "steel", "natural gas"
*   `--lang`: (Optional) Target language for the search. Defaults to `zh`. Pass `--lang en` for English.

Returns: Formatted text containing the factor value, unit, applicable region, year, publishing institution, etc.

### 2. Search Emission Factors (JSON Output)

**Purpose**: Operates the same as regular search, but returns structured JSON data. Highly recommended for programmatic handling and carbon emission calculations.

```bash
npx carbonstop-ccdb@1.0.1 search "electricity" --lang en --json
```

Parameters are identical to formatting search, just append the `--json` flag.

JSON Return Fields:
| Field | Description |
|-------|-------------|
| `name` | Factor Name |
| `factor` | Emission Factor Value |
| `unit` | Unit (e.g., kgCO₂e/kWh) |
| `countries` | Applicable Countries/Regions |
| `year` | Publication Year |
| `institution` | Publishing Institution |
| `specification` | Specification details |
| `description` | Additional description |
| `sourceLevel` | Factor source level |
| `business` | Industry sector |
| `documentType` | Document/Source type |

### 3. Compare Multiple Emission Factors

**Purpose**: Compare the carbon emission factors of up to 5 keywords simultaneously. Useful for horizontal comparison of different energy sources or materials.

```bash
npx carbonstop-ccdb@1.0.1 compare 电力 天然气 柴油
npx carbonstop-ccdb@1.0.1 compare electricity "natural gas" --lang en
npx carbonstop-ccdb@1.0.1 compare electricity "natural gas" --json
```

Parameters:
*   `compare`: Use the `compare` subcommand.
*   `keywords`: List of search keywords, 1-5 items maximum.


## Usage Scenarios & Examples

### Scenario 1: Query Emission Factor for a Specific Energy Source

> User: What is the carbon emission factor for the Chinese power grid?

→ Action: Execute `npx carbonstop-ccdb@1.0.1 search "electricity" --lang en` or `npx carbonstop-ccdb@1.0.1 search "中国电网"`. Find the one corresponding to China and the most recent year.

### Scenario 2: Carbon Emission Calculation

> User: My company used 500,000 kWh of electricity last year, what is the carbon footprint?

→ Workflow:
1. Search the `"electricity"` factor (preferably with `--json`), select China and the latest year.
2. Calculate Carbon Emissions = 500,000 kWh × Factor Value (in kgCO₂e/kWh).

### Scenario 3: Comparing Energy Alternatives

> User: Compare the carbon emission factors of electricity, natural gas, and diesel.

→ Action: Execute `npx carbonstop-ccdb@1.0.1 compare electricity "natural gas" diesel --lang en`

### Scenario 4: Querying Industry-Specific Data

> User: What is the emission factor for the cement industry?

→ Action: Search using `"cement"`.

## Important Notes

1. **Prioritize China Mainland and the Latest Year**: Unless the user specifies another region or year, implicitly prioritize data for China and the most recent year available.
2. **Pay Close Attention to Unit Conversion**: Different factors might have entirely different units (e.g., kgCO₂/kWh vs. tCO₂/TJ). Always double-check before doing mathematical calculations.
3. **Data Authority / Providers**: Take note of the publishing institutions (e.g., MEE, IPCC, IEA, EPA).
4. **No Results Found? Use Synonyms**: If the search yields empty results, attempt to use synonyms (e.g., translate your query, or map "power" → "electricity" → "grid").
5. **Always Use JSON for Calculations**: The `--json` format returns highly precise numerical figures that are ideal for programmatic multiplication.
