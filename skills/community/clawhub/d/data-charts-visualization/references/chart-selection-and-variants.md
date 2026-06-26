# Chart Selection And Variants

Use this file when the agent needs to decide both:

- which chart family best answers the user’s question
- which concrete variant inside that family best matches the scenario

The goal is not visual novelty. The goal is to maximize interpretability with the lowest necessary complexity.

If the underlying data and chart family remain essentially stable and the user is mainly iterating on appearance, presentation feel, or repeated re-renders of the same data, this is no longer chart-selection work. In that case, prefer the config-page handoff rules in `{baseDir}/references/config-page-handoff.md`.

## What To Do When The User Already Names A Chart Or Variant

If the user explicitly names a chart family or variant, default to honoring that instruction instead of re-running chart selection from scratch.

Execution order:

1. detect whether the user named only a family, or a family plus a variant
2. map the phrase into `chart-type + variant`
3. if the mapping is semantically acceptable, execute it directly
4. if it is merely suboptimal but still valid, still follow the user’s request
5. only override when the request is clearly misleading, semantically invalid, or unsupported by the current runtime

In practice:

- if the user says “horizontal stacked bar chart”, do not silently switch to another chart
- if the user says “donut”, do not silently downgrade to classic pie
- if the user says “dual-axis”, do not ignore that just because a single axis could also work

The only valid reasons to challenge the user’s requested chart are:

- the data semantics do not match the requested chart
- the requested variant is not actually supported by the runtime

When that happens:

1. state the mismatch or capability boundary clearly
2. propose the closest workable alternative

## Natural Language To Internal Mapping

When the user directly names a chart or variant, map it into a normalized `chart-type + variant` combination whenever possible.

### Bar Family

- “bar chart”:
  `chart-type = bar`

- “horizontal bar chart”:
  `chart-type = bar`
  `variant = { "layout": "horizontal" }`

- “stacked bar chart”:
  `chart-type = bar`
  `variant = { "stack": true }`

- “horizontal stacked bar chart”:
  `chart-type = bar`
  `variant = { "layout": "horizontal", "stack": true }`

### Pie Family

- “pie chart”:
  `chart-type = pie`

- “donut chart”:
  `chart-type = pie`
  `variant = { "pieMode": "donut" }`

- “rose chart” or “nightingale rose”:
  `chart-type = pie`
  `variant = { "pieMode": "rose" }`

### Dual-Axis Family

- “dual-axis chart”, “dual y-axis chart”:
  `chart-type = dualAxis`
  if the user did not specify series types, default to:
  `variant = { "leftSeriesType": "bar", "rightSeriesType": "line" }`

- “dual-axis bar-line chart”:
  `chart-type = dualAxis`
  `variant = { "leftSeriesType": "bar", "rightSeriesType": "line" }`

- “horizontal dual-axis chart”:
  `chart-type = dualAxis`
  if the user did not specify series types, default to:
  `variant = { "layout": "horizontal", "leftSeriesType": "bar", "rightSeriesType": "line" }`

- “dual-axis line-line chart”:
  `chart-type = dualAxis`
  `variant = { "leftSeriesType": "line", "rightSeriesType": "line" }`

- “dual-axis left-line right-bar”:
  `chart-type = dualAxis`
  `variant = { "leftSeriesType": "line", "rightSeriesType": "bar" }`

### Other Common Terms

- “area chart”:
  `chart-type = area`

- “bubble chart”:
  `chart-type = scatter`
  with third-dimension size semantics carried in the data

- “radar chart”:
  `chart-type = radar`

- “funnel chart”:
  `chart-type = funnel`

- “gauge”:
  `chart-type = gauge`

## Additional Rules For User-Specified Requests

### User Names Only The Chart Family

The agent still needs to complete the best variant.

Examples:

- if the user only says “use a bar chart”, the agent still decides whether it should be horizontal or stacked
- if the user only says “use a pie chart”, the agent still decides whether classic pie or donut is the better default
- if the user only says “use dual-axis”, the agent still decides whether `bar+line` or `line+line` fits better

### User Names Both Family And Variant

Follow the user’s choice directly.

