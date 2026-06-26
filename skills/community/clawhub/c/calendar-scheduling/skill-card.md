## Description: <br>
Schedules meetings, checks availability, and manages calendars across Google, Outlook, and CalDAV while routing datetime and scheduling tasks to focused sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billylui](https://clawhub.ai/user/billylui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and developers use this skill to let MCP-compatible agents check availability, resolve times, manage calendars, and book or propose meetings across connected calendar providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access connected calendars and create bookings through configured providers. <br>
Mitigation: Review OAuth scopes during setup, discover calendars before use, check availability before booking, and keep user confirmation enabled before booking or sending proposals. <br>
Risk: OAuth credentials are stored locally for the MCP server. <br>
Mitigation: Protect ~/.config/temporal-cortex/credentials.json and use Docker containment or restricted filesystem access where appropriate. <br>
Risk: Platform Mode can send scheduling identifiers to Temporal Cortex platform APIs for cross-user scheduling. <br>
Mitigation: Use Local Mode when scheduling identifiers should not be sent to Temporal Cortex platform APIs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/billylui/calendar-scheduling) <br>
- [Temporal Cortex homepage](https://temporal-cortex.com) <br>
- [Temporal Cortex MCP package](https://www.npmjs.com/package/@temporal-cortex/cortex-mcp) <br>
- [Security Model](references/SECURITY-MODEL.md) <br>
- [REST API reference](https://temporal-cortex.com/docs/rest-api) <br>
- [Platform docs](https://app.temporal-cortex.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with tables and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes routing guidance and safety checks for calendar reads, scheduling proposals, and booking actions.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
