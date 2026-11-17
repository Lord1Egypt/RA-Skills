## Description:

Schedule meetings, check availability, and manage calendars across Google, Outlook, and CalDAV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[billylui](https://clawhub.ai/user/billylui)

### License/Terms of Use:

MIT-0

## Use Case:

Individual users and developers use this skill to route calendar requests to Temporal Cortex datetime and scheduling tools for availability checks, meeting proposals, and bookings across Google, Outlook, and CalDAV.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar credentials are required for scheduling tools and are stored in the local Temporal Cortex configuration directory.

Mitigation: Review requested OAuth scopes before connecting calendars and isolate credentials by running the MCP server with Docker containment when stronger separation is needed.

Risk: Booking tools can create calendar events or external booking requests.

Mitigation: Confirm booking details and availability checks before executing book_slot or request_booking.

Risk: Unpinned package installation can increase supply-chain exposure.

Mitigation: Install from the pinned OpenClaw package or run npx with the explicit @0.9.1 package version.

## Reference(s):

- [Security Model](references/SECURITY-MODEL.md)
- [Temporal Cortex Homepage](https://temporal-cortex.com)
- [Temporal Cortex Skills Repository](https://github.com/temporal-cortex/skills)
- [Temporal Cortex MCP Server Source](https://github.com/temporal-cortex/mcp)
- [@temporal-cortex/cortex-mcp npm Package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp)
- [Temporal Cortex REST API Reference](https://temporal-cortex.com/docs/rest-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool names, workflow steps, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes requests to datetime and scheduling sub-skills; calendar booking actions should be confirmed before execution.]

## Skill Version(s):

0.9.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
