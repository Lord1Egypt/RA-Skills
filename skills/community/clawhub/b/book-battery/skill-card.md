## Description:

Book battery services through Lokuli MCP, including service search, availability checks, and booking creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users ask an agent to find battery service options, check provider availability, and create bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking flow may send customer contact details to Lokuli's external MCP service.

Mitigation: Before confirming a booking, verify the provider, time, and contact details, and avoid sharing personal information unless the user intends to create the booking.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-battery)

## Skill Output:

**Output Type(s):** [guidance, API calls, text]

**Output Format:** [Markdown guidance with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Lokuli MCP search, availability, and booking calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
