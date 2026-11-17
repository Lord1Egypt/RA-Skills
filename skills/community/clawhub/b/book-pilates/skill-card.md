## Description:

Book Pilates helps agents search for Pilates services, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users or assistants use this skill to find Pilates services, check available times, and book a selected class or service through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details to an external Lokuli booking endpoint.

Mitigation: Obtain user consent before booking and explain that contact information will be sent to Lokuli.

Risk: A booking call could reserve the wrong Pilates class, provider, time, or contact details.

Mitigation: Confirm the exact class, provider, time, and customer contact details with the user before creating a booking.

## Reference(s):

- [Book Pilates on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-pilates)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Text and JSON-RPC tool call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include booking search criteria, provider and service identifiers, time slots, and customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
