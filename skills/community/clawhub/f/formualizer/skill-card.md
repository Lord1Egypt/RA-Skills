## Description:

Recalculate cached Excel (.xlsx) formula values, inspect cells and ranges, and trace formula precedents or dependents locally using Formualizer — zero LibreOffice, zero Python virtualenv, zero cloud upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psu3d0](https://clawhub.ai/user/psu3d0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and spreadsheet users can use this skill to recalculate cached Excel formulas, inspect workbook cells and ranges, and trace formula dependencies locally. It provides CLI, JavaScript, and MCP usage examples for working with workbooks without uploading them to a cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI example uses npx with an unpinned package version, which could download and execute a changed release.

Mitigation: Review and pin the package version before use, and restrict file and network access to what the task requires.

Risk: The security scan was partial because some referenced paths were unresolved, leaving the evidence incomplete.

Mitigation: Review the unresolved referenced paths and scan the complete release before deployment.

## Reference(s):

- [Formualizer ClawHub release page](https://clawhub.ai/psu3d0/skills/formualizer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with shell, TypeScript, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local workbook usage guidance and directs agents to report formula errors, changed caches, and partial or unsupported diagnostics returned by Formualizer.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
