## Description:

Book Massage helps users find massage services and book appointments through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for massage providers, check availability, and create bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches and bookings are sent to Lokuli's external MCP service.

Mitigation: Tell users when an external service is being used and confirm they want to continue before sending booking requests.

Risk: Completing a booking may share personal contact details and appointment selections.

Mitigation: Confirm customer name, email, phone number, selected provider, service, and time slot before submitting a booking.

## Reference(s):

- [Book Massage ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-massage)
- [Lokuli MCP SSE endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP search, check_availability, and create_booking calls; booking may require customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
