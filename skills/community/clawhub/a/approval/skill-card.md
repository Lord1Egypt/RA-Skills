## Description:

企业办公流程与工时管理 Agent，支持办公流程导航、流程申请与审批、待办事项统计、请假调休申请等。当用户需要查询审批、提交申请、查看待办时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sangjie123](https://clawhub.ai/user/sangjie123)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and workplace operations agents use this skill to navigate office workflows, submit or approve process requests, review pending tasks, and manage leave or compensatory time requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests require a Beyond-Token, and token exposure in shell history, logs, screenshots, or shared documents could disclose access credentials.

Mitigation: Use the skill only with a trusted local approval service, keep Beyond-Token values out of examples and shared artifacts, and pass credentials through protected runtime configuration.

Risk: The bundled curl streaming example does not show a safe JSON request body with a Content-Type header.

Mitigation: Before using the example for real approval or leave data, send valid JSON in the request body and include an appropriate Content-Type header.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sangjie123/skills/approval)
- [Publisher profile](https://clawhub.ai/user/sangjie123)
- [Local approval Agent Card endpoint](http://127.0.0.1:7861/jarvis/a2a/approval/.well-known/agent-card.json)
- [Local approval JSON-RPC endpoint](http://127.0.0.1:7861/jarvis/a2a/approval/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with JSON-RPC and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted local approval service at 127.0.0.1:7861 and a Beyond-Token header for requests.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
