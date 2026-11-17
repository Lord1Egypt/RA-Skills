## Description:

Agent 瘦身师盘点常驻上下文开销，并提供可量化、可回滚的精简与发布检查。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT

## Use Case:

面向 Agent 使用者与开发者，用于盘点规则、记忆、技能、工具和文档的上下文开销，测量 Token 影响，并审阅可回滚的精简计划与发布检查。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports possible bearer-token exposure through redirects and sensitive diagnostic output; analysis is partial.

Mitigation: Review the skill before installation, avoid using credentials during initial evaluation, and inspect redirect handling and diagnostic output for exposed secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/agent-slim)
- [Usage guide](docs/usage.md)
- [Safety boundaries](docs/safety.md)
- [Measurement guide](references/measurement.md)
- [Generic playbook](references/generic-playbook.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown reports, Shell commands, Configuration guidance]

**Output Format:** [JSON audit and plan files, with Markdown reports and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish measured, estimated, unknown, and unmeasured results; proposed file moves default to dry-run and require explicit application.]

## Skill Version(s):

0.3.0 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
