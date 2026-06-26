# Color for Data Visualization

## Core Rule

- Chart color should clarify structure and comparison, not decorate the dashboard.

## Choose the Right Scale Type

| Data type | Use | Avoid |
|-----------|-----|-------|
| Categories | Distinct categorical palette | Sequential ramps that imply order |
| Ordered values | Sequential ramp | Random category colors |
| Above/below midpoint | Diverging scale | Two unrelated accents with no midpoint logic |
| Density or heat | Sequential or perceptual heatmap | Rainbow scales unless there is a strong reason |

- If the viewer needs to compare values, lightness order matters more than hue novelty.
- If the viewer needs to identify groups quickly, separation matters more than aesthetic subtlety.

## Categorical Palettes

- Start with 5-8 clearly distinct colors before worrying about 20-series edge cases.
- Categorical palettes need enough contrast against the background and against each other.
- Reusing one hue at multiple lightness levels can work, but only if the labels stay obvious.
- If the chart is likely to be screenshotted or projected, increase separation beyond what looks acceptable on a laptop.

## Sequential and Diverging Ramps

- Sequential ramps should rise steadily in lightness or intensity so the order is visually obvious.
- Diverging ramps need a meaningful midpoint that does not look like accidental gray mud.
- Perceptual spaces help ramps feel even; RGB interpolation often does not.
- Heatmaps should not hide important thresholds in barely distinguishable middle colors.

## Dashboard Reality

- Thin lines, tiny points, and pale gridlines disappear first.
- Legends far away from the chart increase reliance on memory and color discrimination.
- Direct labeling is often better than adding more legend colors.
- If the chart lives in a dense dashboard, test with surrounding cards and table colors in place.

## Accessibility and Annotation

- Use markers, line styles, labels, or patterns when several series must be compared.
- If a red series and a green series ever represent opposite outcomes, add direct cues.
- Tooltips and legends should repeat the category names clearly instead of relying on swatches alone.
- Small multiples often reduce color complexity better than forcing many categories into one chart.

## Common Data-Viz Traps

- Using rainbow palettes for ordered data.
- Choosing category colors that look distinct only on a white artboard.
- Making warning and error series rely on the same hue family as marketing accents.
- Letting gridlines compete with data because the neutral system is too dark.
- Optimizing for visual flair while the labels remain unreadable in screenshots.