Examples:

- “horizontal stacked bar chart”
- “donut chart”
- “dual-axis line-line chart”

These should map directly into parameters rather than being reinterpreted.

### User Request Is Incomplete But Directionally Clear

Do the minimum completion needed, without changing direction.

Examples:

- if the user says “make it dual-axis” without specifying series types, default to `bar + line`
- if the user says “make it a rose chart”, keep the rose direction and only add a brief note if precise share reading may suffer

### User Request Conflicts With The Data

Do not force an incorrect chart.

Examples:

- the user asks for funnel but the data is only a plain ranking
- the user asks for pie but there are twenty categories

Handling pattern:

1. explain the mismatch
2. explain why following the request literally would be misleading
3. offer the closest workable alternative

## Explicit Example

User says:

> use a horizontal stacked bar chart

The agent should resolve that to:

- chart family: `bar`
- variant: horizontal + stacked
- CLI layer:
  `--chart-type bar`
  `--variant '{"layout":"horizontal","stack":true}'`

Do not reduce that request to a generic bar chart and drop the horizontal or stacked requirements.

## First Decision: What Is The User Actually Comparing?

Choose the chart family from the analytic task, not from surface wording.

- change over ordered time or sequence: prefer `line`, sometimes `area`
- compare discrete categories or rankings: prefer `bar`
- show part-to-whole with few categories: prefer `pie`
- show one KPI against a scale, target, or status band: prefer `gauge`
- compare two metrics with different units on one shared x-axis: consider `dualAxis`
- show relationship, spread, cluster, or outlier behavior between two numeric dimensions: prefer `scatter`
- show multi-dimension profile shape: prefer `radar`
- show ordered step conversion or drop-off: prefer `funnel`

If multiple families are plausible, choose the less cognitively expensive one.

## Line Vs Area

Choose `line` when:

- the primary question is trend direction, inflection, or comparison over time
- precision matters more than visual weight
- there are several series and overlap must remain readable

Choose `area` when:

- the chart is still a trend chart, but magnitude or accumulation should feel stronger
- one or two main series dominate the view
- filled area helps communicate volume, contribution, or momentum

Avoid `area` when:

- too many overlapping series would muddy the chart
- users need precise multi-series comparison more than atmosphere or emphasis

Default rule:

- if uncertain, start with `line`
- upgrade to `area` only when fill clearly adds meaning

## Bar Variants

### Standard Vertical Bar

Choose the default vertical bar when:

- the task is standard category comparison
- the chart will be read like a dashboard column chart
- the x-axis is naturally read from left to right

Choose vertical bar by default when readability is not at risk.

### Horizontal Bar

Choose horizontal bar when:

- the task is ranking, leaderboard, top-N, or bottom-N
- readability matters more than compact width
- users are likely to scan from highest to lowest item

Do not choose bar orientation for decoration.
Treat it as a readability decision, not a styling decision.

Default rule:

- for ranking-style views, prefer `horizontal`
- otherwise prefer the default vertical bar

Pass this as:

```json
{ "layout": "horizontal" }
```

### Stacked Bar

Choose stacked bar when:

- users need both total and composition at the same time
- each category is made of meaningful sub-parts
- the main question is contribution structure, not only side-by-side comparison

Avoid stacked bar when:

- the user mainly wants precise comparison among sub-series across categories
- there is no real part-to-whole relationship

Pass this as:

```json
{ "stack": true }
```

### Horizontal Stacked Bar

Choose this combination when:

- labels are long
- categories are rank-like
- each category also has internal composition

Pass this as:

```json
{ "layout": "horizontal", "stack": true }
```

## Pie Variants

Only use pie-family charts when the number of categories is small and the user mainly cares about share, not precise comparison.

### Classic Pie

Choose classic pie when:

- the user explicitly asked for a traditional pie chart
- the composition is simple
- presentation style should stay plain and familiar

Pass this by keeping `--chart-type pie` with no special pie variant.

### Donut

Choose donut when:

- you still want part-to-whole, but with a cleaner and less dense presentation
- center whitespace improves readability or layout balance
- the user did not insist on a classic full pie

