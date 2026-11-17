## Description:

设计、审查和重构面向 AI Agent 的 CLI。检查可预测性、纵深防御和上下文效率，并用实际证据评分。用于开发 Agent DX CLI 或检视现有 CLI。

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

CLI 开发者和工程师可用此技能设计、审查或重构面向 AI Agent 的命令行工具，并以实际证据评估契约、安全边界、上下文效率及验收结果。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review was partial and explicitly notes Google Drive metadata guidance.

Mitigation: Review the relevant Drive guidance before use, and limit any metadata lookup to information and access already authorized for the task.

## Reference(s):

- [Agent DX 原则、理由与正反例](references/agent-dx-patterns.md)
- [GWS 实践](references/gws.md)
- [SKILL+CLI 编写](references/skill-cli.md)
- [Google Workspace CLI 固定版本源码参考](https://github.com/googleworkspace/cli/tree/a3768d0e82ad83cca2da97724e46bea4ff0e6dbd/crates/google-workspace-cli/src)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with evidence-linked scores, CLI commands, implementation guidance, and verification results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports applicable checks, evidence, unresolved limitations, and verification boundaries; changes remain within existing authorization.]

## Skill Version(s):

0.4.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
