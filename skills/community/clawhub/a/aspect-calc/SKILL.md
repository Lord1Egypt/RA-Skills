---
name: aspect-calc
description: Calculate aspect ratios from dimensions and find missing width or height. Use when the user asks to calculate an aspect ratio, find the height for a given width, simplify a ratio, or resize dimensions while preserving aspect ratio.
---

# Aspect Ratio Calculator

Calculate simplified aspect ratios from pixel dimensions, find missing dimensions from a known ratio, and report decimal and percentage equivalents using GCD simplification.

## Input
- Two dimensions (width and height in pixels), OR
- A known ratio (e.g., `16:9`) and one dimension (width or height), to calculate the missing value

## Output
- Simplified ratio (e.g., `16:9`)
- Decimal ratio (e.g., `1.7778`)
- Percentage (width as % of height, e.g., `177.78%`)
- If solving for missing dimension: the calculated value

## Instructions
1. Parse the user's input to determine the mode:
   - **Mode A**: two pixel dimensions given → calculate ratio and metadata
   - **Mode B**: ratio + one dimension given → calculate the missing dimension
2. **Mode A — Ratio from dimensions:**
   a. Compute `divisor = GCD(width, height)` using the Euclidean algorithm: `GCD(a, b) = b === 0 ? a : GCD(b, a % b)`
   b. Simplified ratio: `(width / divisor):(height / divisor)`
   c. Decimal: `(width / height).toFixed(4)`
   d. Percentage: `(width / height * 100).toFixed(2)%`
3. **Mode B — Dimension from ratio:**
   a. Parse the ratio as `rW:rH`
   b. If width is given: `height = round(width * rH / rW)`
   c. If height is given: `width = round(height * rW / rH)`
4. Identify if the ratio matches a known standard and name it:
   - `16:9` → HD Video / Widescreen
   - `4:3` → Classic TV / Standard
   - `1:1` → Square
   - `21:9` → Ultrawide
   - `9:16` → Mobile Video / Story
   - `3:4` → Portrait Classic
   - `3:2` → 35mm Film
   - `2:3` → Portrait Photo
5. Output all results clearly.

## Options
- `width`: positive integer
- `height`: positive integer
- `ratio`: string in `W:H` format — for Mode B
- `locked`: if true, preserve the current ratio when one dimension changes

## Examples

**Input:** "What is the aspect ratio of 1920x1080?"
**Output:**
- Simplified ratio: **16:9** (HD Video / Widescreen)
- Decimal: 1.7778
- Percentage: 177.78% (width is 177.78% of height)

**Input:** "I have a 16:9 video, width is 1280px — what height do I need?"
**Output:**
- Width: 1280px, Ratio: 16:9
- Height: **720px**
- (1280 × 9 / 16 = 720)

**Input:** "Simplify 2560x1440"
**Output:**
- Simplified ratio: **16:9** (HD Video / Widescreen)
- Decimal: 1.7778
- Percentage: 177.78%

**Input:** "What is the aspect ratio of 800x600?"
**Output:**
- Simplified ratio: **4:3** (Classic TV / Standard)
- Decimal: 1.3333
- Percentage: 133.33%

**Input:** "Give me height for a 21:9 ultrawide at 2560px width"
**Output:**
- Width: 2560px, Ratio: 21:9
- Height: **1097px**
- (2560 × 9 / 21 ≈ 1097)

## Error Handling
- If either dimension is 0 or negative, return an error: "Dimensions must be positive integers greater than 0."
- If a ratio is provided in an invalid format (not `W:H`), ask the user to use the `W:H` format (e.g., `16:9`).
- If both dimensions result in the same ratio numerator and denominator equal to 1 (e.g., prime dimensions with no common factor), output the ratio as-is and note it cannot be simplified further.
