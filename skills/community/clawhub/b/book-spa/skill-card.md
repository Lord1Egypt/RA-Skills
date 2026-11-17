## Description:

Book Spa helps agents search spa providers, check appointment availability, and create bookings through the Lokuli MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to find spa services, check provider availability, and request a booking. Users should confirm the provider, service, time slot, and contact details before a booking is created.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create external spa bookings using personal contact details.

Mitigation: Require explicit user confirmation of the provider, service, time slot, customer name, email, and phone number before allowing a booking call.

Risk: The activation scope is broad for spa-related requests.

Mitigation: Use this skill only when the user clearly intends to search for or book spa appointments.

## Reference(s):

- [Book Spa on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-spa)
- [Publisher profile](https://clawhub.ai/user/edwardrodriguez703-design)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration]

**Output Format:** [Markdown and JSON-RPC tool call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use external MCP calls to search providers, check availability, and create bookings with user contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
