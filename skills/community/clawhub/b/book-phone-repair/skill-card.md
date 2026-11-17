## Description:

Book phone-repair services through Lokuli MCP for users who need to find and book a phone-repair provider.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for phone-repair providers, check availability, and create a booking through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Appointment and contact details may be sent to Lokuli's MCP service during booking.

Mitigation: Confirm the selected provider, service, appointment time, customer name, email, and phone number with the user before creating a booking.

Risk: A booking could be created for the wrong provider, service, or time slot if search and availability results are not reviewed.

Mitigation: Present the chosen provider, service, and time slot for explicit user confirmation before calling the booking tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-phone-repair)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON-RPC MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send appointment and customer contact details to Lokuli's MCP service when creating bookings.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
