# Color Adjustment Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `color-adjustment`

x402 availability: not enabled for this product.

## `color-complement`

Action slug: `color-complement`

Price: `5` credits

Get the complementary color (opposite on the color wheel, 180-degree hue rotation). Returns complement in hex, RGB, and HSL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Base color. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Base color. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-darken`

Action slug: `color-darken`

Price: `5` credits

Darken a color by reducing its lightness. Returns darkened color in hex, RGB, and HSL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | `integer` | no | Percentage to darken (1-100). Default: 10. |
| `color` | `string` | yes | Color to darken. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "amount": 10,
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "amount": {
    "default": 10,
    "description": "Percentage to darken (1-100). Default: 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "color": {
    "description": "Color to darken. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-desaturate`

Action slug: `color-desaturate`

Price: `5` credits

Decrease a color's saturation (move toward gray). Returns desaturated color in hex, RGB, and HSL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | `integer` | no | Percentage to decrease saturation (1-100). Default: 10. |
| `color` | `string` | yes | Color to desaturate. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "amount": 10,
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "amount": {
    "default": 10,
    "description": "Percentage to decrease saturation (1-100). Default: 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "color": {
    "description": "Color to desaturate. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-hex-to-hsl`

Action slug: `color-hex-to-hsl`

Price: `5` credits

Convert any supported color format to HSL values. Returns h, s, l components and hsl() string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-hex-to-rgb`

Action slug: `color-hex-to-rgb`

Price: `5` credits

Convert any supported color format to RGB values. Returns r, g, b components and rgb() string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to convert. Accepts hex (#3498db or 3498db), RGB function (rgb(52,152,219)), HSL function (hsl(204,70,53)), comma-separated RGB (52,152,219), or named color (red, forestgreen, etc.). |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to convert. Accepts hex (#3498db or 3498db), RGB function (rgb(52,152,219)), HSL function (hsl(204,70,53)), comma-separated RGB (52,152,219), or named color (red, forestgreen, etc.).",
    "required": true,
    "type": "string"
  }
}
```

## `color-hsl-to-hex`

Action slug: `color-hsl-to-hex`

Price: `5` credits

Convert HSL color to hexadecimal. Returns hex string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-hsl-to-rgb`

Action slug: `color-hsl-to-rgb`

Price: `5` credits

Convert HSL color to RGB values. Returns r, g, b components and rgb() string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-invert`

Action slug: `color-invert`

Price: `5` credits

Invert a color (each RGB channel becomes 255 minus its value). Returns inverted color in hex and RGB.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to invert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to invert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-lighten`

Action slug: `color-lighten`

Price: `5` credits

Lighten a color by increasing its lightness. Returns lightened color in hex, RGB, and HSL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | `integer` | no | Percentage to lighten (1-100). Default: 10. |
| `color` | `string` | yes | Color to lighten. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "amount": 10,
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "amount": {
    "default": 10,
    "description": "Percentage to lighten (1-100). Default: 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "color": {
    "description": "Color to lighten. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-name-to-hex`

Action slug: `color-name-to-hex`

Price: `5` credits

Convert a CSS/HTML color name to hex, RGB, and HSL values. Supports all 147 standard named colors.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | CSS/HTML color name (e.g., 'coral', 'steelblue', 'forestgreen', 'tomato'). |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "CSS/HTML color name (e.g., 'coral', 'steelblue', 'forestgreen', 'tomato').",
    "required": true,
    "type": "string"
  }
}
```

## `color-palette-generate`

Action slug: `color-palette-generate`

Price: `5` credits

Generate a harmonious color palette using color theory. Uses analogous colors for small palettes (up to 3), pentagon distribution for medium (up to 5), and even distribution for larger palettes.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `count` | `integer` | no | Number of colors to generate (1-20). Default: 5. |

Sample parameters:

```json
{
  "count": 5
}
```

Generated JSON parameter schema:

```json
{
  "count": {
    "default": 5,
    "description": "Number of colors to generate (1-20). Default: 5.",
    "maximum": 20,
    "minimum": 1,
    "required": false,
    "type": "integer"
  }
}
```

## `color-random`

Action slug: `color-random`

Price: `5` credits

Generate a random color. Returns the color in hex, RGB, and HSL formats with all component values.

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `color-rgb-to-hex`

Action slug: `color-rgb-to-hex`

Price: `5` credits

Convert any supported color format to hexadecimal. Returns hex string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-rgb-to-hsl`

Action slug: `color-rgb-to-hsl`

Price: `5` credits

Convert RGB color to HSL values. Returns h, s, l components and hsl() string.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `color` | `string` | yes | Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "color": {
    "description": "Color to convert. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```

## `color-saturate`

Action slug: `color-saturate`

Price: `5` credits

Increase a color's saturation for a more vibrant result. Returns saturated color in hex, RGB, and HSL.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `amount` | `integer` | no | Percentage to increase saturation (1-100). Default: 10. |
| `color` | `string` | yes | Color to saturate. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color. |

Sample parameters:

```json
{
  "amount": 10,
  "color": "example color"
}
```

Generated JSON parameter schema:

```json
{
  "amount": {
    "default": 10,
    "description": "Percentage to increase saturation (1-100). Default: 10.",
    "maximum": 100,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "color": {
    "description": "Color to saturate. Accepts hex, rgb(), hsl(), comma-separated RGB, or named color.",
    "required": true,
    "type": "string"
  }
}
```
