## Description:

Book flooring services through Lokuli MCP for users who need to find flooring providers, check availability, and create bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for flooring services through Lokuli, check appointment availability, and create a booking after confirming the provider, time slot, and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send booking contact details, including name, email, and phone number, to an external Lokuli service.

Mitigation: Confirm the provider, time slot, and user consent before creating a booking or sharing contact details.

Risk: Booking creation may establish a real-world appointment if used without final confirmation.

Mitigation: Use search and availability checks first, then request explicit user confirmation before calling create_booking.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-flooring)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP tools for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
