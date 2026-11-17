## Description:

Manages Feishu calendar workflows, including listing calendars and querying, creating, updating, deleting, recurring, reminder-enabled, timezone-aware, and all-day events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teweitao](https://clawhub.ai/user/teweitao)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to connect an agent to Feishu Calendar so it can inspect calendars and manage events for personal or enterprise scheduling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Feishu calendar permissions can allow an agent to read, create, update, or delete calendar data.

Mitigation: Grant read-only Feishu scopes unless write operations are required, and enable only the minimum permissions needed for the deployment.

Risk: Feishu App Secrets can be exposed if placed in source code, prompts, shared logs, or examples.

Mitigation: Store App ID and App Secret in environment variables or a secrets manager, and avoid including real credentials in prompts or committed files.

Risk: The package test command can fetch and print live calendar details when run with real credentials.

Mitigation: Run tests only with non-production credentials or sanitized calendars, and avoid executing npm test in environments that hold production Feishu credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teweitao/skills/feishu-calendar-event)
- [Feishu Calendar API documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/calendar-v4/calendar/list)
- [Feishu tenant access token documentation](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/authentication-management/auth-v3/auth-v3-tenant_access_token)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JavaScript, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu API request examples, credential setup guidance, calendar operation code, and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, package.json, and skill documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
