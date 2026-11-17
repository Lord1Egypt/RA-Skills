## Description:

识别导出风险、应用脱敏规则、生成审批流程与审计记录。当用户需要导出研究结果或提交审批时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergenceronearth](https://clawhub.ai/user/emergenceronearth)

### License/Terms of Use:

MIT-0

## Use Case:

Research platform users and agent operators use this skill when they need to export research results, review desensitization rules, submit an approval flow, or present audit records for an export-governance step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill assumes a fixed governance JSON path and a localhost status-reporting service.

Mitigation: Install and run it only in environments where that data path and local reporting endpoint are expected and controlled.

Risk: Export-governance data can include sensitive research or patient-level indicators.

Mitigation: Treat displayed governance data as sensitive and confirm desensitization rules before sharing exported results.

Risk: Broad export or approval requests could trigger the workflow outside its intended governance scope.

Mitigation: Use the skill only for export-governance tasks and review generated approval and audit information before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emergenceronearth/skills/agentic-export-governance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured governance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Presents export risk, approval, desensitization, export strategy, and audit-record information from the configured governance data source.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
