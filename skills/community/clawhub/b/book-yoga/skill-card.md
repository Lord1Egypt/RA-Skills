## Description:

Book Yoga helps users search for yoga services and create bookings through Lokuli's MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to find yoga providers, check availability, and create bookings via Lokuli. The skill is suited to agents handling yoga search or booking requests that require location, time slot, and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Booking requests may send customer name, email, phone number, location or ZIP code, and selected time slot to Lokuli.

Mitigation: Use the skill only for intentional Lokuli-powered yoga search or booking, and confirm the provider, time, and contact details before creating a booking.

Risk: The security summary notes consent and trigger-scope caveats for external booking data use.

Mitigation: Confirm user intent before initiating booking-related MCP calls and avoid collecting contact details until they are needed for a booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Markdown guidance with JSON-RPC MCP call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include search criteria, availability parameters, selected booking details, and customer contact details for Lokuli MCP tool calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
