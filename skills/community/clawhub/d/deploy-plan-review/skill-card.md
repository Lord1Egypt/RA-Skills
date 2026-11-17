## Description:

变更方案自动审核助手 reviews Chinese deployment change-plan documents against local templates, cross-checks required deployment spreadsheets, and produces concise audit reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bounding-elk](https://clawhub.ai/user/bounding-elk)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and deployment engineers use this skill to audit deployment change plans before execution. It checks required Word and spreadsheet inputs, compares plans with local templates, flags P0-P3 findings, and produces a concise Markdown summary plus Word and Excel report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment plans, inventories, IP lists, hostnames, generated reports, and scanner evidence may contain sensitive operational data or credentials.

Mitigation: Review the skill before installation, redact credential evidence, restrict file permissions, and use it only with a clear local storage policy.

Risk: The skill persistently archives raw inputs and generated outputs, which can extend the lifetime of sensitive deployment material.

Mitigation: Define retention limits and a cleanup process for data/raw, output reports, and the master tracking workbook.

Risk: Automated plan review can miss context-specific deployment risks or produce findings that require judgment before execution.

Mitigation: Require a qualified reviewer to confirm P0-P3 findings and approve the selected template baseline before deployment.

Risk: Template-based review depends on the local /home/deploy_template baseline and can produce weak results if templates are stale or mismatched.

Mitigation: Keep deployment templates current and verify the selected template when the plan filename or scenario is ambiguous.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bounding-elk/skills/deploy-plan-review)
- [Python 中文 f-string 引号陷阱](artifact/references/pitfalls.md)

## Skill Output:

**Output Type(s):** [markdown, files, guidance]

**Output Format:** [Concise Markdown response plus generated Word and Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores raw input copies, report outputs, and a master issue-tracking workbook in the skill data/output directories.]

## Skill Version(s):

3.3.1 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
