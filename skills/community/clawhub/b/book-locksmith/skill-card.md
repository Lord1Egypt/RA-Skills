## Description:

Book Locksmith helps users find locksmith services, check availability, and create bookings through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for locksmith providers by location, check availability, and create a booking after collecting required customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking details, including customer name, email, and phone number, may be sent to the third-party Lokuli service.

Mitigation: Tell the user that booking details will go to Lokuli, ask before collecting contact details, and collect only the information required for the booking.

Risk: The skill can create a locksmith booking without explicit final-confirmation instructions in the artifact.

Mitigation: Ask the user to confirm the provider, service, time slot, and contact details before calling create_booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-locksmith)

## Skill Output:

**Output Type(s):** [Guidance, API calls]

**Output Format:** [Markdown with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May collect location, provider, service, time slot, name, email, and phone details needed for locksmith booking.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
