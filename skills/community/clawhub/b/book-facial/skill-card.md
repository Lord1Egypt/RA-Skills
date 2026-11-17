## Description:

Book facial services through Lokuli MCP by helping users search providers, check availability, and create bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for facial service providers, check appointment availability, and book facial services through Lokuli's external MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking through the external Lokuli MCP service may send personal contact details and selected appointment information outside the agent environment.

Mitigation: Use the skill only for intended appointment search or booking, and confirm the user's name, email, phone number, selected provider, service, and appointment time before creating a booking.

Risk: Broad facial-service trigger wording may activate the skill for loosely related facial-service requests.

Mitigation: Confirm that the user wants appointment search or booking assistance before calling search, availability, or booking tools.

## Reference(s):

- [Book Facial on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-facial)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, JSON, API calls]

**Output Format:** [Markdown guidance with JSON-RPC tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP search, availability, and booking calls that use customer contact and appointment details.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
