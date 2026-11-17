## Description:

Book Fitness helps agents find fitness services, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for fitness providers, check appointment availability, and book selected services through Lokuli after confirming booking details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a booking may send customer name, email, phone number, booking time, and selected provider or service details to Lokuli's external MCP service.

Mitigation: Use the skill only for explicit fitness search or booking tasks, and confirm the customer, service, provider, and time before creating a booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance]

**Output Format:** [JSON-RPC MCP calls with concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send booking contact details and selected service information to Lokuli's external MCP service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
