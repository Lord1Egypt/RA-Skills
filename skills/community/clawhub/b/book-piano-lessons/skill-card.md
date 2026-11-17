## Description:

Book piano-lesson services through Lokuli MCP by searching providers, checking availability, and creating bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use the skill to find piano-lesson services through Lokuli, check appointment availability, and create a booking with customer contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer contact details to an external booking service.

Mitigation: Confirm the customer name, email, phone number, provider, and service before sending create_booking.

Risk: The skill can create a booking without a clear final confirmation.

Mitigation: Require explicit user confirmation of the provider, service, time, price or fees if available, and cancellation terms before creating a booking.

## Reference(s):

- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON]

**Output Format:** [Markdown instructions with JSON-RPC request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided location and booking contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
