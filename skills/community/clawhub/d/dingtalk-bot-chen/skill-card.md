## Description:

DingTalk Bot integration for messaging, group management, approval workflows, and attendance. Send messages, manage groups, handle approvals, and automate notifications via DingTalk Open API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-aka-chen](https://clawhub.ai/user/jason-aka-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workplace automation agents use this skill to send DingTalk notifications, manage group conversations, create and inspect approvals, and query attendance or vacation information with organization-approved DingTalk credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use DingTalk credentials to send messages and perform organization workflow actions.

Mitigation: Install it only for approved DingTalk workspaces and restrict app scopes to the required messaging, group, approval, and attendance actions.

Risk: Attendance, vacation, approval, user, and group membership data may be sensitive.

Mitigation: Limit access to agents and users with a business need, and handle returned DingTalk data according to the organization's data handling policy.

Risk: The send_to_user path is called out by security guidance because it posts to a relative endpoint instead of the configured DingTalk API base.

Mitigation: Review and correct that implementation before relying on direct user messaging in production workflows.

## Reference(s):

- [DingTalk Open Platform](https://open.dingtalk.com)
- [DingTalk API Documentation](https://open.dingtalk.com/document/)
- [DingTalk Robot Development](https://open.dingtalk.com/document/robot)
- [ClawHub Skill Page](https://clawhub.ai/jason-aka-chen/skills/dingtalk-bot-chen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code examples; DingTalk operations return JSON-compatible API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured DingTalk webhook or internal app credentials for networked DingTalk API actions.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
