## Description:

Book makeup services through Lokuli MCP for service searches, availability checks, and booking creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find makeup service providers, check appointment availability, and create bookings through Lokuli's MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer name, email, and phone number to an external booking service.

Mitigation: Confirm the user wants to share those contact details with Lokuli before creating a booking.

Risk: The skill can create bookings without clear in-skill confirmation guidance.

Mitigation: Verify provider, service, time, price, cancellation terms, and user intent before calling create_booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-makeup)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON-RPC tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider, service, time slot, and customer contact details when creating a booking.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
