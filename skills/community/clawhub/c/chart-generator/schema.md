# Chart Generator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `chart-generator`

x402 availability: not enabled for this product.

## `generate_chart`

Action slug: `generate-chart`

Price: `2` credits

Generate a modern, professional chart image from structured data. Supports 9 chart types (bar, line, pie, doughnut, scatter, bubble, radar, polarArea, horizontalBar), 5 preset themes plus custom styling, and 4 export formats (PNG, SVG, PDF, WebP). Returns chart as a cloud-stored file URL or base64-encoded data.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `background_color` | `string` | no | Background color. Accepts named colors ('white', 'transparent'), HEX ('#FFFFFF'), RGB ('rgb(255,255,255)'), or HSL |
| `chart_type` | `string` | yes | Type of chart to generate |
| `custom_options` | `object` | no | Custom Chart.js options object to override theme defaults. Supports any Chart.js 3.x/4.x option (plugins, scales, etc.) |
| `data` | `object` | yes | Chart.js compatible data object. Must contain 'labels' (array of strings) and/or 'datasets' (array of dataset objects). Each dataset has 'label' (string), 'data' (array of numbers or point objects), and optional color overrides. |
| `device_pixel_ratio` | `integer` | no | Device pixel ratio: 1 for normal displays, 2 for retina/high-DPI |
| `expiration_days` | `integer` | no | Number of days until the stored file expires (1-7) |
| `height` | `integer` | no | Chart height in pixels (100-2000) |
| `output_format` | `string` | no | Output format for the chart image: 'png' (raster), 'svg' (vector), 'pdf' (document), 'webp' (compressed) |
| `return_base64` | `boolean` | no | If true, returns base64-encoded image data instead of a file URL. Useful for embedding in emails or immediate display |
| `store_file` | `boolean` | no | If true, stores the chart in cloud storage and returns a signed download URL |
| `theme` | `string` | no | Preset theme: 'corporate' (professional blues/grays), 'modern_dark' (dark background, vibrant accents), 'minimal' (black/white/gray), 'colorful' (vibrant marketing colors), 'academic' (colorblind-accessible), 'custom' (no preset, use custom_options) |
| `title` | `string` | no | Chart title text displayed on the chart |
| `width` | `integer` | no | Chart width in pixels (100-2000) |

Sample parameters:

```json
{
  "background_color": "white",
  "chart_type": "bar",
  "custom_options": {},
  "data": {
    "datasets": [
      {
        "backgroundColor": "example backgroundColor",
        "borderColor": "example borderColor",
        "borderWidth": 1,
        "data": [
          1
        ],
        "label": "example label"
      }
    ],
    "labels": [
      "example label"
    ]
  },
  "device_pixel_ratio": 1,
  "expiration_days": 7,
  "height": 400,
  "output_format": "png"
}
```

Generated JSON parameter schema:

```json
{
  "background_color": {
    "default": "white",
    "description": "Background color. Accepts named colors ('white', 'transparent'), HEX ('#FFFFFF'), RGB ('rgb(255,255,255)'), or HSL",
    "required": false,
    "type": "string"
  },
  "chart_type": {
    "description": "Type of chart to generate",
    "enum": [
      "bar",
      "line",
      "pie",
      "doughnut",
      "scatter",
      "bubble",
      "radar",
      "polarArea",
      "horizontalBar"
    ],
    "required": true,
    "type": "string"
  },
  "custom_options": {
    "description": "Custom Chart.js options object to override theme defaults. Supports any Chart.js 3.x/4.x option (plugins, scales, etc.)",
    "required": false,
    "type": "object"
  },
  "data": {
    "description": "Chart.js compatible data object. Must contain 'labels' (array of strings) and/or 'datasets' (array of dataset objects). Each dataset has 'label' (string), 'data' (array of numbers or point objects), and optional color overrides.",
    "properties": {
      "datasets": {
        "description": "Array of dataset objects, each with label, data, and optional styling",
        "items": {
          "properties": {
            "backgroundColor": {
              "description": "Background color override for this dataset",
              "required": false,
              "type": "string"
            },
            "borderColor": {
              "description": "Border color override for this dataset",
              "required": false,
              "type": "string"
            },
            "borderWidth": {
              "description": "Border width in pixels",
              "required": false,
              "type": "number"
            },
            "data": {
              "description": "Array of numeric values or point objects ({x, y} for scatter/bubble)",
              "items": {
                "type": "number"
              },
              "required": true,
              "type": "array"
            },
            "label": {
              "description": "Dataset display name",
              "required": false,
              "type": "string"
            }
          },
          "type": "object"
        },
        "required": true,
        "type": "array"
      },
      "labels": {
        "description": "Array of label strings for chart categories/x-axis",
        "items": {
          "type": "string"
        },
        "required": false,
        "type": "array"
      }
    },
    "required": true,
    "type": "object"
  },
  "device_pixel_ratio": {
    "default": 1,
    "description": "Device pixel ratio: 1 for normal displays, 2 for retina/high-DPI",
    "enum": [
      1,
      2
    ],
    "required": false,
    "type": "integer"
  },
  "expiration_days": {
    "default": 7,
    "description": "Number of days until the stored file expires (1-7)",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "height": {
    "default": 400,
    "description": "Chart height in pixels (100-2000)",
    "maximum": 2000,
    "minimum": 100,
    "required": false,
    "type": "integer"
  },
  "output_format": {
    "default": "png",
    "description": "Output format for the chart image: 'png' (raster), 'svg' (vector), 'pdf' (document), 'webp' (compressed)",
    "enum": [
      "png",
      "svg",
      "pdf",
      "webp"
    ],
    "required": false,
    "type": "string"
  },
  "return_base64": {
    "default": false,
    "description": "If true, returns base64-encoded image data instead of a file URL. Useful for embedding in emails or immediate display",
    "required": false,
    "type": "boolean"
  },
  "store_file": {
    "default": true,
    "description": "If true, stores the chart in cloud storage and returns a signed download URL",
    "required": false,
    "type": "boolean"
  },
  "theme": {
    "default": "corporate",
    "description": "Preset theme: 'corporate' (professional blues/grays), 'modern_dark' (dark background, vibrant accents), 'minimal' (black/white/gray), 'colorful' (vibrant marketing colors), 'academic' (colorblind-accessible), 'custom' (no preset, use custom_options)",
    "enum": [
      "corporate",
      "modern_dark",
      "minimal",
      "colorful",
      "academic",
      "custom"
    ],
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Chart title text displayed on the chart",
    "required": false,
    "type": "string"
  },
  "width": {
    "default": 600,
    "description": "Chart width in pixels (100-2000)",
    "maximum": 2000,
    "minimum": 100,
    "required": false,
    "type": "integer"
  }
}
```
