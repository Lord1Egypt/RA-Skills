# Elevation Data - Point, Path, Charts & Statistics Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `elevation-data-point-path-charts-statistics`

x402 availability: not enabled for this product.

## `get_elevation`

Action slug: `get-elevation`

Price: `10` credits

Get elevation data for one or more discrete locations. Returns elevation in meters and feet, resolution, category, and aggregate statistics when multiple points are provided.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `locations` | `array` | yes | List of locations for discrete elevation lookup (max 512). Each location must have latitude and longitude fields. |

Sample parameters:

```json
{
  "locations": [
    {
      "latitude": 1,
      "longitude": 1
    }
  ]
}
```

Generated JSON parameter schema:

```json
{
  "locations": {
    "description": "List of locations for discrete elevation lookup (max 512). Each location must have latitude and longitude fields.",
    "items": {
      "properties": {
        "latitude": {
          "description": "Latitude in decimal degrees (-90 to 90)",
          "required": true,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude in decimal degrees (-180 to 180)",
          "required": true,
          "type": "number"
        }
      },
      "type": "object"
    },
    "maxItems": 512,
    "required": true,
    "type": "array"
  }
}
```

## `get_elevation_profile`

Action slug: `get-elevation-profile`

Price: `10` credits

Same as get_path_elevation but always generates an elevation profile chart image. The chart shows elevation vs. distance with min/max markers and dual axes (meters and feet). A signed URL to the chart image is included in the response.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chart_height` | `integer` | no | Chart height in inches (4-12) |
| `chart_width` | `integer` | no | Chart width in inches (6-20) |
| `path` | `array` | yes | List of locations defining a path (minimum 2 points). Each point must have latitude and longitude fields. |
| `samples` | `integer` | no | Number of evenly-spaced sample points along the path (2-512) |

Sample parameters:

```json
{
  "chart_height": 6,
  "chart_width": 12,
  "path": [
    {
      "latitude": 1,
      "longitude": 1
    }
  ],
  "samples": 100
}
```

Generated JSON parameter schema:

```json
{
  "chart_height": {
    "default": 6,
    "description": "Chart height in inches (4-12)",
    "maximum": 12,
    "minimum": 4,
    "required": false,
    "type": "integer"
  },
  "chart_width": {
    "default": 12,
    "description": "Chart width in inches (6-20)",
    "maximum": 20,
    "minimum": 6,
    "required": false,
    "type": "integer"
  },
  "path": {
    "description": "List of locations defining a path (minimum 2 points). Each point must have latitude and longitude fields.",
    "items": {
      "properties": {
        "latitude": {
          "description": "Latitude in decimal degrees (-90 to 90)",
          "required": true,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude in decimal degrees (-180 to 180)",
          "required": true,
          "type": "number"
        }
      },
      "type": "object"
    },
    "minItems": 2,
    "required": true,
    "type": "array"
  },
  "samples": {
    "default": 100,
    "description": "Number of evenly-spaced sample points along the path (2-512)",
    "maximum": 512,
    "minimum": 2,
    "required": false,
    "type": "integer"
  }
}
```

## `get_path_elevation`

Action slug: `get-path-elevation`

Price: `10` credits

Sample elevation values at evenly-spaced points along a path defined by two or more waypoints. Returns elevation data for each sample point plus path statistics including total distance, ascent, and descent.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `chart_height` | `integer` | no | Chart height in inches (4-12). Only used when a chart is generated. |
| `chart_width` | `integer` | no | Chart width in inches (6-20). Only used when a chart is generated. |
| `generate_chart` | `boolean` | no | Set to true to also generate an elevation profile chart image (default false) |
| `path` | `array` | yes | List of locations defining a path (minimum 2 points). Each point must have latitude and longitude fields. |
| `samples` | `integer` | no | Number of evenly-spaced sample points along the path (2-512) |

Sample parameters:

```json
{
  "chart_height": 6,
  "chart_width": 12,
  "generate_chart": false,
  "path": [
    {
      "latitude": 1,
      "longitude": 1
    }
  ],
  "samples": 100
}
```

Generated JSON parameter schema:

```json
{
  "chart_height": {
    "default": 6,
    "description": "Chart height in inches (4-12). Only used when a chart is generated.",
    "maximum": 12,
    "minimum": 4,
    "required": false,
    "type": "integer"
  },
  "chart_width": {
    "default": 12,
    "description": "Chart width in inches (6-20). Only used when a chart is generated.",
    "maximum": 20,
    "minimum": 6,
    "required": false,
    "type": "integer"
  },
  "generate_chart": {
    "default": false,
    "description": "Set to true to also generate an elevation profile chart image (default false)",
    "required": false,
    "type": "boolean"
  },
  "path": {
    "description": "List of locations defining a path (minimum 2 points). Each point must have latitude and longitude fields.",
    "items": {
      "properties": {
        "latitude": {
          "description": "Latitude in decimal degrees (-90 to 90)",
          "required": true,
          "type": "number"
        },
        "longitude": {
          "description": "Longitude in decimal degrees (-180 to 180)",
          "required": true,
          "type": "number"
        }
      },
      "type": "object"
    },
    "minItems": 2,
    "required": true,
    "type": "array"
  },
  "samples": {
    "default": 100,
    "description": "Number of evenly-spaced sample points along the path (2-512)",
    "maximum": 512,
    "minimum": 2,
    "required": false,
    "type": "integer"
  }
}
```
