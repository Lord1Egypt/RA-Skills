## Description:

Book Barber helps agents search barber services, check availability, and create bookings through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to find barber services, check available time slots, and create bookings through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an external Lokuli booking service and may send customer contact details.

Mitigation: Install only when Lokuli is an acceptable external service, and confirm the name, email, and phone number before sending them.

Risk: The skill can create a real appointment with a barber service.

Mitigation: Verify the barber, service, date, and time slot before creating a booking.

## Reference(s):

- [Book Barber ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-barber)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown with JSON tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP tools for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
