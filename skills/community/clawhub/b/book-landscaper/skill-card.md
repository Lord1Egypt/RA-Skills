## Description:

Book Landscaper helps an agent search for landscapers, check availability, and create bookings through Lokuli's MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to find landscaper services, check available appointment times, and book a service through Lokuli. Agents should collect and confirm booking details before creating an appointment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contact an external MCP service and send personal contact details.

Mitigation: Use it only when the user is comfortable sharing their name, email, and phone number with Lokuli's service.

Risk: The skill can create a landscaping booking without clearly requiring final user confirmation.

Mitigation: Require explicit final confirmation of provider, service, time, price or fees, cancellation terms, and contact details before creating any booking.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration]

**Output Format:** [Markdown with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send booking details, including name, email, and phone number, to an external MCP service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
