## Description:

Automate Cal.com tasks via Rube MCP (Composio): manage bookings, check availability, configure webhooks, and handle teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sohamganatra](https://clawhub.ai/user/sohamganatra)

### License/Terms of Use:


## Use Case:

Developers, operations teams, and scheduling administrators use this skill to guide agents through Cal.com booking, availability, webhook, team, and organization workflows via Rube MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can create bookings, create teams, and update or delete webhook configurations in a connected Cal.com account.

Mitigation: Review proposed actions before execution and confirm the active Cal.com connection, permissions, event type IDs, team IDs, and target booking details.

Risk: Webhook subscriber URLs may receive booking-event data.

Mitigation: Use only HTTPS webhook endpoints that you control or trust, and configure webhook secrets for payload verification.

Risk: Outdated tool schemas or incorrect date and timezone parameters can cause failed or incorrect scheduling operations.

Mitigation: Search Rube MCP tools first for current schemas, check availability before creating bookings, and provide explicit ISO 8601 or IANA timezone values as required.

## Reference(s):

- [Cal Com Automation on ClawHub](https://clawhub.ai/sohamganatra/skills/cal-com-automation)
- [Rube MCP Server](https://rube.app/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with tool names, workflow steps, parameter notes, and setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active Rube MCP connection and an authenticated Cal.com connection.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
