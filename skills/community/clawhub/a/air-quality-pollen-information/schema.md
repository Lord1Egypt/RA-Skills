# Air Quality & Pollen Information Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `air-quality-pollen-information`

x402 availability: not enabled for this product.

## `create_map`

Action slug: `create-map`

Price: `5` credits

Generate a map image with air quality or pollen data overlays. The map is stored in cloud storage for 7 days and a download URL is returned.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `locations` | `array` | yes | List of 1-10 locations to center the map on. Each location needs either latitude/longitude coordinates or an address string. |
| `map_config` | `object` | no | Configuration settings for the generated map. |

Sample parameters:

```json
{
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
```

Generated JSON parameter schema:

```json
{
  "locations": {
    "description": "List of 1-10 locations to center the map on. Each location needs either latitude/longitude coordinates or an address string.",
    "items": {
      "properties": {
        "address": {
          "description": "Address, city/state, or city/country to geocode. Required if latitude/longitude are not provided.",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90). Required if address is not provided.",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180). Required if address is not provided.",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional display name for this location.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "map_config": {
    "description": "Configuration settings for the generated map.",
    "properties": {
      "height": {
        "default": 640,
        "description": "Map height in pixels.",
        "maximum": 2048,
        "minimum": 100,
        "required": false,
        "type": "integer"
      },
      "include_legend": {
        "default": true,
        "description": "Include a legend explaining the color scale on the map.",
        "required": false,
        "type": "boolean"
      },
      "map_type": {
        "default": "roadmap",
        "description": "Base map type.",
        "enum": [
          "roadmap",
          "satellite",
          "terrain",
          "hybrid"
        ],
        "required": false,
        "type": "string"
      },
      "overlay_type": {
        "description": "Environmental data overlay to render on the map.",
        "enum": [
          "aqi",
          "aqi_red_green",
          "pm25",
          "pollen_tree",
          "pollen_grass",
          "pollen_weed"
        ],
        "required": false,
        "type": "string"
      },
      "width": {
        "default": 640,
        "description": "Map width in pixels.",
        "maximum": 2048,
        "minimum": 100,
        "required": false,
        "type": "integer"
      },
      "zoom": {
        "default": 10,
        "description": "Map zoom level.",
        "maximum": 20,
        "minimum": 1,
        "required": false,
        "type": "integer"
      }
    },
    "required": false,
    "type": "object"
  }
}
```

## `get_current_conditions`

Action slug: `get-current-conditions`

Price: `5` credits

Get current Air Quality Index (AQI), pollutant concentrations, and health recommendations for one or more locations.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `extra_computations` | `array` | no | Additional data to compute and include in the response. |
| `include_items` | `array` | no | Filter specific pollutants to include. Omit to receive all pollutants. |
| `locations` | `array` | yes | List of 1-10 locations to query. Each location needs either latitude/longitude coordinates or an address string for geocoding. |
| `universal_aqi` | `boolean` | no | Use universal AQI scale for consistent cross-region comparisons. |

Sample parameters:

```json
{
  "extra_computations": [
    "HEALTH_RECOMMENDATIONS"
  ],
  "include_items": [
    "co"
  ],
  "locations": [
    {
      "address": "example address",
      "latitude": -90,
      "longitude": -180,
      "name": "example name"
    }
  ],
  "universal_aqi": true
}
```

Generated JSON parameter schema:

```json
{
  "extra_computations": {
    "description": "Additional data to compute and include in the response.",
    "items": {
      "enum": [
        "HEALTH_RECOMMENDATIONS",
        "DOMINANT_POLLUTANT_CONCENTRATION",
        "POLLUTANT_ADDITIONAL_INFO"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "include_items": {
    "description": "Filter specific pollutants to include. Omit to receive all pollutants.",
    "items": {
      "enum": [
        "co",
        "no2",
        "o3",
        "so2",
        "pm25",
        "pm10"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "locations": {
    "description": "List of 1-10 locations to query. Each location needs either latitude/longitude coordinates or an address string for geocoding.",
    "items": {
      "properties": {
        "address": {
          "description": "Address, city/state, or city/country to geocode. Required if latitude/longitude are not provided.",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90). Required if address is not provided.",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180). Required if address is not provided.",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional display name for this location.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "universal_aqi": {
    "default": true,
    "description": "Use universal AQI scale for consistent cross-region comparisons.",
    "required": false,
    "type": "boolean"
  }
}
```

