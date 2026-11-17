## Description:

Book art-lessons services through Lokuli MCP for users who need to find providers, check availability, and create bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for art-lesson services through Lokuli, inspect availability, and create a booking after confirming provider, service, time slot, and customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and bookings are handled by Lokuli's external MCP service.

Mitigation: Tell users that the external service is used before booking-related actions and avoid sending contact details unless the user intends to create a booking.

Risk: A booking could be created with the wrong provider, service, time slot, or contact details.

Mitigation: Confirm the provider, service, time slot, name, email, and phone number with the user before submitting a booking request.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-art-lessons)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration]

**Output Format:** [Markdown with JSON-RPC request examples and concise booking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external Lokuli MCP service for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
