# Quality checklist

## Data and calculation

- Source files, tables, date range, grain, keys, status rules, and currency are identified.
- Order totals reconcile before and after joins.
- Refunds, cancellations, discounts, fees, and settlement are assigned to documented layers.
- Customer metrics use a valid identifier scope and show coverage when incomplete.
- Single-month, multi-month, prior-period, and prior-year logic are correct.
- Simulated data and inferred conclusions are clearly labeled.

## Content

- Tabs reflect the business type and available data.
- Product, customer, channel, time, capacity, or subscription modules appear only when relevant.
- Charts do not duplicate one another under different headings.
- Each major section includes a quantified conclusion and an actionable implication.
- Recommendations name the trigger, action, target metric, and review window when possible.

## Charts and layout

- Trend charts have visible axes, ticks, units, grid, and combined tooltips.
- Bars start at zero; line-axis ranges remain honest and visible.
- Stacked charts total correctly and legends match tooltips.
- Plot areas fill their cards without large unused regions.
- Cards, plot backgrounds, borders, and page background remain visually distinct.
- Desktop and mobile layouts have no clipped labels or horizontal overflow.

## Interaction

- All tabs and filters work.
- Every KPI, chart, conclusion, and recommendation responds to the same filter state.
- A one-month selection reduces comparison density.
- A multi-month selection displays monthly changes.
- Hover and tap tooltips work, including one shared tooltip for aligned multi-series charts.
- Empty and unavailable states explain what is missing.

## Delivery

- The HTML opens directly from `file://`.
- The browser console has no errors.
- External assets have a local fallback or are embedded.
- The final filename and visible business name match the user's data.
