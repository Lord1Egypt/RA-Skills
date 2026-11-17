## Description:

Build and troubleshoot cross-Office automation pipelines that move content between Word, Excel, and PowerPoint using Open XML, VBA, python-docx, openpyxl, python-pptx, templates, and batch conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, consultants, and operations teams use this skill to design, implement, and validate repeatable workflows that move content across DOCX, XLSX, PPTX, PDF, and image outputs while preserving Office package structure and formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts or VBA can modify Office documents, spreadsheets, presentations, or macro-enabled packages.

Mitigation: Review generated scripts and VBA before running them, work on copies, and keep an audit trail of inputs, outputs, warnings, skipped records, and validation totals.

Risk: Incorrect Open XML edits can break relationships, content types, formulas, macros, charts, media, or formatting.

Mitigation: Use supported Office libraries where possible, preserve relationship IDs and content types, avoid unsafe XML string replacement, and validate each DOCX, XLSX, and PPTX artifact independently.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with pipeline designs, implementation steps, scripts or code snippets, shell commands, and validation checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify Office desktop automation steps that cannot be performed locally.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
