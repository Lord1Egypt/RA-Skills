## Description:

Create, inspect, and edit Microsoft Excel workbooks and XLSX files with reliable handling for formulas, dates, data types, formatting, recalculation, and template preservation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create, read, edit, convert, and preserve Excel, XLSX, CSV, and TSV workbook deliverables where formulas, formatting, workbook structure, and data-type fidelity matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted spreadsheet cell values can influence filenames during split-by-column workflows and may cause output to be written outside the intended folder.

Mitigation: Use copies of important workbooks, sanitize filename values before splitting, and avoid split-by-column workflows on attacker-controlled data until filename handling is fixed.

Risk: Formula-like values from untrusted CSV or spreadsheet content may remain active in generated XLSX files.

Mitigation: Review generated workbooks before opening or sharing them, and neutralize formula-like cells when processing untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/skills/excel-toolkit)
- [Skill homepage](https://clawic.com/skills/excel-xlsx)
- [ClawHub registry](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and workbook or tabular file outputs when applied by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports linux, darwin, and win32; depends on openpyxl and pandas.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
