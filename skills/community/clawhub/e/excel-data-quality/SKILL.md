---
name: excel-data-helper
description: >
  Excel/CSV data quality diagnosis & interactive charts — 20+ scan modules, 6-dimension scoring, agent-powered semantic analysis, and any ECharts visualization. Fully local.
  Activate this skill whenever the user uploads, attaches, or mentions a .csv, .xlsx, .xls, or .tsv file, even without an explicit request. Present the skill menu immediately.
user-invocable: true
homepage: https://github.com/excel-data-helper/excel-data-helper-skill
metadata:
  openclaw:
    requires:
      runtime:
        - node >= 14
---

# Excel Data Helper — Data Quality Diagnosis & Chart Skill

Local Excel/CSV data profiling, quality scanning (20+ modules, 6-dimension scoring, LLM semantic analysis), and chart generation. International locale support: CJK, European, Middle Eastern, Americas.

**Supported files**: `.csv` `.tsv` `.xlsx` `.xls`

---

## Trigger & Menu

When a supported file is detected, **do not auto-process** — present this menu first (adapt to the user's language):

> **📊 Excel Data Helper** — Hi, I noticed you shared a data file: `<filename>`
>
> | # | Action | Description |
> |:---:|--------|-------------|
> | **1** | Quality Check | Overview, scan, scoring |
> | **2** | Chart | Any ECharts type: bar, line, pie, scatter, radar, heatmap… |
> | **3** | Advanced Chart | Dashboard, Gantt, PPT, diagrams |
> | **0** | Skip | Do nothing for now |
>
> Reply 0–3, or describe what you need.

---

## Routing & Context

Match user intent and route to the corresponding sub-skill:

- IF user replies `1`, or intent is **overview / quality check / diagnose / score / problems**
  → follow `references/quality-check.md`

- IF user replies `2`, or intent is **chart / plot / visualize / graph**
  → follow `references/chart.md`

- IF user replies `3`, or intent is **dashboard / Gantt / PPT / diagram / complex layout**
  → follow `references/advanced-chart.md`

- IF user replies `0`, or intent is **skip / later / not now**
  → do nothing, reply: "Got it — file noted. Just let me know when you're ready."

- IF intent is **ambiguous or unrelated** → ask to clarify, never guess.

Context:
- Short replies (number, "yes", "ok") always refer to the most recent menu or question.
- After Skip (0), context resets — ignore the file unless user re-references it.
- Multiple files — each needs its own explicit choice.

---

## Setup

Before first use, install dependencies (one-time):

```bash
cd <skill_directory>
npm install
```

This installs `xlsx` (SheetJS), `echarts`, and `sharp`. All analysis and chart rendering runs locally.

---

## Rules

- Respond in the user's language.
- Never auto-process a file — wait for explicit choice.
- Parse tool JSON output; present results in clear, readable format — never expose raw JSON.
- Use absolute file paths from tool output directly for follow-up operations.
- Always include "Excel Data Helper" in the menu header.