## `get_forecast`

Action slug: `get-forecast`

Price: `5` credits

Get pollen forecast data for up to 5 days including tree, grass, and weed pollen types with seasonal status and health recommendations.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `forecast_days` | `integer` | no | Number of days of forecast data to return. |
| `include_items` | `array` | no | Filter specific pollen types. Omit to receive all three (tree, grass, weed). Pollutant items are not available for forecasts. |
| `locations` | `array` | yes | List of 1-10 locations to query. Each location needs either latitude/longitude coordinates or an address string. |

Sample parameters:

```json
{
  "forecast_days": 5,
  "include_items": [
    "tree pollen"
  ],
  "locations": [
    {
      "address": "example address",
      "latitude": -90,
      "longitude": -180,
      "name": "example name"
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "forecast_days": {
    "default": 5,
    "description": "Number of days of forecast data to return.",
    "maximum": 5,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "include_items": {
    "description": "Filter specific pollen types. Omit to receive all three (tree, grass, weed). Pollutant items are not available for forecasts.",
    "items": {
      "enum": [
        "tree pollen",
        "grass pollen",
        "weed pollen"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "locations": {
    "description": "List of 1-10 locations to query. Each location needs either latitude/longitude coordinates or an address string.",
    "items": {
      "properties": {
        "address": {
          "description": "Address, city/state, or city/country to geocode. Required if latitude/longitude are not provided.",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90). Required if address is not provided.",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180). Required if address is not provided.",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional display name for this location.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "minItems": 1,
    "required": true,
    "type": "array"
  }
}
```

## `get_history`

Action slug: `get-history`

Price: `5` credits

Get historical air quality data with hourly AQI values and pollutant concentrations, up to 30 days (720 hours) back.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `hours_history` | `integer` | no | Number of hours of historical data to retrieve. |
| `include_items` | `array` | no | Filter specific pollutants. Omit to receive all. Pollen data is not available for history. |
| `locations` | `array` | yes | List of 1-10 locations to query. Each location needs either latitude/longitude coordinates or an address string. |
| `universal_aqi` | `boolean` | no | Use universal AQI scale for consistent cross-region comparisons. |

Sample parameters:

```json
{
  "hours_history": 24,
  "include_items": [
    "co"
  ],
  "locations": [
    {
      "address": "example address",
      "latitude": -90,
      "longitude": -180,
      "name": "example name"
    }
  ],
  "universal_aqi": true
}
```

Generated JSON parameter schema:

```json
{
  "hours_history": {
    "default": 24,
    "description": "Number of hours of historical data to retrieve.",
    "maximum": 720,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "include_items": {
    "description": "Filter specific pollutants. Omit to receive all. Pollen data is not available for history.",
    "items": {
      "enum": [
        "co",
        "no2",
        "o3",
        "so2",
        "pm25",
        "pm10"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "locations": {
    "description": "List of 1-10 locations to query. Each location needs either latitude/longitude coordinates or an address string.",
    "items": {
      "properties": {
        "address": {
          "description": "Address, city/state, or city/country to geocode. Required if latitude/longitude are not provided.",
          "required": false,
          "type": "string"
        },
        "latitude": {
          "description": "Latitude coordinate (-90 to 90). Required if address is not provided.",
          "maximum": 90,
          "minimum": -90,
          "required": false,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude coordinate (-180 to 180). Required if address is not provided.",
          "maximum": 180,
          "minimum": -180,
          "required": false,
          "type": "number"
        },
        "name": {
          "description": "Optional display name for this location.",
          "required": false,
          "type": "string"
        }
      },
      "type": "object"
    },
    "maxItems": 10,
    "minItems": 1,
    "required": true,
    "type": "array"
  },
  "universal_aqi": {
    "default": true,
    "description": "Use universal AQI scale for consistent cross-region comparisons.",
    "required": false,
    "type": "boolean"
  }
}
```
