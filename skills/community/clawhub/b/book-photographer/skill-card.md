## Description:

Helps an agent search for photographers, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find photographer services, check appointment availability, and prepare or create a booking through Lokuli. It is most relevant when the user has provided enough location, service, date, and contact details for a booking workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send location and contact details to an external booking service.

Mitigation: Confirm the user wants to share those details with Lokuli before sending booking or contact information.

Risk: The skill can create bookings without clearly requiring user consent first.

Mitigation: Require explicit user confirmation of provider, service, date, time, and contact details before creating a booking.

Risk: Generic photographer-search requests may route through Lokuli.

Mitigation: Use this skill only when the user is comfortable using Lokuli for photographer search and booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-photographer)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown with JSON-RPC MCP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send user location and contact details to Lokuli and may create bookings through an external service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
