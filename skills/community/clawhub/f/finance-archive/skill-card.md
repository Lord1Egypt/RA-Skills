## Description:

上市公司财务文件归档与整理技能包，自动整理凭证、合同、附件，按标准目录结构归档，支持PDF处理、批量重命名、MD5查重、会计档案保管期限管理及审计支持。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aolikeji](https://clawhub.ai/user/aolikeji)

### License/Terms of Use:

MIT-0

## Use Case:

财务、档案和审计支持人员可使用该技能整理上市公司财务凭证、合同、发票、银行、税务和审计文件，并获得目录结构、命名规范、保管期限和电子归档流程指导。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation triggers may cause the skill to be applied to non-financial files or sensitive company records outside the intended scope.

Mitigation: Use the skill only with clearly scoped finance directories and require confirmation before organizing, renaming, or archiving files.

Risk: The sample batch-renaming behavior can affect financial documents unsafely if destination names are not validated.

Mitigation: Validate destination filenames, prevent path traversal, refuse overwrites, and preview planned changes before executing rename operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aolikeji/skills/finance-archive)
- [ClawHub metadata homepage](https://www.clawhub.com/skills/finance-archive)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with tables, workflows, and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes finance archive naming conventions, retention schedules, PDF/file handling snippets, duplicate-detection examples, and audit-support workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
