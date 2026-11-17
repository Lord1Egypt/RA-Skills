## Description:

Create a formatted Excel (.xlsx) spreadsheet from provided 2D data, applying styles, colors, alignment, and auto-adjusted column widths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sereinzhi](https://clawhub.ai/user/sereinzhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn structured data, chat tables, or report content into formatted Excel workbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper may install missing Python dependencies at runtime.

Mitigation: Preinstall a pinned openpyxl dependency through the normal package process before use in shared or sensitive environments.

Risk: The helper can write or overwrite spreadsheet files in writable paths.

Mitigation: Run it in a sandboxed workspace and require explicit confirmation for output filenames and overwrites.

Risk: Untrusted cell values may remain active as spreadsheet formulas.

Mitigation: Review or sanitize workbook cell values from untrusted sources before opening or sharing generated files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sereinzhi/skills/generate-excel)

## Skill Output:

**Output Type(s):** [files, text]

**Output Format:** [Excel .xlsx workbook plus a JSON-like status result containing the file path and filename.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports plain values and styled cell dictionaries for bold text, font color, background color, and horizontal alignment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
