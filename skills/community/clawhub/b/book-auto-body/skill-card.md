## Description:

Book auto-body services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find auto-body providers through Lokuli MCP, check availability, and create bookings after the user confirms the provider, service, time slot, and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and bookings are handled by Lokuli's external MCP service.

Mitigation: Install only after accepting that workflow data is sent to the external service, and review the selected provider, service, and time slot before booking.

Risk: Creating a booking requires customer name, email, and phone details.

Mitigation: Provide contact details only when intending to create a booking, and confirm those details before submission.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-auto-body)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON-RPC tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP over SSE with JSON-RPC 2.0 POST requests.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
