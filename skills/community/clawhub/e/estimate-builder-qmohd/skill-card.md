## Description:

Build construction project estimates. Generate detailed cost breakdowns with labor, materials, equipment, and overhead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qmohd](https://clawhub.ai/user/qmohd)

### License/Terms of Use:

MIT

## Use Case:

Construction estimators, project managers, and agents supporting construction planning use this skill to create, review, and report project estimates with categorized line items, markups, grand totals, and validation warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet exports can overwrite files if a user chooses an existing output path.

Mitigation: Choose an explicit destination path for generated spreadsheets and confirm it is safe before export.

Risk: Formula-like text in estimate fields can be interpreted by spreadsheet software after XLSX export.

Mitigation: Sanitize untrusted values that begin with =, +, -, or @ before exporting or sharing spreadsheets.

Risk: Currency assumptions can make estimates misleading for non-USD projects.

Mitigation: Specify the desired currency whenever the project is not USD-based.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qmohd/skills/estimate-builder-qmohd)
- [Data Driven Construction website](https://datadrivenconstruction.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, files, guidance]

**Output Format:** [Markdown tables and prose, with optional Python code examples and Excel file exports when used by an agent with filesystem access.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include cost summaries, markup breakdowns, grand totals, validation warnings, DataFrame-compatible structures, and optional XLSX reports.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
