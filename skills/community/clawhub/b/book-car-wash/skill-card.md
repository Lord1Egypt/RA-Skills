## Description:

Book car-wash services through Lokuli MCP. Use when user needs to find and book car-wash. Triggers on requests like "book a car-wash", "find car-wash near me", or any car-wash service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for nearby car-wash providers, check appointment availability, and create a booking through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking through the skill may share the user's name, email, and phone number with Lokuli's external MCP service.

Mitigation: Confirm the provider, service, time slot, and contact details before allowing any booking request to be sent.

Risk: A booking could be made for the wrong provider, service, or time if request details are ambiguous.

Mitigation: Ask the user to confirm the provider, selected service, and appointment time before calling create_booking.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)
- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-car-wash)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code]

**Output Format:** [Markdown with JSON-RPC tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP tools for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
