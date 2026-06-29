# Federal and State Education Data Hub Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `education-statistics-literacy`

x402 availability: not enabled for this product.

## `query_education_data`

Action slug: `query-education-data`

Price: `20` credits

Fetch education statistics for a country or region from the World Bank World Development Indicators database.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `compare_to_region` | `boolean` | no | Include regional averages for comparison. |
| `country_or_region` | `string` | yes | Country or region name in plain language (e.g., 'Kenya', 'South Africa', 'World', 'Sub-Saharan Africa'). |
| `education_level` | `string` | no | Education level to query: 'primary', 'secondary', 'tertiary', 'literacy', or 'all'. |
| `gender_disaggregation` | `boolean` | no | Include gender-disaggregated data (male/female breakdowns). |
| `include_completion_rates` | `boolean` | no | Include completion rates where available. |
| `include_gender_parity` | `boolean` | no | Include gender parity indices (ratio of female to male enrollment/literacy). |
| `include_teacher_ratios` | `boolean` | no | Include pupil-teacher ratios. |
| `time_period` | `string` | no | Time period: 'latest' for most recent, specific year like '2020', or range like '2015:2020'. |

Sample parameters:

```json
{
  "compare_to_region": true,
  "country_or_region": "example country or region",
  "education_level": "all",
  "gender_disaggregation": false,
  "include_completion_rates": true,
  "include_gender_parity": true,
  "include_teacher_ratios": false,
  "time_period": "latest"
}
```

Generated JSON parameter schema:

```json
{
  "compare_to_region": {
    "default": true,
    "description": "Include regional averages for comparison.",
    "required": false,
    "type": "boolean"
  },
  "country_or_region": {
    "description": "Country or region name in plain language (e.g., 'Kenya', 'South Africa', 'World', 'Sub-Saharan Africa').",
    "required": true,
    "type": "string"
  },
  "education_level": {
    "default": "all",
    "description": "Education level to query: 'primary', 'secondary', 'tertiary', 'literacy', or 'all'.",
    "enum": [
      "primary",
      "secondary",
      "tertiary",
      "literacy",
      "all"
    ],
    "required": false,
    "type": "string"
  },
  "gender_disaggregation": {
    "default": false,
    "description": "Include gender-disaggregated data (male/female breakdowns).",
    "required": false,
    "type": "boolean"
  },
  "include_completion_rates": {
    "default": true,
    "description": "Include completion rates where available.",
    "required": false,
    "type": "boolean"
  },
  "include_gender_parity": {
    "default": true,
    "description": "Include gender parity indices (ratio of female to male enrollment/literacy).",
    "required": false,
    "type": "boolean"
  },
  "include_teacher_ratios": {
    "default": false,
    "description": "Include pupil-teacher ratios.",
    "required": false,
    "type": "boolean"
  },
  "time_period": {
    "default": "latest",
    "description": "Time period: 'latest' for most recent, specific year like '2020', or range like '2015:2020'.",
    "required": false,
    "type": "string"
  }
}
```
