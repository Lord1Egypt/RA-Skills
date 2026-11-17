## Description:

Book bartender services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for bartender services, check provider availability, and prepare a booking through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details and booking selections to a third-party Lokuli MCP service.

Mitigation: Use it only when the user intends to make a bartender booking, and disclose that booking details may be sent to Lokuli.

Risk: The create_booking flow can create a booking if invoked without a separate confirmation step.

Mitigation: Require explicit user confirmation of provider, service, date, time, and customer contact details before any create_booking call.

## Reference(s):

- [Book Bartender ClawHub listing](https://clawhub.ai/edwardrodriguez703-design/skills/book-bartender)
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, API calls]

**Output Format:** [Markdown guidance with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve MCP tool calls to search for bartender services, check availability, and create bookings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
