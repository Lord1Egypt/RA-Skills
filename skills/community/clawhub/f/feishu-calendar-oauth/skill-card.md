## Description:

Manages a user's Feishu calendar by helping query, create, update, delete, repeat, and set reminders for calendar events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thinkingmanyangyang](https://clawhub.ai/user/thinkingmanyangyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate personal Feishu calendars through natural-language requests, with PowerShell examples for OAuth setup and calendar API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents storing reusable Feishu OAuth credentials in a plaintext token file.

Mitigation: Use a secure credential store or strict user-only file permissions, and rotate Feishu app credentials if the token file may have been exposed.

Risk: The requested Feishu calendar permissions can allow reading, writing, updating, and deleting calendar data.

Mitigation: Grant only the scopes needed for the intended workflow, and use read-only permissions when users only need schedule lookup.

Risk: Calendar update and delete examples can modify or remove user events without documented confirmation guardrails.

Mitigation: Confirm the target event details before updates or deletions and require explicit user approval for destructive calendar actions.

## Reference(s):

- [OAuth 配置指南](references/oauth-setup.md)
- [API 使用指南](references/api-guide.md)
- [Feishu Open Platform](https://open.feishu.cn/app)
- [ClawHub Skill Page](https://clawhub.ai/thinkingmanyangyang/skills/feishu-calendar-oauth)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with PowerShell code blocks and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu OAuth setup steps and calendar API request examples.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
