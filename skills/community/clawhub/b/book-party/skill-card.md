## Description:

Book party services through Lokuli MCP for users who need to find and reserve party services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for party service providers, check availability, and create bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking creation shares customer name, email, and phone number with Lokuli's external MCP service.

Mitigation: Confirm the customer contact details and intent to book before calling the booking tool.

Risk: Searches and reservations depend on provider, service, date, and time-slot data returned by the external MCP service.

Mitigation: Confirm the provider, service, date, and time slot with the user before creating a reservation.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [Book Party on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-party)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses an external MCP endpoint for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
