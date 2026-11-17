## Description:

Book venue services through Lokuli MCP for users who need to find venue options, check availability, and create bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search for venue services through Lokuli, check availability for a selected provider and service, and create a booking with customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer names, email addresses, phone numbers, venue selections, and time slots to Lokuli's external MCP service.

Mitigation: Confirm the user is comfortable sharing the required contact and booking details with Lokuli before sending requests.

Risk: The skill can create venue bookings without documenting a clear consent checkpoint in the artifact.

Mitigation: Require explicit confirmation of the venue, service, date, time slot, and contact details before calling the booking tool.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [JSON-RPC tool call guidance for MCP requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include venue search queries, availability checks, booking time slots, and customer contact details.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
