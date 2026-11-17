## Description:

Book dance-lesson services through Lokuli MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users can ask an agent to search for dance-lesson services, check provider availability, and create a booking through Lokuli's MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creating a booking may send the user's name, email, phone number, requested time, and selected provider or service to Lokuli's external MCP service.

Mitigation: Confirm the booking details and user intent before calling create_booking, especially when the user is only researching lessons.

## Reference(s):

- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)
- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-dance-lessons)

## Skill Output:

**Output Type(s):** [text, API calls, JSON-RPC requests, guidance]

**Output Format:** [Markdown guidance with JSON-RPC MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit customer contact details and selected booking details to Lokuli when creating a booking.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
