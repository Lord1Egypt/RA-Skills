## Description:

Book language-tutor services through Lokuli MCP by searching providers, checking availability, and creating bookings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can ask an agent to find language tutors, check appointment availability, and create a tutor booking through Lokuli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The booking flow can send customer name, email, phone number, and appointment details to an external booking service.

Mitigation: Ask for explicit user confirmation before creating a booking, and request personal contact details only when the user is ready to submit them.

Risk: The skill can create bookings through an external service without the source clearly requiring explicit confirmation.

Mitigation: Present the provider, service, time slot, and contact details for review before calling the booking action.

## Reference(s):

- [Book Language Tutor listing](https://clawhub.ai/edwardrodriguez703-design/skills/book-language-tutor)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [JSON-RPC tool calls and conversational text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP search, availability, and booking actions; booking may require customer contact details.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
