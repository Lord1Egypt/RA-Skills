## Description:

Dingtalk Calendar helps agents use mcporter to connect to DingTalk MCP calendar and contacts services for creating and managing events, checking free/busy status, and booking meeting rooms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and assistants managing DingTalk schedules use this skill to create, query, update, and delete calendar events, check attendee availability, search contact details, and reserve meeting rooms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, and delete DingTalk calendar data.

Mitigation: Use the minimum calendar permissions needed and confirm event IDs before updates or deletions.

Risk: The skill relies on a globally installed third-party mcporter CLI and configured DingTalk MCP endpoints.

Mitigation: Install only if you trust mcporter and the DingTalk MCP endpoints you configure.

Risk: Calendar free/busy and contact lookups can expose coworker availability or details.

Mitigation: Follow organizational policy before looking up coworkers' details or free/busy status.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/dingtalk-cal-v1)
- [DingTalk MCP Plaza](https://mcp.dingtalk.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generally request JSON output from mcporter.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
