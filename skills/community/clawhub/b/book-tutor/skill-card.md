## Description:

Book tutor services through Lokuli MCP. Use when user needs to find and book tutor. Triggers on requests like "book a tutor", "find tutor near me", or any tutor service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for tutor services through Lokuli, check provider availability, and create a booking after confirming the selected provider, service, time slot, and customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details to a third-party booking service.

Mitigation: Confirm the user intends to use Lokuli and verify the provider, service, time slot, zip code, name, email, and phone number before any booking call.

Risk: Broad tutor-service trigger language could activate the booking workflow before user intent is specific.

Mitigation: Use the skill only for explicit tutor search or booking requests, and require confirmation before creating a booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-tutor)
- [Lokuli MCP SSE endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration]

**Output Format:** [Markdown guidance with JSON-RPC tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce booking-related API calls that include zip code, provider and service identifiers, time slot, customer name, email, and phone number.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
