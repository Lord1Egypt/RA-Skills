## Description:

Book catering services through Lokuli MCP for users who need to find and book catering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for catering options, check availability, and create catering bookings through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking workflow can send customer contact details to Lokuli's external MCP booking service.

Mitigation: Confirm user consent before transmitting names, email addresses, phone numbers, or other contact details.

Risk: A booking could be created without a clear final approval step.

Mitigation: Before calling create_booking, present the provider, service, time slot, and customer details and require explicit user approval.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-catering)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include catering search criteria, availability checks, and booking creation requests containing customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
