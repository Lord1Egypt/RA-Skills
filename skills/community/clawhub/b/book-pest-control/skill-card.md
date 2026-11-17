## Description:

Book Pest Control helps agents find and book pest-control services through Lokuli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can use this skill through an agent to search pest-control providers, check availability, and request a service booking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send searches, scheduling details, and contact information to Lokuli's external service.

Mitigation: Review the skill before installation and avoid providing personal contact details unless the user accepts sharing them with Lokuli.

Risk: The skill can create a real pest-control service booking.

Mitigation: Only allow booking creation after the agent presents the selected provider, service, time slot, and customer contact details for explicit user confirmation.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [Book Pest Control on ClawHub](https://clawhub.ai/edwardrodriguez703-design/skills/book-pest-control)

## Skill Output:

**Output Type(s):** [guidance, API Calls]

**Output Format:** [Markdown with JSON-RPC tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include provider search results, appointment availability, and booking requests.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
