## Description:

Book smog check appointments through Lokuli MCP for users who need a smog check, emissions test, or vehicle inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to find nearby smog stations, review pricing and availability, and create a booking or checkout link after explicit user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts an external MCP service when searching or booking smog appointments.

Mitigation: Use it only for appointment-finding or booking tasks, and make the external service use clear before proceeding.

Risk: Booking requires customer name, email, or phone details.

Mitigation: Do not send personal contact details until the user has selected a provider and explicitly approved the booking step.

## Reference(s):

- [Book Smog ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-smog)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [Markdown with MCP tool call arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include smog station options, pricing, availability slots, and a checkout link after confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
