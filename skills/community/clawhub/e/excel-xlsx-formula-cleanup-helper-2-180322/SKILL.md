---
name: excel-xlsx-formula-cleanup-helper-2
description: Build and troubleshoot cross-Office automation pipelines that move content between Word, Excel, and PowerPoint using Open XML, VBA, python-docx, openpyxl, python-pptx, templates, and batch conversion. Use when Codex needs to coordinate DOCX, XLSX, and PPTX workflows while preserving Office file relationships and formatting.
---

# Office Open XML Automation Helper

Use this skill when the task crosses Office file types: extract Word tables into Excel, turn Excel results into PowerPoint slides, populate Word reports from spreadsheets, batch-convert Office files, or coordinate DOCX/XLSX/PPTX templates.

## Workflow

1. Define the pipeline: source files, destination files, templates, generated artifacts, batch size, and success criteria.
2. Classify each operation:
   - DOCX text, tables, styles, comments, headers, content controls.
   - XLSX worksheets, tables, formulas, named ranges, charts, pivots, macros.
   - PPTX slide masters, layouts, placeholders, charts, media, speaker notes.
3. Preserve source packages. Work on copies and keep an audit trail of inputs, outputs, and record IDs.
4. Choose the safest layer for each step:
   - `python-docx` for supported Word document content.
   - `openpyxl` for supported Excel workbook structure.
   - `python-pptx` for supported slide content and basic charts.
   - Direct Open XML edits for relationships, unsupported features, and preserving package parts.
   - VBA or Office desktop automation only when live Office behavior is required, such as field updates, Power Query refresh, PDF export, or chart rendering fidelity.
5. Keep data transformations separate from document rendering. Normalize data first, then populate templates.
6. Validate each artifact independently, then validate the whole chain.

## Design Rules

- Do not use plain string replacement inside zipped Office XML unless escaping, run boundaries, relationships, and namespaces are understood.
- Preserve relationship IDs and content types when copying media, charts, embedded workbooks, or custom XML parts.
- Avoid saving `.xlsm` or macro-enabled packages through a library path that strips macros.
- Prefer named ranges, content controls, placeholders, and template fields over positional guesses.
- Log generated filenames, input records, warnings, skipped records, and validation totals.

## Validation

Check:

- DOCX page structure, styles, headers/footers, tables, fields, comments, and tracked changes.
- XLSX formulas, named ranges, tables, charts, macros, hidden sheets, and recalculation requirements.
- PPTX slide count, layout assignment, placeholders, charts, media, theme fonts/colors, and notes.
- Batch totals and file-open sanity for every generated output.

## Output

Provide a pipeline design, implementation steps or scripts, validation checklist, and any Office desktop steps that cannot be performed locally.

Read `references/requirement-plan.md` only when the original discovery evidence is needed.
