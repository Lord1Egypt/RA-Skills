## Description:

Build construction project estimates. Generate detailed cost breakdowns with labor, materials, equipment, and overhead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

External construction professionals and project teams use this skill to assemble cost estimates, categorize labor, material, equipment, subcontractor, and other costs, apply markups, and review estimates for common data issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Excel exports that include client, contractor, or other untrusted text can carry unsafe spreadsheet content.

Mitigation: Review or sanitize text fields that begin with =, +, -, or @ before export.

Risk: Exporting to a user-supplied workbook path can overwrite an existing estimate file.

Mitigation: Confirm the output filename before writing an Excel workbook.

Risk: The default currency may not match the project context.

Mitigation: Specify a currency other than USD when the estimate requires it.

## Reference(s):

- [DataDrivenConstruction homepage](https://datadrivenconstruction.io)
- [ClawHub skill page](https://clawhub.ai/datadrivenconstruction/skills/estimate-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown tables, validation notes, and Python usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce cost category summaries, markup breakdowns, grand totals, validation warnings, and Excel export guidance.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
