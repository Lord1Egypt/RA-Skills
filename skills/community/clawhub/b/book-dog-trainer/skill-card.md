## Description:

Book Dog Trainer helps an agent search for dog-trainer services, check appointment availability, and create bookings through Lokuli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill through an agent to find dog-trainer providers, check available time slots, and create a booking after confirming the provider and appointment details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send customer contact details to Lokuli's external booking service.

Mitigation: Confirm exactly which name, email, phone number, provider, service, time, and price details will be sent before creating a booking.

Risk: A booking may be made with an unintended provider or time slot if search and availability results are not reviewed.

Mitigation: Have the user confirm the provider, service, appointment time, and any available pricing before completing the booking.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/edwardrodriguez703-design/skills/book-dog-trainer)
- [Lokuli MCP Endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown with JSON-RPC examples and concise booking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request location, provider, appointment time, and customer contact details before booking.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
