---
name: data-analysis-reporting
description: Turn raw business data (CSV, SQLite, spreadsheets, pasted tables) into clear analytical summaries, trend analysis, and actionable reports for small business operators, analysts, and decision-makers. Asks clarifying questions first, delivers plain-language insights before numbers, and labels statistical confidence explicitly. Does not provide financial advice or present projections as fact.
---

# Data Analysis & Reporting

Turn raw business data into plain-language insights, trend analysis, and actionable reports. Think sharp junior analyst, not statistics engine.

## Trigger conditions

Activate this skill when the user:
- Pastes or uploads tabular data (CSV, markdown table, tab-separated, pipe-delimited)
- Asks to analyze, summarize, or report on business data
- Asks about metrics, KPIs, trends, or performance from a dataset
- Provides a SQLite database and asks questions about it
- Asks for a report, executive summary, or data briefing
- Asks to compare periods, segments, or actuals vs. targets

Do NOT activate when:
- The user wants to build a dashboard or visualization tool (suggest BI tools)
- The user needs real-time streaming analytics
- The user asks for financial advice, investment recommendations, or tax guidance
- The data is code/logs/system metrics (suggest observability tools instead)

## Work the request in this order

1. **Clarify the question** — before touching the data, understand what the user needs to know and why. Ask up to 3 clarifying questions:
   - "What decision does this analysis need to support?"
   - "What time period or comparison matters most?"
   - "Who is the audience for this report?"
   If the user provides clear context, skip to step 2.

2. **Ingest and validate** — parse the data, detect column types, run quality checks
   - Auto-detect: column types (numeric, date, categorical, text)
   - Flag: missing values, outliers, formatting inconsistencies, duplicate rows
   - Report data quality issues before proceeding, not after
   - If data quality is poor enough to undermine analysis, say so and recommend fixes

3. **Propose an analysis plan** — tell the user what you intend to analyze and why, before doing it
   - Name the specific analyses (e.g., "monthly revenue trend with MoM growth rates")
   - Explain what each analysis will reveal relative to their question
   - Let the user adjust before you proceed

4. **Execute the analysis** — run the agreed analyses
   - Summary statistics for numeric columns
   - Trend identification with direction, magnitude, and acceleration
   - Comparisons (period-over-period, segment, actual vs. target) as relevant
   - Distribution and concentration analysis where useful
   - Correlation spotting between metrics
   - Cohort analysis when data supports grouping

5. **Translate to insights** — convert numbers into plain-language findings
   - Lead with what matters, not what was calculated
   - Rank findings by business impact, not statistical significance
   - Connect each finding to the user's original question
   - Flag surprising results and explain why they are surprising

6. **Deliver the report** — structured output following the default format below
   - Include data quality notes inline
   - Label confidence on every statistical claim
   - Suggest follow-up questions the user hasn't asked

7. **Offer next steps** — what deeper analysis could be useful, what data would improve the picture

## Default output structure

Use this structure unless the user clearly wants a different format:

1. **Executive summary** — 3-5 bullet points answering the user's core question in plain language. No jargon. A busy operator should be able to read this section alone and know what matters.

2. **Data quality notes** — what came in, what was cleaned, what to watch out for. Include row/column counts, date range covered, any exclusions made and why.

3. **Key findings** — the substantive analysis, organized by business relevance not by metric. Each finding should follow the pattern:
   - What the data shows (the fact)
   - Why it matters (the implication)
   - How confident we are (the evidence quality)

4. **Trend analysis** — time-series patterns with:
   - Direction and magnitude of change
   - Comparison to prior period or baseline
   - Acceleration or deceleration signals
   - Seasonal or cyclical patterns if detectable

5. **Comparisons** — if the data supports comparison (segments, periods, targets):
   - Side-by-side with explicit metrics
   - Performance gaps highlighted
   - Context for why gaps exist (if inferrable from data)

6. **Watch items** — things that aren't problems yet but could become problems:
   - Emerging negative trends
   - Metrics approaching thresholds
   - Data quality issues that could mask real signals

7. **Recommended actions** — 3 concrete next steps:
   - One action justified by the data right now
   - One thing to monitor or investigate further
   - One data improvement that would sharpen future analysis

8. **Methodology notes** — what was calculated, how, and what assumptions were made. Brief but sufficient for someone to question the analysis.

## Analysis depth calibration

Match analysis depth to data quality and volume:

| Data quality | Row count | Depth |
|---|---|---|
| Clean, complete | >1,000 | Full analysis with statistical tests, confidence intervals, correlation |
| Clean, complete | 100-1,000 | Full analysis, note limited sample for statistical claims |
| Clean, complete | <100 | Summary stats and directional trends only, flag small-sample risk |
| Moderate gaps | Any | Analyze what's clean, quantify the gap, note impact on conclusions |
| Poor quality | Any | Data quality report first, limited directional analysis with heavy caveats |

Do not apply sophisticated statistical methods to data that can't support them. 3 months of revenue data does not justify a seasonal decomposition.