This is the safest default pie-family variant for many business-reporting scenarios.

Pass this as:

```json
{ "pieMode": "donut" }
```

### Rose

Choose rose only when:

- the user wants stronger visual distinction between categories
- expressive differentiation matters more than strict analytical precision
- category count is still small enough to stay readable

Avoid rose when:

- exact part-to-whole reading matters
- the chart is analytical rather than presentation-oriented

Pass this as:

```json
{ "pieMode": "rose" }
```

If the runtime distinguishes rose subtypes, the agent may prefer a more specific value such as `roseRadius` or `roseArea`, but should do so only when the runtime actually supports that value.

## Dual-Axis: When It Is Justified

Use `dualAxis` sparingly.

Choose dual-axis when:

- two metrics share the same x-axis
- the metrics use different units, such as revenue and conversion rate
- or the scale gap is large enough that one metric would be visually flattened on a single axis

Do not use dual-axis when:

- a single axis already works
- the second axis exists only to make the chart look richer
- both metrics are better understood separately

### Dual-Axis Variant Selection

Prefer vertical dual-axis layout when:

- the shared category axis is a timeline, ordered stage list, or other natural left-to-right sequence
- the chart reads like a standard metric-trend or metric-vs-rate comparison

Prefer horizontal dual-axis layout when:

- the shared category axis is a ranked or named category list
- both series still describe the same category set, but a horizontal reading direction fits the comparison better

Pass horizontal dual-axis layout as:

```json
{ "layout": "horizontal", "leftSeriesType": "bar", "rightSeriesType": "line" }
```

Prefer left bar + right line when:

- one metric is a volume, count, total, amount, or throughput
- the other metric is a rate, percentage, average, or efficiency signal

Pass this as:

```json
{ "leftSeriesType": "bar", "rightSeriesType": "line" }
```

Prefer left line + right line when:

- both metrics are fundamentally trend lines
- they need separate axes only because of different units or scales

Pass this as:

```json
{ "leftSeriesType": "line", "rightSeriesType": "line" }
```

Prefer left line + right bar when:

- the line is the primary story
- the bar is supporting context

Use:

```json
{ "leftSeriesType": "line", "rightSeriesType": "bar" }
```

Prefer left bar + right bar only when:

- both metrics are discrete magnitude comparisons
- both genuinely need separate axes

This is the least preferred dual-axis variant because it increases visual heaviness.

Use:

```json
{ "leftSeriesType": "bar", "rightSeriesType": "bar" }
```

## Scatter Vs Bubble

Use `scatter` whenever the task is correlation, spread, clustering, or outlier detection.

Use a bubble-style scatter when:

- a third numeric variable should be encoded into point size
- the user is asking for three-dimensional comparison inside a 2D chart

Bubble is still rendered under `--chart-type scatter`; the data shape carries the extra size semantics.

## Radar: When To Use It

Choose `radar` when:

- the user wants a profile shape across several dimensions
- exact reading is less important than relative balance
- a small number of entities should be compared on the same bounded dimensions

Avoid radar when:

- there are too many dimensions
- the user needs precise ranking or numeric reading

## Funnel: When To Use It

Choose `funnel` when:

- the stages are sequential
- the user is asking about conversion, retention, progression, or drop-off
- step order is integral to the meaning

Do not use funnel for a plain sorted ranking that is not a real process.

## Gauge: When To Use It

Choose `gauge` only when:

- the story is one KPI
- the number is being read against a target, threshold, or status range
- progress, utilization, completion, or health is the message

Avoid gauge when:

- users need comparison across multiple metrics
- a plain number card or bar communicates better

## Final Preference Ladder For Ambiguous Requests

When the user simply asks for “a chart” and the data could fit several families, prefer:

1. `line` for time or sequence
2. `bar` for categories or ranking
3. `area` only if filled magnitude matters
4. `dualAxis` only if a second axis is justified
5. `pie` only for simple low-cardinality composition
6. `scatter` for numeric relationship
7. `funnel` for staged process
8. `radar` for profile comparison
9. `gauge` for one KPI status

Inside each family, choose the least decorative variant that still communicates the intent clearly.
