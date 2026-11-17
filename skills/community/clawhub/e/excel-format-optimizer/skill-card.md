## Description:

Optimizes existing Excel workbooks for desktop readability by improving font readability, standardizing borders, adjusting row and column sizing, and setting worksheet zoom.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jes614753-sketch](https://clawhub.ai/user/jes614753-sketch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect existing Excel workbooks and produce more readable formatting for Windows-oriented desktop review. It is intended for cases involving small fonts, inconsistent borders, narrow columns, cramped rows, or missing zoom settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes workbook formatting and saves a reformatted spreadsheet, which can affect presentation or user expectations.

Mitigation: Diagnose the workbook first, save to a new output filename, and verify formulas, merged cells, fonts, zoom, and file openability before delivery.

Risk: The artifact suggests installing openpyxl from an unpinned third-party package mirror.

Mitigation: Use a dedicated virtual environment and prefer a pinned openpyxl version from a trusted package source or an explicitly trusted mirror.

Risk: Sensitive spreadsheets may be written to an unintended output file.

Mitigation: Confirm the output filename before saving and use a versioned optimized copy when the source file is locked.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jes614753-sketch/skills/excel-format-optimizer)
- [Tsinghua PyPI package index](https://pypi.tuna.tsinghua.edu.cn/simple)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with Python and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create a reformatted .xlsx copy and verify formulas, merged cells, fonts, zoom, and file openability.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
