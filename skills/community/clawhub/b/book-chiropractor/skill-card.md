## Description:

Book chiropractor services through Lokuli MCP for users who need to find and book chiropractor appointments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for chiropractor providers, check appointment availability, and create bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking activity can reveal personal contact details and health-related appointment preferences to an external booking provider.

Mitigation: Confirm the booking provider, appointment time, and exact customer contact details before creating a booking through Lokuli.

Risk: The skill can initiate an external appointment booking action.

Mitigation: Require explicit user confirmation before calling the create_booking tool.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [Book Chiropractor ClawHub page](https://clawhub.ai/edwardrodriguez703-design/skills/book-chiropractor)

## Skill Output:

**Output Type(s):** [API calls, Guidance, Configuration]

**Output Format:** [Markdown with JSON-RPC tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP over SSE with JSON-RPC calls for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
