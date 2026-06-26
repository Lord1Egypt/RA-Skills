---
name: clip-path-generate
description: Generate CSS clip-path code for shapes. Use when the user asks to create a clip path, clip an element to a shape, generate clip-path CSS, or make a polygon, circle, ellipse, or inset clip.
---

# CSS Clip-Path Generator

Generate `clip-path` CSS values for circle, ellipse, polygon, and inset shapes, with optional `-webkit-` vendor prefix.

## Input
- Shape type: `circle` | `ellipse` | `polygon` | `inset` (default `circle`)
- Shape-specific parameters:
  - **circle**: `radius` % (default 50), `cx` % (default 50), `cy` % (default 50)
  - **ellipse**: `rx` % (default 50), `ry` % (default 35), `cx` % (default 50), `cy` % (default 50)
  - **inset**: `top` %, `right` %, `bottom` %, `left` % (default all 10)
  - **polygon**: list of `x% y%` point pairs (at least 3 points)
- Vendor prefix: boolean (default `false`)

## Output
- `clip-path: <value>;`
- Optionally `-webkit-clip-path: <value>;` if vendor prefix requested

## Instructions
1. Parse the user's request for shape type and parameters.
2. Build the clip-path value:
   - **circle**: `circle(<radius>% at <cx>% <cy>%)`
   - **ellipse**: `ellipse(<rx>% <ry>% at <cx>% <cy>%)`
   - **inset**: `inset(<top>% <right>% <bottom>% <left>%)`
   - **polygon**: `polygon(<x1>% <y1>%, <x2>% <y2>%, ...)` — join all points with `, `
3. If the user mentions a named preset shape, map to its polygon points:
   - **Triangle**: `polygon(50% 10%, 90% 90%, 10% 90%)`
   - **Pentagon**: `polygon(50% 5%, 95% 35%, 80% 90%, 20% 90%, 5% 35%)`
   - **Hexagon**: `polygon(50% 5%, 90% 25%, 90% 75%, 50% 95%, 10% 75%, 10% 25%)`
   - **Star**: `polygon(50% 5%, 61% 35%, 95% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 5% 35%, 39% 35%)`
   - **Arrow**: `polygon(5% 35%, 60% 35%, 60% 10%, 95% 50%, 60% 90%, 60% 65%, 5% 65%)`
4. Output `clip-path: <value>;`
5. If vendor prefix requested, also output `-webkit-clip-path: <value>;` above the standard property.
6. Include a short usage example showing the property applied to a `.element` class.

## Options
- `shape`: `circle` | `ellipse` | `polygon` | `inset` — default `circle`
- `radius`: 0–50 — default `50` (circle only)
- `cx`: 0–100 — default `50`
- `cy`: 0–100 — default `50`
- `rx`: 0–50 — default `50` (ellipse only)
- `ry`: 0–50 — default `35` (ellipse only)
- `top` / `right` / `bottom` / `left`: 0–50 — default `10` (inset only)
- `vendorPrefix`: true | false — default `false`

## Examples

**Input:** "Circle clip path, 40% radius, centered"
**Output:**
```css
clip-path: circle(40% at 50% 50%);
```

**Input:** "Triangle clip path"
**Output:**
```css
clip-path: polygon(50% 10%, 90% 90%, 10% 90%);
```

**Input:** "Ellipse clip, 60% wide 40% tall, centered, with webkit prefix"
**Output:**
```css
-webkit-clip-path: ellipse(60% 40% at 50% 50%);
clip-path: ellipse(60% 40% at 50% 50%);
```

**Input:** "Inset rectangle 15% margin all sides"
**Output:**
```css
clip-path: inset(15% 15% 15% 15%);
```

## Error Handling
- If polygon has fewer than 3 points, inform the user and ask for at least 3 coordinate pairs.
- If any percentage is outside 0–100, clamp it and note the adjustment.
- If shape type is unrecognized, default to `circle` and notify the user.
- For Safari compatibility, remind the user to add the `-webkit-clip-path` vendor prefix (or set vendorPrefix to true).
