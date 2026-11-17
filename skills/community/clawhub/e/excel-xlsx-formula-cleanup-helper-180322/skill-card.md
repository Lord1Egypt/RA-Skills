## Description:

Diagnose and fix Microsoft Excel XLSX workbook issues involving formulas, named ranges, Power Query refreshes, pivot tables, VBA/macro preservation, workbook corruption, and repeatable data cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, finance and operations teams, spreadsheet-heavy small businesses, and developers use this skill to diagnose and repair Excel workbooks while preserving formulas, formatting, macros, Power Query assets, pivots, and business logic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook repair suggestions or generated scripts could damage important spreadsheets if applied directly.

Mitigation: Work on copies, review proposed edits before applying them, and validate formulas, ranges, tables, pivots, macros, and expected recalculation afterward.

Risk: .xlsm files, external links, Power Query connections, pivot caches, and business-critical formulas can be lost or changed by unsupported tooling.

Mitigation: Inspect workbook package parts and supported library behavior before saving, preserve macro-related parts when required, and note when desktop Excel or Power Query refresh is still needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyro-ma/skills/excel-xlsx-formula-cleanup-helper-180322)
- [ClawHub publisher profile](https://clawhub.ai/user/kyro-ma)
- [Requirement plan](references/requirement-plan.md)
- [Power BI introduction and data acquisition](https://segmentfault.com/a/1190000020692249)
- [Power Query connecting multiple tables](https://segmentfault.com/a/1190000046365752)
- [Excel SQL query answer](https://segmentfault.com/q/1010000042660742/a-1020000042660744)
- [openpyxl simple examples](https://segmentfault.com/a/1190000022195748)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workbook-specific diagnoses, repair plans, scripts, and validation steps; edits should be reviewed before applying to important files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
