---
name: color-adjustment
description: "Color Adjustment: Color manipulation: convert between hex/RGB/HSL, complement, darken/lighten, invert, adjust saturation, generate palettes. Accepts 140+ named colors. Use when an agent needs color adjustment, hex to rgb conversion, rgb to hex conversion, hex to hsl conversion, hsl to hex conversion, color complement, color, color darken through AgentPMT-hosted remote tool calls. Discovery terms: color adjustment, hex to rgb conversion, rgb to hex conversion, hex to hsl conversion."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/color-adjustment
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/color-adjustment"}}
---
# Color Adjustment

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A color conversion and manipulation utility for working with colors across multiple formats used in web development, graphic design, and user interface design. It features a smart color parser that accepts input in any common format including hexadecimal codes with or without hash prefix in both short and long forms, RGB functional notation, HSL functional notation, comma-separated RGB values, and over 140 CSS named colors like coral, steelblue, and papayawhip. Format conversion functions translate between hex, RGB, and HSL color spaces with full component extraction for programmatic use. Color manipulation operations include finding complementary colors by rotating 180 degrees on the color wheel, darkening and lightening by adjustable percentages through lightness modification, inverting colors by subtracting each channel from 255, and adjusting saturation up or down for more vibrant or muted tones. The random color generator produces full color specifications across all formats, while the palette generator creates harmonious color schemes using color theory principles including analogous, complementary, and evenly-distributed hue rotations with subtle saturation and lightness variations. All operations return results in multiple formats simultaneously for immediate use in CSS, design tools, or further processing.

## Product Instructions
### Color Adjustment - Instructions

#### Overview

Color Adjustment provides color format conversion, manipulation, and generation utilities. It accepts colors in multiple formats (hex, RGB, HSL, named colors) with automatic format detection, and performs conversions, adjustments, and palette generation.

#### Accepted Color Formats

The `color` parameter accepts any of the following formats -- the parser auto-detects:

