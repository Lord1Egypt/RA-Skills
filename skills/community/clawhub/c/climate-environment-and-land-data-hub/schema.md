# Climate, Environment, and Land Data Hub Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `climate-environmental-data`

x402 availability: not enabled for this product.

## `query_climate_data`

Action slug: `query-climate-data`

Price: `10` credits

Fetch climate and environmental data for a country or region from the World Bank. Returns CO2 emissions, greenhouse gas data, forest coverage, renewable energy percentages, air quality (PM2.5), water withdrawals, and electricity access. Includes trend analysis, global comparisons, and Paris Agreement/SDG progress tracking.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `country_or_region` | `string` | no | Country name in English (e.g., 'Kenya', 'United States', 'China') or 3-letter ISO code (e.g., 'KEN', 'USA'). Defaults to 'World' if omitted. |
| `environmental_topic` | `string` | no | Environmental topic to query. Options: emissions, forests, water, energy, air_quality, or all. |
| `include_paris_targets` | `boolean` | no | Include Paris Agreement targets and SDG alignment (SDG 7, 13, 15) in the response. |
| `include_per_capita` | `boolean` | no | Include per capita calculations where applicable. Set to false to exclude per-capita indicators (e.g., CO2 per capita). |
| `time_period` | `string` | no | Time period: 'latest' for most recent data, or year range like '2015:2020'. |

Sample parameters:

```json
{
  "country_or_region": "example country or region",
  "environmental_topic": "all",
  "include_paris_targets": true,
  "include_per_capita": true,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "country_or_region": {
    "description": "Country name in English (e.g., 'Kenya', 'United States', 'China') or 3-letter ISO code (e.g., 'KEN', 'USA'). Defaults to 'World' if omitted.",
    "required": false,
    "type": "string"
  },
  "environmental_topic": {
    "default": "all",
    "description": "Environmental topic to query. Options: emissions, forests, water, energy, air_quality, or all.",
    "enum": [
      "emissions",
      "forests",
      "water",
      "energy",
      "air_quality",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "include_paris_targets": {
    "default": true,
    "description": "Include Paris Agreement targets and SDG alignment (SDG 7, 13, 15) in the response.",
    "required": false,
    "type": "boolean"
  },
  "include_per_capita": {
    "default": true,
    "description": "Include per capita calculations where applicable. Set to false to exclude per-capita indicators (e.g., CO2 per capita).",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' for most recent data, or year range like '2015:2020'.",
    "required": false,
    "type": "string"
  }
}
```
