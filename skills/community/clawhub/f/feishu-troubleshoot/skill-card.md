## Description:

Guides users through Feishu permission, bot capability, event subscription, and long-connection settings so OpenClaw can receive and reply to messages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinadu-ai](https://clawhub.ai/user/tinadu-ai)

### License/Terms of Use:


## Use Case:

Developers and operators configuring OpenClaw with Feishu use this skill to troubleshoot bot replies, permission imports, calendar and task access, event subscriptions, and app publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Feishu chat, calendar, task-writing, and employee-ID scopes may grant more access than a deployment needs.

Mitigation: Review each scope before import, grant only the message, calendar, task, and employee-ID permissions the integration requires, prefer read-only scopes where possible, and revoke unused write or directory access from published apps.

Risk: Permission JSON snippets may be pasted into production apps without environment-specific review.

Mitigation: Validate the scopes and bot event behavior in a limited Feishu app before publishing changes broadly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinadu-ai/skills/feishu-troubleshoot)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with JSON permission snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only troubleshooting guidance; no code execution is required.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact skill.json lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
