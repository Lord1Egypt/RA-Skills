## Description:

Book DJ helps an agent find DJ providers, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for DJ services, check provider availability, and create bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may send customer contact details or create a booking before the user has confirmed the transaction.

Mitigation: Require explicit confirmation of the provider, service, time slot, customer name, email, and phone number before calling the booking tool.

Risk: The skill depends on Lokuli's external MCP service for DJ search, availability, and booking actions.

Mitigation: Install only when external Lokuli MCP access is intended, and review the MCP endpoint and requested booking details before use.

## Reference(s):

- [Book DJ on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-dj)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-RPC tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP search, availability-check, and booking guidance that may include customer contact details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
