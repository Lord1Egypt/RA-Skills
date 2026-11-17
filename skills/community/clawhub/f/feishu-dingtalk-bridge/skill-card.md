## Description:

打通飞书/钉钉开放API，实现日程同步、审批追踪、文档解析与智能待办分发的企业协同中枢

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to coordinate Feishu and DingTalk calendar, approval, document, and task workflows. It helps aggregate enterprise collaboration data into structured Markdown reports with task lists, status summaries, and automation recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Feishu or DingTalk access tokens may be provided as ordinary inputs and exposed through chat, logs, or traces.

Mitigation: Use narrowly scoped, short-lived credentials; avoid pasting production tokens into ordinary workflow fields; prefer managed secrets or OAuth connections; confirm host-side token redaction.

Risk: Calendar, approval, document, and task data may contain sensitive enterprise or employee information.

Mitigation: Review deployment settings and generated reports for redaction, limit app permissions to the needed modules, and validate that outputs omit tokens and private employee fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boboy-j/skills/feishu-dingtalk-bridge)
- [Publisher profile](https://clawhub.ai/user/boboy-j)
- [Feishu Open Platform](https://open.feishu.cn/)
- [DingTalk Open Platform](https://open.dingtalk.com/)

## Skill Output:

**Output Type(s):** [markdown, guidance]

**Output Format:** [Markdown report with tables, status summaries, task lists, and automation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires platform, action, and auth_token inputs; outputs should not expose access tokens or employee privacy fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
