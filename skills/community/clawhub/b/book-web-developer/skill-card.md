## Description:

Book Web Developer helps agents search availability and create bookings for web-developer services through Lokuli's MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for web-developer service providers, check availability, and create a booking through Lokuli after confirming provider, service, time slot, and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send personal contact details to an external booking service.

Mitigation: Confirm the provider, service, time slot, customer name, email, and phone number before allowing a booking call.

Risk: The trigger language is broad and may activate for general web-developer service requests.

Mitigation: Use the skill only when the user intentionally asks Lokuli to search or book web-developer services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-web-developer)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, configuration, api calls]

**Output Format:** [Markdown guidance with JSON-RPC MCP call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send customer name, email, and phone number to an external booking service when a booking call is allowed.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
