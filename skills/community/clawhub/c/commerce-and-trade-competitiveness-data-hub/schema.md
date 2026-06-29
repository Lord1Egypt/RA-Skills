# Commerce and Trade Competitiveness Data Hub Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `trade-competitiveness-data`

x402 availability: not enabled for this product.

## `query_trade_data`

Action slug: `query-trade-data`

Price: `5` credits

Fetch trade and competitiveness data for a country or region from the World Bank. Returns merchandise exports/imports, trade balance, tariff rates, high-tech/ICT export shares, Logistics Performance Index, Ease of Doing Business scores, trade openness ratios, CAGR trend analysis, and regional comparisons.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `calculate_trade_balance` | `boolean` | no | Calculate trade balance (exports minus imports) if both merchandise export and import data are available. |
| `country_or_region` | `string` | yes | Country or region name in English (e.g., 'China', 'Japan', 'Vietnam', 'Sub-Saharan Africa'). Also accepts partial matches and income groups ('High Income', 'OECD'). Unicode names are not supported. |
| `include_doing_business` | `boolean` | no | Include Doing Business rankings and ease of doing business scores. Setting to false also filters out time-to-export/import and cost-to-export/import indicators. |
| `include_lpi` | `boolean` | no | Include Logistics Performance Index (LPI) scores and rankings. |
| `include_regional_comparison` | `boolean` | no | Include regional and global comparison data (World, High Income, Upper Middle Income, Lower Middle Income) for key indicators. |
| `include_trends` | `boolean` | no | Include trend analysis with absolute change, percent change, direction, and CAGR for indicators with multiple data points. |
| `time_period` | `string` | no | Time period: 'latest' (most recent), 'last_5_years', 'last_10_years', or specific range 'YYYY:YYYY' (e.g., '2015:2020'). |
| `trade_topic` | `string` | no | Trade topic to query. Options: exports, imports, competitiveness, logistics, tariffs, trade_costs, or all. |

Sample parameters:

```json
{
  "calculate_trade_balance": true,
  "country_or_region": "example country or region",
  "include_doing_business": true,
  "include_lpi": true,
  "include_regional_comparison": true,
  "include_trends": true,
  "time_period": "latest",
  "trade_topic": "all"
}
```

Generated JSON parameter schema:

```json
{
  "calculate_trade_balance": {
    "default": true,
    "description": "Calculate trade balance (exports minus imports) if both merchandise export and import data are available.",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country or region name in English (e.g., 'China', 'Japan', 'Vietnam', 'Sub-Saharan Africa'). Also accepts partial matches and income groups ('High Income', 'OECD'). Unicode names are not supported.",
    "required": true,
    "type": "string"
  },
  "include_doing_business": {
    "default": true,
    "description": "Include Doing Business rankings and ease of doing business scores. Setting to false also filters out time-to-export/import and cost-to-export/import indicators.",
    "required": false,
    "type": "boolean"
  },
  "include_lpi": {
    "default": true,
    "description": "Include Logistics Performance Index (LPI) scores and rankings.",
    "required": false,
    "type": "boolean"
  },
  "include_regional_comparison": {
    "default": true,
    "description": "Include regional and global comparison data (World, High Income, Upper Middle Income, Lower Middle Income) for key indicators.",
    "required": false,
    "type": "boolean"
  },
  "include_trends": {
    "default": true,
    "description": "Include trend analysis with absolute change, percent change, direction, and CAGR for indicators with multiple data points.",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' (most recent), 'last_5_years', 'last_10_years', or specific range 'YYYY:YYYY' (e.g., '2015:2020').",
    "required": false,
    "type": "string"
  },
  "trade_topic": {
    "default": "all",
    "description": "Trade topic to query. Options: exports, imports, competitiveness, logistics, tariffs, trade_costs, or all.",
    "enum": [
      "exports",
      "imports",
      "competitiveness",
      "logistics",
      "tariffs",
      "trade_costs",
      "all"
    ],
    "required": false,
    "type": "string"
  }
}
```
