## Description:

Book lashes services through Lokuli MCP. Use when user needs to find and book lashes. Triggers on requests like "book a lashes", "find lashes near me", or any lashes service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for lash service providers, check appointment availability, and create bookings through Lokuli's MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer contact details to an external booking service and create appointments.

Mitigation: Confirm the provider, service, time slot, customer name, email, and phone number before creating a booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-lashes)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [MCP tool calls using JSON-RPC request objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses search, check_availability, and create_booking calls against Lokuli MCP.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
