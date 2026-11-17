## Description:

Book plumber services through Lokuli MCP for users who need to find and book a plumber.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill through an agent to search for plumber providers, check availability, and create a booking through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer name, email, and phone number to an external booking service.

Mitigation: Confirm the provider, appointment time, customer name, email, and phone number with the user before making any booking call.

Risk: The security evidence says the skill does not clearly require user consent before booking.

Mitigation: Require explicit user approval before calling the create_booking tool.

## Reference(s):

- [Book Plumber ClawHub Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-plumber)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external SSE MCP endpoint and may result in booking calls that include customer contact details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
