## Description:

钉钉 OA 审批处理插件，支持查询待办、查看审批详情、执行同意或拒绝，以及查询假期余额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whauff](https://clawhub.ai/user/whauff)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operators use this skill through an agent to review DingTalk OA approval tasks, inspect approval details, approve or reject tasks, and check vacation balances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change real DingTalk OA approval records by approving or refusing tasks.

Mitigation: Require the agent or operator to display task details and obtain explicit confirmation before any approve or reject action.

Risk: The skill requires DingTalk application credentials that can read approval details and perform approval actions.

Mitigation: Use a least-privilege DingTalk app, protect and rotate the AppSecret, and grant only the DingTalk permissions required for the intended workflow.

Risk: The security scan notes that requested sensitive access is broader than well-scoped.

Mitigation: Avoid granting contact-directory access unless it is separately needed and review DingTalk app permissions before deployment.

## Reference(s):

- [DingTalk Open Platform](https://open.dingtalk.com/)
- [DingTalk OA Approval API Documentation](https://open.dingtalk.com/document/orgapp-server/query-the-tasks-to-be-processed-by-the-user)
- [DingTalk User ID Documentation](https://open.dingtalk.com/document/orgapp-server/obtain-the-userid-of-a-member)
- [DingTalk Error Code Documentation](https://open.dingtalk.com/document/orgapp-server/error-code)
- [API Reference](references/api-docs.md)
- [Configuration Guide](references/configuration.md)
- [ClawHub Skill Page](https://clawhub.ai/whauff/skills/dingtalk-approval)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration guidance]

**Output Format:** [Markdown and plain text status messages produced from DingTalk API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured DingTalk user ID, appKey, and appSecret; approval actions should be confirmed before execution.]

## Skill Version(s):

2.3.2 (source: server release evidence, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
