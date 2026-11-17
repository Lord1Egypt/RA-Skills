## Description:

Excel diagnoses spreadsheet problems and selects the best path - formula, pivot table, cleaning workflow, or VBA - to deliver resilient, readable, version-aware solutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agisearch](https://clawhub.ai/user/agisearch)

### License/Terms of Use:

MIT-0

## Use Case:

External spreadsheet users, finance analysts, and operations teams use this skill to diagnose spreadsheet problems and receive formulas, pivot table steps, cleaning workflows, modeling guidance, or VBA macros with likely failure points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated VBA macro code could change workbook data or run in a security-sensitive Excel environment if executed without review.

Mitigation: Review any generated macro before running it, test it on a copy of the workbook, and prefer formulas or pivot tables when they fit the task.

Risk: Spreadsheet guidance may be incorrect when the user's workbook structure, platform, or Excel version is underspecified.

Mitigation: Provide workbook layout and platform details, then verify formulas, pivot setups, and cleaning workflows against representative data before relying on them.

## Reference(s):

- [Excel ClawHub skill page](https://clawhub.ai/agisearch/skills/excel-pro)
- [README](artifact/README.md)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, configuration]

**Output Format:** [Markdown with formulas, VBA code blocks, step-by-step spreadsheet instructions, and failure-point warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May adapt recommendations by spreadsheet platform and version.]

## Skill Version(s):

2.0.0 (source: frontmatter, artifact configuration, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
