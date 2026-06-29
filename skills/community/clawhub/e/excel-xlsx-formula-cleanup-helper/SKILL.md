---
name: excel-xlsx-formula-cleanup-helper
description: Diagnose and fix Microsoft Excel XLSX workbook issues involving formulas, named ranges, Power Query refreshes, pivot tables, VBA/macro preservation, workbook corruption, and repeatable data cleanup. Use when Codex needs to inspect or automate Excel files while preserving formulas, workbook structure, formatting, and business logic.
---

# Excel XLSX Formula Cleanup

Use this skill for spreadsheet repair and automation tasks where correctness matters more than simply rewriting cells. Treat an `.xlsx` workbook as a structured package with formulas, styles, relationships, cached values, tables, queries, pivots, and sometimes macros.

## Workflow

1. Clarify the workbook goal: fix broken formulas, clean imported data, preserve macros, refresh reporting logic, repair corruption, or generate a reusable workflow.
2. Protect the workbook. Work on a copy and avoid destructive recalculation or macro removal unless requested.
3. Choose the right inspection path:
   - Use `openpyxl` for formulas, worksheets, styles, dimensions, tables, data validation, conditional formatting, and charts it supports.
   - Treat `.xlsm` files carefully; preserve the VBA project with library support or package-level copying.
   - Inspect ZIP/OOXML parts for workbook relationships, external links, pivot caches, slicers, Power Query metadata, and unsupported structures.
4. Map each problem to a workbook layer: formula text, named range, table reference, external link, query connection, pivot cache, style, merged cell, or hidden sheet.
5. Make minimal repairs and keep formulas as formulas. Do not replace formulas with stale cached values unless the user asks for a static export.
6. Validate formulas and shape:
   - Confirm worksheet names, table names, named ranges, and formulas still point to valid ranges.
   - Check row/column counts, date and number formats, hidden sheets, filters, and merged cells.
   - Note when a desktop Excel recalculation or Power Query refresh is still required.

## Common Fix Patterns

- **Broken formulas**: trace sheet names, structured references, named ranges, separators, and external workbook links before editing formula strings.
- **Power Query refresh issues**: inspect connection definitions and query metadata; explain which parts require Excel desktop or Power BI tooling.
- **Pivot table drift**: preserve pivot caches where possible and warn when Python libraries cannot safely rebuild them.
- **VBA preservation**: keep `.xlsm` package parts intact; never save through a path that drops macros unless producing a macro-free copy is the goal.
- **Data cleanup**: normalize values in staging sheets or tables, then keep reporting formulas and dashboards stable.

## Outputs

Provide:

- A workbook diagnosis tied to specific sheets, ranges, formulas, or package parts.
- A safe repair or automation plan, plus code changes when requested.
- A validation checklist covering formulas, ranges, tables, pivots, macros, and expected recalculation.

Read `references/requirement-plan.md` only when the original demand evidence is needed.
