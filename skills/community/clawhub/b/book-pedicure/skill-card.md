## Description:

Book pedicure services through Lokuli MCP. Use when user needs to find and book pedicure. Triggers on requests like "book a pedicure", "find pedicure near me", or any pedicure service request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardrodriguez703-design](https://clawhub.ai/user/edwardrodriguez703-design)

### License/Terms of Use:


## Use Case:

External users use this skill to search for pedicure providers, check appointment availability, and create a booking through Lokuli. Booking may require customer name, email, and phone number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a booking through a third-party service using personal contact details.

Mitigation: Before booking, confirm the provider, service, appointment time, and that the user's name, email, and phone number will be sent to Lokuli.

Risk: The release was flagged for review because final consent and confirmation are not clearly required in the artifact.

Mitigation: Require an explicit user confirmation immediately before calling the booking tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardrodriguez703-design/skills/book-pedicure)
- [Lokuli MCP endpoint](https://lokuli.com/mcp/sse)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON-RPC call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Lokuli MCP endpoint for search, availability checks, and booking creation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
