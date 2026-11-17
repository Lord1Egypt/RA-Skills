## Description:

Book brake-service services through Lokuli MCP, including search, availability checks, and booking creation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill to find brake-service providers through Lokuli, check appointment availability, and create a booking after confirming service details and contact information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a user's name, email, phone number, and booking details to Lokuli's MCP service.

Mitigation: Confirm the provider, appointment time, and exact contact details with the user before creating a booking.

Risk: The release security verdict is suspicious because the skill can create a third-party booking without explicit consent guidance in the artifact.

Mitigation: Review the provider and booking action before installation or use, and proceed only when the user has clearly approved the booking.

## Reference(s):

- [Book Brake Service on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-brake-service)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown instructions with JSON-RPC examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Lokuli MCP search, check_availability, and create_booking operations.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
