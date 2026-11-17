## Description:

Works with Bitrix24 via REST API and the Bitrix24 MCP documentation server for CRM, tasks, calendar, chat, open lines, projects, time tracking, drive, feed, sites, products, quotes, users, and related business workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitrix24](https://clawhub.ai/user/bitrix24)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business operators use this skill to retrieve, summarize, and update Bitrix24 work data through an agent, including CRM records, tasks, meetings, files, chats, customer support conversations, and team status. Administrators configure a dedicated Bitrix24 webhook before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify sensitive Bitrix24 business data, including CRM records, tasks, calendars, chats, files, employee time data, and customer conversations.

Mitigation: Use a dedicated Bitrix24 webhook with only the minimum scopes required and avoid admin-wide permissions.

Risk: Security review found that some paths can change business data without consistently enforcing the confirmation behavior promised by the skill instructions.

Mitigation: Review before installing, and require the publisher to fix batch confirmation enforcement and fail closed on unknown or irregular mutating methods before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bitrix24/skills/bitrix24-rest)
- [Bitrix24 skill homepage](https://github.com/bitrix24/bitrix24-skill)
- [Bitrix24 MCP documentation server](https://mcp-dev.bitrix24.tech/mcp)
- [Access and Auth](references/access.md)
- [CRM](references/crm.md)
- [Tasks](references/tasks.md)
- [Calendar](references/calendar.md)
- [Chat and Notifications](references/chat.md)
- [Open Lines](references/openlines.md)
- [MCP Workflow](references/mcp-workflow.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown responses with optional shell commands, configuration snippets, and JSON results from Bitrix24 API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a Bitrix24 webhook URL from the BITRIX24_WEBHOOK_URL environment variable and may call the Bitrix24 MCP documentation server for method guidance.]

## Skill Version(s):

1.2.1 (source: release evidence and changelog, released 2026-04-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
