---
name: claw-trace
description: "Trace and debug a single OpenClaw conversation session. Use when you need to analyze openclaw logs, correlate them with the current session context, inspect workflow steps, summarize module activity, or produce a structured trace report."
---

# ClawTrace

ClawTrace analyzes one OpenClaw session at a time. It combines OpenClaw logs and current session context to reconstruct steps, summarize module activity, and generate a Markdown trace report.

## When to Use

- Inspect one OpenClaw session end to end
- Explain slow, failed, retried, or noisy runs
- Generate a structured session trace report
- Produce evidence-based optimization suggestions

## Core Rules

1. Always analyze one session at a time.
2. Always use both data sources before writing the report:
   - `openclaw logs --json --local-time --no-color`
   - current session context
3. Never invent missing values. Use `Not available`, `Estimated`, or `Unknown` when needed.
4. Prefer exact identifiers and timestamps over inferred values.
5. Write the report in the user's language unless the user asks for another language.
6. If the user's chat channel supports file sending, prefer delivering the report as a Markdown file; otherwise reply directly in chat using the same report structure.
7. Do not output raw logs, raw JSON, or verbatim log lines in the final report.

## Inputs

### Logs

Use JSON logs so events can be parsed reliably.

```bash
openclaw logs --json --local-time --no-color
```

- `--limit <n>` to restrict line count
- `--max-bytes <n>` to avoid huge tails
- `--interval <ms>` if polling is needed
- `--timeout <ms>` if waiting for fresh output
- `--expect-final` only when the task requires waiting for the final response

### Context

Use current session context to identify the target run and recover information not explicit in logs, such as request scope, recent responses, session clues, and context-size indicators.

## Analysis Workflow

### 1: Identify the Target Session

- `sessionId`
- `sessionKey`
- `runId`
- channel
- nearby timestamps
- current-session clues

If multiple runs exist in the same session, prefer the latest completed run unless the user clearly points to a different one.

### 2: Extract Key Events

Extract session, prompt, agent, tool, lane, context, warning, error, and related gateway events, and capture the key fields needed for analysis such as time, level, module, sessionID, runID, tool, toolCallID, duration, summary, and outcome.

### 3: Reconstruct Steps

Convert events into ordered steps such as `queue`, `prompt`, `agent`, `tool`, `gateway`, `context`, `warn`, `error`, and `done`.

When possible, pair start and end events to compute duration. If only one side exists, mark duration as `Unknown`.

### 4: Compute Metrics

- Session ID
- Session Key
- Run ID
- Start and End Time
- Total Duration
- Step Count
- Tool Count
- Warning Count
- Error Count
- Module Count
- Context Indicators
- Token Indicators

Use exact values when present. Otherwise mark them as `Estimated` or `Not available`.

### 5: Produce Optimization Suggestions

Only give evidence-based suggestions, such as duplicate tool calls, oversized context, repeated warnings, long tool durations, queue delays, or excessive gateway noise.

If there is no clear optimization opportunity, say that no evidence-backed optimization was found.

## Output Format

If file sending is supported in the user's chat channel, prefer a Markdown file such as `clawtrace-run-<runId>.md` or `clawtrace-report-<timestamp>.md`; otherwise return the same structure directly in chat.

Example Markdown output:

```md
# ClawTrace Report

## Overview
Scope: RunId=<runId> or Message=<message>
Start: <start>
End: <end>
Total Tokens Used: <tokens>
Total Duration: <total_duration> (seconds)
Total Steps: <steps_count> 
Tools Used: <tools_list> (separated by comma)
Warnings: <warn_count>
Errors: <error_count>
Generated at: <time>

Suggestions:
- <evidence-based suggestion>
- <evidence-based suggestion>

## Modules

| Module | Success | Warn | Error | Total Steps | Avg Time Cost | Notes |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| <module> | <success> | <warn> | <error> | <total_steps> | <avg_time_cost> | <notes> |

## Steps

| Step | Time | Type | Module | Action | Duration | Result | Notes |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| 1 | <time> | <type> | <module> | <action> | <duration> | <result> | <notes> |
| 2 | <time> | <type> | <module> | <action> | <duration> | <result> | <notes> |
```

Sort the `Steps` table strictly by time in ascending order. Use `Success`, `Failed`, `Warning`, or `Unknown` for `Result`, and do not include raw logs or raw JSON.

### Partial Data

If the logs contain `Log tail truncated (increase --max-bytes).`, explicitly state that the report is based on partial logs.

Do not fabricate missing steps. Mark uncertain durations and metrics as `Unknown`, `Estimated`, or `Not available`.

### Noise Filtering

Ignore unrelated background noise such as cron timers, heartbeats, and unrelated channel traffic unless they materially affect the target session.

## Quality Standard

The report should quickly show which session was analyzed, how long it took, what modules and steps were involved, where time went, what warnings or failures happened, and what to optimize next. If evidence is weak, say so clearly.