---
name: border-radius
description: Generate CSS border-radius code. Use when the user asks to generate rounded corners, create a border radius, make a blob shape, or produce border-radius CSS.
---

# CSS Border Radius Generator

Generate `border-radius` CSS for uniform rounding or per-corner customization, including special shapes like blobs and leaves.

## Input
- Mode: `uniform` (all corners equal) or `per-corner`
- Uniform value: integer 0–9999 px (default `16`)
- Per-corner values: top-left, top-right, bottom-right, bottom-left in px (defaults `16 16 16 16`)

## Output
- CSS property: `border-radius: <value>;`
- Tailwind CSS class equivalent

## Instructions
1. Parse the user's request. Determine if all corners are the same or each is specified separately.
2. Compute the CSS value:
   - All corners equal: `border-radius: <value>px;`
   - Mixed corners: `border-radius: <tl>px <tr>px <br>px <bl>px;`
3. Compute the Tailwind class:
   - All equal, value is 0: `rounded-none`
   - All equal, value >= 9999: `rounded-full`
   - All equal, other: `rounded-[<value>px]`
   - Mixed: `rounded-[<tl>px_<tr>px_<br>px_<bl>px]`
4. Output both CSS and Tailwind.
5. If the user mentions a shape preset, map it:
   - None → `0 0 0 0`
   - Small → `4 4 4 4`
   - Medium → `8 8 8 8`
   - Large → `16 16 16 16`
   - XL → `24 24 24 24`
   - Full / pill / circle → `9999 9999 9999 9999`
   - Blob → `30px 70px 70px 30px`
   - Leaf → `0px 50px 0px 50px`

## Options
- `topLeft`: 0–9999 — default `16`
- `topRight`: 0–9999 — default `16`
- `bottomRight`: 0–9999 — default `16`
- `bottomLeft`: 0–9999 — default `16`
- `linked`: if true, all corners use the same value

## Examples

**Input:** "Rounded corners, 12px all sides"
**Output:**
```css
border-radius: 12px;
```
Tailwind: `rounded-[12px]`

**Input:** "Blob shape border radius"
**Output:**
```css
border-radius: 30px 70px 70px 30px;
```
Tailwind: `rounded-[30px_70px_70px_30px]`

**Input:** "Full pill / circle border radius"
**Output:**
```css
border-radius: 9999px;
```
Tailwind: `rounded-full`

**Input:** "Top corners 24px, bottom corners 0"
**Output:**
```css
border-radius: 24px 24px 0px 0px;
```
Tailwind: `rounded-[24px_24px_0px_0px]`

## Error Handling
- If a value is negative, set it to 0 and inform the user that border-radius cannot be negative.
- If a value exceeds 9999, cap at 9999 (used to represent fully rounded / `rounded-full`).
- If the user provides a unit other than px (e.g., rem, %), note the unit in the output and omit the Tailwind arbitrary value if not px.
