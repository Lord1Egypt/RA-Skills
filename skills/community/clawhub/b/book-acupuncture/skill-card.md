## Description:

Book acupuncture services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for acupuncture providers, check availability, and create appointment bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking workflow can send search, availability, appointment, and contact details to Lokuli.

Mitigation: Use the skill only when the user is comfortable sharing those details with Lokuli, and share only the information needed for the requested booking.

Risk: The create_booking action can create appointments without the artifact clearly requiring user confirmation.

Mitigation: Require explicit user confirmation of the provider, service, time slot, name, email, and phone number before creating a booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-acupuncture)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON-RPC examples and MCP endpoint details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SSE and JSON-RPC 2.0 requests for provider search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
