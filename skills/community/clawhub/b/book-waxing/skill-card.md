## Description:

Book Waxing helps agents search for waxing providers, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to find waxing services, compare appointment availability, and create bookings through Lokuli. The agent should confirm booking details and contact information before submitting a booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad waxing requests can enter an external booking flow that may send the user's contact details.

Mitigation: Before creating a booking, confirm the provider, service, date and time, and that the user's name, email, and phone may be sent to Lokuli.

Risk: The skill depends on Lokuli's external service for waxing searches and bookings.

Mitigation: Install and use this skill only when the user is comfortable relying on Lokuli for booking availability and data handling.

## Reference(s):

- [Book Waxing on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-waxing)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown with JSON examples and booking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route waxing search, availability, and booking requests to Lokuli's external service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
