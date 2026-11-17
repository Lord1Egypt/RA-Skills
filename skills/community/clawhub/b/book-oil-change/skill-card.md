## Description:

Book oil-change services through Lokuli MCP. Use when user needs to find and book oil-change. Triggers on requests like "book a oil-change", "find oil-change near me", or any oil-change service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for nearby oil-change services, check provider availability, and create a booking through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a booking may send the user's name, email, and phone number to Lokuli.

Mitigation: Before booking, confirm the provider, service, time slot, and that those contact details will be sent for the reservation.

Risk: The skill depends on Lokuli's external MCP service for oil-change search and booking.

Mitigation: Install and use it only when the user is comfortable relying on that external service.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-oil-change)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Markdown with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external Lokuli MCP service; booking requests may send customer name, email, and phone number.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
