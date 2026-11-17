## Description:

Book appliance-repair services through Lokuli's MCP server, including provider search, availability checks, and booking creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for appliance-repair providers, check appointment availability, and create a booking through Lokuli's external MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking through this skill may send customer name, email, phone number, preferred time, and repair request details to Lokuli's external MCP service.

Mitigation: Use the skill only when the user intends to search or book appliance repair through Lokuli, and confirm the exact booking details before creating a booking.

Risk: An incorrect provider, service, date, time slot, or contact detail could create an unwanted or inaccurate booking.

Mitigation: Present the proposed booking details for user confirmation before calling the create_booking tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-appliance-repair)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider, service, time slot, customer contact details, and repair request details needed for booking.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
