## Description:

Helps agents find physical-therapy providers, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to search for physical-therapy services, review available appointment slots, and request a booking through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking requests may send contact details and selected appointment information to Lokuli.

Mitigation: Confirm the provider, date, time, and personal information with the user before allowing a booking call.

Risk: The skill can initiate a physical-therapy appointment booking through an external MCP service.

Mitigation: Require explicit user approval before calling the booking tool.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-physical-therapy)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration]

**Output Format:** [Text and JSON-RPC tool call payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request contact details and appointment selections before booking through an external MCP service.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
