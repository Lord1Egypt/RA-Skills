## Description:

Book real-world local services through Lokuli MCP, including searching providers, checking availability, collecting required contact details, and generating payment links after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and assistants use this skill to find local service providers, compare pricing and availability, and create bookings only after explicit confirmation. It supports common local service needs such as auto, beauty, health, home, education, repair, and event services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Lokuli and may send personal contact information, location, selected provider, service, and time slot when a booking is approved.

Mitigation: Confirm the provider, pricing, time slot, and contact details with the user before creating a booking or cart.

Risk: Booking and cart creation can produce payment flows for real-world services.

Mitigation: Require explicit user approval before booking and provide the checkout link for the user to complete payment.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-local)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON-RPC tool-call examples and booking workflow text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before booking; approved bookings return Stripe checkout URLs for user payment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
