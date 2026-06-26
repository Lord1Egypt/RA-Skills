---
name: deepscan-monitor
description: Run and monitor PapersFlow DeepScan jobs. Use when the user wants long-running research progress, intermediate findings, final reports, or plotting from a completed run.
---

# DeepScan Monitor

Use this skill when the user wants Claude to manage a longer-running PapersFlow research workflow instead of a single search call.

## Workflow

1. Use `run_deepscan` to start the job.
2. Immediately tell the user that the run is asynchronous.
3. Poll with `get_deepscan_live_snapshot` for the best live view of:
   - progress
   - status message
   - checkpoint state
   - top papers
   - partial summary
   - key findings
4. Fall back to `get_deepscan_status` if the user only wants lightweight progress checks.
5. Once `finalReportAvailable` is true or the run is completed, call `get_deepscan_report`.
6. Use `summarize_evidence` when the user wants a cross-report summary from stored DeepScan history.
7. Use `run_python_plot` only after you have stable report data worth plotting.

## Important Behavior

- Do not imply the MCP server will push completion notifications into Claude automatically.
- Poll deliberately and explain that the run is being checked.
- Prefer `get_deepscan_live_snapshot` over `get_deepscan_status` when the user wants richer live information.
- If a report is not ready yet, say that clearly and keep the next action obvious.

## Progress Update Style

When a run is still active, summarize:

- current status
- progress percentage
- current stage or status message
- any checkpoint question
- notable live papers
- key findings if available

Keep updates brief unless the user asks for more detail.

## Plotting Guidance

Use `run_python_plot` only for meaningful visualizations after you have stable report outputs, for example:

- papers by year
- citation distribution
- venue distribution
- grouped comparison across a small number of finished runs

Do not generate plots for sparse or obviously low-quality data without saying so.

## Examples

- User asks: "Run a DeepScan on evaluation benchmarks for agentic retrieval systems and keep me posted."
- User asks: "Check how my DeepScan is progressing and tell me the key findings so far."
- User asks: "The run is finished, summarize the final report and plot papers by year."
- User asks: "Summarize the evidence from my recent DeepScan reports on protein structure prediction."
