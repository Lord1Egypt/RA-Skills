## Description:

Book transmission services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for transmission services, check availability, and create a booking through Lokuli's MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer name, email, and phone number may be sent to Lokuli or a downstream provider during booking creation.

Mitigation: Ask for explicit user confirmation before submitting contact details or creating an appointment.

Risk: The skill can create bookings without clear consent instructions.

Mitigation: Confirm provider, service, time slot, customer contact details, and booking intent before calling create_booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-transmission)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API calls]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external MCP endpoint and may transmit customer contact details when creating a booking.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
