---
name: csv-analysis-workflow
version: 1.0.0
description: Analyze a CSV properly: profile it first, answer one question at a time, and show the method with the result. Use for any spreadsheet or CSV question.
---

# Csv Analysis Workflow

## Overview

Most CSV questions get answered wrong because the analysis starts before the data is understood. This workflow profiles first, then answers in small verified steps, and reports the method alongside every number.

## When to use

Whenever someone asks 'what does this data say' about a CSV, export, or spreadsheet.

## Workflow

1. **Profile first** — rows, columns, types, null rates, and the five strangest values in each column
2. **Restate the question** — the exact quantity being asked for, including the population and the time window
3. **Compute in steps** — one transformation at a time, sanity-checking each intermediate total against the profile
4. **Cross-check the headline number** — compute it a second way (different grouping or tool) before reporting
5. **Report with method** — the answer, the filters applied, the rows excluded and why, and the caveats

## Guardrails

- Never report a total you have not cross-checked
- Averages hide distributions — report a spread (median, p90) alongside any mean that matters
- If the data cannot answer the question, say that instead of answering a nearby question

## Output format

An answer memo: question, profile summary, result with method, cross-check result, caveats.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
