---
name: comparative-synthesis
description: Compare and synthesize findings across multiple completed DeepScan reports. Use when the user wants cross-run analysis, trend comparison, or a unified summary from several research sessions.
---

# Comparative Synthesis

Use this skill when the user wants to compare, contrast, or synthesize findings across multiple completed DeepScan runs rather than monitor a single active job.

## Workflow

1. Use `summarize_evidence` to pull cross-report summaries from the user's DeepScan history.
2. If the user references specific runs, use `get_deepscan_report` for each to get full report data.
3. Identify overlapping papers, conflicting findings, and complementary themes across runs.
4. Use `run_python_plot` to visualize comparisons when the data supports it.

## Output Style

Structure the synthesis around:

- **Common ground** — papers, methods, or findings that appear across multiple runs
- **Divergences** — where different runs reached different conclusions or surfaced different literature
- **Gaps** — topics or questions that no run adequately covered
- **Trends** — temporal patterns, emerging methods, or shifting consensus visible across runs

Keep sections short and reference specific papers by title and year.

## Tool Guidance

### Use `summarize_evidence`

Call this first. It aggregates across the user's stored DeepScan history and is the fastest way to get a cross-run view.

Use for:

- "What do my recent DeepScans say about X?"
- "Summarize everything I've researched on topic Y"
- "Compare findings across my last three runs"

### Use `get_deepscan_report`

Call for specific runs when the user wants:

- side-by-side comparison of two named runs
- detailed data from a particular session that `summarize_evidence` condensed too aggressively

### Use `run_python_plot`

Use after you have structured data from reports. Good comparison plots include:

- paper overlap Venn or bar chart across runs
- citation count distributions side by side
- publication year histograms per run
- venue frequency comparison
- topic/method co-occurrence heatmap

Only plot when there is enough data to be meaningful. Say so if the data is too sparse.

### Do NOT use

- `run_deepscan` — this skill synthesizes completed runs, not starts new ones
- `search_literature` — use the existing DeepScan data, not new searches

## Examples

- User asks: "Compare my DeepScan on transformer efficiency with the one on model distillation."
- User asks: "What themes keep showing up across all my recent research sessions?"
- User asks: "Plot the publication year distribution from my last two DeepScans side by side."
- User asks: "Synthesize everything I've researched on protein folding this month."