- **Hex**: `#3498db` or `3498db` (with or without #, 3 or 6 digits)
- **RGB function**: `rgb(52, 152, 219)`
- **HSL function**: `hsl(204, 70, 53)`
- **Comma-separated RGB**: `52,152,219`
- **Named color**: `red`, `forestgreen`, `dodgerblue`, etc. (all standard CSS/HTML color names)

---

#### Actions

##### Conversions

###### color-hex-to-rgb
Convert any supported color format to RGB values.

- **Required**: `color` -- the color to convert
- **Optional**: none

**Example**:
```json
{ "action": "color-hex-to-rgb", "color": "#3498db" }
```

###### color-rgb-to-hex
Convert any supported color format to hex.

- **Required**: `color` -- the color to convert (e.g., `rgb(52, 152, 219)` or `52,152,219`)
- **Optional**: none

**Example**:
```json
{ "action": "color-rgb-to-hex", "color": "rgb(255, 0, 0)" }
```

###### color-hex-to-hsl
Convert any supported color format to HSL values.

- **Required**: `color` -- the color to convert
- **Optional**: none

**Example**:
```json
{ "action": "color-hex-to-hsl", "color": "#0000FF" }
```

###### color-hsl-to-hex
Convert HSL color to hex.

- **Required**: `color` -- the color in HSL or any supported format
- **Optional**: none

**Example**:
```json
{ "action": "color-hsl-to-hex", "color": "hsl(204, 70, 53)" }
```

###### color-rgb-to-hsl
Convert RGB color to HSL.

- **Required**: `color` -- the color to convert
- **Optional**: none

**Example**:
```json
{ "action": "color-rgb-to-hsl", "color": "rgb(255, 255, 0)" }
```

###### color-hsl-to-rgb
Convert HSL color to RGB.

- **Required**: `color` -- the color to convert
- **Optional**: none

**Example**:
```json
{ "action": "color-hsl-to-rgb", "color": "hsl(120, 100, 50)" }
```

###### color-name-to-hex
Convert a CSS/HTML color name to hex, RGB, and HSL values.

- **Required**: `color` -- the named color (e.g., `coral`, `steelblue`, `tomato`)
- **Optional**: none

**Example**:
```json
{ "action": "color-name-to-hex", "color": "forestgreen" }
```

---

##### Manipulations

###### color-complement
Get the complementary color (opposite on the color wheel, 180-degree hue rotation).

- **Required**: `color` -- the base color
- **Optional**: none

**Example**:
```json
{ "action": "color-complement", "color": "#FF0000" }
```

###### color-darken
Darken a color by reducing its lightness.

- **Required**: `color` -- the color to darken
- **Optional**: `amount` -- percentage to darken (1-100, default: 10)

**Example**:
```json
{ "action": "color-darken", "color": "#3498db", "amount": 20 }
```

###### color-lighten
Lighten a color by increasing its lightness.

- **Required**: `color` -- the color to lighten
- **Optional**: `amount` -- percentage to lighten (1-100, default: 10)

**Example**:
```json
{ "action": "color-lighten", "color": "navy", "amount": 15 }
```

###### color-invert
Invert a color (each RGB channel becomes 255 minus its value).

- **Required**: `color` -- the color to invert
- **Optional**: none

**Example**:
```json
{ "action": "color-invert", "color": "#3498db" }
```

###### color-saturate
Increase a color's saturation.

- **Required**: `color` -- the color to saturate
- **Optional**: `amount` -- percentage to increase saturation (1-100, default: 10)

**Example**:
```json
{ "action": "color-saturate", "color": "rgb(150, 120, 100)", "amount": 30 }
```

###### color-desaturate
Decrease a color's saturation (move toward gray).

- **Required**: `color` -- the color to desaturate
- **Optional**: `amount` -- percentage to decrease saturation (1-100, default: 10)

**Example**:
```json
{ "action": "color-desaturate", "color": "#e74c3c", "amount": 25 }
```

---

##### Generators

###### color-random
Generate a random color. Returns hex, RGB, and HSL values.

- **Required**: none
- **Optional**: none

**Example**:
```json
{ "action": "color-random" }
```

###### color-palette-generate
Generate a harmonious color palette. Uses analogous colors for small palettes (up to 3), pentagon distribution for medium palettes (up to 5), and even distribution for larger palettes.

- **Required**: none
- **Optional**: `count` -- number of colors to generate (1-20, default: 5)

**Example**:
```json
{ "action": "color-palette-generate", "count": 8 }
```

---

#### Common Workflows

1. **Brand color exploration**: Use `color-name-to-hex` to start from a named color, then `color-complement` to find a contrasting accent, and `color-lighten` / `color-darken` to create variants.
2. **Building a UI palette**: Use `color-palette-generate` with a desired count, then fine-tune individual colors with `color-saturate` or `color-desaturate`.
3. **Format conversion for developers**: Convert between hex, RGB, and HSL using the conversion actions to match the format required by your CSS, design tool, or API.
4. **Accessibility checks**: Use `color-lighten` and `color-darken` to create sufficient contrast between text and background colors.

#### Important Notes

- All actions except `color-random` and `color-palette-generate` require the `color` parameter.
- The `amount` parameter only applies to `color-darken`, `color-lighten`, `color-saturate`, and `color-desaturate`.
- The `count` parameter only applies to `color-palette-generate`.
- All responses include the result in multiple formats (hex, RGB, and/or HSL) for convenience.
- Named colors support all 147 standard CSS/HTML color names (e.g., `aliceblue`, `coral`, `midnightblue`, `tomato`).

## When To Use
- Use this skill for `Color Adjustment` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: color adjustment, hex to rgb conversion, rgb to hex conversion, hex to hsl conversion, hsl to hex conversion, color complement, color, color darken.
- Supported action names: `color-complement`, `color-darken`, `color-desaturate`, `color-hex-to-hsl`, `color-hex-to-rgb`, `color-hsl-to-hex`, `color-hsl-to-rgb`, `color-invert`, `color-lighten`, `color-name-to-hex`, `color-palette-generate`, `color-random`, `color-rgb-to-hex`, `color-rgb-to-hsl`, `color-saturate`.

## Use Cases
- Hex to RGB conversion
- RGB to hex conversion
- hex to HSL conversion
- HSL to hex conversion
- RGB to HSL conversion
- HSL to RGB conversion
- color format translation
- CSS color conversion
- web color conversion
- color space conversion
- color code translation
- complementary color finder
- opposite color calculation
- color wheel complement
- color harmony generation
- darken color

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `color-complement` (action slug: `color-complement`): Get the complementary color (opposite on the color wheel, 180-degree hue rotation). Returns complement in hex, RGB, and HSL. Price: `5` credits. Parameters: `color`.
- `color-darken` (action slug: `color-darken`): Darken a color by reducing its lightness. Returns darkened color in hex, RGB, and HSL. Price: `5` credits. Parameters: `amount`, `color`.
- `color-desaturate` (action slug: `color-desaturate`): Decrease a color's saturation (move toward gray). Returns desaturated color in hex, RGB, and HSL. Price: `5` credits. Parameters: `amount`, `color`.
- `color-hex-to-hsl` (action slug: `color-hex-to-hsl`): Convert any supported color format to HSL values. Returns h, s, l components and hsl() string. Price: `5` credits. Parameters: `color`.
- `color-hex-to-rgb` (action slug: `color-hex-to-rgb`): Convert any supported color format to RGB values. Returns r, g, b components and rgb() string. Price: `5` credits. Parameters: `color`.
- `color-hsl-to-hex` (action slug: `color-hsl-to-hex`): Convert HSL color to hexadecimal. Returns hex string. Price: `5` credits. Parameters: `color`.
- `color-hsl-to-rgb` (action slug: `color-hsl-to-rgb`): Convert HSL color to RGB values. Returns r, g, b components and rgb() string. Price: `5` credits. Parameters: `color`.
- `color-invert` (action slug: `color-invert`): Invert a color (each RGB channel becomes 255 minus its value). Returns inverted color in hex and RGB. Price: `5` credits. Parameters: `color`.
- `color-lighten` (action slug: `color-lighten`): Lighten a color by increasing its lightness. Returns lightened color in hex, RGB, and HSL. Price: `5` credits. Parameters: `amount`, `color`.
- `color-name-to-hex` (action slug: `color-name-to-hex`): Convert a CSS/HTML color name to hex, RGB, and HSL values. Supports all 147 standard named colors. Price: `5` credits. Parameters: `color`.
- `color-palette-generate` (action slug: `color-palette-generate`): Generate a harmonious color palette using color theory. Uses analogous colors for small palettes (up to 3), pentagon distribution for medium (up to 5), and even distribution for larger palettes. Price: `5` credits. Parameters: `count`.
- `color-random` (action slug: `color-random`): Generate a random color. Returns the color in hex, RGB, and HSL formats with all component values. Price: `5` credits. Parameters: none.
- `color-rgb-to-hex` (action slug: `color-rgb-to-hex`): Convert any supported color format to hexadecimal. Returns hex string. Price: `5` credits. Parameters: `color`.
- `color-rgb-to-hsl` (action slug: `color-rgb-to-hsl`): Convert RGB color to HSL values. Returns h, s, l components and hsl() string. Price: `5` credits. Parameters: `color`.
- `color-saturate` (action slug: `color-saturate`): Increase a color's saturation for a more vibrant result. Returns saturated color in hex, RGB, and HSL. Price: `5` credits. Parameters: `amount`, `color`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "color-adjustment"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "color-adjustment"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "color-adjustment"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "color-adjustment"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "color-adjustment"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "color-adjustment"
  }
}
```

## Call This Tool
Product slug: `color-adjustment`

Marketplace page: https://www.agentpmt.com/marketplace/color-adjustment

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
    "name": "Color-Adjustment",
    "arguments": {
      "action": "color-complement",
      "color": "example color"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "color-adjustment",
  "parameters": {
    "action": "color-complement",
    "color": "example color"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `color-complement` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/color-adjustment
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