## Confidence labeling

Every analytical claim gets a confidence indicator:

- **High confidence** — large sample, clean data, clear pattern, well-understood metric
- **Moderate confidence** — adequate sample, minor data issues, pattern present but could shift
- **Low confidence** — small sample, data quality concerns, pattern is directional at best
- **Flagged** — interesting signal but insufficient evidence to draw conclusions; noted for monitoring

When confidence is low, say what additional data would raise it.

## Number formatting

- Currency: match the user's format or default to $X,XXX.XX
- Percentages: one decimal place for rates (5.2%), whole numbers for large changes (up 23%)
- Large numbers: use K/M/B shorthand with one decimal ($1.2M, 45.3K users)
- Growth rates: always specify the comparison basis (MoM, QoQ, YoY) and the absolute numbers behind the percentage
- Do not present a percentage without context: "Revenue grew 15% MoM ($42K to $48.3K)" not just "Revenue grew 15%"

## Handling common business metrics

When the user's data contains standard business metrics, calculate them consistently:

Read `references/business-metrics.md` for definitions, formulas, and interpretation guidance for:
- MRR / ARR and expansion/contraction/churn components
- Customer churn rate (logo and revenue)
- CAC, LTV, and LTV:CAC ratio
- Gross and net margins
- Growth rates (MoM, QoQ, YoY, CAGR)
- Unit economics

Always show the formula used when presenting a calculated metric. Different businesses define "churn" differently — confirm the user's definition before calculating.

## Data quality checks

Run these checks on every dataset before analysis:

Read `references/data-quality-checks.md` for the full checklist covering:
- Completeness (missing values by column, row completeness rate)
- Consistency (date format uniformity, categorical value normalization)
- Validity (values within expected ranges, negative amounts where unexpected)
- Uniqueness (duplicate detection, key column analysis)
- Timeliness (date range coverage, gap detection)
- Outlier flagging (statistical and domain-based)

Report data quality findings before analysis results. If quality issues materially affect conclusions, say so at the top of the executive summary.

## Report structure templates

Read `references/report-templates.md` for pre-built structures for common report types:
- Executive summary report (1-page, for leadership)
- Detailed analysis report (full findings with methodology)
- Comparison report (A vs. B with decision framework)
- Trend report (time-series focused with forecasting context)
- Health check report (KPI dashboard in text form)

Use the appropriate template when the user's request clearly maps to one. Default to the standard output structure when it doesn't.

## Sparse-data and minimal-signal analysis

When the dataset is too small or too noisy for robust analysis:

1. **State the limitation plainly** — "This dataset has 12 rows covering 3 months. Statistical analysis is limited."
2. **Provide what's possible** — totals, simple averages, directional observations
3. **Name what would be needed** — "6+ months of data would allow trend detection; 100+ transactions would support segment analysis"
4. **One observation worth monitoring** — the single most interesting signal, clearly labeled as preliminary
5. **Do not pad** — a short, honest report is better than a long, hedged one

## No-data gate

When the user asks for analysis but provides no data:

1. Ask what data they have available and in what format
2. Suggest the minimum viable dataset for the analysis they want
3. Offer to help them structure their data for analysis
4. Provide a sample template they can populate

Do not generate fictional analysis or example reports unless the user explicitly asks for a template or demo.

## Multi-dataset analysis

When the user provides multiple related datasets:

- Identify join keys and relationship types before merging
- Report any orphaned records (rows that don't match across datasets)
- Be explicit about which dataset each finding comes from
- Note where merged analysis adds insight vs. where datasets should be analyzed separately

## Boundaries

- **No financial advice.** Analyze data and identify patterns. Do not recommend investments, tax strategies, or financial products.
- **No projections as fact.** Forecasts must be labeled with assumptions, methodology, and confidence range. "If current trends continue" not "revenue will be."
- **Statistical confidence labeling.** Small samples and high variance get explicit warnings. Do not present a 3-point trend with the same confidence as a 300-point trend.
- **Inference/fact separation.** Data points are facts. Patterns derived from them are inferences. Recommendations are opinions. Label each.
- **No private database access without explicit user setup.** Work on data the user provides.
- **PII detection and exclusion.** Scan every dataset for columns containing personally identifiable information (SSN, email addresses, phone numbers, physical addresses, government IDs, dates of birth). When PII is detected:
  1. Immediately flag the PII columns prominently at the top of the output, before any analysis.
  2. Exclude all PII columns from analysis — do not compute statistics on, reference values from, or reproduce any PII in the report.
  3. Proceed with analysis on non-PII columns only (e.g., purchase totals, visit counts, plan types).
  4. Recommend the user remove PII columns before sharing data for analysis.
  5. Never quote, echo, or reference specific PII values (e.g., do not include an SSN in a "data quality finding").
- **No audit-grade output.** Reports are analytical aids, not auditable financial statements.
- **No data fabrication.** Never generate synthetic data to fill gaps without explicit user request and clear labeling.
