# excel-wps-table-diagnosis

Read table structure first, then suggest practical Excel/WPS formulas and cleanup workflows.

先看表结构，再给出更稳妥的 Excel/WPS 处理建议。

## Overview

Most spreadsheet problems are not really formula problems.

Usually the harder part is figuring out what the table is trying to do, what is broken, and what should be cleaned before anyone reaches for a nested formula that nobody wants to maintain next week.

This repository is built around a simple workflow:

- inspect table structure
- identify likely data issues
- choose the next sensible step
- recommend formulas that are more likely to work in both Excel and WPS
- provide simpler fallback approaches when needed

The focus is ordinary office spreadsheet work: messy columns, awkward lookups, summary tables, and the kind of formula trouble that usually appears five minutes before someone needs the file.

## 中文说明

这个项目主要是整理一套更稳妥的 Excel/WPS 表格处理方法。

重点不是“函数越多越好”，而是先判断表结构，再决定该清洗、匹配、汇总，还是该少写点花哨公式，给未来的自己留条活路。

如果一件事更适合用辅助列、分列、筛选或者透视表来做，这里会优先选那些更省心的办法。

## Quick Start

Start with these files:

- `README.md`
- `SKILL.md`
- `WORKFLOW.md`
- `examples/README.md`
- `docs/quick-start.md`

Use the current draft like this:

1. Prepare table headers and a few sample rows.
2. Describe the task in plain language.
3. Prefer the safest Excel/WPS-friendly approach over the flashiest one.

## Use As A Skill

To use this repository as a Codex-style skill:

1. Place this folder under your skill directory.
2. Keep `SKILL.md` at the repository root.
3. Keep `agents/openai.yaml` in place so the skill has UI metadata.
4. Invoke it with a table header, a few sample rows, or a direct spreadsheet task.

Typical prompts:

- `Use $excel-wps-table-diagnosis to inspect this table and tell me what should be cleaned first.`
- `Use $excel-wps-table-diagnosis to suggest a WPS-friendly lookup formula for these two sheets.`
- `Use $excel-wps-table-diagnosis to troubleshoot this formula and suggest a safer fallback.`

## 用法

可以直接按下面这种方式使用：

1. 贴出表头和几行样例数据
2. 说明你要做什么，或者直接说“先帮我看这张表”
3. 优先采用兼容 WPS 和 Excel 的稳妥方案

比较适合的提问方式：

- “先看一下这张表，告诉我应该先处理什么”
- “这两张表按编号怎么匹配，WPS 里也能用”
- “这列日期格式很乱，先怎么清洗比较稳”
- “这个公式为什么会报错，有没有更稳的写法”

## What This Project Focuses On

- Table diagnosis from headers and sample rows
- Formula suggestions for Excel and WPS
- Data cleaning guidance
- Lookup and matching workflows
- Summarization and categorization
- Common formula error troubleshooting

## Why I Made This

A lot of spreadsheet helpers jump straight to formulas.

In real work, that is usually not enough. Before choosing a formula, it helps to know:

- which columns are usable
- whether the data is clean
- whether dates and text formats are consistent
- whether the task is better solved with formulas, helper columns, split text, filters, or a pivot table

That part is not glamorous, but it is usually the part that saves the most time.

## Typical Use Cases

- inspect a table and suggest what to clean first
- recommend a formula that works in WPS
- match two sheets by ID or name
- detect blanks, duplicates, and inconsistent formats
- suggest how to summarize a department, sales, or status table
- troubleshoot common spreadsheet formula errors

## Project Files

- `SKILL.md`: the skill entry file used by the skill runner
- `WORKFLOW.md`: workflow notes and handling rules
- `examples/table-diagnosis.md`: sample diagnosis workflow
- `examples/sheet-match.md`: sample sheet matching workflow
- `examples/text-cleanup.md`: sample text cleanup workflow
- `examples/approval-flow.md`: diagnosis first, execution after approval
- `examples/README.md`: example index
- `docs/quick-start.md`: short orientation for first-time visitors
- `docs/use-cases.md`: use-case overview
- `docs/roadmap.md`: project direction
- `CONTRIBUTING.md`: contribution notes
- `CHANGELOG.md`: release history

## Examples

### 1. Diagnose a Messy Table

Input:

`Look at this table and tell me what should be cleaned first.`

Expected output:

- identify blank cells in key columns
- flag duplicate identifiers
- detect mixed date formats
- suggest a practical cleanup order

### 2. Match Two Sheets

Input:

`I need to match Sheet A and Sheet B by customer ID.`

Expected output:

- identify the matching key
- suggest a lookup formula
- provide a WPS-friendly alternative if needed
- recommend a helper-column approach if it is more stable

### 3. Clean a Text Column

Input:

`This column has extra spaces and inconsistent formatting.`

Expected output:

- suggest suitable text functions
- explain whether one formula is enough
- prefer step-by-step cleanup when it is easier to maintain

## Design Principles

- Diagnose before suggesting formulas
- Prefer simple and maintainable solutions
- Consider Excel/WPS compatibility early
- Use helper columns when they make the result more reliable
- Do not force formulas when built-in spreadsheet tools are a better fit

## What This Project Is Not

- not a full office automation toolkit
- not a chart or formatting generator
- not a function encyclopedia with no table context

## Intended Users

- people who work with Excel or WPS regularly
- users who know the task they want to finish, but not the best formula
- beginners who want practical spreadsheet guidance
- anyone dealing with messy office tables

## Repository Notes

- current focus: table diagnosis, formula suggestions, and cleanup workflows
- compatibility is considered early for both Excel and WPS
- this repository is intentionally kept focused on practical spreadsheet tasks

## Roadmap

- better diagnosis from sample data
- stronger Excel/WPS compatibility rules
- formula error repair suggestions
- multi-table merge and reconciliation support
- report-oriented table processing suggestions

## Known Problems

- compatibility behavior still needs more real-world verification across different Excel and WPS versions
- the current examples are small and clean, and still need more messy office-table cases
- some workflows are easier to describe than to standardize, especially when the source table structure is inconsistent
- a few sections still sound slightly more organized than the average spreadsheet emergency really deserves

## Planned Improvements

- add more examples based on common office tables
- document safer fallback workflows for older spreadsheet environments
- improve guidance for messy date, text, and lookup columns
- make the workflow notes easier to scan for first-time users

## Current Status

This repository is still in an early public draft stage. The main structure is in place, but the real work now is collecting better edge cases, simplifying the wording, and making sure the recommendations hold up outside neat toy examples.

## License

MIT
