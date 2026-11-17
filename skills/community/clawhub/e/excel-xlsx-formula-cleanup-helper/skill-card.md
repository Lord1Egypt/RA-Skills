## Description:

Diagnose and fix Microsoft Excel XLSX workbook issues involving formulas, named ranges, Power Query refreshes, pivot tables, VBA/macro preservation, workbook corruption, and repeatable data cleanup while preserving workbook structure, formatting, and business logic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, finance and operations teams, spreadsheet-heavy small businesses, and developers use this skill to diagnose and repair Excel workbook issues while preserving formulas, macros, pivots, queries, formatting, and business logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect sensitive spreadsheet contents when invoked for workbook repair.

Mitigation: Use copies of important workbooks, limit shared data to what is needed for diagnosis, and avoid invoking it for generic Excel questions that do not require workbook inspection.

Risk: Workbook repairs can alter macros, formulas, pivots, queries, or other business-critical logic.

Mitigation: Confirm intent before modifying macros or production workbooks, preserve workbook package parts where possible, and validate formulas, named ranges, tables, pivots, macros, and expected recalculation after changes.

Risk: Python workbook libraries may not safely rebuild every Excel feature, including some pivot caches, Power Query metadata, slicers, and unsupported OOXML structures.

Mitigation: Inspect relevant OOXML package parts, make minimal repairs, and state when Microsoft Excel desktop or Power BI tooling is required for refresh or final verification.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [Power Query connection example](https://segmentfault.com/a/1190000046365752)
- [Excel SQL query answer](https://segmentfault.com/q/1010000042660742/a-1020000042660744)
- [openpyxl 3.0.3 Chinese manual](https://segmentfault.com/a/1190000022195748)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workbook diagnoses tied to sheets, ranges, formulas, package parts, repair plans, and validation steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
