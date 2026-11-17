## Description:

Book Tires helps users find tire services and book appointments through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for tire services, check appointment availability, and create bookings with Lokuli providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact an external Lokuli booking service for tire searches and appointments.

Mitigation: Install and use the skill only when external Lokuli service contact is acceptable for the user's request.

Risk: The skill can create bookings that include personal contact details.

Mitigation: Only create a booking after the user has reviewed and confirmed the provider, appointment time, and contact details to be sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-tires)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Text guidance with JSON-RPC MCP tool call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve external service calls and customer contact details when creating bookings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
