# ExcelDashboard AI Report Outline Format

Use this reference to prepare `create_report.outline`. It is based on the project's report Skill outline format and Default layout specifications. It defines page syntax and available layouts, rather than prescribing a fixed number or sequence of analysis pages. Choose pages according to the report goal, audience, and verified data.

## Document and Page Syntax

Start the outline with a `# ` main title, followed by a nonempty `> ` subtitle and a `<!-- meta ... -->` block. Start each page with a `## ` heading and separate pages with `---`. Set `meta.pages` to the actual number of `## ` page headings. Do not add page numbers to page titles.

```markdown
# Report title

> Scope, subject, or central topic

<!-- meta
goal: Goal of this report
skill: Report type
style: default
lang: business
pages: Actual page count
audience: Intended audience
date_range: Actual start and end dates
generated: Generation date
-->

---

## Page title
`layout: English layout name from the table below`
`layout_intent: Reason for selecting this layout`
`layout_slots: Slot names defined for this layout`

- [slot: A slot name declared above] Component title [chart: line]
  | Actual time field | Actual metric field |
  |---|---|
  | Actual period | Actual value and unit |
  - [hint: Annotation supported by the actual data]
```

This example illustrates syntax, not a complete report template. Replace all explanatory text with actual content before submission; do not leave placeholders. Write page-level `layout`, `layout_intent`, and `layout_slots` using the single-line backtick format above. Each main content bullet's `[slot: ...]` must appear in `layout_slots`. Match the number of bullets to the selected layout. Layouts without main content slots must not include content bullets. For `[text]` slots, provide final copy; for `[smart_layout]`, provide structured content; for `[chart: ...]`, provide verified data that can be plotted.

Include a data overview, data definitions, analysis, and a closing decision. Use "Data overview" on page 1 to present the core findings and "Data definitions" on page 2 to explain sources, scope, definitions, and trustworthiness. Use the final page to consolidate findings and actions. Determine the number, sequence, titles, and layouts of intermediate analysis pages from the analysis itself. Prefer conclusion-based titles for analysis pages.

## Layout Selection

Write the layout name in `layout:`. One bullet represents one main content slot, not an additional chart. Use meaningful slot names such as `main-chart`, `left-chart`, `right-chart`, `spec-body`, and `takeaways`; avoid generic names such as `slot1`.

| Layout | Appropriate content and structure | Main content slots |
|---|---|---:|
| `KPI Ledger` | Core metric overview with verified KPIs and three lower-section conclusions: evidence, attribution, and recommendation. Each KPI includes its name, current value, and description. | 1 |
| `Specification Sheet` | Sources, dates, metric definitions, units, and limitations. Use a two-column specification table with at most 5 body rows; put additional details in footnotes. | 1 |
| `Single-Chart Insight` | One main chart supporting one conclusion, with three lines for evidence, attribution, and recommendation. Use `chart`. | 1 |
| `Dual-Chart Comparison` | Two complementary charts on the same topic, with two lines for evidence and risk. Place one `chart` on each side. | 2 |
| `Dual-Track Comparison` | A/B or before-and-after comparison using matching dimensions and definitions. Mirror the factual panels, each with a main metric and brief supporting facts. | 2 |
| `Closing Statement` | Final-page findings and priority actions in two columns, with 2-3 items each and no more than 3. Number findings 01-03 and actions P1-P3; include a "Goal:" line at the bottom. | 1 |
| `Horizontal Timeline` | A linear process with 4-7 steps. Use one timeline component; each node includes its number, key value or status, and stage name. | 1 |
| `Feedback Loop` | A closed cycle with 3-5 steps. Do not use it for a linear process. | 1 |
| `Three Forces Cards` | Three comparable drivers or growth opportunities, each with a short title and one explanatory sentence. | 3 |
| `Three-Column Argument` | A progressive argument across three columns, each supported by facts or data. Use `chart`. | 3 |
| `Four-Column Features` | Four equally weighted features or actions with matching structure. | 4 |
| `Six-Cell Definition` | Six equally weighted definitions, snapshots, or metrics, each with a short title and description. | 6 |
| `Micro-Card Briefing` | Six short observations or tips in a 3-by-2 grid. Each item includes a brief conclusion and footnote. | 6 |
| `Matrix Overview` | An overview of 8-12 comparable items, with a total or overall assessment below. | 8-12 |
| `System Architecture` | A strictly nested three-layer Core / Middle / Outer architecture. Do not use it for an ordinary list. | 1 |
| `Image Hero` | One real image used as evidence, with an explanation or supporting KPI. Do not use it without an actual image. | 1 |
| `Minimal Statement` | A single central claim or section opening. Do not use it for data charts. | 0 |
| `Dot-Matrix Statement` | A qualitative statement or section transition with brief anchor text. Do not use it for data charts. | 0 |
| `Statement Banner` | An intermediate claim with supporting explanation. Do not use it as a substitute for the final decision page. | 0-1 |

For analysis pages with verified quantitative data, consider `Single-Chart Insight` or `Dual-Chart Comparison` first. Choose another layout when the content does not fit. Content in multiple slots should complement rather than repeat the same data. Use `chart` for chart-based layouts and prefer `smart_layout` for processes, matrices, and comparisons. Do not invent metrics, images, or items to fill a layout.

## Charts and Values

Supported chart types are `line`, `bar`, `column`, `grouped_bar`, `stacked_bar`, `grouped_column`, `stacked_column`, `pie`, `donut`, `combo`, `scatter`, and `bubble`. Immediately follow each `[chart: ...]` bullet with a Markdown table whose headers use actual business field names. Ordinary charts use a dimension and metric; grouped charts add a series field; `combo` uses separate columns for the bar and line metrics; scatter charts use X/Y; bubble charts add size. Table-based `smart_layout` content also requires column headers. Preserve units, dates, currencies, and percentage definitions in the data rows. Include only aggregated plotting data, not raw detail records.

After a chart's data rows, include a meaningful `[hint: ...]` to annotate a target line, average, unusual period, or important series or category. Do not add hints to `smart_layout`. Do not present unverified causes as facts. Explain missing data and conflicting definitions on the definitions page or the relevant analysis page. Before submission, verify that page counts, slot counts, chart fields, values, and conclusions are consistent.
