## Description:

Book eyebrows services through Lokuli's MCP server by searching providers, checking availability, and creating bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to find eyebrow service providers, check appointment availability, and create a booking through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create third-party bookings using personal contact details without explicit consent or confirmation instructions.

Mitigation: Require explicit user confirmation of the provider, service, time slot, name, email, and phone number before calling create_booking.

Risk: The skill contacts Lokuli to search services and complete bookings.

Mitigation: Tell the user before sending location, search, availability, or booking details to Lokuli and continue only with permission.

## Reference(s):

- [Book Eyebrows on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-eyebrows)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Markdown and JSON-RPC request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact a third-party MCP service and use customer contact details to complete a booking.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
