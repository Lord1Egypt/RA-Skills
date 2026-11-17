## Description:

Helps agents search for pool-service providers, check availability, and create bookings through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill through an agent to find pool-service providers, check appointment availability, and book a selected time slot with customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking flow sends customer contact details to Lokuli when creating a booking.

Mitigation: Confirm the provider, service, time slot, customer name, email, and phone number with the user before calling create_booking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-pool-service)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [JSON-RPC tool calls and brief text confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Contacts Lokuli MCP and may use customer name, email, and phone when creating a booking.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
