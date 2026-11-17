# Dashboard UI and interaction

## Information architecture

Start with a compact header, filters, key findings, and an overview. Add domain tabs only when the underlying data supports them. Use separate product and customer tabs when both are substantial.

A useful tab normally answers one business question in this order:

1. What happened?
2. Where did it happen?
3. Why did it change?
4. What should the operator do next?

Avoid repeating the same monthly trend under different titles. Each chart must contribute a distinct decision signal.

## Chart selection

- Time trend: column plus smooth line, or smooth line for comparable metrics.
- Monthly customer composition: stacked columns for new and returning customers.
- Monthly frequency composition: one stacked column per month with frequency bands.
- Category or item comparison: sorted horizontal bars with values and units.
- Mix or share: donut only for a small number of categories; otherwise stacked bars.
- Change drivers: waterfall or ranked contribution bars.
- Weekday and hour pattern: monthly smooth curves across weekday or hour, or a heatmap when density matters.
- Funnel: staged conversion chart with counts and rates.
- Cohort retention: cohort heatmap or aligned retention curves.

Tables are for lookup and audit. Do not use a wide table as the main explanation when a chart and conclusion communicate the pattern better.

## Tooltips and legends

- Every analytical chart needs hover or tap details.
- For multiple series sharing an x-axis, show one combined tooltip containing that x-value and all visible series.
- Legends toggle series when practical and use the same names, colors, units, and order as the tooltip.
- Tooltips must not obscure the active point on small screens.

## Layout and visual system

- Keep cards visually separate from the page background. The plotting region may use a subtle tint or grid, but do not create a second heavy card inside every card.
- Give charts enough height and let the plot fill the available card. Remove unexplained blank areas.
- Use visible but quiet grid lines for trend charts. Include y-axis ticks, labels, and units.
- Keep filters short. Prefer start month, end month, channel, and store over a long all-purpose filter bar.
- Remove decorative color strips that do not encode information.
- Use motion to reveal hierarchy and state changes. Keep it brief and respect `prefers-reduced-motion`.
- Support desktop and mobile layouts without horizontal overflow.

## Dynamic copy

Titles, subtitles, chart notes, findings, conclusions, and action plans must update with the filter state. Avoid implementation phrases such as “柱形平滑趋势折线”. Use business labels such as “日均净营业额” and “环比变化”.

## Offline delivery

Prefer a self-contained HTML file with embedded data, CSS, and JavaScript. If a chart library is required, bundle it locally or provide a graceful local fallback so `file://` remains usable.
