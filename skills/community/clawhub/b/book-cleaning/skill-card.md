## Description:

Book Cleaning helps agents search for cleaning services, check availability, and create bookings through the Lokuli MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to find cleaning providers, check available time slots, and book a selected cleaning service through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details to an external booking service.

Mitigation: Confirm the selected provider, booking time, customer name, email address, and phone number before submitting a booking request.

Risk: The skill can create bookings without explicit confirmation guidance in the artifact.

Mitigation: Require clear user approval before calling the booking tool or sending contact details.

## Reference(s):

- [Book Cleaning on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-cleaning)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve MCP tool calls that search services, check availability, and create bookings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
