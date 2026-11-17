## Description:

Book IT support services through Lokuli MCP by searching providers, checking availability, and creating bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to find IT support providers through Lokuli, check available appointment times, and create bookings after confirming booking details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send customer contact details to an external Lokuli MCP service when creating a booking.

Mitigation: Confirm the provider, time slot, customer name, email, and phone number before creating a booking.

Risk: Booking actions depend on provider and availability data returned by Lokuli MCP.

Mitigation: Review the selected provider and appointment details before treating a booking as final.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP over SSE and JSON-RPC 2.0 for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
