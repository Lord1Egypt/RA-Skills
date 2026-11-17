## Description:

BOM与SOP对比校对技能。支持多个BOM文件合并后与SOP对比，检测名称规格、位号、数量差异，在SOP文件中标注差异、追加BOM数据并生成报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[2656255594](https://clawhub.ai/user/2656255594)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing, operations, and quality teams use this skill to compare one or more BOM spreadsheets against an SOP workbook, mark differences, append BOM reference data, and generate a reconciliation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive BOM/SOP workbooks could be exposed through cached files or Feishu file-sending behavior.

Mitigation: Use a tightly controlled workspace, least-privileged Feishu credentials, trusted recipients only, and explicit user approval before upload.

Risk: Untrusted large XLSX or ZIP inputs could create processing and cleanup risk.

Mitigation: Avoid untrusted large archives until archive-size, path, and cleanup controls are verified.

Risk: Cached BOM/SOP data retention may be broader than needed for routine reconciliation.

Mitigation: Clarify retention requirements and shorten or automate cleanup for cached workbook-derived data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/2656255594/skills/bom-sop-check)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with file-processing commands and generated spreadsheet/report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces annotated SOP workbooks and reconciliation reports when supplied with compatible BOM/SOP spreadsheet inputs.]

## Skill Version(s):

2.1.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
