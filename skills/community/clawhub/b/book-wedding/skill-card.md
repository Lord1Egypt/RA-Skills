## Description:

Book Wedding helps agents search wedding services, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to find wedding service providers, check availability, and request bookings through Lokuli after confirming booking details and personal contact information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create external wedding-service bookings using personal contact details without clear final confirmation guidance.

Mitigation: Before creating a booking, require explicit user confirmation of the provider, service, time, known price or fees, known cancellation terms, and every personal detail that will be sent.

Risk: The agent depends on Lokuli's external MCP service for wedding search and booking.

Mitigation: Install and use the skill only when external service calls to Lokuli are acceptable for the user's workflow and data-sharing expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-wedding)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown guidance with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve external search, availability checks, and booking requests through Lokuli's MCP service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
